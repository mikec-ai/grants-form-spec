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


class PHS398ModularBudgetTests(unittest.TestCase):
    def test_promotion_packet_is_pinned_and_preserves_runtime_evidence(self) -> None:
        if not (CROSSWALK / ".git").exists():
            self.skipTest("pinned crosswalk checkout is unavailable")
        packet = export_packet(CROSSWALK, "PHS398ModularBudget", CROSSWALK_REVISION)
        self.assertEqual(packet["metrics"], {
            "sourceRecords": 44,
            "sourceBehaviors": 21,
            "applicantBehaviorRecords": 13,
            "presentationBehaviorRecords": 0,
            "runtimeRules": 16,
            "semanticProposals": 44,
            "acceptedSemanticMappings": 0,
            "openReviewGates": 37,
        })
        self.assertEqual(
            packet["extraction"]["sourceSetSha256"],
            "4add1297349b180ccc7e270d98449201e1ec83f5cdbfa2eea6828c956993a8b6",
        )
        calculations = [rule for rule in packet["runtimeRules"] if rule["mechanism"] == "calculation"]
        evaluation_order = [
            rule for rule in packet["runtimeRules"] if rule["mechanism"] == "evaluation_order"
        ]
        self.assertEqual(len(calculations), 8)
        self.assertEqual(len(evaluation_order), 8)
        self.assertTrue(all(isinstance(rule["sourceValue"], str) for rule in evaluation_order))
        self.assertTrue(all(not row["publishable"] for row in packet["semanticProposals"]))

    def test_form_compiles_modular_periods_calculations_and_attachments(self) -> None:
        root = ROOT / "dist/forms/phs398-modular-budget"
        schema = load(root / "schema.json")
        ui = load(root / "sgg/ui-schema.json")
        rules = load(root / "sgg/rule-schema.json")
        period = load(ROOT / "dist/question-bank/budget/phs398-modular/period/schema.json")
        fields = [row for row in objects(ui) if row.get("type") == "field"]
        lists = [row for row in objects(ui) if row.get("type") == "fieldList"]
        calculations = [row["gg_pre_population"] for row in objects(rules) if "gg_pre_population" in row]

        self.assertEqual(len(fields), 13)
        self.assertEqual(len(lists), 2)
        self.assertEqual(schema["properties"]["periods"]["maxItems"], 5)
        indirect_items = period["$defs"]["PHSModularIndirectCosts"]["properties"][
            "indirectCostItems"
        ]
        self.assertEqual(indirect_items["maxItems"], 4)
        direct_choice = period["$defs"]["PHSModularDirectCosts"]["properties"][
            "directCostLessConsortiumFandA"
        ]
        self.assertNotIn("enum", direct_choice)

        self.assertEqual(len(calculations), 8)
        self.assertEqual(sorted(rule["order"] for rule in calculations), list(range(1, 9)))
        self.assertEqual(
            rules["periods"]["directCosts"]["totalDirectCosts"]["gg_pre_population"]["fields"],
            ["@THIS.directCostLessConsortiumFandA", "@THIS.consortiumFandA"],
        )
        self.assertEqual(
            rules["cumulativeBudgetInformation"]["cumulativeTotalDirectAndIndirectCosts"]
            ["gg_pre_population"]["fields"],
            ["periods[*].totalDirectAndIndirectCosts"],
        )
        self.assertEqual(
            sum(
                row.get("gg_validation", {}).get("rule") == "attachment"
                for row in objects(rules)
            ),
            3,
        )

        evidence = load(root / "evidence.json")
        manifest = load(root / "manifest.json")
        profile = load(root / "targets/grants-gov-xml.json")
        self.assertEqual(evidence["semanticReview"], {"status": "unreviewed", "mappings": []})
        self.assertEqual(manifest["artifacts"]["targets/grants-gov-xml.json"], "generated")
        self.assertEqual(
            profile["xsd"]["sha256"],
            "f166abebd40e6912861dca5c5c4a83c7a82779f1ae67a2c0fa8b4aafc25d5bff",
        )


if __name__ == "__main__":
    unittest.main()
