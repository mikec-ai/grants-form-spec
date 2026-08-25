from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
AUDIT = ROOT / "research/rr-federal-non-federal-budget/source-audit.json"


def load_audit() -> dict[str, object]:
    return json.loads(AUDIT.read_text())


class RRFederalNonFederalBudgetSourceAuditTests(unittest.TestCase):
    def test_exact_crosswalk_revision_and_official_sources_remain_pinned(self) -> None:
        audit = load_audit()
        receipt = audit["crosswalkReceipt"]
        sources = audit["sources"]

        self.assertEqual(
            receipt["revision"],
            "4312f6504b060e2b9ffdbd2307fc41130c3123a0",
        )
        self.assertEqual(receipt["portfolioRecordId"], "frozen:RRFedNonFedBudget")
        self.assertEqual(receipt["canonicalMetadata"]["fid"], "738")
        self.assertEqual(
            sources["xsd"]["sha256"],
            "2ae0445e5f0a7228c1b0cdecbedc8fb4bb064f6249644e20f3dc99164bd44a1f",
        )
        self.assertEqual(
            sources["dat"]["sha256"],
            "cfa2cd8cb6003f44093c085fd3503c8b32d7cf6ac4a15c6362ca706fa5c8255e",
        )

    def test_source_structure_and_behavior_queue_remain_separate(self) -> None:
        audit = load_audit()
        inventory = audit["deterministicInventory"]
        xsd = inventory["xsd"]
        accounting = inventory["crosswalkSourceAccounting"]
        queue = inventory["behaviorReviewQueue"]

        self.assertEqual(xsd["rootSequenceChildren"], 6)
        self.assertEqual(xsd["requiredRootChildren"], 5)
        self.assertEqual(xsd["optionalRootChildren"], 1)
        self.assertEqual(
            xsd["repeatingRootChildren"],
            [{"name": "BudgetYear", "minOccurs": 1, "maxOccurs": 5}],
        )
        self.assertEqual(accounting["questionAndStructureRecords"], 364)
        self.assertEqual(accounting["behaviorRecords"], 391)
        self.assertEqual(queue["status"], "agent_proposed")
        self.assertEqual(queue["acceptedBindings"], 0)
        self.assertFalse(queue["publishedCoverageEligible"])

    def test_no_variant_oracle_runtime_or_subaward_wrapper_claim_is_made(self) -> None:
        audit = load_audit()

        self.assertEqual(
            audit["semanticBoundary"]["parameterizedVariantClaim"], "not_accepted"
        )
        self.assertEqual(audit["oracleBoundary"]["legacySimplerOracle"], "not_found")
        self.assertEqual(
            audit["oracleBoundary"]["runtimeCompatibilityClaim"], "not_made"
        )
        self.assertEqual(
            audit["oracleBoundary"]["consumerReadinessClaim"], "not_made"
        )
        self.assertEqual(audit["scopeBoundary"]["subawardTenYearWrapper"], "excluded")
        self.assertEqual(
            audit["scopeBoundary"]["subawardThirtyYearWrapper"], "excluded"
        )
        self.assertEqual(
            audit["scopeBoundary"]["productionFormDeclaration"], "not_created"
        )
        self.assertEqual(audit["sources"]["pdf"]["reviewState"], "not_acquired")


if __name__ == "__main__":
    unittest.main()
