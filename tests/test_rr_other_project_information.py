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
        self.assertEqual(packet["metrics"], {
            "sourceRecords": 63,
            "sourceBehaviors": 54,
            "applicantBehaviorRecords": 54,
            "presentationBehaviorRecords": 0,
            "runtimeRules": 24,
            "semanticProposals": 63,
            "acceptedSemanticMappings": 0,
            "openReviewGates": 61,
        })
        self.assertEqual(
            packet["extraction"]["sourceSetSha256"],
            "c3ebbfc4870fb5be7c7afc3ad84bec0717329458745e5d36b3361de04fe79a04",
        )
        self.assertTrue(all(not row["publishable"] for row in packet["semanticProposals"]))

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
            {
                row["definition"]
                for row in fields
                if "conditional" in row
            },
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
        conditional_required = set()
        for question_id in (
            "human-subjects",
            "vertebrate-animals",
            "environmental-impact",
            "historic-designation",
            "international-activities",
        ):
            question = load(
                ROOT
                / f"dist/question-bank/research-project/{question_id}/schema.json"
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
        self.assertEqual(evidence["semanticReview"], {"status": "unreviewed", "mappings": []})
        self.assertEqual(manifest["artifacts"]["targets/grants-gov-xml.json"], "generated")
        self.assertEqual(
            profile["xsd"]["sha256"],
            "b2144c290ed5ad6d942e70815d195d7d6aa4e8e6c82fc3932d8540e3aa303ef5",
        )


if __name__ == "__main__":
    unittest.main()
