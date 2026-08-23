from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = ROOT / "scripts" / "validate_artifacts.mjs"
PROJECTOR = ROOT / "scripts" / "project_evidence.mjs"


class ArtifactGraphValidatorTests(unittest.TestCase):
    def _write_graph(self, root: Path, *, ref: str = "../../question-bank/generics/name/schema.json") -> Path:
        dist = root / "dist"
        question = dist / "question-bank" / "generics" / "name"
        form = dist / "forms" / "example"
        question.mkdir(parents=True)
        form.mkdir(parents=True)

        self._json(question / "schema.json", {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "generics/name/schema.json",
            "type": "string",
        })
        self._json(question / "ui.json", {"type": "Control", "scope": "#"})
        self._json(question / "index.json", {
            "id": "generics/name", "kind": "question", "name": "Name",
            "description": "A name.", "tags": ["name"],
            "classification": "semanticQuestion", "composes": [],
        })

        self._json(form / "schema.json", {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "example/schema.json",
            "type": "object",
            "properties": {"name": {"$ref": ref}},
        })
        self._json(form / "ui.json", {
            "type": "Group",
            "elements": [{"type": "Control", "scope": "#/properties/name"}],
        })
        self._json(form / "index.json", {
            "id": "example", "kind": "form", "name": "Example",
            "description": "Example form.", "tags": [],
        })
        self._json(form / "manifest.json", {
            "contract": "resolved-form-package/v1",
            "form": {
                "id": "example", "formId": "f140c7db-724d-4954-bebd-081c0527908c",
                "legacyFormId": 1, "formName": "EXAMPLE", "shortFormName": "Example",
                "formVersion": "1.0", "agencyCode": "SGG", "ombNumber": "",
                "formType": "EXAMPLE", "sggVersion": "1.0",
            },
            "artifacts": {"schema.json": "generated", "ui.json": "generated"},
        })
        return dist

    @staticmethod
    def _json(path: Path, value: object) -> None:
        path.write_text(json.dumps(value), encoding="utf-8")

    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["node", str(VALIDATOR), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def _run_projector(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["node", str(PROJECTOR), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_accepts_a_hand_authored_artifact_graph(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist = self._write_graph(Path(directory))
            result = self._run("--dist", str(dist))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("status: passed", result.stdout)
        self.assertIn("blocks: 2", result.stdout)

    def test_rejects_a_dangling_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist = self._write_graph(Path(directory), ref="../../question-bank/missing/schema.json")
            result = self._run("--dist", str(dist))

        self.assertEqual(result.returncode, 1)
        self.assertIn("artifact_invalid", result.stdout)
        self.assertIn("cannot read JSON", result.stdout)

    def test_rejects_an_unknown_composed_question(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist = self._write_graph(Path(directory))
            index_path = dist / "question-bank" / "generics" / "name" / "index.json"
            index = json.loads(index_path.read_text(encoding="utf-8"))
            index["composes"] = ["generics/missing"]
            self._json(index_path, index)
            result = self._run("--dist", str(dist))

        self.assertEqual(result.returncode, 1)
        self.assertIn("composes unknown question generics/missing", result.stdout)

    def test_rejects_an_xml_mapping_field_outside_the_canonical_form(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            form = dist / "forms/example"
            target = form / "targets/grants-gov-xml.json"
            target.parent.mkdir()
            self._json(target, {
                "contract": "grants-gov-xml-profile/v1",
                "formId": "example",
                "xsd": {
                    "uri": "https://example.gov/forms/Example-V1.0.xsd",
                    "sha256": "a" * 64,
                },
                "namespaces": {"default": "https://example.gov/forms/Example-V1.0"},
                "root": {
                    "element": "Example", "namespacePrefix": "Example",
                    "attributes": {"FormVersion": "1.0"},
                },
                "mapping": {
                    "fields": {"notAFormField": {"element": "Name", "kind": "value"}}
                },
            })
            manifest_path = form / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["artifacts"]["targets/grants-gov-xml.json"] = "generated"
            self._json(manifest_path, manifest)
            result = self._run("--dist", str(dist))

        self.assertEqual(result.returncode, 1)
        self.assertIn("XML mapping coverage mismatch", result.stdout)
        self.assertIn("notAFormField", result.stdout)

    def test_rejects_an_xml_group_with_a_dangling_source_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            form = dist / "forms/example"
            target = form / "targets/grants-gov-xml.json"
            target.parent.mkdir()
            self._json(target, {
                "contract": "grants-gov-xml-profile/v1",
                "formId": "example",
                "xsd": {
                    "uri": "https://example.gov/forms/Example-V1.0.xsd",
                    "sha256": "a" * 64,
                },
                "namespaces": {"default": "https://example.gov/forms/Example-V1.0"},
                "root": {
                    "element": "Example", "namespacePrefix": "Example",
                    "attributes": {"FormVersion": "1.0"},
                },
                "mapping": {"fields": {
                    "wireWrapper": {
                        "element": "WireWrapper", "kind": "group",
                        "fields": {
                            "name": {
                                "element": "Name", "kind": "value", "source": "/missing",
                            },
                        },
                    },
                }},
            })
            manifest_path = form / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["artifacts"]["targets/grants-gov-xml.json"] = "generated"
            self._json(manifest_path, manifest)
            result = self._run("--dist", str(dist))

        self.assertEqual(result.returncode, 1)
        self.assertIn("XML mapping source does not resolve: /missing", result.stdout)

    def test_unknown_flag_is_an_actionable_usage_error(self) -> None:
        result = self._run("--dits", "somewhere")

        self.assertEqual(result.returncode, 2)
        self.assertIn("usage_error", result.stdout)
        self.assertIn("unknown argument --dits", result.stdout)
        self.assertIn("--help", result.stdout)

    def test_projects_validated_evidence_and_declares_it_in_the_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            evidence = root / "evidence" / "forms" / "example" / "evidence.json"
            evidence.parent.mkdir(parents=True)
            self._json(evidence, {
                "contract": "grants-form-evidence/v1",
                "block": {"id": "example", "kind": "form"},
                "sources": [{
                    "id": "example-xsd", "type": "xsd",
                    "uri": "https://example.gov/example.xsd", "version": "1.0",
                    "sha256": "a" * 64,
                }],
                "extraction": {
                    "repository": "https://github.com/example/forms",
                    "revision": "1" * 40,
                    "artifact": "artifacts/example.jsonl.manifest.json",
                    "sourceSetSha256": "b" * 64,
                    "extractedAt": "2026-08-18T14:19:31Z",
                },
                "semanticReview": {"status": "unreviewed", "mappings": []},
            })
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )
            manifest = json.loads((dist / "forms/example/manifest.json").read_text())

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("sidecars: 1", result.stdout)
        self.assertEqual(manifest["artifacts"]["evidence.json"], "passthrough")

    def test_projector_rejects_unknown_flags(self) -> None:
        result = self._run_projector("--source", "somewhere")

        self.assertEqual(result.returncode, 2)
        self.assertIn("usage_error", result.stdout)
        self.assertIn("unknown argument --source", result.stdout)


if __name__ == "__main__":
    unittest.main()
