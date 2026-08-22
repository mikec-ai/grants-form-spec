from __future__ import annotations

import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from scripts.package_artifacts import build_bundle, verify_bundle


class ArtifactBundleTests(unittest.TestCase):
    def test_bundle_is_reproducible_and_self_verifying(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "dist/forms/key-contacts").mkdir(parents=True)
            (root / "dist/forms/key-contacts/schema.json").write_text('{"type":"object"}\n')
            (root / "dist/question-bank/name").mkdir(parents=True)
            (root / "dist/question-bank/name/schema.json").write_text('{"type":"string"}\n')

            first = root / "build/first.tar.gz"
            second = root / "build/second.tar.gz"
            build_bundle(root=root, output=first, revision="abc123")
            build_bundle(root=root, output=second, revision="abc123")

            self.assertEqual(first.read_bytes(), second.read_bytes())
            manifest = verify_bundle(first)
            self.assertEqual(manifest["source"]["revision"], "abc123")
            self.assertEqual(len(manifest["files"]), 2)
            self.assertTrue(first.with_suffix(".gz.sha256").is_file())

    def test_verifier_rejects_changed_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = root / "changed.tar.gz"
            manifest = {
                "contract": "grants-form-artifacts/v1",
                "source": {"repository": "example", "revision": "abc123"},
                "files": [{"path": "dist/schema.json", "sha256": "wrong", "size": 2}],
            }
            with tarfile.open(bundle, mode="w:gz") as archive:
                for name, data in (
                    ("artifact-manifest.json", json.dumps(manifest).encode()),
                    ("dist/schema.json", b"{}"),
                ):
                    info = tarfile.TarInfo(name)
                    info.size = len(data)
                    archive.addfile(info, io.BytesIO(data))

            with self.assertRaisesRegex(ValueError, "digest mismatch"):
                verify_bundle(bundle)


if __name__ == "__main__":
    unittest.main()
