from __future__ import annotations

import copy
import hashlib
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

    def _accepted_fixture(self) -> tuple[Path, Path]:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        (root / "dist/forms/example").mkdir(parents=True)
        (root / "dist/forms/example/index.json").write_text(
            json.dumps({"fieldOccurrences": [{"path": "/field"}]})
        )
        (root / "parity/decisions").mkdir(parents=True)
        decision_path = "parity/decisions/example-acceptance.json"
        record = {
            "id": "example.schema.delta",
            "formId": "example",
            "target": {
                "dimension": "schema",
                "differenceKey": "/field#type",
                "semanticTarget": {"kind": "canonical_form_path", "value": "/properties/field"},
            },
            "classification": "approved_incompatibility",
            "rationale": "Fixture delta requiring an accountable decision.",
            "sourceSupport": {"status": "unverified", "evidenceReferences": []},
            "evidenceReferences": [
                {
                    "id": "comparator-evidence",
                    "repository": "https://github.com/mikec-ai/simpler-grants-gov.git",
                    "revision": "1" * 40,
                    "path": "api/tests/example.py",
                }
            ],
            "differentialAssertion": {
                "comparatorContract": "sgg-portable-legacy-differential/v3",
                "evidenceReferenceId": "comparator-evidence",
                "testId": "test_example",
            },
            "review": {
                "status": "accepted",
                "reviewer": "accountable-reviewer",
                "reviewedAt": "2026-08-25T12:00:00Z",
                "decisionEvidence": [],
            },
        }
        decision = {
            "contract": "grants-form-parity-decision/v1",
            "id": "example-acceptance",
            "ledgerRecordId": record["id"],
            "formId": record["formId"],
            "target": record["target"],
            "classification": record["classification"],
            "decision": "accepted",
            "reviewer": record["review"]["reviewer"],
            "reviewedAt": record["review"]["reviewedAt"],
            "rationale": "The accountable reviewer accepts this exact bounded incompatibility.",
        }
        artifact_path = root / decision_path
        artifact_path.write_text(json.dumps(decision, sort_keys=True) + "\n")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
        subprocess.run(["git", "add", decision_path], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "Pin decision"], cwd=root, check=True)
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True
        ).stdout.strip()
        decision_reference = {
            "id": decision["id"],
            "repository": "https://github.com/mikec-ai/grants-form-spec.git",
            "revision": revision,
            "path": decision_path,
        }
        record["review"]["decisionEvidence"] = [decision_reference]
        comparator_receipt_path = root / "parity/comparator.json"
        comparator_receipt_path.write_text(
            json.dumps(
                {
                    "contract": "grants-form-parity-evidence-verification/v1",
                    "repository": record["evidenceReferences"][0]["repository"],
                    "revision": record["evidenceReferences"][0]["revision"],
                    "files": [{"path": "api/tests/example.py", "sha256": "2" * 64}],
                }
            )
        )
        decision_receipt_path = root / "parity/decision-verification.v1.json"
        decision_receipt_path.write_text(
            json.dumps(
                {
                    "contract": "grants-form-parity-decision-verification/v1",
                    "artifacts": [
                        {
                            **{key: decision_reference[key] for key in ("repository", "revision", "path")},
                            "sha256": hashlib.sha256(artifact_path.read_bytes()).hexdigest(),
                        }
                    ],
                }
            )
        )
        ledger = {
            "contract": "grants-form-parity-delta-ledger/v1",
            "evidenceVerification": {
                "repository": record["evidenceReferences"][0]["repository"],
                "revision": record["evidenceReferences"][0]["revision"],
                "receipt": "parity/comparator.json",
            },
            "decisionVerification": {"receipt": "parity/decision-verification.v1.json"},
            "records": [record],
        }
        ledger_path = root / "parity/ledger.json"
        ledger_path.write_text(json.dumps(ledger))
        return root, ledger_path

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
        with self.assertRaisesRegex(ValueError, "absent from the offline verification receipt"):
            validate_ledger(ROOT, self._write(accepted))

    def test_accepts_exact_offline_verified_accountable_decision(self) -> None:
        root, ledger_path = self._accepted_fixture()

        ledger = validate_ledger(root, ledger_path)

        self.assertEqual(ledger["records"][0]["review"]["status"], "accepted")

    def test_rejects_missing_tampered_and_stale_decision_artifacts(self) -> None:
        root, ledger_path = self._accepted_fixture()
        ledger = json.loads(ledger_path.read_text())
        receipt_path = root / ledger["decisionVerification"]["receipt"]
        receipt = json.loads(receipt_path.read_text())
        artifact_path = root / receipt["artifacts"][0]["path"]

        artifact_path.unlink()
        with self.assertRaisesRegex(ValueError, "artifact is missing"):
            validate_ledger(root, ledger_path)

        root, ledger_path = self._accepted_fixture()
        ledger = json.loads(ledger_path.read_text())
        receipt_path = root / ledger["decisionVerification"]["receipt"]
        receipt = json.loads(receipt_path.read_text())
        artifact_path = root / receipt["artifacts"][0]["path"]
        artifact_path.write_bytes(artifact_path.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            validate_ledger(root, ledger_path)

        receipt["artifacts"][0]["sha256"] = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
        receipt_path.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(ValueError, "stale from its pinned revision"):
            validate_ledger(root, ledger_path)

    def test_rejects_stale_unverified_and_reused_decision_evidence(self) -> None:
        root, ledger_path = self._accepted_fixture()
        ledger = json.loads(ledger_path.read_text())
        ledger["records"][0]["review"]["reviewer"] = "different-reviewer"
        ledger_path.write_text(json.dumps(ledger))
        with self.assertRaisesRegex(ValueError, "stale for ledger fields.*reviewer"):
            validate_ledger(root, ledger_path)

        root, ledger_path = self._accepted_fixture()
        ledger = json.loads(ledger_path.read_text())
        ledger["records"][0]["review"]["decisionEvidence"][0]["revision"] = "3" * 40
        ledger_path.write_text(json.dumps(ledger))
        with self.assertRaisesRegex(ValueError, "absent from the offline verification receipt"):
            validate_ledger(root, ledger_path)

        root, ledger_path = self._accepted_fixture()
        ledger = json.loads(ledger_path.read_text())
        reused = copy.deepcopy(ledger["records"][0])
        reused["id"] = "example.schema.second-delta"
        reused["target"]["differenceKey"] = "/field#title"
        ledger["records"].append(reused)
        ledger_path.write_text(json.dumps(ledger))
        with self.assertRaisesRegex(ValueError, "reuses a decision artifact"):
            validate_ledger(root, ledger_path)

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
