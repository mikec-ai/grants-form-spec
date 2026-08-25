from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
AUDIT = ROOT / "research/sf425/source-audit.json"


def load_audit() -> dict[str, object]:
    return json.loads(AUDIT.read_text())


class SF425SourceAuditTests(unittest.TestCase):
    def test_exact_crosswalk_revision_and_source_artifacts_remain_pinned(self) -> None:
        audit = load_audit()
        receipt = audit["crosswalkReceipt"]
        sources = audit["sources"]

        self.assertEqual(
            receipt["revision"],
            "4312f6504b060e2b9ffdbd2307fc41130c3123a0",
        )
        self.assertEqual(receipt["recordId"], "expanded:SF425_3_0-V3.0_F751")
        self.assertEqual(
            sources["xsd"]["sha256"],
            "0f5cd6705399fb4c2dd4310150de49e3f9f0abd00349d3bc2983aa9bc13eee69",
        )
        self.assertEqual(
            sources["dat"]["sha256"],
            "6f44d8d685dd84f28df66b390f79d237b78a26a81e4ca1b412df1c39f429eb7d",
        )

    def test_deterministic_structure_is_separate_from_unreviewed_semantics(self) -> None:
        audit = load_audit()
        inventory = audit["deterministicInventory"]
        xsd = inventory["xsd"]
        queue = inventory["datBehaviorReviewQueue"]

        self.assertEqual(xsd["rootSequenceChildren"], 49)
        self.assertEqual(xsd["requiredRootChildren"], 18)
        self.assertEqual(xsd["optionalRootChildren"], 31)
        self.assertEqual(
            xsd["repeatingRootChildren"],
            [{"name": "IndirectExpense", "minOccurs": 1, "maxOccurs": 2}],
        )
        self.assertEqual(queue["status"], "not_reviewed")
        self.assertEqual(queue["behaviorRecords"], 252)
        self.assertEqual(queue["acceptedBindings"], 0)
        self.assertEqual(audit["semanticBoundary"]["acceptedMappings"], 0)
        self.assertFalse(audit["semanticBoundary"]["publishedCoverageEligible"])

    def test_no_oracle_runtime_consumer_or_rendered_parity_claim_is_made(self) -> None:
        audit = load_audit()

        self.assertEqual(audit["oracleBoundary"]["legacySimplerOracle"], "not_found")
        self.assertEqual(
            audit["oracleBoundary"]["runtimeCompatibilityClaim"], "not_made"
        )
        self.assertEqual(
            audit["oracleBoundary"]["consumerReadinessClaim"], "not_made"
        )
        self.assertEqual(audit["sources"]["pdf"]["reviewState"], "not_acquired")
        self.assertEqual(audit["sources"]["pdf"]["reviewedPages"], [])


if __name__ == "__main__":
    unittest.main()
