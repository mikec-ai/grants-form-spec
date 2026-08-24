from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_xml_profile_fixtures import CONTRACT, verify_profiles


class XmlProfileFixtureGateTests(unittest.TestCase):
    def _fixture(self, directory: Path, *, payload: bytes = b"official\n") -> tuple[Path, Path, Path]:
        dist = directory / "dist" / "forms"
        fixtures = directory / "fixtures"
        profile_dir = dist / "example"
        profile = profile_dir / "targets" / "grants-gov-xml.json"
        evidence = profile_dir / "evidence.json"
        xsd = fixtures / "example-1.0" / "Example-V1.0.xsd"
        manifest = fixtures / "root-fixture-manifest.json"
        uri = "https://apply07.grants.gov/apply/forms/schemas/Example-V1.0.xsd"
        digest = hashlib.sha256(b"official\n").hexdigest()
        profile.parent.mkdir(parents=True)
        xsd.parent.mkdir(parents=True)
        xsd.write_bytes(payload)
        profile.write_text(json.dumps({"formId": "example", "xsd": {"uri": uri, "sha256": digest}}))
        evidence.write_text(json.dumps({"sources": [{"type": "xsd", "uri": uri, "nativeVersion": "1.0", "sha256": digest}]}))
        manifest.write_text(json.dumps({"contract": CONTRACT, "fixtures": [{"formId": "example", "uri": uri, "nativeVersion": "1.0", "role": "root", "sha256": digest, "path": "example-1.0/Example-V1.0.xsd"}]}))
        return dist, fixtures, manifest

    def _manifest(self, manifest: Path) -> dict:
        return json.loads(manifest.read_text())

    def test_accepts_one_exact_manifested_root_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist, fixtures, manifest = self._fixture(Path(directory))
            self.assertEqual(verify_profiles(dist, fixtures, manifest), (1, 1))

    def test_rejects_normalized_bytes_with_the_same_filename(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist, fixtures, manifest = self._fixture(Path(directory), payload=b"normalized\n")
            with self.assertRaisesRegex(ValueError, "bytes do not match"):
                verify_profiles(dist, fixtures, manifest)

    def test_rejects_stale_sibling_with_the_same_basename(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist, fixtures, manifest = self._fixture(Path(directory))
            duplicate = fixtures / "normalized" / "Example-V1.0.xsd"
            duplicate.parent.mkdir()
            duplicate.write_bytes(b"normalized\n")
            with self.assertRaisesRegex(ValueError, "exactly one candidate"):
                verify_profiles(dist, fixtures, manifest)

    def test_rejects_relative_or_wrong_host_root_uri(self) -> None:
        for bad_uri in ("Example-V1.0.xsd", "https://example.gov/apply/forms/schemas/Example-V1.0.xsd"):
            with self.subTest(uri=bad_uri), tempfile.TemporaryDirectory() as directory:
                dist, fixtures, manifest = self._fixture(Path(directory))
                document = self._manifest(manifest)
                document["fixtures"][0]["uri"] = bad_uri
                manifest.write_text(json.dumps(document))
                with self.assertRaisesRegex(ValueError, "official forms/schema URI"):
                    verify_profiles(dist, fixtures, manifest)

    def test_rejects_system_dependency_uri_or_non_root_role(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist, fixtures, manifest = self._fixture(Path(directory))
            document = self._manifest(manifest)
            document["fixtures"][0]["uri"] = "https://apply07.grants.gov/apply/system/schemas/Example-V1.0.xsd"
            manifest.write_text(json.dumps(document))
            with self.assertRaisesRegex(ValueError, "official forms/schema URI"):
                verify_profiles(dist, fixtures, manifest)
        with tempfile.TemporaryDirectory() as directory:
            dist, fixtures, manifest = self._fixture(Path(directory))
            document = self._manifest(manifest)
            document["fixtures"][0]["role"] = "dependency"
            manifest.write_text(json.dumps(document))
            with self.assertRaisesRegex(ValueError, "role must be root"):
                verify_profiles(dist, fixtures, manifest)

    def test_rejects_wrong_version_or_fixture_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist, fixtures, manifest = self._fixture(Path(directory))
            document = self._manifest(manifest)
            document["fixtures"][0]["nativeVersion"] = "2.0"
            manifest.write_text(json.dumps(document))
            with self.assertRaisesRegex(ValueError, "official URI version"):
                verify_profiles(dist, fixtures, manifest)
        with tempfile.TemporaryDirectory() as directory:
            dist, fixtures, manifest = self._fixture(Path(directory))
            document = self._manifest(manifest)
            document["fixtures"][0]["path"] = "example-1.0/Wrong-V1.0.xsd"
            manifest.write_text(json.dumps(document))
            with self.assertRaisesRegex(ValueError, "path does not match"):
                verify_profiles(dist, fixtures, manifest)

    def test_rejects_manifest_and_evidence_colluding_on_wrong_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist, fixtures, manifest = self._fixture(Path(directory))
            document = self._manifest(manifest)
            document["fixtures"][0]["nativeVersion"] = "2.0"
            manifest.write_text(json.dumps(document))
            evidence = dist / "example" / "evidence.json"
            evidence_document = json.loads(evidence.read_text())
            evidence_document["sources"][0]["nativeVersion"] = "2.0"
            evidence.write_text(json.dumps(evidence_document))
            with self.assertRaisesRegex(ValueError, "official URI version"):
                verify_profiles(dist, fixtures, manifest)

    def test_rejects_duplicate_claims_and_stale_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist, fixtures, manifest = self._fixture(Path(directory))
            document = self._manifest(manifest)
            document["fixtures"].append(dict(document["fixtures"][0], formId="other"))
            manifest.write_text(json.dumps(document))
            with self.assertRaisesRegex(ValueError, "claimed by both"):
                verify_profiles(dist, fixtures, manifest)
        with tempfile.TemporaryDirectory() as directory:
            dist, fixtures, manifest = self._fixture(Path(directory))
            document = self._manifest(manifest)
            stale = dict(document["fixtures"][0])
            stale.update({"formId": "stale", "uri": "https://apply07.grants.gov/apply/forms/schemas/Stale-V1.0.xsd", "path": "stale-1.0/Stale-V1.0.xsd"})
            stale_path = fixtures / stale["path"]
            stale_path.parent.mkdir()
            stale_path.write_bytes(b"official\n")
            document["fixtures"].append(stale)
            manifest.write_text(json.dumps(document))
            with self.assertRaisesRegex(ValueError, "stale rows"):
                verify_profiles(dist, fixtures, manifest)
