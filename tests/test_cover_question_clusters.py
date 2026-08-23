from __future__ import annotations

import json
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
        analysis = load(ROOT / "build/analysis/form-analysis.json")
        associations = {
            (row["formId"], row["occurrencePath"], row["questionId"]): row
            for row in analysis["formQuestionWorkbook"]
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

    def test_ratchet_and_analysis_report_no_forced_residual(self) -> None:
        baseline = load(ROOT / "analysis/unclassified-fields-baseline.v1.json")
        analysis = load(ROOT / "build/analysis/form-analysis.json")
        self.assertEqual(len(baseline["initial"]), 76)
        self.assertEqual(baseline["resolved"], baseline["initial"])
        self.assertEqual(analysis["status"]["unclassifiedFormFieldCount"], 0)
        self.assertEqual(analysis["unclassifiedFormFields"], [])
        self.assertEqual(analysis["status"]["reviewedAssociationCount"], 0)


if __name__ == "__main__":
    unittest.main()
