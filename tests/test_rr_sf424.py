from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from scripts.promote_crosswalk import export_packet


ROOT = Path(__file__).parents[1]
CROSSWALK = ROOT.parent / "Smarter-grants-management"
CROSSWALK_REVISION = "dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef"


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
        self.assertTrue(all(mapping["status"] == "proposed" for mapping in review["mappings"]))
        self.assertTrue(all("reviewedBy" not in mapping for mapping in review["mappings"]))


if __name__ == "__main__":
    unittest.main()
