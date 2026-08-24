from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PROJECTOR = ROOT / "scripts" / "project_response_normalizations.mjs"


class ResponseNormalizationProjectorTests(unittest.TestCase):
    def _fixture(
        self,
        root: Path,
        *,
        schema: dict[str, object] | None = None,
        path: str = "/optionalNarrative",
        evidence_ref: str = "reviewed-omission",
        declared_evidence_ref: str | None = None,
        second_operation: dict[str, object] | None = None,
        review_status: str = "reviewed",
        evidence_path: str | None = None,
        evidence_operation: str = "empty-string-to-absent",
        form_id: str = "arbitrary-form",
        form_version: str = "7.3",
    ) -> tuple[Path, Path, Path]:
        dist = root / "dist"
        form = dist / "forms" / form_id
        form.mkdir(parents=True)
        normalization_root = root / "normalizations"
        normalization_root.mkdir()

        self._json(form / "schema.json", schema or {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"{form_id}/schema.json",
            "type": "object",
            "properties": {
                "optionalNarrative": {"type": "string", "minLength": 1, "maxLength": 50},
            },
        })
        self._json(form / "manifest.json", {
            "contract": "resolved-form-package/v1",
            "form": {"id": form_id, "formVersion": form_version},
            "artifacts": {"schema.json": "generated", "ui.json": "generated"},
        })
        self._json(form / "evidence.json", {
            "contract": "grants-form-evidence/v1",
            "block": {"id": form_id, "kind": "form", "formVersion": form_version},
            "sources": [{
                "id": "official-xsd",
                "type": "xsd",
                "uri": "https://example.gov/example-v7.3.xsd",
                "nativeVersion": "7.3",
                "sha256": "a" * 64,
            }],
            "responseNormalizationEvidence": [{
                "id": evidence_ref,
                "canonicalPath": evidence_path or path,
                "operation": evidence_operation,
                "authority": "official_source",
                "reviewStatus": review_status,
                "sourceEvidence": [{
                    "sourceId": "official-xsd",
                    "sourcePath": "Example.OptionalNarrative",
                    "sourceRecord": "The optional element rejects a present empty string.",
                }],
                "disposition": "The exact empty string represents omission at the compatibility boundary.",
            }],
        })
        operations: list[dict[str, object]] = [{
            "path": path,
            "operation": "empty-string-to-absent",
            "evidenceRef": declared_evidence_ref or evidence_ref,
        }]
        if second_operation is not None:
            operations.append(second_operation)
        declaration = normalization_root / f"{form_id}.json"
        self._json(declaration, {
            "contract": "grants-form-response-normalization/v1",
            "form": {"id": form_id, "formVersion": form_version},
            "operations": operations,
        })
        return dist, normalization_root, form

    @staticmethod
    def _json(path: Path, value: object) -> None:
        path.write_text(json.dumps(value), encoding="utf-8")

    def _run(self, dist: Path, normalizations: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "node",
                str(PROJECTOR),
                "--dist",
                str(dist),
                "--normalizations",
                str(normalizations),
                *extra,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_projects_a_generic_exact_path_and_hashes_the_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist, normalizations, form = self._fixture(Path(directory))
            first = self._run(dist, normalizations)
            emitted = form / "response-normalization.json"
            first_bytes = emitted.read_bytes()
            second = self._run(dist, normalizations)
            second_bytes = emitted.read_bytes()
            manifest = json.loads((form / "manifest.json").read_text())

        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(first_bytes, second_bytes)
        self.assertEqual(
            manifest["artifacts"]["response-normalization.json"],
            {
                "origin": "passthrough",
                "sha256": hashlib.sha256(first_bytes).hexdigest(),
            },
        )

    def test_rejects_unknown_operation_and_malformed_pointer_at_contract_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist, normalizations, _ = self._fixture(Path(directory))
            declaration = next(normalizations.glob("*.json"))
            document = json.loads(declaration.read_text())
            document["operations"][0]["operation"] = "trim-empty-string"
            document["operations"][0]["path"] = "optionalNarrative"
            self._json(declaration, document)
            result = self._run(dist, normalizations)

        self.assertEqual(result.returncode, 1)
        self.assertIn("normalization_invalid", result.stdout)
        self.assertIn("must be equal to constant", result.stdout)
        self.assertIn("must match pattern", result.stdout)

    def test_rejects_duplicate_exact_path_even_with_a_different_evidence_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            second = {
                "path": "/optionalNarrative",
                "operation": "empty-string-to-absent",
                "evidenceRef": "different-reference",
            }
            dist, normalizations, _ = self._fixture(
                Path(directory), second_operation=second,
            )
            result = self._run(dist, normalizations)

        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate normalization path /optionalNarrative", result.stdout)

    def test_rejects_duplicate_form_declarations_before_writing_any_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dist, normalizations, form = self._fixture(Path(directory))
            source = next(normalizations.glob("*.json"))
            self._json(normalizations / "duplicate.json", json.loads(source.read_text()))
            manifest_before = (form / "manifest.json").read_bytes()
            result = self._run(dist, normalizations)

            self.assertFalse((form / "response-normalization.json").exists())
            self.assertEqual((form / "manifest.json").read_bytes(), manifest_before)

        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate response normalization declarations", result.stdout)

    def test_rejects_stale_required_non_string_nullable_and_empty_permitting_targets(self) -> None:
        cases = [
            (
                "/missing",
                {"type": "object", "properties": {"optionalNarrative": {"type": "string", "minLength": 1}}},
                "does not resolve",
            ),
            (
                "/optionalNarrative",
                {"type": "object", "required": ["optionalNarrative"], "properties": {"optionalNarrative": {"type": "string", "minLength": 1}}},
                "targets a required property",
            ),
            (
                "/optionalNarrative",
                {"type": "object", "properties": {"optionalNarrative": {"type": "number"}}},
                "non-null scalar string",
            ),
            (
                "/optionalNarrative",
                {"type": "object", "properties": {"optionalNarrative": {"type": ["string", "null"], "minLength": 1}}},
                "non-null scalar string",
            ),
            (
                "/optionalNarrative",
                {"type": "object", "properties": {"optionalNarrative": {"type": "string", "minLength": 0}}},
                "must reject a present empty string",
            ),
        ]
        for path, schema, message in cases:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as directory:
                dist, normalizations, _ = self._fixture(Path(directory), path=path, schema=schema)
                result = self._run(dist, normalizations)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn(message, result.stdout)

    def test_rejects_array_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            schema = {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"optionalNarrative": {"type": "string", "minLength": 1}},
                        },
                    },
                },
            }
            dist, normalizations, _ = self._fixture(
                Path(directory), schema=schema, path="/items/0/optionalNarrative",
            )
            result = self._run(dist, normalizations)

        self.assertEqual(result.returncode, 1)
        self.assertIn("traverses an array", result.stdout)

    def test_rejects_missing_unreviewed_and_nonmatching_evidence(self) -> None:
        cases = [
            ({"declared_evidence_ref": "missing"}, "unresolved evidenceRef missing"),
            ({"review_status": "proposed"}, "does not exactly review"),
            ({"evidence_path": "/other"}, "does not exactly review"),
            ({"evidence_operation": "different"}, "does not exactly review"),
        ]
        for overrides, message in cases:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as directory:
                dist, normalizations, _ = self._fixture(Path(directory), **overrides)
                result = self._run(dist, normalizations)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn(message, result.stdout)

    def test_unknown_flag_is_usage_error(self) -> None:
        for args in (["--unknown"], ["--help", "--unknown"]):
            with self.subTest(args=args):
                result = subprocess.run(
                    ["node", str(PROJECTOR), *args],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("usage_error", result.stdout)
                self.assertIn("--help", result.stdout)


class Sf424aResponseNormalizationTests(unittest.TestCase):
    def test_emitted_policy_has_only_the_three_reviewed_occurrences(self) -> None:
        form = ROOT / "dist/forms/sf424a"
        policy = json.loads((form / "response-normalization.json").read_text())
        manifest = json.loads((form / "manifest.json").read_text())
        schema = json.loads((form / "schema.json").read_text())
        paths = [operation["path"] for operation in policy["operations"]]

        self.assertEqual(policy["contract"], "grants-form-response-normalization/v1")
        self.assertEqual(
            paths,
            ["/directChargesExplanation", "/indirectChargesExplanation", "/remarks"],
        )
        required = set(schema.get("required", []))
        self.assertTrue(required.isdisjoint({
            "directChargesExplanation", "indirectChargesExplanation", "remarks",
        }))
        artifact = (form / "response-normalization.json").read_bytes()
        self.assertEqual(
            manifest["artifacts"]["response-normalization.json"]["sha256"],
            hashlib.sha256(artifact).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()
