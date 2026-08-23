from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.promote_crosswalk import export_packet, import_packet


class PromotionImporterTests(unittest.TestCase):
    @staticmethod
    def _write(path: Path, value: object, *, jsonl: bool = False) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        if jsonl:
            path.write_text("".join(json.dumps(item) + "\n" for item in value), encoding="utf-8")
        else:
            path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def _repo(self, root: Path) -> tuple[Path, str]:
        repo = root / "crosswalk"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)

        xsd_provenance = f"sha256:{'a' * 64} https://example.gov/forms/Example_1_0-V1.0.xsd"
        dat_provenance = f"sha256:{'b' * 64} https://example.gov/forms/Example_1_0-V1.0_F1.xls"
        records = [
            {
                "form_id": "Example", "form_version": "1.0", "path": "Example_1_0",
                "question_key": "question:root", "record_kind": "container", "data_type": "FieldSet",
                "prompt": "Example", "required": True, "min_occurs": 1, "max_occurs": 1,
                "constraints": {}, "provenance": [xsd_provenance],
            },
            {
                "form_id": "Example", "form_version": "1.0", "path": "Example_1_0.Name",
                "question_key": "question:name", "record_kind": "question", "data_type": "string",
                "prompt": "Name", "required": True, "min_occurs": 1, "max_occurs": 1,
                "constraints": {"minLength": 1, "maxLength": 60}, "provenance": [xsd_provenance],
            },
        ]
        manifest_path = repo / "artifacts/proof/grantsgov-Example.jsonl.manifest.json"
        self._write(manifest_path, {
            "record_count": 2, "extracted_at": "2026-08-18T12:00:00+00:00",
        })
        self._write(repo / "artifacts/proof/grantsgov-Example.jsonl", records, jsonl=True)

        behavior = {
            "behavior_key": "behavior:one", "input_role": "applicant_entered", "fid": "1",
            "provenance": [dat_provenance], "condition": "Required", "field_id": "Name",
        }
        self._write(
            repo / "harness/contracts/expansion-a/evidence/Example-behaviors.jsonl",
            [behavior], jsonl=True,
        )
        family = {
            "title": "Example form",
            "component_assignments": [{
                "source_question_key": "question:name", "source_path": "Example_1_0.Name",
                "module_ids": ["generic-name"], "role": None,
            }],
        }
        family_path = repo / "artifacts/authoring/example-family/forms/Example.json"
        self._write(family_path, family)
        family_sha = hashlib.sha256(family_path.read_bytes()).hexdigest()
        self._write(repo / "artifacts/authoring/form-authoring-contract-v2/forms/Example.json", {
            "output_adapter_oracle": {
                "input": {"path": "artifacts/authoring/example-family/forms/Example.json", "sha256": family_sha},
                "metrics": {"source_behavior_records": 1},
            },
        })
        self._write(repo / "artifacts/authoring/runtime-rule-ast-resolved-v1/forms/Example.json", {
            "rules": [{
                "rule_id": "rule:one", "mechanism": "condition", "effect": "required",
                "operator": "equals", "value": "Y", "disposition": "working",
                "execution_class": "executable", "source_rule": "Required when yes",
                "target": {"path": "Example_1_0.Name"},
                "dependencies": [{"path": "Example_1_0.Name"}],
                "source_value": {"provenance": [dat_provenance]},
            }],
        })
        subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm", "fixture"], check=True)
        revision = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"], check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        return repo, revision

    def test_export_is_pinned_reproducible_and_review_gated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, revision = self._repo(Path(directory))
            first = export_packet(repo, "Example", revision)
            # A dirty working copy must not alter a revision-pinned packet.
            (repo / "artifacts/proof/grantsgov-Example.jsonl").write_text("corrupt\n", encoding="utf-8")
            second = export_packet(repo, "Example", revision)

        self.assertEqual(first, second)
        self.assertEqual(first["metrics"]["sourceRecords"], 2)
        self.assertEqual(first["metrics"]["acceptedSemanticMappings"], 0)
        self.assertEqual(first["semanticProposals"][0]["status"], "proposed")
        self.assertFalse(first["semanticProposals"][0]["publishable"])
        self.assertTrue(any(gate["kind"] == "semantic_identity" for gate in first["reviewGates"]))

    def test_import_writes_staging_not_canonical_authoring(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, revision = self._repo(root)
            packet = export_packet(repo, "Example", revision)
            output = root / "stage"
            report = import_packet(packet, output)
            evidence = json.loads((output / "evidence.json").read_text(encoding="utf-8"))
            draft = (output / "draft.tsp").read_text(encoding="utf-8")

        self.assertEqual(evidence["semanticReview"], {"status": "unreviewed", "mappings": []})
        self.assertEqual(report["generated"]["sourceRecordsTranscribed"], 2)
        self.assertEqual(report["generated"]["semanticMappingsAccepted"], 0)
        self.assertIn("namespace PromotionDraft.Example", draft)
        self.assertIn("@minLength(1)", draft)
        self.assertIn("not a canonical form declaration", draft)

    def test_import_preserves_unbounded_repetition_without_inventing_a_limit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, _ = self._repo(root)
            records_path = repo / "artifacts/proof/grantsgov-Example.jsonl"
            records = [
                json.loads(line)
                for line in records_path.read_text(encoding="utf-8").splitlines()
            ]
            records[1]["max_occurs"] = "unbounded"
            self._write(records_path, records, jsonl=True)
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-qm", "unbounded repetition"],
                check=True,
            )
            revision = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            packet = export_packet(repo, "Example", revision)
            output = root / "stage"
            import_packet(packet, output)
            draft = (output / "draft.tsp").read_text(encoding="utf-8")

        self.assertIn("name: string[];", draft)
        self.assertNotIn("@maxItems", draft)

    def test_export_uses_family_ledger_when_separate_behavior_artifact_is_absent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, _ = self._repo(Path(directory))
            behavior_path = repo / "harness/contracts/expansion-a/evidence/Example-behaviors.jsonl"
            behavior = json.loads(behavior_path.read_text(encoding="utf-8").splitlines()[0])
            behavior_path.unlink()
            family_path = repo / "artifacts/authoring/example-family/forms/Example.json"
            family = json.loads(family_path.read_text(encoding="utf-8"))
            family["source_behaviors"] = [behavior]
            self._write(family_path, family)
            family_sha = hashlib.sha256(family_path.read_bytes()).hexdigest()
            contract_path = repo / "artifacts/authoring/form-authoring-contract-v2/forms/Example.json"
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            contract["output_adapter_oracle"]["input"]["sha256"] = family_sha
            self._write(contract_path, contract)
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "embed behaviors"], check=True)
            revision = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"], check=True,
                capture_output=True, text=True,
            ).stdout.strip()

            packet = export_packet(repo, "Example", revision)

        self.assertEqual(packet["metrics"]["sourceBehaviors"], 1)
        behavior_artifact = next(
            item for item in packet["artifacts"] if item["role"] == "behavior_records"
        )
        self.assertEqual(
            behavior_artifact["path"],
            "artifacts/authoring/example-family/forms/Example.json",
        )
        self.assertFalse(any(
            item["kind"] == "source_conflict" for item in packet["reviewGates"]
        ))

    def test_export_compares_contract_with_family_scope_not_broader_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, _ = self._repo(Path(directory))
            behavior_path = repo / "harness/contracts/expansion-a/evidence/Example-behaviors.jsonl"
            applicant = json.loads(behavior_path.read_text(encoding="utf-8").splitlines()[0])
            presentation = {
                **applicant,
                "behavior_key": "behavior:presentation",
                "input_role": "presentation",
            }
            unknown = {
                **applicant,
                "behavior_key": "behavior:unknown",
                "input_role": "unknown",
            }
            self._write(behavior_path, [applicant, presentation, unknown], jsonl=True)

            family_path = repo / "artifacts/authoring/example-family/forms/Example.json"
            family = json.loads(family_path.read_text(encoding="utf-8"))
            family["source_behaviors"] = [
                applicant,
                {**applicant, "behavior_key": "behavior:defaulted", "input_role": "defaulted"},
            ]
            self._write(family_path, family)
            family_sha = hashlib.sha256(family_path.read_bytes()).hexdigest()
            contract_path = repo / "artifacts/authoring/form-authoring-contract-v2/forms/Example.json"
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            contract["output_adapter_oracle"]["input"]["sha256"] = family_sha
            contract["output_adapter_oracle"]["metrics"]["source_behavior_records"] = 2
            self._write(contract_path, contract)
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "split behavior scopes"], check=True)
            revision = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"], check=True,
                capture_output=True, text=True,
            ).stdout.strip()

            packet = export_packet(repo, "Example", revision)

        self.assertEqual(packet["metrics"]["sourceBehaviors"], 3)
        self.assertEqual(packet["metrics"]["applicantBehaviorRecords"], 1)
        self.assertEqual(packet["metrics"]["presentationBehaviorRecords"], 1)
        self.assertFalse(any(
            item["kind"] == "source_conflict" for item in packet["reviewGates"]
        ))

    def test_export_allows_a_source_form_with_no_runtime_rule_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, _ = self._repo(Path(directory))
            runtime_path = (
                repo
                / "artifacts/authoring/runtime-rule-ast-resolved-v1/forms/Example.json"
            )
            runtime_path.unlink()
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "no runtime rules"], check=True)
            revision = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"], check=True,
                capture_output=True, text=True,
            ).stdout.strip()

            packet = export_packet(repo, "Example", revision)

        self.assertEqual(packet["runtimeRules"], [])
        self.assertEqual(packet["metrics"]["runtimeRules"], 0)
        self.assertFalse(any(
            item["role"] == "runtime_rules" for item in packet["artifacts"]
        ))

    def test_export_preserves_unresolved_runtime_rule_without_inventing_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, _ = self._repo(Path(directory))
            runtime_path = (
                repo
                / "artifacts/authoring/runtime-rule-ast-resolved-v1/forms/Example.json"
            )
            runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
            runtime["rules"][0].update({
                "target": None,
                "dependencies": None,
                "source_value": None,
                "disposition": "blocked",
            })
            self._write(runtime_path, runtime)
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "unresolved rule"], check=True)
            revision = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"], check=True,
                capture_output=True, text=True,
            ).stdout.strip()

            packet = export_packet(repo, "Example", revision)

        self.assertEqual(packet["runtimeRules"][0]["targetPath"], "")
        self.assertEqual(packet["runtimeRules"][0]["dependencyPaths"], [])
        self.assertEqual(packet["runtimeRules"][0]["provenance"], [])
        self.assertEqual(packet["runtimeRules"][0]["disposition"], "blocked")
        self.assertTrue(any(
            item["kind"] == "behavior_semantics" for item in packet["reviewGates"]
        ))


if __name__ == "__main__":
    unittest.main()
