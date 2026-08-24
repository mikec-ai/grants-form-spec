from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.build_proof_package import build_package


ROOT = Path(__file__).resolve().parent.parent


class ProofPackageTests(unittest.TestCase):
    def test_repository_proof_package_builds_deterministically(self) -> None:
        source = ROOT / "proof-package/v1/proof-package.json"
        with (
            tempfile.TemporaryDirectory() as first_dir,
            tempfile.TemporaryDirectory() as second_dir,
        ):
            first = Path(first_dir)
            second = Path(second_dir)
            package = build_package(root=ROOT, source_path=source, output_dir=first)
            build_package(root=ROOT, source_path=source, output_dir=second)

            self.assertEqual(package["contract"], "grants-form-proof-package/v1")
            self.assertEqual(len(package["claims"]), 7)
            self.assertEqual(
                first.joinpath("proof-manifest.json").read_bytes(),
                second.joinpath("proof-manifest.json").read_bytes(),
            )
            self.assertEqual(
                first.joinpath("index.md").read_bytes(),
                second.joinpath("index.md").read_bytes(),
            )
            index = first.joinpath("index.md").read_text()
            self.assertIn("Reviewed pairwise similarity is currently unavailable", index)
            self.assertIn("zero accepted occurrence mappings", index)
            self.assertNotIn("corrected-reviewed-pairwise-question-analysis", index)

            producer_revision = package["source"]["producerRevision"]
            producer_paths = [
                evidence
                for claim in package["claims"]
                for evidence in claim["evidence"]
                if evidence["kind"] == "producer_path"
            ]
            self.assertTrue(producer_paths)
            self.assertTrue(
                all(evidence["revision"] == producer_revision for evidence in producer_paths)
            )

            budget_claim = next(
                claim for claim in package["claims"] if claim["id"] == "rr-budget-family-reuse"
            )
            self.assertIn("64 conditioned occurrences", budget_claim["statement"])
            self.assertIn("50 represented", budget_claim["statement"])
            self.assertIn("10 compiled", budget_claim["statement"])
            self.assertIn("four explicitly source-bound and uncompiled", budget_claim["statement"])
            inventory_evidence = next(
                evidence
                for evidence in budget_claim["evidence"]
                if evidence.get("path") == "analysis/rr-budget-dat-conditions.v1.json"
            )
            inventory = json.loads(
                subprocess.run(
                    [
                        "git",
                        "show",
                        f"{inventory_evidence['revision']}:{inventory_evidence['path']}",
                    ],
                    cwd=ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout
            )
            self.assertEqual(inventory["counts"]["nonEmptyConditionOccurrences"], 64)
            self.assertEqual(
                inventory["counts"]["byDisposition"],
                {
                    "compiled-by-at-least-one-path-when-present": 10,
                    "represented-by-existing-declaration": 50,
                    "source-bound-uncompiled": 4,
                },
            )
            self.assertEqual(inventory["reviewStatus"], "unreviewed")

            cohort_claim = next(
                claim
                for claim in package["claims"]
                if claim["id"] == "uniform-seven-form-static-differential"
            )
            self.assertIn(
                "One form passes because all supported dimensions match exactly",
                cohort_claim["statement"],
            )
            self.assertIn("Six forms are blocked", cohort_claim["statement"])
            self.assertIn(
                "mechanically bounded but remain proposed and unaccepted",
                cohort_claim["statement"],
            )
            self.assertIn("15 report parity", cohort_claim["statement"])
            self.assertIn("12 report proposed deltas", cohort_claim["statement"])
            self.assertIn("zero unexplained failures", cohort_claim["statement"])
            self.assertIn("16 are source-verified", cohort_claim["statement"])
            self.assertIn("zero are accepted", cohort_claim["statement"])
            self.assertIn(
                "Project Narrative Attachments has exact parity",
                cohort_claim["statement"],
            )
            self.assertEqual(
                cohort_claim["evidence"][0]["revision"],
                "29fafef5c1f1032b559b519d73387475932297fd",
            )
            self.assertEqual(
                cohort_claim["evidence"][0]["generatedReceipt"],
                "api/test-results/legacy-differential/summary.json",
            )
            self.assertNotIn("artifactRevision", cohort_claim["evidence"][0])
            self.assertNotIn("artifactId", cohort_claim["evidence"][0])
            limitations = " ".join(cohort_claim["limitations"])
            self.assertIn("Serialized XML", limitations)
            self.assertIn("rule outcomes", limitations)
            self.assertIn("runtime lifecycle", limitations)
            self.assertIn("not release readiness", limitations)

    def test_claim_without_limitations_is_rejected(self) -> None:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        source_document = {
            "contract": "grants-form-proof-package-source/v1",
            "title": "Test",
            "summary": "Test package",
            "repositories": {
                "producer": {
                    "url": "https://github.com/mikec-ai/grants-form-spec",
                    "revision": revision,
                },
                "consumer": {"url": "https://github.com/mikec-ai/simpler-grants-gov"},
            },
            "claims": [
                {
                    "id": "missing-boundary",
                    "title": "Unsupported claim",
                    "statement": "A claim without a limitation must fail.",
                    "status": "observed_reproducible",
                    "evidence": [
                        {
                            "kind": "producer_path",
                            "label": "README",
                            "revision": revision,
                            "path": "README.md",
                        }
                    ],
                    "reproduce": ["Read README.md"],
                    "limitations": [],
                }
            ],
            "pendingInputs": [],
            "releaseBoundaries": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            source = temporary / "source.json"
            source.write_text(json.dumps(source_document))
            with self.assertRaisesRegex(ValueError, "limitations"):
                build_package(root=ROOT, source_path=source, output_dir=temporary / "out")

    def test_worktree_file_does_not_satisfy_pinned_evidence(self) -> None:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        with tempfile.TemporaryDirectory(dir=ROOT) as evidence_dir:
            evidence_path = Path(evidence_dir) / "current-only.json"
            evidence_path.write_text("{}\n")
            relative_evidence = evidence_path.relative_to(ROOT).as_posix()
            source_document = {
                "contract": "grants-form-proof-package-source/v1",
                "title": "Pinned evidence test",
                "summary": "Current files must not satisfy historical evidence.",
                "repositories": {
                    "producer": {
                        "url": "https://github.com/mikec-ai/grants-form-spec",
                        "revision": revision,
                    },
                    "consumer": {"url": "https://github.com/mikec-ai/simpler-grants-gov"},
                },
                "claims": [
                    {
                        "id": "current-only-evidence",
                        "title": "Current-only evidence",
                        "statement": "This evidence is absent from the pinned revision.",
                        "status": "observed_reproducible",
                        "evidence": [
                            {
                                "kind": "producer_path",
                                "label": "Uncommitted evidence",
                                "revision": revision,
                                "path": relative_evidence,
                            }
                        ],
                        "reproduce": ["Attempt to build the proof package"],
                        "limitations": ["The evidence is intentionally uncommitted"],
                    }
                ],
                "pendingInputs": [],
                "releaseBoundaries": ["Test-only package"],
            }
            source = Path(evidence_dir) / "source.json"
            source.write_text(json.dumps(source_document))
            with self.assertRaisesRegex(ValueError, "producer evidence is not available"):
                build_package(root=ROOT, source_path=source, output_dir=Path(evidence_dir) / "out")

    def test_producer_path_revision_must_match_package_revision(self) -> None:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        source_document = {
            "contract": "grants-form-proof-package-source/v1",
            "title": "Pinned producer test",
            "summary": "Producer evidence must use one revision.",
            "repositories": {
                "producer": {
                    "url": "https://github.com/mikec-ai/grants-form-spec",
                    "revision": revision,
                },
                "consumer": {"url": "https://github.com/mikec-ai/simpler-grants-gov"},
            },
            "claims": [
                {
                    "id": "mismatched-producer-revision",
                    "title": "Mismatched revision",
                    "statement": "This producer evidence points elsewhere.",
                    "status": "observed_reproducible",
                    "evidence": [
                        {
                            "kind": "producer_path",
                            "label": "README",
                            "revision": "1" * 40,
                            "path": "README.md",
                        }
                    ],
                    "reproduce": ["Attempt to build"],
                    "limitations": ["Test-only claim"],
                }
            ],
            "pendingInputs": [],
            "releaseBoundaries": ["Test-only package"],
        }
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            source = temporary / "source.json"
            source.write_text(json.dumps(source_document))
            with self.assertRaisesRegex(ValueError, "must match repositories.producer.revision"):
                build_package(root=ROOT, source_path=source, output_dir=temporary / "out")


if __name__ == "__main__":
    unittest.main()
