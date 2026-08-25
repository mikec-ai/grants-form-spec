from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.promote_crosswalk import export_packet

ROOT = Path(__file__).parents[1]
CROSSWALK = ROOT.parent / "grants-question-crosswalk-mp-cover"
CROSSWALK_REVISION = "4312f6504b060e2b9ffdbd2307fc41130c3123a0"


def load(path: Path) -> object:
    return json.loads(path.read_text())


def objects(value: object):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


class RROtherProjectInformationTests(unittest.TestCase):
    def test_promotion_packet_is_pinned_and_review_gated(self) -> None:
        if not (CROSSWALK / ".git").exists():
            self.skipTest("pinned crosswalk checkout is unavailable")
        packet = export_packet(CROSSWALK, "RROtherProjectInfo", CROSSWALK_REVISION)
        self.assertEqual(
            packet["metrics"],
            {
                "sourceRecords": 63,
                "sourceBehaviors": 54,
                "applicantBehaviorRecords": 54,
                "presentationBehaviorRecords": 0,
                "runtimeRules": 24,
                "semanticProposals": 63,
                "acceptedSemanticMappings": 0,
                "openReviewGates": 61,
            },
        )
        self.assertEqual(
            packet["extraction"]["sourceSetSha256"],
            "c3ebbfc4870fb5be7c7afc3ad84bec0717329458745e5d36b3361de04fe79a04",
        )
        self.assertTrue(
            all(not row["publishable"] for row in packet["semanticProposals"])
        )

    def test_exact_source_behaviors_are_pinned_without_semantic_acceptance(
        self,
    ) -> None:
        evidence = load(
            ROOT / "evidence/forms/rr-other-project-information/evidence.json"
        )
        source = evidence["sources"][0]
        self.assertEqual(
            source,
            {
                "id": "source-1-54234acd9882",
                "sha256": "54234acd9882a129120c0a5dd44c5cde2998b66ffdfe91a4bb4a745e0d39c2ff",
                "type": "dat",
                "uri": "https://apply07.grants.gov/apply/forms/formversions/RR_OtherProjectInfo_1_4-V1.4_F619.xls",
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
                    "/humanSubjects/exemptFromFederalRegulations",
                    "01-a-1",
                    "Required if YES to question 01-0, otherwise disabled.",
                ),
                (
                    "/humanSubjects/exemptions",
                    "01-a-1c",
                    "Required if YES selected for question 01-a-1, otherwise disabled.",
                ),
                (
                    "/humanSubjects/exemptions",
                    "01-a-1d",
                    "Enabled only if ExemptFedReg = Yes.",
                ),
                (
                    "/humanSubjects/exemptions",
                    "01-a-1e",
                    "Enabled only if ExemptFedReg = Yes.",
                ),
                (
                    "/humanSubjects/exemptions",
                    "01-a-1f",
                    "Enabled only if ExemptFedReg = Yes.",
                ),
                (
                    "/humanSubjects/exemptions",
                    "01-a-1g",
                    "Enabled only if ExemptFedReg = Yes.",
                ),
                (
                    "/humanSubjects/exemptions",
                    "01-a-1h",
                    "Enabled only if ExemptFed = Yes.",
                ),
                (
                    "/humanSubjects/exemptions",
                    "01-a-1i",
                    "Enabled only if ExemptFedReg = Yes.",
                ),
                (
                    "/humanSubjects/exemptions",
                    "01-a-1j",
                    "Enabled only if ExemptFedReg = Yes.",
                ),
                (
                    "/humanSubjects/exemptions",
                    "01-a-1k",
                    "Enabled only if ExemptFedReg = Yes.",
                ),
                (
                    "/humanSubjects/irbReviewPending",
                    "01-a-2a",
                    "Required if ExemptFedReg = No. Otherwise disabled.",
                ),
                (
                    "/humanSubjects/irbApprovalDate",
                    "01-a-3",
                    "Required if IRBReviewPending = No, otherwise disabled.",
                ),
                (
                    "/humanSubjects/assuranceNumber",
                    "01-a-4",
                    'Active only if "Yes" to HumanSubjectsIndicator.',
                ),
                (
                    "/vertebrateAnimals/iacucReviewPending",
                    "02-a-2a",
                    "Required if VertebrateAnimalsIndicator = Yes. Otherwise disabled.",
                ),
                (
                    "/vertebrateAnimals/iacucApprovalDate",
                    "02-a-3",
                    "Required if VertebrateAnimalsIACUCReviewIndicator = No. Otherwise disabled.",
                ),
                (
                    "/vertebrateAnimals/assuranceNumber",
                    "02-a-4",
                    "Required if VertebrateAnimalsIACUCReviewIndicator = No. Enabled only if VertebrateAnimalsIndicator = Yes.",
                ),
                (
                    "/environmentalImpact/environmentalImpactExplanation",
                    "04-b",
                    "Required if EnvironmentalImpactIndicator is Yes, otherwise disabled",
                ),
                (
                    "/environmentalImpact/hasEnvironmentalExemptionOrAssessment",
                    "04-c",
                    "Enabled only if answer to 4.a. = Yes.",
                ),
                (
                    "/environmentalImpact/environmentalExemptionOrAssessmentExplanation",
                    "04-d",
                    "Required if EnvironmentalExemptionIndicator is Yes, otherwise disabled",
                ),
                (
                    "/historicPlaces/explanation",
                    "05-a",
                    "Required if HistoricDesignation is Yes, otherwise disabled",
                ),
                (
                    "/internationalActivities/countries",
                    "06-a",
                    "Required if InternationalActivitiesIndicator is Yes, otherwise disabled",
                ),
                (
                    "/projectSummaryAbstract",
                    "07-0",
                    "Required unless SubmissionTypeCode (SF424(R&R)) on Cover Page is Pre-application. Validation occurs server-side, not on PDF or webform.",
                ),
                (
                    "/projectNarrative",
                    "08-0",
                    "Required unless SubmissionTypeCode (SF424(R&R)) on Cover Page is Pre-application. Validation occurs server-side, not on PDF or webform.",
                ),
                (
                    "/otherAttachments",
                    "12-1",
                    "Read only checkbox, no matching xml data element. Indicates whether an Optional Other Attachment is attached.",
                ),
            ],
        )
        self.assertTrue(
            all(
                row["sourceId"] == source["id"]
                and row["executionStatus"] == "source-bound-uncompiled"
                for row in official
            )
        )
        compiled = [
            row
            for row in evidence["behaviorEvidence"]
            if row["executionStatus"] == "compiled"
        ]
        self.assertEqual(
            {row["canonicalPath"] for row in compiled},
            {
                "humanSubjects.exemptFromFederalRegulations",
                "humanSubjects.exemptions",
                "humanSubjects.irbReviewPending",
                "humanSubjects.irbApprovalDate",
                "humanSubjects.assuranceNumber",
                "vertebrateAnimals.iacucReviewPending",
                "vertebrateAnimals.iacucApprovalDate",
                "vertebrateAnimals.assuranceNumber",
                "environmentalImpact.environmentalImpactExplanation",
                "environmentalImpact.hasEnvironmentalExemptionOrAssessment",
                "environmentalImpact.environmentalExemptionOrAssessmentExplanation",
                "historicPlaces.explanation",
                "internationalActivities.countries",
            },
        )
        self.assertTrue(all(row["authority"] == "unresolved" for row in compiled))
        self.assertEqual(
            evidence["semanticReview"], {"status": "unreviewed", "mappings": []}
        )

    def test_form_compiles_policy_questions_and_distinct_attachments(self) -> None:
        root = ROOT / "dist/forms/rr-other-project-information"
        schema = load(root / "schema.json")
        ui = load(root / "sgg/ui-schema.json")
        rules = load(root / "sgg/rule-schema.json")
        human_subjects = load(
            ROOT / "dist/question-bank/research-project/human-subjects/schema.json"
        )
        fields = [row for row in objects(ui) if row.get("type") == "field"]
        conditions = [row["conditional"] for row in fields if "conditional" in row]

        self.assertEqual(len(fields), 26)
        self.assertEqual(len(conditions), 13)
        self.assertEqual(
            {row["definition"] for row in fields if "conditional" in row},
            {
                "/properties/humanSubjects/properties/exemptFromFederalRegulations",
                "/properties/humanSubjects/properties/exemptions",
                "/properties/humanSubjects/properties/irbReviewPending",
                "/properties/humanSubjects/properties/irbApprovalDate",
                "/properties/humanSubjects/properties/assuranceNumber",
                "/properties/vertebrateAnimals/properties/iacucReviewPending",
                "/properties/vertebrateAnimals/properties/iacucApprovalDate",
                "/properties/vertebrateAnimals/properties/assuranceNumber",
                "/properties/environmentalImpact/properties/environmentalImpactExplanation",
                "/properties/environmentalImpact/properties/hasEnvironmentalExemptionOrAssessment",
                "/properties/environmentalImpact/properties/environmentalExemptionOrAssessmentExplanation",
                "/properties/historicPlaces/properties/explanation",
                "/properties/internationalActivities/properties/countries",
            },
        )
        conditional_fields = {
            row["definition"]: row["conditional"]
            for row in fields
            if "conditional" in row
        }
        expected_triggers = {
            "/properties/humanSubjects/properties/exemptFromFederalRegulations": (
                "/humanSubjects/involvesHumanSubjects",
                "Y: Yes",
            ),
            "/properties/humanSubjects/properties/exemptions": (
                "/humanSubjects/exemptFromFederalRegulations",
                "Y: Yes",
            ),
            "/properties/humanSubjects/properties/irbReviewPending": (
                "/humanSubjects/exemptFromFederalRegulations",
                "N: No",
            ),
            "/properties/humanSubjects/properties/irbApprovalDate": (
                "/humanSubjects/irbReviewPending",
                "N: No",
            ),
            "/properties/humanSubjects/properties/assuranceNumber": (
                "/humanSubjects/involvesHumanSubjects",
                "Y: Yes",
            ),
            "/properties/vertebrateAnimals/properties/iacucReviewPending": (
                "/vertebrateAnimals/involvesVertebrateAnimals",
                "Y: Yes",
            ),
            "/properties/vertebrateAnimals/properties/iacucApprovalDate": (
                "/vertebrateAnimals/iacucReviewPending",
                "N: No",
            ),
            "/properties/vertebrateAnimals/properties/assuranceNumber": (
                "/vertebrateAnimals/iacucReviewPending",
                "N: No",
            ),
            "/properties/environmentalImpact/properties/environmentalImpactExplanation": (
                "/environmentalImpact/hasEnvironmentalImpact",
                "Y: Yes",
            ),
            "/properties/environmentalImpact/properties/hasEnvironmentalExemptionOrAssessment": (
                "/environmentalImpact/hasEnvironmentalImpact",
                "Y: Yes",
            ),
            "/properties/environmentalImpact/properties/environmentalExemptionOrAssessmentExplanation": (
                "/environmentalImpact/hasEnvironmentalExemptionOrAssessment",
                "Y: Yes",
            ),
            "/properties/historicPlaces/properties/explanation": (
                "/historicPlaces/hasHistoricDesignation",
                "Y: Yes",
            ),
            "/properties/internationalActivities/properties/countries": (
                "/internationalActivities/involvesInternationalActivities",
                "Y: Yes",
            ),
        }
        for definition, (pointer, value) in expected_triggers.items():
            with self.subTest(definition=definition):
                self.assertEqual(
                    conditional_fields[definition],
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
        conditional_required = set()
        for question_id in (
            "human-subjects",
            "vertebrate-animals",
            "environmental-impact",
            "historic-designation",
            "international-activities",
        ):
            question = load(
                ROOT / f"dist/question-bank/research-project/{question_id}/schema.json"
            )
            for row in objects(question):
                then = row.get("then")
                if "if" not in row or not isinstance(then, dict):
                    continue
                conditional_required.update(then.get("required", []))
        self.assertEqual(
            conditional_required,
            {
                "exemptFromFederalRegulations",
                "irbReviewPending",
                "irbApprovalDate",
                "assuranceNumber",
                "iacucReviewPending",
                "iacucApprovalDate",
                "environmentalImpactExplanation",
                "hasEnvironmentalExemptionOrAssessment",
                "environmentalExemptionOrAssessmentExplanation",
                "explanation",
                "countries",
            },
        )
        self.assertEqual(
            human_subjects["$defs"]["ResearchProjectYesNoCode"]["enum"],
            ["Y: Yes", "N: No"],
        )
        exemptions = human_subjects["properties"]["exemptions"]
        self.assertEqual(exemptions["minItems"], 1)
        self.assertEqual(exemptions["maxItems"], 8)
        self.assertEqual(
            human_subjects["$defs"]["HumanSubjectExemptionCode"]["enum"],
            ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"],
        )
        self.assertNotIn("projectSummaryAbstract", schema["required"])
        self.assertNotIn("projectNarrative", schema["required"])
        self.assertEqual(
            sum(
                row.get("gg_validation", {}).get("rule") == "attachment"
                for row in objects(rules)
            ),
            6,
        )

        evidence = load(root / "evidence.json")
        manifest = load(root / "manifest.json")
        profile = load(root / "targets/grants-gov-xml.json")
        self.assertEqual(
            evidence["semanticReview"], {"status": "unreviewed", "mappings": []}
        )
        self.assertEqual(
            manifest["artifacts"]["targets/grants-gov-xml.json"], "generated"
        )
        self.assertEqual(
            profile["xsd"]["sha256"],
            "b2144c290ed5ad6d942e70815d195d7d6aa4e8e6c82fc3932d8540e3aa303ef5",
        )


if __name__ == "__main__":
    unittest.main()
