from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from scripts.promote_crosswalk import export_packet


ROOT = Path(__file__).parents[1]
CROSSWALK = ROOT.parent / "Smarter-grants-management"
CROSSWALK_REVISION = "dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef"


def objects(value: object):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


class RRSF424Tests(unittest.TestCase):
    def test_promotion_packet_is_exact_and_review_gated(self) -> None:
        if not (CROSSWALK / ".git").is_dir():
            self.skipTest("sibling crosswalk checkout is unavailable")

        packet = export_packet(CROSSWALK, "RRSF424", CROSSWALK_REVISION)
        self.assertEqual(packet["metrics"], {
            "sourceRecords": 139,
            "sourceBehaviors": 145,
            "applicantBehaviorRecords": 119,
            "presentationBehaviorRecords": 24,
            "runtimeRules": 28,
            "semanticProposals": 139,
            "acceptedSemanticMappings": 0,
            "openReviewGates": 150,
        })
        self.assertEqual(packet["extraction"]["sourceSetSha256"],
                         "81ad602bf94391d4a7db80558802288452848aef97e68d4ca4ad1fe3d4b7e035")
        self.assertTrue(all(not proposal["publishable"] for proposal in packet["semanticProposals"]))

    def test_emitted_form_covers_all_extracted_applicant_questions(self) -> None:
        schema = json.loads((ROOT / "dist/forms/rr-sf424/schema.json").read_text())
        ui = json.loads((ROOT / "dist/forms/rr-sf424/sgg/ui-schema.json").read_text())
        rules = json.loads((ROOT / "dist/forms/rr-sf424/sgg/rule-schema.json").read_text())

        self.assertEqual(len(schema["properties"]), 28)
        self.assertEqual(len(ui), 21)
        self.assertEqual(sum(len(section["children"]) for section in ui), 106)
        applicant = json.loads(
            (ROOT / "dist/question-bank/research-application/applicant/schema.json").read_text()
        )
        organization = applicant["$defs"]["ResearchApplicantOrganization"]
        self.assertIn("employerId", organization["properties"])
        self.assertNotIn(
            "/properties/applicantInfo/properties/organizationInfo/properties/employerId",
            {
                child["definition"]
                for section in ui
                for child in section["children"]
                if "definition" in child
            },
        )
        self.assertEqual(
            {name for name, rule in rules.items() if rule.get("gg_validation", {}).get("rule") == "attachment"},
            {"sflllAttachment", "preApplicationAttachment", "coverLetterAttachment"},
        )
        self.assertEqual(
            rules["proposedProjectPeriod"]["proposedEndDate"]["gg_validation"],
            {"rule": "date_not_before", "fields": ["@THIS.proposedStartDate"]},
        )

    def test_eight_dat_conditions_are_source_bound_without_false_ui_parity(self) -> None:
        root = ROOT / "dist/forms/rr-sf424"
        evidence = json.loads((root / "evidence.json").read_text())
        records = evidence["behaviorEvidence"]
        official = [row for row in records if row["authority"] == "official_source"]
        unresolved = [row for row in records if row["authority"] == "unresolved"]

        source = next(row for row in evidence["sources"] if row["type"] == "dat")
        self.assertEqual(
            source,
            {
                "id": "source-1-532938a75c58",
                "type": "dat",
                "uri": (
                    "https://apply07.grants.gov/apply/forms/sample/"
                    "RR_SF424_5_0-V5.0_F768.xls"
                ),
                "sha256": (
                    "532938a75c587bdc8813fd3af625be4338281d0491999fc39aeaaac51b79c9c1"
                ),
                "nativeVersion": None,
            },
        )
        self.assertEqual(len(official), 8)
        self.assertEqual({row["sourceId"] for row in official}, {"source-1-532938a75c58"})
        self.assertEqual(
            [(row["canonicalPath"], row["sourcePath"]) for row in official],
            [
                ("/grantsGovTrackingId", "04-2"),
                ("/applicantType/applicantTypeCodeOtherExplanation", "07-1"),
                (
                    "/applicantType/smallBusinessOrganizationType/"
                    "sociallyEconomicallyDisadvantaged",
                    "07-3",
                ),
                ("/applicantType/smallBusinessOrganizationType/womenOwned", "07-2"),
                ("/applicationType/otherAgencySubmissionExplanation", "08-2-3"),
                ("/applicationType/revisionCode", "08-1-1 through 08-1-5"),
                ("/applicationType/revisionCodeOtherExplanation", "08-1-6"),
                ("/stateReview/stateReviewDate", "16-3"),
            ],
        )
        self.assertEqual(
            [row["sourceRecord"] for row in official],
            [
                "Required if SubmissionTypeCode = Changed/Corrected Application",
                "Other Field remain grayed out unless they select \"Other as the Applicant "
                "Type. Required if \"Other\" is selected as the Applicant Type.",
                "If Small Business Organization is selected above, please answer but not "
                "required. Grayed out until Small Business Organization is selected. Not a "
                "picklist. Each is own checkbox",
                "If Small Business Organization is selected above, please answer, but not "
                "required. Grayed out until Small Business Organization is selected. Not a "
                "picklist. Each is own checkbox",
                "Required if OtherAgencySubmission = Y. Grayed out until "
                "OtherAgencySubmission = Y.",
                "Can select two. Checkbox Implementation Grayed-out until "
                "ApplicationTypeCode = Revision. Not a picklist. Each is own checkbox. Valid "
                "combinations are AC, AD, BC, BD, or E Enumerations in schema should include: "
                "A, B, C, D, E, AC, AD, BC, BD to enforce stricter validation.",
                "Required if RevisionCode = E. Other Grayed out until 'E' is selected for "
                "RevisionCode.",
                "Conditionally required and active if StateReviewCodeType = Yes. If "
                "StateReviewCodeType is not Yes, then inactive.",
            ],
        )
        self.assertEqual(
            {row["executionStatus"] for row in official}, {"source-bound-uncompiled"}
        )

        self.assertEqual(len(unresolved), 8)
        self.assertEqual({row["executionStatus"] for row in unresolved}, {"compiled"})
        self.assertEqual(
            {row["canonicalPath"] for row in unresolved},
            {
                "grantsGovTrackingId",
                "applicantType.applicantTypeCodeOtherExplanation",
                "applicantType.smallBusinessOrganizationType."
                "sociallyEconomicallyDisadvantaged",
                "applicantType.smallBusinessOrganizationType.womenOwned",
                "applicationType.otherAgencySubmissionExplanation",
                "applicationType.revisionCode",
                "applicationType.revisionCodeOtherExplanation",
                "stateReview.stateReviewDate",
            },
        )
        self.assertTrue(all(row["owner"] == "form-semantic-review" for row in unresolved))
        self.assertTrue(all(row["reason"] and row["removalCondition"] for row in unresolved))

    def test_all_eight_current_ui_dispositions_pin_exact_paths_and_effects(self) -> None:
        ui = json.loads(
            (ROOT / "dist/forms/rr-sf424/sgg/ui-schema.json").read_text()
        )
        conditions = {
            row["definition"]: row["conditional"]
            for row in objects(ui)
            if row.get("type") == "field" and "conditional" in row
        }
        expected = {
            "/properties/grantsGovTrackingId": (
                "/submissionTypeCode",
                "Change/Corrected Application",
            ),
            "/properties/applicantType/properties/applicantTypeCodeOtherExplanation": (
                "/applicantType/applicantTypeCode",
                "X: Other (specify)",
            ),
            (
                "/properties/applicantType/properties/smallBusinessOrganizationType/"
                "properties/sociallyEconomicallyDisadvantaged"
            ): ("/applicantType/applicantTypeCode", "R: Small Business"),
            (
                "/properties/applicantType/properties/smallBusinessOrganizationType/"
                "properties/womenOwned"
            ): ("/applicantType/applicantTypeCode", "R: Small Business"),
            "/properties/applicationType/properties/otherAgencySubmissionExplanation": (
                "/applicationType/isOtherAgencySubmission",
                "Y: Yes",
            ),
            "/properties/applicationType/properties/revisionCode": (
                "/applicationType/applicationTypeCode",
                "Revision",
            ),
            "/properties/applicationType/properties/revisionCodeOtherExplanation": (
                "/applicationType/revisionCode",
                "E",
            ),
            "/properties/stateReview/properties/stateReviewDate": (
                "/stateReview/stateReviewCodeType",
                "Y: Yes",
            ),
        }
        self.assertEqual(set(conditions), set(expected))
        for definition, (pointer, value) in expected.items():
            with self.subTest(definition=definition):
                self.assertEqual(
                    conditions[definition],
                    {
                        "when": {
                            "op": "equals",
                            "ref": {"scope": "root", "pointer": pointer},
                            "value": value,
                        },
                        "then": {"visible": True},
                        "otherwise": {"visible": False},
                    },
                )

    def test_analysis_exposes_reuse_without_claiming_review(self) -> None:
        result = subprocess.run(
            ["python3", str(ROOT / "scripts/analyze.py"), "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        projection = json.loads(result.stdout)
        associations = [
            row for row in projection["formQuestionAssociations"]
            if row["formId"] == "rr-sf424"
        ]
        question_ids = {row["questionId"] for row in associations}
        self.assertEqual(len(associations), 70)
        self.assertTrue({
            "generics/address",
            "generics/person-name",
            "primary-org/legal-name",
            "primary-org/uei",
            "project/title",
            "project/start-date",
            "project/end-date",
            "research-application/applicant",
            "research-application/principal-investigator",
            "research-application/authorized-representative",
        }.issubset(question_ids))

        evidence = json.loads((ROOT / "dist/forms/rr-sf424/evidence.json").read_text())
        review = evidence["semanticReview"]
        self.assertEqual(review["status"], "proposed")
        self.assertEqual(len(review["mappings"]), 22)
        mappings = {
            row["canonicalPointer"]: row["sourcePath"] for row in review["mappings"]
        }
        self.assertEqual(
            mappings,
            {
                "#/properties/stateReceivedDate": "RR_SF424_5_0.StateReceivedDate",
                "#/properties/stateId": "RR_SF424_5_0.StateID",
                "#/properties/agencyRoutingNumber": "RR_SF424_5_0.AgencyRoutingNumber",
                "#/properties/submissionTypeCode": "RR_SF424_5_0.SubmissionTypeCode",
                "#/properties/applicantId": "RR_SF424_5_0.ApplicantID",
                "#/properties/federalId": "RR_SF424_5_0.FederalID",
                "#/properties/applicantType/properties/applicantTypeCode": (
                    "RR_SF424_5_0.ApplicantType.ApplicantTypeCode"
                ),
                "#/properties/applicantType/properties/applicantTypeCodeOtherExplanation": (
                    "RR_SF424_5_0.ApplicantType.ApplicantTypeCodeOtherExplanation"
                ),
                (
                    "#/properties/applicantType/properties/smallBusinessOrganizationType/"
                    "properties/sociallyEconomicallyDisadvantaged"
                ): (
                    "RR_SF424_5_0.ApplicantType.SmallBusinessOrganizationType."
                    "isSociallyEconomicallyDisadvantaged"
                ),
                (
                    "#/properties/applicantType/properties/smallBusinessOrganizationType/"
                    "properties/womenOwned"
                ): "RR_SF424_5_0.ApplicantType.SmallBusinessOrganizationType.isWomenOwned",
                "#/properties/applicationType/properties/applicationTypeCode": (
                    "RR_SF424_5_0.ApplicationType.ApplicationTypeCode"
                ),
                "#/properties/applicationType/properties/isOtherAgencySubmission": (
                    "RR_SF424_5_0.ApplicationType.isOtherAgencySubmission"
                ),
                "#/properties/applicationType/properties/otherAgencySubmissionExplanation": (
                    "RR_SF424_5_0.ApplicationType.OtherAgencySubmissionExplanation"
                ),
                "#/properties/applicationType/properties/revisionCode": (
                    "RR_SF424_5_0.ApplicationType.RevisionCode"
                ),
                "#/properties/applicationType/properties/revisionCodeOtherExplanation": (
                    "RR_SF424_5_0.ApplicationType.RevisionCodeOtherExplanation"
                ),
                "#/properties/estimatedProjectFunding/properties/totalEstimatedAmount": (
                    "RR_SF424_5_0.EstimatedProjectFunding.TotalEstimatedAmount"
                ),
                "#/properties/estimatedProjectFunding/properties/totalNonFederalRequested": (
                    "RR_SF424_5_0.EstimatedProjectFunding.TotalNonfedrequested"
                ),
                (
                    "#/properties/estimatedProjectFunding/properties/"
                    "totalFederalNonFederalRequested"
                ): "RR_SF424_5_0.EstimatedProjectFunding.TotalfedNonfedrequested",
                "#/properties/estimatedProjectFunding/properties/estimatedProgramIncome": (
                    "RR_SF424_5_0.EstimatedProjectFunding.EstimatedProgramIncome"
                ),
                "#/properties/stateReview/properties/stateReviewCodeType": (
                    "RR_SF424_5_0.StateReview.StateReviewCodeType"
                ),
                "#/properties/stateReview/properties/stateReviewDate": (
                    "RR_SF424_5_0.StateReview.StateReviewDate"
                ),
                "#/properties/grantsGovTrackingId": "RR_SF424_5_0.GGTrackingID",
            },
        )
        self.assertEqual(
            {mapping["sourceId"] for mapping in review["mappings"]},
            {"source-2-f140f32afed9"},
        )
        self.assertEqual({mapping["status"] for mapping in review["mappings"]}, {"proposed"})
        self.assertTrue(all(mapping["note"] for mapping in review["mappings"]))
        self.assertTrue(all("reviewedBy" not in mapping for mapping in review["mappings"]))
        self.assertEqual(
            sum(mapping["status"] == "accepted" for mapping in review["mappings"]),
            0,
        )


if __name__ == "__main__":
    unittest.main()
