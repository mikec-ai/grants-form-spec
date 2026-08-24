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
            "fieldOccurrences": [{
                "path": "/name", "leaf": True, "blockIds": ["generics/name"],
            }],
        })
        self._json(form / "manifest.json", {
            "contract": "resolved-form-package/v1",
            "form": {
                "id": "example",
                "legacyFormId": 1, "formName": "EXAMPLE", "shortFormName": "Example",
                "formVersion": "1.0", "agencyCode": "SGG", "ombNumber": "",
            },
            "artifacts": {
                "schema.json": "generated",
                "ui.json": "generated",
                "sgg/rule-schema.json": "generated",
                "sgg/ui-schema.json": "generated",
            },
        })
        (form / "sgg").mkdir()
        self._json(form / "sgg/rule-schema.json", {})
        self._json(form / "sgg/ui-schema.json", [])
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

    def _write_evidence(
        self,
        root: Path,
        *,
        behavior_evidence: list[dict[str, object]],
        operational_behavior_evidence: list[dict[str, object]] | None = None,
        source_type: str = "dat",
    ) -> Path:
        evidence = root / "evidence/forms/example/evidence.json"
        evidence.parent.mkdir(parents=True)
        self._json(evidence, {
            "contract": "grants-form-evidence/v1",
            "block": {"id": "example", "kind": "form", "formVersion": "1.0"},
            "sources": [{
                "id": "example-source", "type": source_type,
                "uri": "https://example.gov/example-source.json", "nativeVersion": None,
                "sha256": "a" * 64,
            }],
            "behaviorEvidence": behavior_evidence,
            "operationalBehaviorEvidence": operational_behavior_evidence or [],
            "extraction": {
                "repository": "https://github.com/example/forms",
                "revision": "1" * 40,
                "artifact": "artifacts/example.jsonl.manifest.json",
                "sourceSetSha256": "b" * 64,
                "extractedAt": "2026-08-18T14:19:31Z",
            },
            "semanticReview": {"status": "unreviewed", "mappings": []},
        })
        return evidence

    @staticmethod
    def _official_prefill(path: str = "/name") -> dict[str, object]:
        return {
            "canonicalPath": path,
            "operationKind": "prefill",
            "valueSource": {
                "kind": "canonical",
                "blockId": "example",
                "path": "/name",
            },
            "editability": "protected",
            "authority": "official_source",
            "executionStatus": "source-bound-uncompiled",
            "sourceId": "example-source",
            "sourcePath": "F-1",
            "sourceRecord": "Copy the source value and protect the destination.",
        }

    @staticmethod
    def _official_calculation(path: str) -> dict[str, object]:
        return {
            "canonicalPath": path,
            "ruleKind": "calculation",
            "authority": "official_source",
            "sourceId": "example-source",
            "sourcePath": f"Example.{path}",
            "sourceRecord": "F-1",
        }

    def _add_calculation(self, dist: Path, target: str = "name") -> None:
        self._json(dist / "forms/example/sgg/rule-schema.json", {
            target: {
                "gg_pre_population": {
                    "rule": "sum_monetary",
                    "fields": ["source"],
                },
            },
        })

    def test_accepts_a_hand_authored_artifact_graph(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist = self._write_graph(Path(directory))
            result = self._run("--dist", str(dist))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("status: passed", result.stdout)
        self.assertIn("blocks: 2", result.stdout)

    def test_resolves_nested_paths_through_an_empty_local_all_of_extension(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist = self._write_graph(Path(directory))
            question = dist / "question-bank/generics/name/schema.json"
            form = dist / "forms/example"
            self._json(question, {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "generics/name/schema.json",
                "type": "object",
                "properties": {"value": {"type": "string"}},
            })
            self._json(form / "schema.json", {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "example/schema.json",
                "type": "object",
                "properties": {"details": {"$ref": "#/$defs/LocalDetails"}},
                "$defs": {
                    "LocalDetails": {
                        "type": "object",
                        "properties": {},
                        "allOf": [{
                            "$ref": "../../question-bank/generics/name/schema.json",
                        }],
                    },
                },
            })
            self._json(form / "ui.json", {
                "type": "Group",
                "elements": [{
                    "type": "Control",
                    "scope": "#/properties/details/properties/value",
                }],
            })
            self._json(form / "index.json", {
                "id": "example", "kind": "form", "name": "Example",
                "description": "Example form.", "tags": [],
                "fieldOccurrences": [{
                    "path": "/details", "leaf": False,
                    "blockIds": ["generics/name"],
                }, {
                    "path": "/details/value", "leaf": True,
                    "blockIds": ["generics/name"],
                }],
            })
            result = self._run("--dist", str(dist))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("status: passed", result.stdout)

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

    def test_rejects_an_incomplete_field_occurrence_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist = self._write_graph(Path(directory))
            index_path = dist / "forms" / "example" / "index.json"
            index = json.loads(index_path.read_text(encoding="utf-8"))
            index["fieldOccurrences"] = []
            self._json(index_path, index)
            result = self._run("--dist", str(dist))

        self.assertEqual(result.returncode, 1)
        self.assertIn("field occurrence coverage mismatch", result.stdout)
        self.assertIn("missing /name", result.stdout)

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

    def test_accepts_a_top_level_wire_constant_outside_the_canonical_form(self) -> None:
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
                    "wireVersion": {
                        "element": "FormVersionIdentifier", "kind": "value", "constant": "1.0",
                    },
                    "name": {"element": "Name", "kind": "value"},
                }},
            })
            manifest_path = form / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["artifacts"]["targets/grants-gov-xml.json"] = "generated"
            self._json(manifest_path, manifest)
            result = self._run("--dist", str(dist))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("status: passed", result.stdout)

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

    def test_non_emitting_xml_paths_must_be_unmapped_exact_scalar_leaves(self) -> None:
        for response_path, expected in (
            ("/name", "overlaps a mapped or declared path"),
            ("/technical", "status: passed"),
            ("/unmappedContainer", "must resolve to an exact canonical scalar leaf"),
        ):
            with self.subTest(response_path=response_path), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                dist = self._write_graph(root)
                form = dist / "forms/example"
                schema_path = form / "schema.json"
                schema = json.loads(schema_path.read_text())
                schema["properties"].update({
                    "technical": {"type": "string"},
                    "container": {
                        "type": "object",
                        "properties": {"value": {"type": "string"}},
                    },
                    "unmappedContainer": {
                        "type": "object",
                        "properties": {"value": {"type": "string"}},
                    },
                })
                self._json(schema_path, schema)
                index_path = form / "index.json"
                index = json.loads(index_path.read_text())
                index["fieldOccurrences"].extend([
                    {"path": "/technical", "leaf": True, "blockIds": ["generics/name"]},
                    {"path": "/container", "leaf": False, "blockIds": ["generics/name"]},
                    {"path": "/container/value", "leaf": True, "blockIds": ["generics/name"]},
                    {"path": "/unmappedContainer", "leaf": False, "blockIds": ["generics/name"]},
                    {"path": "/unmappedContainer/value", "leaf": True, "blockIds": ["generics/name"]},
                ])
                self._json(index_path, index)
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
                        "element": "Example", "namespacePrefix": "default",
                        "attributes": {"FormVersion": "1.0"},
                    },
                    "mapping": {
                        "nonEmittingResponsePaths": [response_path] + (
                            [] if response_path == "/unmappedContainer"
                            else ["/unmappedContainer/value"]
                        ),
                        "fields": {
                            "name": {"element": "Name", "kind": "value"},
                            "wireGroup": {
                                "element": "WireGroup", "kind": "group",
                                "fields": {
                                    "wireContainer": {
                                        "element": "Container", "kind": "object", "source": "/container",
                                        "fields": {"value": {"element": "Value", "kind": "value"}},
                                    },
                                },
                            },
                        },
                    },
                })
                manifest_path = form / "manifest.json"
                manifest = json.loads(manifest_path.read_text())
                manifest["artifacts"]["targets/grants-gov-xml.json"] = "generated"
                self._json(manifest_path, manifest)
                result = self._run("--dist", str(dist))

            if response_path == "/technical":
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            else:
                self.assertEqual(result.returncode, 1)
            self.assertIn(expected, result.stdout)

    def test_rejects_an_xml_leaf_container_with_an_unknown_namespace(self) -> None:
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
                    "name": {
                        "element": "Name", "kind": "value",
                        "container": {"element": "Names", "namespace": "missing"},
                    },
                }},
            })
            manifest_path = form / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["artifacts"]["targets/grants-gov-xml.json"] = "generated"
            self._json(manifest_path, manifest)
            result = self._run("--dist", str(dist))

        self.assertEqual(result.returncode, 1)
        self.assertIn("mapping container names unknown namespace missing", result.stdout)

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
                "block": {"id": "example", "kind": "form", "formVersion": "1.0"},
                "sources": [{
                    "id": "example-xsd", "type": "xsd",
                    "uri": "https://example.gov/example-V1.0.xsd", "nativeVersion": "1.0",
                    "sha256": "a" * 64,
                }, {
                    "id": "example-dat", "type": "dat",
                    "uri": "https://example.gov/example-V1.0_F1.xls", "nativeVersion": None,
                    "sha256": "c" * 64,
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

    def test_projector_requires_an_exact_disposition_for_each_calculation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._add_calculation(dist)
            self._write_evidence(root, behavior_evidence=[])
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("calculation target name has no behavior evidence disposition", result.stdout)

    def test_projector_preserves_uncompiled_source_evidence_without_emitting_a_rule(self) -> None:
        record = {
            "canonicalPath": "/name",
            "ruleKind": "condition",
            "authority": "official_source",
            "executionStatus": "source-bound-uncompiled",
            "sourceId": "example-source",
            "sourcePath": "F-1",
            "sourceRecord": "Required when a cross-form value is Yes.",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._write_evidence(root, behavior_evidence=[record])
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )
            projected = json.loads((dist / "forms/example/evidence.json").read_text())
            rules = json.loads((dist / "forms/example/sgg/rule-schema.json").read_text())

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(projected["behaviorEvidence"], [record])
        self.assertEqual(rules, {})

    def test_projector_preserves_operational_evidence_without_emitting_a_rule(self) -> None:
        record = self._official_prefill()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._write_evidence(
                root,
                behavior_evidence=[],
                operational_behavior_evidence=[record],
            )
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )
            projected = json.loads((dist / "forms/example/evidence.json").read_text())
            rules = json.loads((dist / "forms/example/sgg/rule-schema.json").read_text())

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(projected["operationalBehaviorEvidence"], [record])
        self.assertEqual(rules, {})

    def test_projector_rejects_operational_destination_outside_emitted_occurrences(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._write_evidence(
                root,
                behavior_evidence=[],
                operational_behavior_evidence=[self._official_prefill("/missing")],
            )
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("operational behavior destination /missing", result.stdout)
        self.assertIn("not an exact emitted field occurrence", result.stdout)

    def test_projector_rejects_missing_operational_evidence_source(self) -> None:
        record = self._official_prefill()
        record["sourceId"] = "missing-source"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._write_evidence(
                root,
                behavior_evidence=[],
                operational_behavior_evidence=[record],
            )
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("names missing source missing-source", result.stdout)

    def test_projector_rejects_operational_authority_source_type_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._write_evidence(
                root,
                behavior_evidence=[],
                operational_behavior_evidence=[self._official_prefill()],
                source_type="implementation",
            )
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("claims official_source authority from implementation source", result.stdout)

    def test_projector_rejects_dangling_canonical_operational_source(self) -> None:
        record = self._official_prefill()
        record["valueSource"] = {
            "kind": "canonical",
            "blockId": "example",
            "path": "/missing",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._write_evidence(
                root,
                behavior_evidence=[],
                operational_behavior_evidence=[record],
            )
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("example:/missing is not an exact emitted field occurrence", result.stdout)

    def test_projector_rejects_unverified_adapter_projected_status(self) -> None:
        record = self._official_prefill()
        record["executionStatus"] = "adapter-projected"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._write_evidence(
                root,
                behavior_evidence=[],
                operational_behavior_evidence=[record],
            )
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("must be equal to constant", result.stdout)
        self.assertIn("operationalBehaviorEvidence", result.stdout)

    def test_projector_rejects_uncompiled_evidence_for_a_nonexistent_occurrence(self) -> None:
        record = {
            "canonicalPath": "/missing",
            "ruleKind": "condition",
            "authority": "official_source",
            "executionStatus": "source-bound-uncompiled",
            "sourceId": "example-source",
            "sourcePath": "F-1",
            "sourceRecord": "Required when a cross-form value is Yes.",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._write_evidence(root, behavior_evidence=[record])
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("is not an exact emitted field occurrence", result.stdout)

    def test_projector_rejects_count_substitution_with_an_input_only_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._add_calculation(dist, "total")
            index_path = dist / "forms/example/index.json"
            index = json.loads(index_path.read_text())
            index["fieldOccurrences"].append({
                "path": "/total", "leaf": True, "blockIds": ["generics/name"],
            })
            self._json(index_path, index)
            self._write_evidence(
                root, behavior_evidence=[self._official_calculation("name")],
            )
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("calculation evidence name is not an exact emitted rule target", result.stdout)

    def test_projector_rejects_duplicate_target_dispositions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._add_calculation(dist)
            record = self._official_calculation("name")
            self._write_evidence(root, behavior_evidence=[record, record])
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate calculation evidence disposition for target name", result.stdout)

    def test_projector_rejects_duplicate_emitted_target_identities(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            conditional = {
                "type": "field",
                "definition": "/properties/name",
                "conditional": {
                    "when": {"op": "equals", "ref": {"scope": "root", "pointer": "/kind"}},
                    "then": {"visible": True},
                    "otherwise": {"visible": False},
                },
            }
            self._json(
                dist / "forms/example/sgg/ui-schema.json",
                [conditional, conditional],
            )
            self._write_evidence(root, behavior_evidence=[{
                "canonicalPath": "name",
                "ruleKind": "condition",
                "authority": "unresolved",
                "owner": "form-semantic-review",
                "reason": "The exact source-bound condition has not been reconciled.",
                "removalCondition": "Replace after exact official-source review.",
            }])
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate emitted condition target name", result.stdout)
        self.assertIn("stable occurrence identity is required", result.stdout)

    def test_projector_rejects_ambiguous_array_path_normalization(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._json(dist / "forms/example/sgg/rule-schema.json", {
                "items": {"amount": {"gg_pre_population": {
                    "rule": "sum_monetary", "fields": ["source"],
                }}},
            })
            index_path = dist / "forms/example/index.json"
            index = json.loads(index_path.read_text())
            index["fieldOccurrences"].extend([{
                "path": "/items/amount", "leaf": True,
                "blockIds": ["generics/name"],
            }, {
                "path": "/items/[]/amount", "leaf": True,
                "blockIds": ["generics/name"],
            }])
            self._json(index_path, index)
            self._write_evidence(root, behavior_evidence=[])
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("calculation target items.amount has 2 exact occurrence candidates", result.stdout)

    def test_projector_rejects_unknown_prepopulation_metadata_instead_of_inferring_calculation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._json(dist / "forms/example/sgg/rule-schema.json", {
                "name": {"gg_pre_population": {
                    "rule": "agency_name",
                    "cache": "application",
                }},
            })
            self._write_evidence(root, behavior_evidence=[])
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("unsupported gg_pre_population operand shape", result.stdout)

    def test_projector_rejects_ambiguous_calculation_operand_shapes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._json(dist / "forms/example/sgg/rule-schema.json", {
                "name": {"gg_pre_population": {
                    "rule": "multiply_by_percentage",
                    "fields": ["amount", "percentage"],
                    "amount": "amount",
                    "percentage": "percentage",
                }},
            })
            self._write_evidence(root, behavior_evidence=[])
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("unsupported gg_pre_population operand shape", result.stdout)

    def test_projector_rejects_implementation_source_as_official_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._add_calculation(dist)
            self._write_evidence(
                root,
                behavior_evidence=[self._official_calculation("name")],
                source_type="implementation",
            )
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("claims official_source authority from implementation source", result.stdout)

    def test_projector_accepts_an_explicit_unresolved_condition(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            self._json(dist / "forms/example/sgg/ui-schema.json", [{
                "type": "field",
                "definition": "/properties/name",
                "conditional": {
                    "when": {"op": "equals", "ref": {"scope": "root", "pointer": "/kind"}},
                    "then": {"visible": True},
                    "otherwise": {"visible": False},
                },
            }])
            self._write_evidence(root, behavior_evidence=[{
                "canonicalPath": "name",
                "ruleKind": "condition",
                "authority": "unresolved",
                "owner": "form-semantic-review",
                "reason": "The exact source-bound condition has not been reconciled.",
                "removalCondition": "Replace after exact official-source review.",
            }])
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_projector_rejects_behavior_path_outside_emitted_form_and_rules(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            rules = dist / "forms" / "example" / "sgg" / "rule-schema.json"
            self._json(rules, {})
            evidence = root / "evidence" / "forms" / "example" / "evidence.json"
            evidence.parent.mkdir(parents=True)
            self._json(evidence, {
                "contract": "grants-form-evidence/v1",
                "block": {"id": "example", "kind": "form", "formVersion": "1.0"},
                "sources": [{
                    "id": "example-dat", "type": "dat",
                    "uri": "https://example.gov/example_F1.xls", "nativeVersion": None,
                    "sha256": "a" * 64,
                }],
                "behaviorEvidence": [{
                    "canonicalPath": "unmounted.name",
                    "ruleKind": "calculation",
                    "authority": "official_source",
                    "sourceId": "example-dat",
                    "sourcePath": "Example.Name",
                    "sourceRecord": "A-1",
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

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "calculation evidence unmounted.name is not an exact emitted rule target",
            result.stdout,
        )

    def test_projector_rejects_native_version_inherited_from_form_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            evidence = root / "evidence" / "forms" / "example" / "evidence.json"
            evidence.parent.mkdir(parents=True)
            self._json(evidence, {
                "contract": "grants-form-evidence/v1",
                "block": {"id": "example", "kind": "form", "formVersion": "4.0"},
                "sources": [{
                    "id": "global-library", "type": "xsd",
                    "uri": "https://example.gov/GlobalLibrary-V2.0.xsd",
                    "nativeVersion": "4.0", "sha256": "a" * 64,
                }],
                "extraction": {
                    "repository": "https://github.com/example/forms", "revision": "1" * 40,
                    "artifact": "artifacts/example.jsonl.manifest.json",
                    "sourceSetSha256": "b" * 64, "extractedAt": "2026-08-18T14:19:31Z",
                },
                "semanticReview": {"status": "unreviewed", "mappings": []},
            })
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("nativeVersion", result.stdout)
        self.assertIn("version 2.0 stated by", result.stdout)

    def test_projector_rejects_unsupported_version_looking_xsd_uris(self) -> None:
        for filename in ["Schema-V2.xsd", "Schema-V2_0.xsd", "SchemaV2.0.xsd"]:
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                dist = self._write_graph(root)
                evidence = root / "evidence" / "forms" / "example" / "evidence.json"
                evidence.parent.mkdir(parents=True)
                self._json(evidence, {
                    "contract": "grants-form-evidence/v1",
                    "block": {"id": "example", "kind": "form", "formVersion": "1.0"},
                    "sources": [{
                        "id": "unsupported-xsd", "type": "xsd",
                        "uri": f"https://example.gov/{filename}", "nativeVersion": None,
                        "sha256": "a" * 64,
                    }],
                    "extraction": {
                        "repository": "https://github.com/example/forms", "revision": "1" * 40,
                        "artifact": "artifacts/example.jsonl.manifest.json",
                        "sourceSetSha256": "b" * 64,
                        "extractedAt": "2026-08-18T14:19:31Z",
                    },
                    "semanticReview": {"status": "unreviewed", "mappings": []},
                })
                result = self._run_projector(
                    "--evidence", str(root / "evidence"), "--dist", str(dist),
                )

            self.assertEqual(result.returncode, 1)
            self.assertIn("unsupported version-looking XSD URI", result.stdout)
            self.assertIn("-V<major>.<minor>.xsd", result.stdout)

    def test_projector_rejects_evidence_for_another_form_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = self._write_graph(root)
            evidence = root / "evidence" / "forms" / "example" / "evidence.json"
            evidence.parent.mkdir(parents=True)
            self._json(evidence, {
                "contract": "grants-form-evidence/v1",
                "block": {"id": "example", "kind": "form", "formVersion": "2.0"},
                "sources": [{
                    "id": "unversioned", "type": "implementation",
                    "uri": "https://example.gov/source.json", "nativeVersion": None,
                    "sha256": "a" * 64,
                }],
                "extraction": {
                    "repository": "https://github.com/example/forms", "revision": "1" * 40,
                    "artifact": "artifacts/example.jsonl.manifest.json",
                    "sourceSetSha256": "b" * 64, "extractedAt": "2026-08-18T14:19:31Z",
                },
                "semanticReview": {"status": "unreviewed", "mappings": []},
            })
            result = self._run_projector(
                "--evidence", str(root / "evidence"), "--dist", str(dist),
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("evidence formVersion 2.0", result.stdout)
        self.assertIn("formVersion 1.0", result.stdout)

    def test_projector_rejects_unknown_flags(self) -> None:
        result = self._run_projector("--source", "somewhere")

        self.assertEqual(result.returncode, 2)
        self.assertIn("usage_error", result.stdout)
        self.assertIn("unknown argument --source", result.stdout)


if __name__ == "__main__":
    unittest.main()
