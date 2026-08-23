#!/usr/bin/env python3
"""Build and consume a review-gated design-time promotion packet.

The exporter reads tracked artifacts at an explicit crosswalk Git revision. It therefore ignores
uncommitted sibling work and produces the same packet from the same revision. The importer writes
staging material only; it never adds a form to the canonical TypeSpec entry point.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse


CONTRACT = "grants-form-promotion/v1"
REPOSITORY = "https://github.com/mikec-ai/grants-question-crosswalk"
PROVENANCE = re.compile(r"^sha256:([0-9a-f]{64}) (https://.+)$")


class PromotionError(RuntimeError):
    pass


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise PromotionError(f"unsafe artifact path: {value}")
    return str(path)


@dataclass(frozen=True)
class Snapshot:
    root: Path
    revision: str

    @classmethod
    def open(cls, root: Path, revision: str | None) -> "Snapshot":
        root = root.resolve()
        if revision is None:
            revision = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise PromotionError(f"revision must be a full 40-character Git SHA: {revision}")
        return cls(root, revision)

    def bytes(self, path: str) -> bytes:
        path = safe_path(path)
        result = subprocess.run(
            ["git", "-C", str(self.root), "show", f"{self.revision}:{path}"],
            capture_output=True,
        )
        if result.returncode:
            detail = result.stderr.decode(errors="replace").strip()
            raise PromotionError(f"cannot read {path} at {self.revision}: {detail}")
        return result.stdout

    def exists(self, path: str) -> bool:
        path = safe_path(path)
        result = subprocess.run(
            ["git", "-C", str(self.root), "cat-file", "-e", f"{self.revision}:{path}"],
            capture_output=True,
        )
        return result.returncode == 0

    def json(self, path: str) -> dict[str, Any]:
        try:
            return json.loads(self.bytes(path))
        except json.JSONDecodeError as error:
            raise PromotionError(f"invalid JSON in {path}: {error}") from error

    def jsonl(self, path: str) -> list[dict[str, Any]]:
        records = []
        for number, line in enumerate(self.bytes(path).decode().splitlines(), start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise PromotionError(f"invalid JSON in {path}:{number}: {error}") from error
        return records


def artifact(snapshot: Snapshot, path: str, role: str) -> dict[str, str]:
    return {"path": safe_path(path), "sha256": digest(snapshot.bytes(path)), "role": role}


def check_declared_hash(document: dict[str, Any], path: str, actual: str) -> None:
    expected = document.get("sha256")
    if expected and expected != actual:
        raise PromotionError(f"declared digest for {path} is {expected}, actual digest is {actual}")


def classification(record: dict[str, Any]) -> dict[str, str]:
    kind = record.get("record_kind", "")
    declared = record.get("constraints", {}).get("declared_type", "")
    if kind == "container":
        return {"value": "container", "status": "deterministic"}
    if kind == "technical_field":
        return {"value": "technical_field", "status": "deterministic"}
    if "AttachedFileDataType" in declared or record.get("data_type") == "AttachedFileDataType":
        return {"value": "attachment", "status": "deterministic"}
    return {"value": "unresolved", "status": "unreviewed"}


def source_list(*collections: list[dict[str, Any]]) -> list[dict[str, str]]:
    sources: dict[tuple[str, str], dict[str, str]] = {}
    for collection in collections:
        for record in collection:
            provenance = list(record.get("provenance", []))
            source_value = record.get("source_value")
            if isinstance(source_value, dict):
                provenance += list(source_value.get("provenance", []))
            for value in provenance:
                match = PROVENANCE.match(value)
                if match:
                    sha, uri = match.groups()
                    sources[(uri, sha)] = {"uri": uri, "sha256": sha}
    return [sources[key] for key in sorted(sources)]


def gate(kind: str, source_path: str, message: str) -> dict[str, str]:
    raw = f"{kind}\0{source_path}\0{message}".encode()
    return {
        "id": f"gate:sha256:{digest(raw)}",
        "kind": kind,
        "sourcePath": source_path,
        "status": "open",
        "message": message,
    }


def optional_object(value: object, label: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise PromotionError(f"{label} must be an object or null")
    return value


def optional_array(value: object, label: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise PromotionError(f"{label} must be an array or null")
    return value


def export_packet(crosswalk: Path, form_id: str, revision: str | None) -> dict[str, Any]:
    snapshot = Snapshot.open(crosswalk, revision)
    manifest_path = f"artifacts/proof/grantsgov-{form_id}.jsonl.manifest.json"
    records_path = f"artifacts/proof/grantsgov-{form_id}.jsonl"
    contract_path = f"artifacts/authoring/form-authoring-contract-v2/forms/{form_id}.json"
    runtime_path = f"artifacts/authoring/runtime-rule-ast-resolved-v1/forms/{form_id}.json"
    behaviors_path = f"harness/contracts/expansion-a/evidence/{form_id}-behaviors.jsonl"

    manifest = snapshot.json(manifest_path)
    source_records = snapshot.jsonl(records_path)
    if not source_records:
        raise PromotionError(f"{records_path} contains no records")
    authoring = snapshot.json(contract_path)
    family_path = safe_path(authoring["output_adapter_oracle"]["input"]["path"])
    family = snapshot.json(family_path)
    has_runtime_artifact = snapshot.exists(runtime_path)
    runtime = snapshot.json(runtime_path) if has_runtime_artifact else {"rules": []}
    if snapshot.exists(behaviors_path):
        behavior_records = snapshot.jsonl(behaviors_path)
        behavior_artifact_path = behaviors_path
    else:
        behavior_records = family.get("source_behaviors", [])
        if not isinstance(behavior_records, list):
            raise PromotionError(
                f"{family_path} source_behaviors must be an array when {behaviors_path} is absent"
            )
        behavior_artifact_path = family_path

    if manifest.get("record_count") != len(source_records):
        raise PromotionError(
            f"{manifest_path} declares {manifest.get('record_count')} records; found {len(source_records)}"
        )
    for record in source_records:
        if record.get("form_id") != form_id:
            raise PromotionError(f"source record belongs to {record.get('form_id')}, expected {form_id}")

    artifacts = [
        artifact(snapshot, manifest_path, "xsd_manifest"),
        artifact(snapshot, records_path, "xsd_records"),
        artifact(snapshot, behavior_artifact_path, "behavior_records"),
        artifact(snapshot, contract_path, "authoring_contract"),
        artifact(snapshot, family_path, "component_proposals"),
    ]
    if has_runtime_artifact:
        artifacts.append(artifact(snapshot, runtime_path, "runtime_rules"))
    check_declared_hash(
        authoring["output_adapter_oracle"]["input"], family_path,
        next(item["sha256"] for item in artifacts if item["path"] == family_path),
    )

    records = []
    for record in source_records:
        records.append({
            "sourceKey": record["question_key"],
            "path": record["path"],
            "recordKind": record["record_kind"],
            "dataType": record.get("data_type", ""),
            "prompt": record.get("prompt", ""),
            "required": record.get("required"),
            "minOccurs": record.get("min_occurs"),
            "maxOccurs": record.get("max_occurs"),
            "constraints": record.get("constraints", {}),
            "classification": classification(record),
            "provenance": record.get("provenance", []),
        })

    behavior_evidence = [{
        "id": item["behavior_key"],
        "inputRole": item.get("input_role", ""),
        "sourceRecord": item,
        "reviewStatus": "unreviewed",
    } for item in behavior_records]

    runtime_rules = []
    for rule in runtime.get("rules", []):
        rule_id = rule["rule_id"]
        target = optional_object(rule.get("target"), f"runtime rule {rule_id} target")
        dependencies = optional_array(
            rule.get("dependencies"), f"runtime rule {rule_id} dependencies"
        )
        source_value = rule.get("source_value")
        runtime_rules.append({
            "id": rule_id,
            "mechanism": rule.get("mechanism", ""),
            "targetPath": target.get("path", ""),
            "dependencyPaths": [
                optional_object(item, f"runtime rule {rule_id} dependency").get("path", "")
                for item in dependencies
            ],
            "effect": rule.get("effect", ""),
            "operator": rule.get("operator", ""),
            "value": rule.get("value"),
            "sourceValue": source_value,
            "disposition": rule.get("disposition", ""),
            "executionClass": rule.get("execution_class", ""),
            "sourceRule": rule.get("source_rule", ""),
            "provenance": source_value.get("provenance", [])
            if isinstance(source_value, dict)
            else [],
            "reviewStatus": "proposed",
        })

    semantic_proposals = [{
        "sourceKey": item["source_question_key"],
        "sourcePath": item["source_path"],
        "moduleIds": item.get("module_ids", []),
        "role": item.get("role"),
        "status": "proposed",
        "publishable": False,
    } for item in family.get("component_assignments", [])]

    gates = []
    applicant_behavior_count = sum(
        item["inputRole"] == "applicant_entered" for item in behavior_evidence
    )
    presentation_behavior_count = sum(
        item["inputRole"] == "presentation" for item in behavior_evidence
    )
    declared_behavior_count = authoring.get("output_adapter_oracle", {}).get("metrics", {}).get(
        "source_behavior_records"
    )
    family_behavior_records = family.get("source_behaviors")
    if family_behavior_records is not None:
        if not isinstance(family_behavior_records, list):
            raise PromotionError(f"{family_path} source_behaviors must be an array")
        comparable_behavior_count = len(family_behavior_records)
        behavior_scope = "family source behavior"
    elif behavior_artifact_path == family_path:
        comparable_behavior_count = len(behavior_evidence)
        behavior_scope = "source behavior"
    else:
        comparable_behavior_count = applicant_behavior_count
        behavior_scope = "applicant behavior"
    if declared_behavior_count is not None and declared_behavior_count != comparable_behavior_count:
        gates.append(gate(
            "source_conflict", "",
            f"Authoring contract reports {declared_behavior_count} {behavior_scope} records, but the declared behavior scope contains {comparable_behavior_count} comparable records.",
        ))
    for record in records:
        if record["classification"]["value"] == "unresolved":
            gates.append(gate(
                "semantic_identity", record["path"],
                "Determine whether this source question reuses an accepted semantic question or introduces a form-specific delta.",
            ))
        if record["classification"]["value"] == "attachment":
            gates.append(gate(
                "attachment_semantics", record["path"],
                "Separate the information requirement from the attachment capture mechanism before promotion.",
            ))
        if record["constraints"].get("enumeration"):
            gates.append(gate(
                "enum_wire_values", record["path"],
                "Confirm that extracted label/value pairs preserve the exact XML wire value before authoring an enum.",
            ))
    for rule in runtime_rules:
        gates.append(gate(
            "behavior_semantics", rule["targetPath"],
            f"Review proposed {rule['mechanism']} rule {rule['id']} against source behavior and policy evidence.",
        ))
    gates.sort(key=lambda item: item["id"])

    sources = source_list(source_records, behavior_records, runtime.get("rules", []))
    if not sources:
        raise PromotionError("no source provenance could be parsed")
    source_set_sha = digest(canonical(sources))
    extracted_at = manifest["extracted_at"].replace("+00:00", "Z")

    return {
        "contract": CONTRACT,
        "form": {
            "id": form_id,
            "version": source_records[0]["form_version"],
            "title": family.get("title") or form_id,
            "sourceRoot": source_records[0]["path"],
        },
        "extraction": {
            "repository": REPOSITORY,
            "revision": snapshot.revision,
            "manifest": manifest_path,
            "extractedAt": extracted_at,
            "sourceSetSha256": source_set_sha,
        },
        "sources": sources,
        "artifacts": artifacts,
        "records": records,
        "behaviorEvidence": behavior_evidence,
        "runtimeRules": runtime_rules,
        "semanticProposals": semantic_proposals,
        "reviewGates": gates,
        "metrics": {
            "sourceRecords": len(records),
            "sourceBehaviors": len(behavior_evidence),
            "applicantBehaviorRecords": applicant_behavior_count,
            "presentationBehaviorRecords": presentation_behavior_count,
            "runtimeRules": len(runtime_rules),
            "semanticProposals": len(semantic_proposals),
            "acceptedSemanticMappings": 0,
            "openReviewGates": len(gates),
        },
    }


def identifier(value: str, *, upper: bool = False) -> str:
    words = re.findall(r"[A-Za-z]+|[0-9]+", value)
    if not words:
        return "Generated"
    if len(words) == 1 and words[0].isupper():
        return words[0].title() if upper else words[0].lower()
    if upper:
        return "".join(word[:1].upper() + word[1:] for word in words)
    first, *rest = words
    return first[:1].lower() + first[1:] + "".join(word[:1].upper() + word[1:] for word in rest)


def tsp_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_tsp(packet: dict[str, Any]) -> str:
    records = packet["records"]
    by_path = {item["path"]: item for item in records}
    children: dict[str, list[dict[str, Any]]] = {path: [] for path in by_path}
    root = packet["form"]["sourceRoot"]
    for item in records:
        if item["path"] == root:
            continue
        parent = item["path"].rsplit(".", 1)[0]
        if parent not in children:
            raise PromotionError(f"record {item['path']} has missing parent {parent}")
        children[parent].append(item)

    def model_name(path: str) -> str:
        relative = path.removeprefix(root).lstrip(".")
        return f"{identifier(relative or packet['form']['id'], upper=True)}Draft"

    def scalar_type(item: dict[str, Any]) -> str:
        kind = item["dataType"].lower()
        if kind in {"boolean"}:
            return "boolean"
        if kind in {"integer", "int", "int32"}:
            return "int32"
        return "string"

    lines = [
        'import "@simpler-grants/form-spec";',
        "",
        "using SimplerForms;",
        "",
        f"namespace PromotionDraft.{identifier(packet['form']['id'], upper=True)};",
        "",
        "// Generated staging scaffold. Source facts are transcribed; semantic reuse is not accepted here.",
        f"// Promotion packet source set: sha256:{packet['extraction']['sourceSetSha256']}",
        "",
    ]

    model_paths = [path for path in by_path if children[path]]
    model_paths.sort(key=lambda value: (value.count("."), value), reverse=True)
    for path in model_paths:
        item = by_path[path]
        is_root = path == root
        if is_root:
            form_uuid = uuid.uuid5(uuid.NAMESPACE_URL, f"promotion:{packet['form']['id']}:{packet['form']['version']}")
            fid = next((
                evidence["sourceRecord"].get("fid")
                for evidence in packet["behaviorEvidence"]
                if str(evidence["sourceRecord"].get("fid", "")).isdigit()
            ), None)
            lines.extend([
                "/** Review-gated source scaffold; not a canonical form declaration. */",
                "@Form.meta(#{",
                f"  id: {tsp_string('draft/' + identifier(packet['form']['id']))},",
                f"  formId: {tsp_string(str(form_uuid))},",
            ])
            if fid is not None:
                lines.append(f"  legacyFormId: {int(fid)},")
            lines.extend([
                f"  formName: {tsp_string('[Promotion draft] ' + packet['form']['title'])},",
                f"  shortFormName: {tsp_string(packet['form']['sourceRoot'])},",
                f"  formVersion: {tsp_string(packet['form']['version'])},",
                '  agencyCode: "GRANTS_GOV",',
                f"  formType: {tsp_string(packet['form']['id'])},",
                '  sggVersion: "1.0",',
                "})",
            ])
        lines.append(f"model {model_name(path)} {{")
        for child in children[path]:
            name = identifier(child["path"].rsplit(".", 1)[-1])
            nested = bool(children.get(child["path"]))
            value_type = model_name(child["path"]) if nested else scalar_type(child)
            max_occurs = child["maxOccurs"]
            repeated = max_occurs == "unbounded" or (
                isinstance(max_occurs, int) and max_occurs > 1
            )
            lines.append(f"  // Source: {child['path']} ({child['classification']['value']}/{child['classification']['status']})")
            if child["constraints"].get("enumeration"):
                lines.append(
                    f"  // REVIEW: {len(child['constraints']['enumeration'])} extracted enum values remain in the promotion packet."
                )
            lines.append(f"  @UI.label({tsp_string(child['prompt'] or name)})")
            constraints = child["constraints"]
            length = constraints.get("length")
            if not nested and isinstance(length, int):
                lines.extend([f"  @minLength({length})", f"  @maxLength({length})"])
            else:
                if not nested and isinstance(constraints.get("minLength"), int):
                    lines.append(f"  @minLength({constraints['minLength']})")
                if not nested and isinstance(constraints.get("maxLength"), int):
                    lines.append(f"  @maxLength({constraints['maxLength']})")
            if not nested and isinstance(constraints.get("pattern"), str):
                lines.append(f"  @pattern({tsp_string(constraints['pattern'])})")
            if repeated:
                if isinstance(child["minOccurs"], int):
                    lines.append(f"  @minItems({child['minOccurs']})")
                if isinstance(child["maxOccurs"], int):
                    lines.append(f"  @maxItems({child['maxOccurs']})")
                value_type += "[]"
            optional = "" if child["required"] else "?"
            lines.append(f"  {name}{optional}: {value_type};")
            lines.append("")
        if lines[-1] == "":
            lines.pop()
        lines.extend(["}", ""])
    return "\n".join(lines)


def source_type(uri: str) -> str:
    lower = urlparse(uri).path.lower()
    if lower.endswith(".xsd"):
        return "xsd"
    if lower.endswith(".xls") or lower.endswith(".xlsx"):
        return "dat"
    if lower.endswith(".pdf"):
        return "pdf"
    return "implementation"


def native_source_version(uri: str, kind: str) -> str | None:
    if kind != "xsd":
        return None
    filename = urlparse(uri).path.rsplit("/", 1)[-1]
    match = re.search(r"-V([0-9]+\.[0-9]+)\.xsd$", filename, re.IGNORECASE)
    if match:
        return match.group(1)
    if re.search(r"(?:^|[-_])V[0-9]", filename, re.IGNORECASE):
        raise PromotionError(
            f"unsupported version-looking XSD URI {uri}; expected a filename ending in "
            "-V<major>.<minor>.xsd"
        )
    return None


def import_packet(packet: dict[str, Any], out: Path) -> dict[str, Any]:
    if packet.get("contract") != CONTRACT:
        raise PromotionError(f"unsupported promotion contract: {packet.get('contract')}")
    out.mkdir(parents=True, exist_ok=True)
    form_slug = re.sub(r"[^a-z0-9]+", "-", packet["form"]["id"].lower()).strip("-")
    evidence_sources = []
    for index, source in enumerate(packet["sources"], start=1):
        kind = source_type(source["uri"])
        evidence_sources.append({
            "id": f"source-{index}-{source['sha256'][:12]}",
            "type": kind,
            "uri": source["uri"],
            "nativeVersion": native_source_version(source["uri"], kind),
            "sha256": source["sha256"],
        })
    evidence = {
        "contract": "grants-form-evidence/v1",
        "block": {
            "id": form_slug,
            "kind": "form",
            "formVersion": packet["form"]["version"],
        },
        "sources": evidence_sources,
        "extraction": {
            "repository": packet["extraction"]["repository"],
            "revision": packet["extraction"]["revision"],
            "artifact": packet["extraction"]["manifest"],
            "sourceSetSha256": packet["extraction"]["sourceSetSha256"],
            "extractedAt": packet["extraction"]["extractedAt"],
        },
        "semanticReview": {"status": "unreviewed", "mappings": []},
    }
    review_queue = {
        "contract": "grants-form-promotion-review/v1",
        "form": packet["form"],
        "claimsBoundary": (
            "All component and semantic assignments are proposals. No generated item contributes "
            "to published semantic coverage until explicitly reviewed and accepted."
        ),
        "semanticProposals": packet["semanticProposals"],
        "reviewGates": packet["reviewGates"],
    }
    enum_records = sum(bool(item["constraints"].get("enumeration")) for item in packet["records"])
    report = {
        "contract": "grants-form-promotion-spike-report/v1",
        "form": packet["form"],
        "generated": {
            "sourceRecordsTranscribed": len(packet["records"]),
            "sourceBehaviorsPreserved": len(packet["behaviorEvidence"]),
            "applicantBehaviorRecords": packet["metrics"]["applicantBehaviorRecords"],
            "presentationBehaviorRecords": packet["metrics"]["presentationBehaviorRecords"],
            "runtimeRuleProposalsPreserved": len(packet["runtimeRules"]),
            "provenanceSourcesPinned": len(packet["sources"]),
            "semanticMappingsAccepted": 0,
        },
        "remainingReview": {
            "openGates": len(packet["reviewGates"]),
            "semanticProposals": len(packet["semanticProposals"]),
            "enumWireValueChecks": enum_records,
            "sourceConflicts": sum(
                item["kind"] == "source_conflict" for item in packet["reviewGates"]
            ),
        },
        "assessment": (
            "The importer eliminates deterministic retranscription and provenance assembly. "
            "It intentionally does not eliminate semantic, policy, or behavior review."
        ),
    }
    outputs = {
        "promotion.json": packet,
        "evidence.json": evidence,
        "review-queue.json": review_queue,
        "import-report.json": report,
    }
    for name, value in outputs.items():
        (out / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "draft.tsp").write_text(render_tsp(packet), encoding="utf-8")
    return report


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Export or import a review-gated form promotion packet.",
    )
    commands = result.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export", help="Export pinned crosswalk evidence as a neutral packet.")
    export.add_argument("--crosswalk", required=True, type=Path)
    export.add_argument("--form", required=True)
    export.add_argument("--revision")
    export.add_argument("--out", required=True, type=Path)
    consume = commands.add_parser("import", help="Generate staging-only form-spec material.")
    consume.add_argument("--packet", required=True, type=Path)
    consume.add_argument("--out", required=True, type=Path)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "export":
            packet = export_packet(args.crosswalk, args.form, args.revision)
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print("promotion:")
            print("  status: exported")
            print(f"  form: {packet['form']['id']}")
            print(f"  records: {packet['metrics']['sourceRecords']}")
            print(f"  behaviors: {packet['metrics']['sourceBehaviors']}")
            print(f"  review_gates: {packet['metrics']['openReviewGates']}")
        else:
            packet = json.loads(args.packet.read_text(encoding="utf-8"))
            report = import_packet(packet, args.out)
            print("promotion:")
            print("  status: imported_to_staging")
            print(f"  form: {report['form']['id']}")
            print(f"  output: {args.out}")
            print(f"  accepted_semantic_mappings: {report['generated']['semanticMappingsAccepted']}")
        return 0
    except (PromotionError, KeyError, OSError, json.JSONDecodeError) as error:
        print("error:")
        print("  code: promotion_failed")
        print(f"  message: {json.dumps(str(error))}")
        print("help[1]: Verify the pinned crosswalk artifacts and review the reported gate")
        return 1


if __name__ == "__main__":
    sys.exit(main())
