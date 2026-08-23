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
        self.assertEqual(len(self.analysis["questionInventory"]), 127)
        self.assertEqual(len(self.analysis["formQuestionWorkbook"]), 593)
        self.assertEqual(len(self.analysis["pairwiseExploratory"]), 406)
        self.assertEqual(len(self.analysis["marginalCapabilityReuse"]), 29)
        self.assertEqual(self.analysis["status"]["unclassifiedFormFieldCount"], 0)

    def test_unreviewed_semantics_never_enter_published_metrics(self) -> None:
        self.assertEqual(self.analysis["status"]["reviewedAssociationCount"], 0)
        self.assertEqual(self.analysis["status"]["exploratoryAssociationCount"], 593)
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
        self.assertEqual(row["mappingStatus"], "unmapped")
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

    def test_unclassified_baseline_is_fully_resolved(self) -> None:
        rows = self.analysis["unclassifiedFormFields"]
        self.assertEqual(len(rows), self.analysis["status"]["unclassifiedFormFieldCount"])
        self.assertEqual(rows, [])

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

    def test_lifecycle_attestation_and_control_roles_are_explicit(self) -> None:
        expected = {
            "rr-sf424-multi-project-cover": {
                "/agencyRoutingNumber": "applicantInput",
                "/aorSignature": "attestation",
                "/aorSignedDate": "attestation",
                "/grantsTrackingNumber": "applicantInput",
                "/stateId": "applicantInput",
                "/stateReceivedDate": "applicantInput",
                "/submittedDate": "applicantInput",
                "/trustAgree": "attestation",
            },
            "rr-sf424": {
                "/agencyRoutingNumber": "applicantInput",
                "/grantsGovTrackingId": "applicantInput",
                "/stateId": "applicantInput",
                "/stateReceivedDate": "applicantInput",
                "/trustAgree": "attestation",
            },
            "sf424": {
                "/certificationAgree": "attestation",
                "/stateApplicationId": "systemValue",
                "/stateReceiveDate": "systemValue",
            },
            "sf424-short": {
                "/applicationCertification": "attestation",
                "/sameAsProjectDirector": "technicalField",
            },
            "sf424a": {"/confirmation": "technicalField"},
        }
        resolved = set()
        for form_id, roles_by_path in expected.items():
            form = json.loads((ROOT / "dist" / "forms" / form_id / "index.json").read_text())
            actual = {
                occurrence["path"]: occurrence["responseRole"]
                for occurrence in form["fieldOccurrences"]
                if occurrence["path"] in roles_by_path
            }
            self.assertEqual(actual, roles_by_path)
            resolved.update(f"{form_id}:{path}" for path in roles_by_path)

        unresolved = {
            f'{row["formId"]}:{row["fieldPath"]}'
            for row in self.analysis["unclassifiedFormFields"]
        }
        self.assertTrue(resolved.isdisjoint(unresolved))
        baseline = json.loads(
            (ROOT / "analysis" / "unclassified-fields-baseline.v1.json").read_text()
        )
        self.assertTrue(resolved.issubset(set(baseline["resolved"])))

    def test_system_owned_lifecycle_values_retain_canonical_identity(self) -> None:
        expected = {
            ("sf424", "/stateReceiveDate"): "application/state-received-date",
            ("sf424", "/stateApplicationId"):
                "application/state-application-identifier",
        }
        rows = {
            (row["formId"], row["occurrencePath"]): row
            for row in self.analysis["formQuestionWorkbook"]
        }
        emitted_occurrences = {}
        for form_id in {form_id for form_id, _ in expected}:
            form = json.loads((ROOT / "dist/forms" / form_id / "index.json").read_text())
            emitted_occurrences.update({
                (form_id, occurrence["path"]): occurrence
                for occurrence in form["fieldOccurrences"]
            })
        for key, question_id in expected.items():
            with self.subTest(form=key[0], path=key[1]):
                row = rows[key]
                self.assertEqual(row["questionId"], question_id)
                self.assertEqual(row["responseRole"], "systemValue")
                self.assertEqual(emitted_occurrences[key]["blockIds"], [question_id])
                self.assertEqual(
                    emitted_occurrences[key]["responseRole"], "systemValue"
                )
                self.assertEqual(row["mappingStatus"], "proposed")
                self.assertTrue(row["countedInExploratorySimilarity"])
                self.assertFalse(row["countedInPublishedSimilarity"])
                self.assertFalse(row["publishable"])
                self.assertIsNotNone(row["sourceId"])
                self.assertIsNotNone(row["sourcePath"])
                self.assertIsNone(row["reviewedBy"])
                self.assertIsNone(row["reviewedAt"])

        for form_id, count in {
            "rr-sf424": 22,
            "rr-sf424-multi-project-cover": 22,
            "sf424": 15,
        }.items():
            evidence = json.loads(
                (ROOT / "dist" / "forms" / form_id / "evidence.json").read_text()
            )
            review = evidence["semanticReview"]
            self.assertEqual(review["status"], "proposed")
            self.assertEqual(len(review["mappings"]), count)
            self.assertTrue(
                all(mapping["status"] == "proposed" for mapping in review["mappings"])
            )
            self.assertTrue(
                all("reviewedBy" not in mapping for mapping in review["mappings"])
            )

    def test_rr_lifecycle_values_entered_by_applicants_retain_origin(self) -> None:
        expected = {
            ("rr-sf424", "/agencyRoutingNumber"):
                "application/federal-agency-routing-number",
            ("rr-sf424-multi-project-cover", "/agencyRoutingNumber"):
                "application/federal-agency-routing-number",
            ("rr-sf424", "/stateReceivedDate"):
                "application/state-received-date",
            ("rr-sf424-multi-project-cover", "/stateReceivedDate"):
                "application/state-received-date",
            ("rr-sf424", "/stateId"):
                "application/state-application-identifier",
            ("rr-sf424-multi-project-cover", "/stateId"):
                "application/state-application-identifier",
            ("rr-sf424", "/grantsGovTrackingId"):
                "application/previous-grants-gov-tracking-number",
            ("rr-sf424-multi-project-cover", "/grantsTrackingNumber"):
                "application/previous-grants-gov-tracking-number",
        }
        rows = {
            (row["formId"], row["occurrencePath"]): row
            for row in self.analysis["formQuestionWorkbook"]
        }
        for key, question_id in expected.items():
            with self.subTest(form=key[0], path=key[1]):
                row = rows[key]
                self.assertEqual(row["questionId"], question_id)
                self.assertEqual(row["responseRole"], "applicantInput")
                self.assertEqual(row["mappingStatus"], "proposed")
                self.assertTrue(row["countedInExploratorySimilarity"])
                self.assertFalse(row["countedInPublishedSimilarity"])
                self.assertFalse(row["publishable"])
                self.assertIsNotNone(row["sourceId"])
                self.assertIsNotNone(row["sourcePath"])
                self.assertIsNone(row["reviewedBy"])
                self.assertIsNone(row["reviewedAt"])

        sf424_award = next(
            row
            for row in self.analysis["formQuestionWorkbook"]
            if row["formId"] == "sf424"
            and row["occurrencePath"] == "/federalAwardIdentifier"
        )
        self.assertEqual(
            sf424_award["questionId"], "application/federal-award-identifier"
        )
        self.assertEqual(sf424_award["responseRole"], "applicantInput")
        self.assertEqual(sf424_award["mappingStatus"], "proposed")
        self.assertFalse(sf424_award["publishable"])

        rr_evidence = json.loads(
            (ROOT / "dist/forms/rr-sf424/evidence.json").read_text()
        )
        instructions = next(
            source
            for source in rr_evidence["sources"]
            if source["type"] == "instructions"
        )
        self.assertEqual(
            instructions["sha256"],
            "666647fdeb7d9d69f2d36dedc74f09ff6a9540776f87c5a5c5b0593219736bd1",
        )
        mp_evidence = json.loads(
            (ROOT / "dist/forms/rr-sf424-multi-project-cover/evidence.json").read_text()
        )
        dat = next(source for source in mp_evidence["sources"] if source["type"] == "dat")
        self.assertEqual(
            dat["sha256"],
            "361e00da500cb092997dadefcac9723cba3be63417a46375d2a5845797beae8e",
        )

        for form_id in ("rr-sf424", "rr-sf424-multi-project-cover"):
            ui = json.loads(
                (ROOT / "dist/forms" / form_id / "sgg/ui-schema.json").read_text()
            )
            fields = {
                child["definition"]: child
                for section in ui
                for child in section["children"]
                if child.get("definition") in {
                    "/properties/stateReceivedDate",
                    "/properties/stateId",
                }
            }
            self.assertEqual(
                {path: field["type"] for path, field in fields.items()},
                {
                    "/properties/stateReceivedDate": "field",
                    "/properties/stateId": "field",
                },
            )

        sf424_ui = json.loads(
            (ROOT / "dist/forms/sf424/sgg/ui-schema.json").read_text()
        )
        sf424_state_types = {
            child["definition"]: child["type"]
            for section in sf424_ui
            for child in section["children"]
            if child.get("definition") in {
                "/properties/stateReceiveDate",
                "/properties/stateApplicationId",
            }
        }
        self.assertEqual(
            sf424_state_types,
            {
                "/properties/stateReceiveDate": "null",
                "/properties/stateApplicationId": "null",
            },
        )

    def test_residual_reference_proposals_remain_exploratory(self) -> None:
        expected = {
            ("key-contacts", "/keyContacts/[]/projectRole"),
            ("sf424-short", "/applicantWebAddress"),
            ("sf424-short", "/projectDescription"),
            ("sf424a", "/activityLineItems/[]/activityTitle"),
            ("sf424a", "/activityLineItems/[]/assistanceListingNumber"),
            ("sf424a", "/directChargesExplanation"),
            ("sf424a", "/indirectChargesExplanation"),
            ("sf424a", "/remarks"),
        }
        rows = {
            (row["formId"], row["occurrencePath"]): row
            for row in self.analysis["formQuestionWorkbook"]
        }
        for key in expected:
            with self.subTest(form=key[0], path=key[1]):
                row = rows[key]
                self.assertEqual(row["mappingStatus"], "proposed")
                self.assertFalse(row["publishable"])
                self.assertTrue(row["countedInExploratorySimilarity"])
                self.assertFalse(row["countedInPublishedSimilarity"])
                self.assertIsNotNone(row["sourceId"])
                self.assertIsNotNone(row["sourcePath"])
                self.assertIsNone(row["reviewedBy"])
                self.assertIsNone(row["reviewedAt"])

    def test_sf424_short_copy_control_has_pinned_behavior_evidence(self) -> None:
        evidence = json.loads(
            (ROOT / "dist" / "forms" / "sf424-short" / "evidence.json").read_text()
        )
        dat = next(source for source in evidence["sources"] if source["type"] == "dat")
        self.assertEqual(
            dat["uri"],
            "https://apply07.grants.gov/apply/forms/sample/"
            "SF424_Short_3_0-V3.0_F711.xls",
        )
        self.assertEqual(
            dat["sha256"],
            "a905f905928a730b10d48d0b77cbb59397edb3ad3c99770391e1e160c3fb06df",
        )
        occurrence = next(
            row
            for row in json.loads(
                (ROOT / "dist/forms/sf424-short/index.json").read_text()
            )["fieldOccurrences"]
            if row["path"] == "/sameAsProjectDirector"
        )
        self.assertEqual(occurrence["responseRole"], "technicalField")
        decision = (ROOT / "documentation/lifecycle-field-ownership.md").read_text()
        self.assertIn("source parity is explicitly unresolved", decision)

    def test_applicant_entered_submission_date_remains_unreviewed(self) -> None:
        row = next(
            row
            for row in self.analysis["formQuestionWorkbook"]
            if row["formId"] == "rr-sf424-multi-project-cover"
            and row["questionId"] == "application/submission-date-entered"
        )
        self.assertEqual(row["occurrencePath"], "/submittedDate")
        self.assertEqual(row["responseRole"], "applicantInput")
        self.assertEqual(row["mappingStatus"], "unmapped")
        self.assertEqual(row["formSemanticReviewStatus"], "proposed")
        self.assertFalse(row["publishable"])


if __name__ == "__main__":
    unittest.main()
