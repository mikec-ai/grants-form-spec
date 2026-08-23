from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ANALYZER = ROOT / "scripts" / "analyze.py"


class AttachmentSemanticAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.output_dir = Path(cls.temp_dir.name)
        result = subprocess.run(
            [
                "python3",
                str(ANALYZER),
                "--json",
                "--output-dir",
                str(cls.output_dir),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        cls.analysis = json.loads(result.stdout)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()

    def test_attachment_roles_are_distinct_semantic_questions(self) -> None:
        expected = {
            "project-narrative-attachments": "project/narrative",
            "budget-narrative-attachments": "budget/narrative",
            "other-narrative-attachments": "application/other-narrative",
        }
        for form_id, question_id in expected.items():
            with self.subTest(form=form_id):
                self.assertEqual(self.analysis["asks"][form_id], [question_id])
                self.assertEqual(
                    self.analysis["usesCaptureMechanisms"][form_id],
                    ["generics/attachment"],
                )

    def test_capture_mechanism_does_not_inflate_semantic_similarity(self) -> None:
        attachment_forms = {
            "project-narrative-attachments",
            "budget-narrative-attachments",
            "other-narrative-attachments",
        }
        rows = [
            row
            for row in self.analysis["pairwise"]
            if {row["formA"], row["formB"]}.issubset(attachment_forms)
        ]
        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertEqual(row["questionsInCommon"], 0)
            self.assertEqual(row["similarity"], 0.0)

    def test_associations_preserve_role_path_and_composition(self) -> None:
        semantic = [
            row
            for row in self.analysis["formQuestionAssociations"]
            if row["formId"] == "project-narrative-attachments"
        ]
        mechanism = [
            row
            for row in self.analysis["formCaptureMechanisms"]
            if row["formId"] == "project-narrative-attachments"
        ]
        self.assertEqual(
            semantic,
            [{
                "formId": "project-narrative-attachments",
                "questionId": "project/narrative",
                "path": "/attachments/[]",
                "relationship": "direct",
            }],
        )
        self.assertEqual(
            mechanism,
            [{
                "formId": "project-narrative-attachments",
                "mechanismId": "generics/attachment",
                "path": "/attachments/[]",
                "relationship": "transitive",
            }],
        )

    def test_unknown_flag_is_an_actionable_usage_error(self) -> None:
        result = subprocess.run(
            ["python3", str(ANALYZER), "--wat"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments: --wat", result.stderr)

    def test_rr_subaward_budget_reuses_every_rr_budget_question(self) -> None:
        budget = set(self.analysis["asks"]["rr-budget"])
        subaward = set(self.analysis["asks"]["rr-subaward-budget"])
        self.assertTrue(budget)
        self.assertLessEqual(budget, subaward)
        self.assertEqual(subaward - budget, {"budget/research/details"})

        row = next(
            row
            for row in self.analysis["pairwise"]
            if {row["formA"], row["formB"]} == {"rr-budget", "rr-subaward-budget"}
        )
        self.assertEqual(row["questionsInCommon"], len(budget))
        budget_share = row["shareOfA"] if row["formA"] == "rr-budget" else row["shareOfB"]
        self.assertEqual(budget_share, 1.0)

    def test_rr_budget_10yr_reuses_the_complete_rr_budget_question_set(self) -> None:
        five_year = set(self.analysis["asks"]["rr-budget"])
        ten_year = set(self.analysis["asks"]["rr-budget-10yr"])

        self.assertTrue(five_year)
        self.assertEqual(ten_year, five_year)

        row = next(
            row
            for row in self.analysis["pairwise"]
            if {row["formA"], row["formB"]} == {"rr-budget", "rr-budget-10yr"}
        )
        self.assertEqual(row["questionsInCommon"], len(five_year))
        self.assertEqual(row["similarity"], 1.0)
        self.assertEqual(row["shareOfA"], 1.0)
        self.assertEqual(row["shareOfB"], 1.0)

    def test_rr_subaward_budget_30_reuses_the_complete_subaward_question_set(self) -> None:
        ten_subawards = set(self.analysis["asks"]["rr-subaward-budget"])
        thirty_subawards = set(self.analysis["asks"]["rr-subaward-budget-30"])

        self.assertTrue(ten_subawards)
        self.assertEqual(thirty_subawards, ten_subawards)

        row = next(
            row
            for row in self.analysis["pairwise"]
            if {row["formA"], row["formB"]}
            == {"rr-subaward-budget", "rr-subaward-budget-30"}
        )
        self.assertEqual(row["questionsInCommon"], len(ten_subawards))
        self.assertEqual(row["similarity"], 1.0)
        self.assertEqual(row["shareOfA"], 1.0)
        self.assertEqual(row["shareOfB"], 1.0)

    def test_rr_subaward_budget_10yr_30_swaps_only_the_duration_profile(self) -> None:
        five_year = set(self.analysis["asks"]["rr-subaward-budget-30"])
        ten_year = set(self.analysis["asks"]["rr-subaward-budget-10yr-30"])

        self.assertTrue(five_year)
        self.assertEqual(five_year - ten_year, {"budget/research/details"})
        self.assertEqual(ten_year - five_year, {"budget/research/details-10yr"})
        self.assertEqual(len(five_year), len(ten_year))

        row = next(
            row
            for row in self.analysis["pairwise"]
            if {row["formA"], row["formB"]}
            == {"rr-subaward-budget-30", "rr-subaward-budget-10yr-30"}
        )
        common = five_year & ten_year
        self.assertEqual(row["questionsInCommon"], len(common))
        self.assertEqual(row["similarity"], len(common) / len(five_year | ten_year))
        self.assertEqual(row["shareOfA"], len(common) / len(five_year))
        self.assertEqual(row["shareOfB"], len(common) / len(ten_year))

    def test_project_abstract_is_text_semantics_not_attachment_capture(self) -> None:
        self.assertEqual(
            set(self.analysis["asks"]["project-abstract-summary"]),
            {
                "opportunity/number",
                "opportunity/assistance-listing-number",
                "primary-org/legal-name",
                "generics/organization-name",
                "project/title",
                "project/abstract",
            },
        )
        self.assertEqual(
            self.analysis["usesCaptureMechanisms"]["project-abstract-summary"],
            [],
        )

    def test_spreadsheet_ready_outputs_are_complete(self) -> None:
        expected = {
            "form-analysis.json",
            "question-inventory.csv",
            "form-question-associations.csv",
            "unclassified-form-fields.csv",
            "pairwise-exploratory.csv",
            "pairwise-reviewed.csv",
            "capability-occurrences.csv",
            "marginal-capability-reuse.csv",
        }
        self.assertEqual({path.name for path in self.output_dir.iterdir()}, expected)
        self.assertEqual(len(self.analysis["questionInventory"]), 102)
        self.assertEqual(len(self.analysis["formQuestionWorkbook"]), 426)
        self.assertEqual(len(self.analysis["pairwiseExploratory"]), 171)
        self.assertEqual(len(self.analysis["marginalCapabilityReuse"]), 19)
        self.assertEqual(self.analysis["status"]["unclassifiedFormFieldCount"], 68)

    def test_unreviewed_semantics_never_enter_published_metrics(self) -> None:
        self.assertEqual(self.analysis["status"]["reviewedAssociationCount"], 0)
        self.assertEqual(self.analysis["status"]["exploratoryAssociationCount"], 426)
        self.assertTrue(
            all(not row["publishable"] for row in self.analysis["formQuestionWorkbook"])
        )
        self.assertTrue(
            all(not row["eligible"] for row in self.analysis["pairwiseReviewed"])
        )
        self.assertTrue(
            all(row["similarity"] is None for row in self.analysis["pairwiseReviewed"])
        )

    def test_association_joins_question_xml_and_source_provenance(self) -> None:
        row = next(
            row
            for row in self.analysis["formQuestionWorkbook"]
            if row["formId"] == "rr-sf424" and row["questionId"] == "primary-org/uei"
        )
        self.assertEqual(row["questionName"], "SAM UEI")
        self.assertEqual(row["occurrencePath"], "/applicantInfo/organizationInfo/samUei")
        self.assertEqual(
            row["xmlPath"],
            "/RR_SF424_5_0:RR_SF424_5_0/RR_SF424_5_0:ApplicantInfo/"
            "RR_SF424_5_0:OrganizationInfo/globLib:SAMUEI",
        )
        self.assertEqual(
            row["xsdUri"],
            "https://apply07.grants.gov/apply/forms/schemas/RR_SF424_5_0-V5.0.xsd",
        )
        self.assertEqual(row["xsdNativeVersion"], "5.0")
        self.assertEqual(len(row["xsdSha256"]), 64)
        self.assertEqual(len(row["extractionRevision"]), 40)
        self.assertEqual(row["mappingStatus"], "unreviewed")
        self.assertEqual(row["responseRole"], "unclassified")
        self.assertTrue(row["countedInExploratorySimilarity"])
        self.assertFalse(row["countedInPublishedSimilarity"])

    def test_occurrence_constraints_are_not_confused_with_question_identity(self) -> None:
        row = next(
            row
            for row in self.analysis["formQuestionWorkbook"]
            if row["formId"] == "project-narrative-attachments"
        )
        self.assertEqual(row["questionId"], "project/narrative")
        self.assertEqual(row["schemaType"], "string")
        self.assertTrue(row["required"])
        self.assertEqual(row["minItems"], 1)
        self.assertEqual(row["maxItems"], 100)
        mechanism = next(
            row
            for row in self.analysis["capabilityOccurrences"]
            if row["formId"] == "project-narrative-attachments"
            and row["kind"] == "captureMechanism"
        )
        self.assertEqual(mechanism["capabilityId"], "generics/attachment")

    def test_marginal_curve_records_configuration_only_reuse(self) -> None:
        short = next(
            row
            for row in self.analysis["marginalCapabilityReuse"]
            if row["formId"] == "sf424-short"
        )
        self.assertEqual(short["newQuestionCount"], 2)
        self.assertEqual(short["reusedQuestionCount"], short["questionCount"] - 2)
        self.assertEqual(short["newBehaviorCount"], 0)
        self.assertEqual(short["reusedBehaviorCount"], short["behaviorCount"])
        self.assertEqual(short["measurementStatus"], "implementation-derived-unreviewed")

    def test_unclassified_form_fields_are_visible_but_not_counted_as_questions(self) -> None:
        rows = self.analysis["unclassifiedFormFields"]
        self.assertEqual(len(rows), self.analysis["status"]["unclassifiedFormFieldCount"])
        self.assertTrue(rows)
        self.assertTrue(all(row["fieldPath"].startswith("/") for row in rows))
        self.assertTrue(all(row["classification"] == "unclassified" for row in rows))
        self.assertTrue(all(not row["countedAsQuestion"] for row in rows))

    def test_canonical_lineage_survives_spreads_inheritance_and_overrides(self) -> None:
        rows = self.analysis["unclassifiedFormFields"]
        by_form = {
            form_id: {row["fieldName"] for row in rows if row["formId"] == form_id}
            for form_id in {
                "rr-budget",
                "rr-budget-10yr",
                "performance-site",
                "rr-key-person-expanded",
                "rr-sf424-multi-project-cover",
            }
        }
        self.assertNotIn("budgetType", by_form["rr-budget"])
        self.assertNotIn("budgetType", by_form["rr-budget-10yr"])
        self.assertTrue(
            {"state", "province", "zipCode"}.isdisjoint(by_form["performance-site"])
        )
        self.assertTrue(
            {"state", "province", "zipCode", "projectRole"}.isdisjoint(
                by_form["rr-key-person-expanded"]
            )
        )
        self.assertTrue(
            {"state", "province", "department", "division", "employerId"}.isdisjoint(
                by_form["rr-sf424-multi-project-cover"]
            )
        )

    def test_authored_response_roles_flow_to_question_occurrences(self) -> None:
        system = next(
            row
            for row in self.analysis["formQuestionWorkbook"]
            if row["formId"] == "sf424"
            and row["questionId"] == "application/date-received"
        )
        calculated = next(
            row
            for row in self.analysis["formQuestionWorkbook"]
            if row["formId"] == "sf424"
            and row["questionId"] == "generics/monetary-amount"
            and row["occurrencePath"] == "/totalEstimatedFunding"
        )
        self.assertEqual(system["responseRole"], "systemValue")
        self.assertEqual(calculated["responseRole"], "calculatedOutput")


if __name__ == "__main__":
    unittest.main()
