from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "dist" / "forms"
QUESTIONS = ROOT / "dist" / "question-bank" / "budget" / "research"
AUDIT = ROOT / "analysis" / "rr-budget-source-content-audit.v1.json"

DAT_SHA256 = "c85158ce7ddcc756d6e8a55a050e00b4a95cdfc8d9a2d91b7bd94c7f8bdb1035"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def collect_rules(node: object, rule_name: str) -> list[dict]:
    matches: list[dict] = []
    if isinstance(node, dict):
        validation = node.get("gg_validation")
        if isinstance(validation, dict) and validation.get("rule") == rule_name:
            matches.append(validation)
        for value in node.values():
            matches.extend(collect_rules(value, rule_name))
    elif isinstance(node, list):
        for value in node:
            matches.extend(collect_rules(value, rule_name))
    return matches


class ResearchBudgetSourceContentTests(unittest.TestCase):
    def test_attachment_pair_labels_and_help_are_exact_f770_records(self) -> None:
        equipment = load(QUESTIONS / "equipment" / "schema.json")["properties"]
        key_personnel = load(QUESTIONS / "key-personnel" / "schema.json")["properties"]

        self.assertEqual(
            equipment["additionalEquipmentsAttachment"],
            {
                "$ref": "../../../../question-bank/budget/research/additional-equipment/schema.json",
                "title": "Additional Equipment:",
                "description": (
                    "One possible attachment per budget period. Required if "
                    "TotalFundForAttachedEquipment is entered and greater than zero."
                ),
            },
        )
        self.assertEqual(
            equipment["totalFundForAttachedEquipment"]["description"],
            "Required and must be greater than zero if an AdditionalEquipmentsAttachment exists.",
        )
        self.assertEqual(
            key_personnel["attachedKeyPersons"]["description"],
            (
                "One possible attachment per budget period. Required if "
                "TotalFundForAttachedKeyPersons is entered and greater than zero."
            ),
        )
        self.assertEqual(
            key_personnel["totalFundForAttachedKeyPersons"]["description"],
            "Required and must be greater than zero if an AttachedKeyPersons attachment exists.",
        )

    def test_end_date_source_rule_compiles_once_in_every_family_profile(self) -> None:
        period = load(QUESTIONS / "period" / "schema.json")["properties"]
        self.assertEqual(
            period["budgetPeriodEndDate"]["description"],
            "End Date cannot be before Start Date.",
        )

        for form_id in (
            "rr-budget",
            "rr-budget-10yr",
            "rr-subaward-budget",
            "rr-subaward-budget-30",
            "rr-subaward-budget-10yr-30",
        ):
            with self.subTest(form_id=form_id):
                rules = load(FORMS / form_id / "sgg" / "rule-schema.json")
                self.assertEqual(
                    collect_rules(rules, "date_not_before"),
                    [
                        {
                            "rule": "date_not_before",
                            "fields": ["@THIS.budgetPeriodStartDate"],
                        }
                    ],
                )

    def test_audit_keeps_source_pin_and_unresolved_boundaries_explicit(self) -> None:
        audit = load(AUDIT)
        self.assertEqual(audit["source"]["sha256"], DAT_SHA256)
        self.assertEqual(audit["source"]["nativeVersion"], "3.0")
        self.assertEqual(len(audit["implementedCorrections"]), 5)
        self.assertEqual(
            {item["sourcePath"] for item in audit["implementedCorrections"]},
            {"0-11", "A-2-1", "A-3-1", "C-2-0", "C-2-1"},
        )
        self.assertEqual(audit["semanticReview"]["status"], "unreviewed")
        self.assertEqual(
            {path for item in audit["unresolved"] for path in item["sourcePaths"]},
            {"B-1-2", "B-2-2", "B-3-2", "B-4-2", "0-06", "0-07", "0-08", "0-10", "L-1-1"},
        )


if __name__ == "__main__":
    unittest.main()
