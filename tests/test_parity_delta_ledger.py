from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_parity_delta_ledger import ROOT, validate_ledger

LEDGER = ROOT / "parity" / "legacy-deltas.v1.json"


class ParityDeltaLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = json.loads(LEDGER.read_text())

    def _write(self, document: dict) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "ledger.json"
        path.write_text(json.dumps(document))
        return path

    def test_current_ledger_is_exact_proposed_and_offline_verified(self) -> None:
        ledger = validate_ledger(ROOT, LEDGER)
        self.assertEqual(len(ledger["records"]), 50)
        self.assertEqual(
            len(
                {
                    (
                        row["formId"],
                        row["target"]["dimension"],
                        row["target"]["differenceKey"],
                    )
                    for row in ledger["records"]
                }
            ),
            50,
        )
        self.assertEqual({row["review"]["status"] for row in ledger["records"]}, {"proposed"})
        self.assertEqual(
            sum(row["sourceSupport"]["status"] == "verified" for row in ledger["records"]),
            16,
        )
        self.assertEqual(
            sum(row["sourceSupport"]["status"] == "unverified" for row in ledger["records"]),
            34,
        )
        self.assertTrue(
            all(
                row["classification"] == "authoritative_source_correction"
                for row in ledger["records"]
                if row["sourceSupport"]["status"] == "verified"
            )
        )

    def test_rejects_missing_and_stale_exact_targets(self) -> None:
        missing = copy.deepcopy(self.ledger)
        missing["records"][0]["target"]["semanticTarget"]["value"] = "/properties/notReal"
        with self.assertRaisesRegex(ValueError, "semantic target is absent"):
            validate_ledger(ROOT, self._write(missing))

        duplicate = copy.deepcopy(self.ledger)
        duplicate["records"].append(copy.deepcopy(duplicate["records"][0]))
        duplicate["records"][-1]["id"] = "different-id"
        with self.assertRaisesRegex(ValueError, "duplicate or incomplete exact delta target"):
            validate_ledger(ROOT, self._write(duplicate))

    def test_rejects_rule_target_until_exact_rule_resolution_exists(self) -> None:
        unsupported = copy.deepcopy(self.ledger)
        unsupported["records"][0]["target"]["semanticTarget"] = {
            "kind": "rule_path",
            "value": "/rules/example",
        }
        with self.assertRaisesRegex(ValueError, "semantic target is absent"):
            validate_ledger(ROOT, self._write(unsupported))

    def test_rejects_missing_evidence_and_assertion(self) -> None:
        missing = copy.deepcopy(self.ledger)
        missing["records"][0]["evidenceReferences"] = []
        with self.assertRaisesRegex(ValueError, "no evidence reference"):
            validate_ledger(ROOT, self._write(missing))

        assertion = copy.deepcopy(self.ledger)
        assertion["records"][0]["differentialAssertion"]["evidenceReferenceId"] = "missing"
        with self.assertRaisesRegex(ValueError, "no exercising differential assertion"):
            validate_ledger(ROOT, self._write(assertion))

    def test_accepted_review_requires_decision_evidence(self) -> None:
        accepted = copy.deepcopy(self.ledger)
        accepted["records"][0]["review"] = {
            "status": "accepted",
            "reviewer": "accountable-reviewer",
            "reviewedAt": "2026-08-24T12:00:00Z",
            "decisionEvidence": [],
        }
        with self.assertRaisesRegex(ValueError, "accepted review lacks"):
            validate_ledger(ROOT, self._write(accepted))

    def test_accepted_review_requires_resolved_classification(self) -> None:
        accepted = copy.deepcopy(self.ledger)
        accepted["records"][0]["review"] = {
            "status": "accepted",
            "reviewer": "accountable-reviewer",
            "reviewedAt": "2026-08-24T12:00:00Z",
            "decisionEvidence": [accepted["records"][0]["evidenceReferences"][0]],
        }
        with self.assertRaisesRegex(ValueError, "lacks a resolved classification"):
            validate_ledger(ROOT, self._write(accepted))

    def test_authoritative_source_classification_requires_verified_support(self) -> None:
        unsupported = copy.deepcopy(self.ledger)
        unsupported["records"][0]["classification"] = "authoritative_source_correction"
        with self.assertRaisesRegex(ValueError, "lacks verified source support"):
            validate_ledger(ROOT, self._write(unsupported))

    def test_accepted_review_requires_independent_decision_artifact_receipt(self) -> None:
        accepted = copy.deepcopy(self.ledger)
        record = next(
            row
            for row in accepted["records"]
            if row["classification"] == "authoritative_source_correction"
        )
        record["review"] = {
            "status": "accepted",
            "reviewer": "accountable-reviewer",
            "reviewedAt": "2026-08-24T12:00:00Z",
            "decisionEvidence": [record["evidenceReferences"][0]],
        }
        with self.assertRaisesRegex(ValueError, "independent decision-artifact receipt"):
            validate_ledger(ROOT, self._write(accepted))

    def test_cli_rejects_unknown_flags_with_usage_exit(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/validate_parity_delta_ledger.py", "--unknown"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("unrecognized arguments", result.stderr)


if __name__ == "__main__":
    unittest.main()
