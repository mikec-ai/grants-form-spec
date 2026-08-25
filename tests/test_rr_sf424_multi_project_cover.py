from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.promote_crosswalk import export_packet

ROOT = Path(__file__).parents[1]
CROSSWALK = ROOT.parent / "grants-question-crosswalk-mp-cover"
CROSSWALK_REVISION = "c1573287e0664d7b991e69c352038534b771189f"


class RRSF424MultiProjectCoverTests(unittest.TestCase):
    def test_promotion_packet_is_exact_and_review_gated(self) -> None:
        if not (CROSSWALK / ".git").exists():
            self.skipTest("pinned crosswalk checkout is unavailable")

        packet = export_packet(CROSSWALK, "RRSF424MPCover", CROSSWALK_REVISION)

        self.assertEqual(
            packet["metrics"],
            {
                "sourceRecords": 139,
                "sourceBehaviors": 143,
                "applicantBehaviorRecords": 123,
                "presentationBehaviorRecords": 20,
                "runtimeRules": 40,
                "semanticProposals": 139,
                "acceptedSemanticMappings": 0,
                "openReviewGates": 162,
            },
        )
        self.assertEqual(
            packet["extraction"]["sourceSetSha256"],
            "3224ce9eac55ccc27a8cae4f257efe10b69872ef5bb6c3fa22d82c9ed4427fac",
        )
        self.assertTrue(
            all(not row["publishable"] for row in packet["semanticProposals"])
        )

    def test_source_structure_is_a_parameterized_sibling_not_a_label_match(
        self,
    ) -> None:
        if not (CROSSWALK / ".git").exists():
            self.skipTest("pinned crosswalk checkout is unavailable")

        standalone = export_packet(
            ROOT.parent / "Smarter-grants-management",
            "RRSF424",
            "dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef",
        )
        multi = export_packet(CROSSWALK, "RRSF424MPCover", CROSSWALK_REVISION)
        standalone_root = standalone["form"]["sourceRoot"]
        multi_root = multi["form"]["sourceRoot"]
        standalone_paths = {
            row["path"].removeprefix(standalone_root): row
            for row in standalone["records"]
        }
        multi_paths = {
            row["path"].removeprefix(multi_root): row for row in multi["records"]
        }

        self.assertEqual(set(standalone_paths) - set(multi_paths), {".GGTrackingID"})
        self.assertEqual(
            set(multi_paths) - set(standalone_paths), {".GrantsTrackingNumber"}
        )
        self.assertEqual(len(set(standalone_paths) & set(multi_paths)), 138)
        self.assertTrue(
            all(
                not row["required"]
                for path, row in multi_paths.items()
                if path and row["recordKind"] != "technical_field"
            )
        )

    def test_emitted_form_preserves_optional_cardinality_and_typed_behavior(
        self,
    ) -> None:
        root = ROOT / "dist/forms/rr-sf424-multi-project-cover"
        schema = json.loads((root / "schema.json").read_text())
        ui = json.loads((root / "sgg/ui-schema.json").read_text())
        rules = json.loads((root / "sgg/rule-schema.json").read_text())
        fields = [field for section in ui for field in section["children"]]

        self.assertEqual(len(schema["properties"]), 28)
        self.assertNotIn("required", schema)
        self.assertEqual(
            schema["properties"]["applicantInfo"]["$ref"],
            "#/$defs/MultiProjectApplicant",
        )
        self.assertEqual(
            schema["properties"]["principalInvestigator"]["$ref"],
            "#/$defs/MultiProjectPrincipalInvestigator",
        )
        self.assertEqual(
            schema["properties"]["authorizedRepresentative"]["$ref"],
            "#/$defs/MultiProjectAuthorizedRepresentative",
        )
        self.assertEqual(
            schema["$defs"]["MultiProjectApplicant"]["allOf"],
            [
                {
                    "$ref": "../../question-bank/research-application/applicant/schema.json"
                }
            ],
        )
        self.assertEqual(len(ui), 21)
        self.assertEqual(len(fields), 106)
        self.assertEqual(sum("conditional" in field for field in fields), 14)
        self.assertEqual(
            sum(
                field.get("conditional", {}).get("then", {}).get("interaction")
                == "enabled"
                for field in fields
            ),
            10,
        )
        self.assertEqual(
            sum(
                field.get("conditional", {}).get("then", {}).get("interaction")
                == "readOnly"
                for field in fields
            ),
            4,
        )
        self.assertEqual(
            set(rules),
            {
                "sflllAttachment",
                "preApplicationAttachment",
                "coverLetterAttachment",
            },
        )
        self.assertEqual(
            schema["$defs"]["MultiProjectApplicationType"]["allOf"],
            [
                {
                    "$ref": "../../question-bank/research-application/application-type/schema.json"
                }
            ],
        )
        application_type = json.loads(
            (
                ROOT
                / "dist/question-bank/research-application/application-type/schema.json"
            ).read_text()
        )
        self.assertEqual(
            application_type["properties"]["revisionCode"]["x-encoded-checkbox-group"][
                "combinations"
            ][-1],
            {"value": "BD", "members": ["B", "D"]},
        )

        evidence = json.loads((root / "evidence.json").read_text())
        review = evidence["semanticReview"]
        self.assertEqual(review["status"], "proposed")
        self.assertEqual(len(review["mappings"]), 22)
        self.assertTrue(
            all(mapping["status"] == "proposed" for mapping in review["mappings"])
        )
        self.assertTrue(
            all("reviewedBy" not in mapping for mapping in review["mappings"])
        )

    def test_exact_source_conditions_remain_separate_from_compiled_dispositions(
        self,
    ) -> None:
        evidence = json.loads(
            (
                ROOT / "evidence/forms/rr-sf424-multi-project-cover/evidence.json"
            ).read_text()
        )
        dat = evidence["sources"][0]
        self.assertEqual(
            dat,
            {
                "id": "source-1-361e00da500c",
                "type": "dat",
                "uri": "https://apply07.grants.gov/apply/forms/sample/RR_SF424_Multi_Project_Cover_4_0-V4.0_F769.xls",
                "sha256": "361e00da500cb092997dadefcac9723cba3be63417a46375d2a5845797beae8e",
                "nativeVersion": None,
            },
        )

        official = [
            row
            for row in evidence["behaviorEvidence"]
            if row["authority"] == "official_source"
        ]
        self.assertEqual(
            [
                (row["canonicalPath"], row["sourcePath"], row["sourceRecord"])
                for row in official
            ],
            [
                (
                    "/applicantInfo/organizationInfo/address/state",
                    "05-5e",
                    "This field is active if Country is US. If Country is not US, then this field is inactive.",
                ),
                (
                    "/applicantInfo/organizationInfo/address/province",
                    "05-5e1",
                    "If Country is US then this field is inactive. If Country is not US, then this field is active",
                ),
                (
                    "/applicantInfo/contactPersonInfo/address/state",
                    "05-6j",
                    "This field is active if Country is US. If Country is not US, then inactive",
                ),
                (
                    "/applicantInfo/contactPersonInfo/address/province",
                    "05-6k",
                    "If Country is US then this field is inactive. If Country is not US, then it is active.",
                ),
                (
                    "/applicantType/applicantTypeCodeOtherExplanation",
                    "07-1",
                    'Other Field remain grayed out unless they select "Other as the Applicant Type.',
                ),
                (
                    "/applicantType/smallBusinessOrganizationType/sociallyEconomicallyDisadvantaged",
                    "07-4",
                    "If Small Business Organization is selected above, please answer but not required. Grayed out until Small Business Organzation is selected. Not a picklist. Each is own checkbox",
                ),
                (
                    "/applicantType/smallBusinessOrganizationType/womenOwned",
                    "07-3",
                    "If Small Business Organization is selected above, please answer, but not required. Grayed out until Small Business Organzation is selected. Not a picklist. Each is own checkbox",
                ),
                (
                    "/applicationType/otherAgencySubmissionExplanation",
                    "08-2-3",
                    "Grayed out until OtherAgencySubmission = Y.",
                ),
                (
                    "/applicationType/revisionCode",
                    "08-1-1 through 08-1-5",
                    "Can select two. Checkbox Implementation Grayed-out until ApplicationTypeCode = Revision. Not a picklist. Each is own checkbox. Valid combinations are AC, AD, BC, BD, or E Enumerations in schema should include: A, B, C, D, E, AC, AD, BC, BD to enforce stricter validation.",
                ),
                (
                    "/applicationType/revisionCodeOtherExplanation",
                    "08-1-6",
                    "Grayed out until 'E' is selected for RevisionCode.",
                ),
                (
                    "/principalInvestigator/address/province",
                    "14-10e1",
                    "If Country is US then inactive. If Country is not US, then active.",
                ),
                (
                    "/stateReview/stateReviewDate",
                    "16-3",
                    "Grayed-out until StateReviewCodeType = Yes.",
                ),
                (
                    "/authorizedRepresentative/address/state",
                    "19-10e",
                    "If Country is US then active. If Country is not US, then inactive",
                ),
                (
                    "/authorizedRepresentative/address/province",
                    "19-10e1",
                    "If Country is US then inactive. If Country is not US, then active.",
                ),
            ],
        )
        self.assertTrue(all(row["sourceId"] == dat["id"] for row in official))
        self.assertTrue(
            all(row["executionStatus"] == "source-bound-uncompiled" for row in official)
        )

        compiled = [
            row
            for row in evidence["behaviorEvidence"]
            if row["executionStatus"] == "compiled"
        ]
        expected_conditionals = {
            "applicantInfo.organizationInfo.address.state": (
                "/applicantInfo/organizationInfo/address/country",
                "USA: UNITED STATES",
                "enabled",
                "disabled",
            ),
            "applicantInfo.organizationInfo.address.province": (
                "/applicantInfo/organizationInfo/address/country",
                "USA: UNITED STATES",
                "readOnly",
                "enabled",
            ),
            "applicantInfo.contactPersonInfo.address.state": (
                "/applicantInfo/contactPersonInfo/address/country",
                "USA: UNITED STATES",
                "enabled",
                "disabled",
            ),
            "applicantInfo.contactPersonInfo.address.province": (
                "/applicantInfo/contactPersonInfo/address/country",
                "USA: UNITED STATES",
                "readOnly",
                "enabled",
            ),
            "applicantType.applicantTypeCodeOtherExplanation": (
                "/applicantType/applicantTypeCode",
                "X: Other (specify)",
                "enabled",
                "disabled",
            ),
            "applicantType.smallBusinessOrganizationType.sociallyEconomicallyDisadvantaged": (
                "/applicantType/applicantTypeCode",
                "R: Small Business",
                "enabled",
                "disabled",
            ),
            "applicantType.smallBusinessOrganizationType.womenOwned": (
                "/applicantType/applicantTypeCode",
                "R: Small Business",
                "enabled",
                "disabled",
            ),
            "applicationType.otherAgencySubmissionExplanation": (
                "/applicationType/isOtherAgencySubmission",
                "Y: Yes",
                "enabled",
                "disabled",
            ),
            "applicationType.revisionCode": (
                "/applicationType/applicationTypeCode",
                "Revision",
                "enabled",
                "disabled",
            ),
            "applicationType.revisionCodeOtherExplanation": (
                "/applicationType/revisionCode",
                "E",
                "enabled",
                "disabled",
            ),
            "principalInvestigator.address.province": (
                "/principalInvestigator/address/country",
                "USA: UNITED STATES",
                "readOnly",
                "enabled",
            ),
            "stateReview.stateReviewDate": (
                "/stateReview/stateReviewCodeType",
                "Y: Yes",
                "enabled",
                "disabled",
            ),
            "authorizedRepresentative.address.state": (
                "/authorizedRepresentative/address/country",
                "USA: UNITED STATES",
                "enabled",
                "disabled",
            ),
            "authorizedRepresentative.address.province": (
                "/authorizedRepresentative/address/country",
                "USA: UNITED STATES",
                "readOnly",
                "enabled",
            ),
        }
        self.assertEqual(
            {row["canonicalPath"] for row in compiled}, set(expected_conditionals)
        )
        self.assertTrue(all(row["authority"] == "unresolved" for row in compiled))
        self.assertTrue(all(row["owner"] == "form-semantic-review" for row in compiled))
        self.assertTrue(
            all(row["reason"] and row["removalCondition"] for row in compiled)
        )

        ui = json.loads(
            (
                ROOT / "dist/forms/rr-sf424-multi-project-cover/sgg/ui-schema.json"
            ).read_text()
        )
        emitted = {
            field["definition"]
            .removeprefix("/properties/")
            .replace("/properties/", "."): field["conditional"]
            for section in ui
            for field in section["children"]
            if "conditional" in field
        }
        self.assertEqual(set(emitted), set(expected_conditionals))
        for path, (pointer, value, then, otherwise) in expected_conditionals.items():
            self.assertEqual(
                emitted[path],
                {
                    "when": {
                        "op": "equals",
                        "ref": {"scope": "root", "pointer": pointer},
                        "value": value,
                    },
                    "then": {"interaction": then},
                    "otherwise": {"interaction": otherwise},
                },
            )

    def test_semantic_identity_packet_is_exact_and_unaccepted(self) -> None:
        evidence = json.loads(
            (
                ROOT / "evidence/forms/rr-sf424-multi-project-cover/evidence.json"
            ).read_text()
        )
        review = evidence["semanticReview"]
        expected_pointers = {
            "#/properties/stateReceivedDate",
            "#/properties/stateId",
            "#/properties/agencyRoutingNumber",
            "#/properties/grantsTrackingNumber",
            "#/properties/submissionTypeCode",
            "#/properties/applicantId",
            "#/properties/federalId",
            "#/properties/applicantType/properties/applicantTypeCode",
            "#/properties/applicantType/properties/applicantTypeCodeOtherExplanation",
            "#/properties/applicantType/properties/smallBusinessOrganizationType/properties/sociallyEconomicallyDisadvantaged",
            "#/properties/applicantType/properties/smallBusinessOrganizationType/properties/womenOwned",
            "#/properties/applicationType/properties/applicationTypeCode",
            "#/properties/applicationType/properties/isOtherAgencySubmission",
            "#/properties/applicationType/properties/otherAgencySubmissionExplanation",
            "#/properties/applicationType/properties/revisionCode",
            "#/properties/applicationType/properties/revisionCodeOtherExplanation",
            "#/properties/estimatedProjectFunding/properties/totalEstimatedAmount",
            "#/properties/estimatedProjectFunding/properties/totalNonFederalRequested",
            "#/properties/estimatedProjectFunding/properties/totalFederalNonFederalRequested",
            "#/properties/estimatedProjectFunding/properties/estimatedProgramIncome",
            "#/properties/stateReview/properties/stateReviewCodeType",
            "#/properties/stateReview/properties/stateReviewDate",
        }
        self.assertEqual(review["status"], "proposed")
        self.assertEqual(
            {mapping["canonicalPointer"] for mapping in review["mappings"]},
            expected_pointers,
        )
        self.assertEqual(len(review["mappings"]), 22)
        self.assertTrue(
            all(
                mapping["sourceId"] == "source-2-5d5599068d72"
                for mapping in review["mappings"]
            )
        )
        self.assertTrue(
            all(mapping["status"] == "proposed" for mapping in review["mappings"])
        )
        self.assertTrue(all(mapping["note"] for mapping in review["mappings"]))
        self.assertTrue(
            all("reviewedBy" not in mapping for mapping in review["mappings"])
        )


if __name__ == "__main__":
    unittest.main()
