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


class RRKeyPersonExpandedTests(unittest.TestCase):
    def test_promotion_packet_preserves_broad_evidence_without_false_conflict(self) -> None:
        if not (CROSSWALK / ".git").exists():
            self.skipTest("pinned crosswalk checkout is unavailable")

        packet = export_packet(CROSSWALK, "RRKeyPersonExpanded", CROSSWALK_REVISION)

        self.assertEqual(packet["metrics"], {
            "sourceRecords": 101,
            "sourceBehaviors": 67,
            "applicantBehaviorRecords": 56,
            "presentationBehaviorRecords": 8,
            "runtimeRules": 10,
            "semanticProposals": 101,
            "acceptedSemanticMappings": 0,
            "openReviewGates": 73,
        })
        self.assertEqual(
            packet["extraction"]["sourceSetSha256"],
            "8866396d99e32eeec6618ea63c52c2b205718dc481482b27ab61699ecd2efeb0",
        )
        self.assertFalse(any(
            gate["kind"] == "source_conflict" for gate in packet["reviewGates"]
        ))
        self.assertTrue(all(not row["publishable"] for row in packet["semanticProposals"]))

    def test_form_compiles_repeated_people_and_typed_conditions_generically(self) -> None:
        root = ROOT / "dist/forms/rr-key-person-expanded"
        schema = load(root / "schema.json")
        ui = load(root / "sgg/ui-schema.json")
        rules = load(root / "sgg/rule-schema.json")
        all_ui = list(objects(ui))
        fields = [row for row in all_ui if row.get("type") == "field"]
        conditions = [row["conditional"] for row in fields if "conditional" in row]

        self.assertEqual(len(schema["properties"]), 5)
        self.assertEqual(schema["required"], ["principalInvestigator"])
        self.assertEqual(schema["properties"]["seniorKeyPersons"]["maxItems"], 99)
        self.assertEqual(len(fields), 57)
        self.assertEqual(len(conditions), 6)
        self.assertEqual(sum(c["when"]["op"] == "in" for c in conditions), 2)
        self.assertTrue(all(
            c["when"]["values"] == ["Other Professional", "Other (Specify)"]
            for c in conditions if c["when"]["op"] == "in"
        ))

        rule_objects = list(objects(rules))
        self.assertEqual(sum(row.get("gg_validation", {}).get("rule") == "attachment"
                             for row in rule_objects), 7)

        role_schema = load(ROOT / "dist/question-bank/research-person/details/schema.json")
        self.assertEqual(
            role_schema["$defs"]["ResearchProjectRole"]["enum"],
            [
                "PD/PI", "Co-PD/PI", "Faculty", "Post Doctoral",
                "Post Doctoral Associate", "Post Doctoral Scholar",
                "Other Professional", "Graduate Student", "Undergraduate Student",
                "Technician", "Consultant", "Co-Investigator", "Other (Specify)",
            ],
        )
        required_branches = role_schema["allOf"]
        self.assertEqual(len(required_branches), 2)
        self.assertTrue(all(
            branch["then"]["required"] == ["otherProjectRole"]
            for branch in required_branches
        ))

        evidence = load(root / "evidence.json")
        self.assertEqual(evidence["semanticReview"], {"status": "unreviewed", "mappings": []})


if __name__ == "__main__":
    unittest.main()
