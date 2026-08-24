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
            self.assertEqual(len(package["claims"]), 6)
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


if __name__ == "__main__":
    unittest.main()
