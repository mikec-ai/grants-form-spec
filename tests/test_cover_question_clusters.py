from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(path: Path) -> dict:
    return json.loads(path.read_text())


class CoverQuestionClusterTests(unittest.TestCase):
    standard = {
        "/submissionType": "application/standard-submission-type",
        "/applicationType": "application/standard-application-type",
        "/revisionType": "application/standard-application-type",
        "/revisionOtherSpecify": "application/standard-application-type",
        "/applicantId": "application/standard-applicant-control-identifier",
        "/federalEntityIdentifier": "application/federal-entity-identifier",
        "/federalAwardIdentifier": "application/federal-award-identifier",
        "/departmentName": "primary-org/organizational-unit",
        "/divisionName": "primary-org/organizational-unit",
        "/organizationAffiliation": "poc/organization-affiliation",
        "/stateReview": "application/standard-state-review",
        "/stateReviewAvailableDate": "application/standard-state-review",
        "/delinquentFederalDebt": "application/delinquent-federal-debt-status",
    }
    research = {
        "/submissionTypeCode": "research-application/submission-type",
        "/applicantId": "research-application/applicant-control-identifier",
        "/federalId": "research-application/previous-federal-award-identifier",
        "/applicantType/applicantTypeCode": "primary-org/research-applicant-type",
        "/applicantType/applicantTypeCodeOtherExplanation": "primary-org/research-applicant-type",
        "/applicantType/smallBusinessOrganizationType/sociallyEconomicallyDisadvantaged": "primary-org/research-applicant-type",
        "/applicantType/smallBusinessOrganizationType/womenOwned": "primary-org/research-applicant-type",
        "/applicationType/applicationTypeCode": "research-application/application-type",
        "/applicationType/isOtherAgencySubmission": "research-application/application-type",
        "/applicationType/otherAgencySubmissionExplanation": "research-application/application-type",
        "/applicationType/revisionCode": "research-application/application-type",
        "/applicationType/revisionCodeOtherExplanation": "research-application/application-type",
        "/estimatedProjectFunding/totalEstimatedAmount": "research-application/estimated-project-funding",
        "/estimatedProjectFunding/totalNonFederalRequested": "research-application/estimated-project-funding",
        "/estimatedProjectFunding/totalFederalNonFederalRequested": "research-application/estimated-project-funding",
        "/estimatedProjectFunding/estimatedProgramIncome": "research-application/estimated-project-funding",
        "/stateReview/stateReviewCodeType": "research-application/state-review",
        "/stateReview/stateReviewDate": "research-application/state-review",
    }

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        result = subprocess.run(
            [
                "python3",
                str(ROOT / "scripts/analyze.py"),
                "--json",
                "--output-dir",
                cls.temp_dir.name,
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

    def assert_occurrences(self, form_id: str, expected: dict[str, str]) -> None:
        index = load(ROOT / f"dist/forms/{form_id}/index.json")
        actual = {row["path"]: row for row in index["fieldOccurrences"]}
        for path, block_id in expected.items():
            with self.subTest(form=form_id, path=path):
                self.assertIn(block_id, actual[path]["blockIds"])
                self.assertEqual(actual[path]["responseRole"], "applicantInput")

    def test_exact_cover_partition_preserves_family_boundaries(self) -> None:
        self.assertEqual(len(self.standard), 13)
        self.assertEqual(len(self.research), 18)
        self.assert_occurrences("sf424", self.standard)
        self.assert_occurrences("rr-sf424", self.research)
        self.assert_occurrences("rr-sf424-multi-project-cover", self.research)

        tracking = {
            "rr-sf424": (
                "/grantsGovTrackingId",
                "application/previous-grants-gov-tracking-number",
            ),
            "rr-sf424-multi-project-cover": (
                "/grantsTrackingNumber",
                "application/previous-grants-gov-tracking-number",
            ),
        }
        for form_id, (path, block_id) in tracking.items():
            self.assert_occurrences(form_id, {path: block_id})

        standard_ids = set(self.standard.values())
        research_ids = set(self.research.values())
        self.assertTrue(standard_ids.isdisjoint(research_ids))

    def test_all_fifty_source_mappings_remain_proposed_and_unpublished(self) -> None:
        targets = {
            "sf424": set(self.standard),
            "rr-sf424": set(self.research) | {"/grantsGovTrackingId"},
            "rr-sf424-multi-project-cover": set(self.research),
        }
        self.assertEqual(sum(map(len, targets.values())), 50)
        associations = {
            (row["formId"], row["occurrencePath"], row["questionId"]): row
            for row in self.analysis["formQuestionWorkbook"]
        }

        for form_id, paths in targets.items():
            evidence = load(ROOT / f"dist/forms/{form_id}/evidence.json")
            mappings = {
                mapping["canonicalPointer"]: mapping
                for mapping in evidence["semanticReview"]["mappings"]
            }
            source_ids = {source["id"] for source in evidence["sources"]}
            for path in paths:
                pointer = "#"
                for part in path.strip("/").split("/"):
                    pointer += "/items" if part == "[]" else f"/properties/{part}"
                with self.subTest(form=form_id, path=path):
                    mapping = mappings[pointer]
                    self.assertEqual(mapping["status"], "proposed")
                    self.assertIn(mapping["sourceId"], source_ids)
                    self.assertTrue(mapping["sourcePath"])
                    self.assertNotIn("reviewedBy", mapping)
                    self.assertNotIn("reviewedAt", mapping)
                    block_ids = load(ROOT / f"dist/forms/{form_id}/index.json")
                    occurrence = next(
                        row for row in block_ids["fieldOccurrences"] if row["path"] == path
                    )
                    question_ids = set(occurrence["blockIds"])
                    matching = [
                        row
                        for question_id in question_ids
                        if (row := associations.get((form_id, path, question_id)))
                    ]
                    self.assertTrue(matching)
                    self.assertTrue(all(row["mappingStatus"] == "proposed" for row in matching))
                    self.assertTrue(all(not row["publishable"] for row in matching))

        intended = {
            ("sf424", path, question_id)
            for path, question_id in self.standard.items()
        } | {
            (form_id, path, question_id)
            for form_id in ("rr-sf424", "rr-sf424-multi-project-cover")
            for path, question_id in self.research.items()
        } | {
            (
                "rr-sf424",
                "/grantsGovTrackingId",
                "application/previous-grants-gov-tracking-number",
            )
        }
        self.assertEqual(len(intended), 50)
        projected = {
            key: associations[key] for key in intended
        }
        self.assertEqual(len(projected), 50)
        self.assertTrue(
            all(row["mappingStatus"] == "proposed" for row in projected.values())
        )
        cover_rows = {
            (row["formId"], row["occurrencePath"], row["questionId"])
            for row in self.analysis["formQuestionWorkbook"]
            if (
                row["formId"] == "sf424"
                and row["questionId"] in set(self.standard.values())
            ) or (
                row["formId"] in {
                    "rr-sf424",
                    "rr-sf424-multi-project-cover",
                }
                and row["questionId"] in set(self.research.values())
            ) or (
                row["formId"] == "rr-sf424"
                and row["questionId"]
                == "application/previous-grants-gov-tracking-number"
            )
        }
        self.assertEqual(cover_rows, intended)
        cluster_ids = set(self.standard.values()) | set(self.research.values())
        compound_roots = {
            "/applicantType",
            "/applicationType",
            "/estimatedProjectFunding",
            "/stateReview",
        }
        self.assertFalse([
            row
            for row in self.analysis["formQuestionWorkbook"]
            if row["questionId"] in cluster_ids
            and row["occurrencePath"] in compound_roots
            and row["mappingStatus"] == "unmapped"
        ])

    def test_portable_schema_and_ui_preserve_source_presentation(self) -> None:
        rr_schema = load(ROOT / "dist/forms/rr-sf424/schema.json")
        self.assertEqual(
            rr_schema["properties"]["submissionTypeCode"]["title"],
            "Type of Submission",
        )

        multi_schema = load(
            ROOT / "dist/forms/rr-sf424-multi-project-cover/schema.json"
        )
        self.assertEqual(
            multi_schema["properties"]["estimatedProjectFunding"]["title"],
            "Estimated Project Funding",
        )
        multi_ui = load(ROOT / "dist/forms/rr-sf424-multi-project-cover/ui.json")

        def controls(value: object) -> list[dict]:
            if isinstance(value, list):
                return [node for item in value for node in controls(item)]
            if not isinstance(value, dict):
                return []
            return [value, *[
                node for item in value.values() for node in controls(item)
            ]]

        funding = [
            node
            for node in controls(multi_ui)
            if "estimatedProjectFunding" in str(node.get("scope", ""))
        ]
        self.assertEqual(funding, [{
            "type": "Control",
            "scope": "#/properties/estimatedProjectFunding",
            "label": "Estimated Project Funding",
        }])

        sf_schema = load(ROOT / "dist/forms/sf424/schema.json")
        descriptions = {
            "submissionType": "Select one type of submission in accordance with agency instructions.",
            "applicationType": "Select one type of application in accordance with agency instructions.",
            "revisionType": "Select a revision type from the list provided. A selection is required if Type of Application is Revision.",
            "revisionOtherSpecify": "Please specify the type of revision. This field is required if E. Other is checked.",
            "departmentName": "Enter the name of primary organizational department, service, laboratory, or equivalent level within the organization which will undertake the assistance activity.",
            "divisionName": "Enter the name of primary organizational division, office, or major subdivision which will undertake the assistance activity.",
            "stateReview": "One selection is required.",
            "stateReviewAvailableDate": "If 'a' is selected, enter the date the application was submitted to the State.",
            "delinquentFederalDebt": "If 'Yes,' provide explanation in attachment.",
        }
        for path, description in descriptions.items():
            with self.subTest(path=path):
                self.assertEqual(sf_schema["properties"][path]["description"], description)
        revision_other = sf_schema["properties"]["revisionOtherSpecify"]
        self.assertNotIn("minLength", revision_other)
        self.assertNotIn("maxLength", revision_other)

    def test_permanent_gate_and_analysis_report_no_forced_residual(self) -> None:
        exceptions = load(ROOT / "analysis/unclassified-field-exceptions.v1.json")
        self.assertEqual(exceptions, {"version": 1, "exceptions": []})
        self.assertEqual(self.analysis["status"]["unclassifiedFormFieldCount"], 0)
        self.assertEqual(self.analysis["unclassifiedFormFields"], [])
        self.assertEqual(self.analysis["status"]["reviewedAssociationCount"], 0)


if __name__ == "__main__":
    unittest.main()
