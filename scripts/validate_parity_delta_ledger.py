#!/usr/bin/env python3
"""Validate the portable parity-delta ledger and its offline evidence receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "parity" / "legacy-deltas.v1.json"
CONTRACT = "grants-form-parity-delta-ledger/v1"
DECISION_CONTRACT = "grants-form-parity-decision/v1"
DECISION_RECEIPT_CONTRACT = "grants-form-parity-decision-verification/v1"
PRODUCER_REPOSITORY = "https://github.com/mikec-ai/grants-form-spec.git"


def _git_blob(root: Path, revision: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise ValueError(f"decision artifact is absent at its pinned revision: {path}")
    return result.stdout


def _load_decision_artifacts(
    root: Path, ledger: dict[str, Any]
) -> dict[tuple[str, str, str], dict[str, Any]]:
    verification = ledger.get("decisionVerification", {})
    receipt_path = root / verification.get("receipt", "")
    if not receipt_path.is_file():
        raise ValueError("parity decision verification receipt is missing")
    receipt = json.loads(receipt_path.read_text())
    if receipt.get("contract") != DECISION_RECEIPT_CONTRACT:
        raise ValueError("unsupported parity decision verification receipt")
    entries = receipt.get("artifacts")
    if not isinstance(entries, list):
        raise ValueError("parity decision verification receipt has no artifacts array")
    verified: dict[tuple[str, str, str], dict[str, Any]] = {}
    for entry in entries:
        repository = entry.get("repository") if isinstance(entry, dict) else None
        revision = entry.get("revision") if isinstance(entry, dict) else None
        path = entry.get("path") if isinstance(entry, dict) else None
        digest = entry.get("sha256") if isinstance(entry, dict) else None
        key = (repository, revision, path)
        if (
            repository != PRODUCER_REPOSITORY
            or not re.fullmatch(r"[0-9a-f]{40}", str(revision))
            or not isinstance(path, str)
            or not re.fullmatch(r"parity/decisions/[a-z0-9][a-z0-9.-]+\.json", path)
            or not re.fullmatch(r"[0-9a-f]{64}", str(digest))
            or key in verified
        ):
            raise ValueError("parity decision verification receipt has invalid artifacts")
        local_path = root / path
        if not local_path.is_file():
            raise ValueError(f"verified decision artifact is missing: {path}")
        payload = local_path.read_bytes()
        if hashlib.sha256(payload).hexdigest() != digest:
            raise ValueError(f"verified decision artifact digest mismatch: {path}")
        if _git_blob(root, revision, path) != payload:
            raise ValueError(f"decision artifact is stale from its pinned revision: {path}")
        artifact = json.loads(payload)
        required = {
            "contract",
            "id",
            "ledgerRecordId",
            "formId",
            "target",
            "classification",
            "decision",
            "reviewer",
            "reviewedAt",
            "rationale",
        }
        if set(artifact) != required or artifact.get("contract") != DECISION_CONTRACT:
            raise ValueError(f"verified decision artifact has an invalid contract: {path}")
        verified[key] = artifact
    return verified


def _pointer_exists(document: Any, pointer: str) -> bool:
    node = document
    for raw in pointer.removeprefix("/").split("/") if pointer != "/" else []:
        step = raw.replace("~1", "/").replace("~0", "~")
        if step == "items" and isinstance(node, dict):
            node = node.get("items")
        elif step == "properties" and isinstance(node, dict):
            node = node.get("properties")
        elif isinstance(node, dict):
            node = node.get(step)
        elif isinstance(node, list) and step.isdigit() and int(step) < len(node):
            node = node[int(step)]
        else:
            return False
        if node is None:
            return False
    return True


def _semantic_target_exists(root: Path, record: dict[str, Any]) -> bool:
    form_id = record["formId"]
    semantic = record["target"]["semanticTarget"]
    if semantic["kind"] == "canonical_form_path":
        path = root / "dist" / "forms" / form_id / "index.json"
        if not path.is_file():
            return False
        steps = semantic["value"].removeprefix("/").split("/")
        occurrence = "/" + "/".join(
            "[]" if step == "items" else step for step in steps if step != "properties"
        )
        declared = {row["path"] for row in json.loads(path.read_text())["fieldOccurrences"]}
        return occurrence in declared
    if semantic["kind"] == "ui_section":
        path = root / "dist" / "forms" / form_id / "sgg" / "ui-schema.json"
        if not path.is_file():
            return False
        document = json.loads(path.read_text())
        return any(
            isinstance(node, dict) and node.get("name") == semantic["value"]
            for node in document
        )
    if semantic["kind"] == "policy_reference":
        match = re.fullmatch(r"policy:([^@]+)@([^#]+)#(.+)", semantic["value"])
        if not match:
            return False
        policy_id, version, section_id = match.groups()
        for path in (root / "policies").glob("*.json"):
            document = json.loads(path.read_text())
            if document.get("id") == policy_id and document.get("version") == version:
                return section_id in {section.get("id") for section in document.get("sections", [])}
        return False
    # Rule-path identity needs exact resolution against the emitted rule artifact. Until that
    # resolver exists, accepting a nonempty string would recreate a blanket allowance.
    return False


def validate_ledger(root: Path, ledger_path: Path) -> dict[str, Any]:
    ledger = json.loads(ledger_path.read_text())
    if ledger.get("contract") != CONTRACT:
        raise ValueError(f"unsupported parity delta ledger: {ledger.get('contract')!r}")
    verification = ledger.get("evidenceVerification", {})
    receipt_path = root / verification.get("receipt", "")
    if not receipt_path.is_file():
        raise ValueError("parity delta evidence verification receipt is missing")
    receipt = json.loads(receipt_path.read_text())
    for field in ("repository", "revision"):
        if receipt.get(field) != verification.get(field):
            raise ValueError(f"evidence verification {field} does not match the ledger pin")
    verified = {entry["path"]: entry["sha256"] for entry in receipt.get("files", [])}
    if not verified or any(not re.fullmatch(r"[0-9a-f]{64}", digest) for digest in verified.values()):
        raise ValueError("evidence verification receipt has no valid file digests")
    used_verified_paths: set[str] = set()
    verified_decisions = _load_decision_artifacts(root, ledger)
    used_decisions: set[tuple[str, str, str]] = set()

    records = ledger.get("records")
    if not isinstance(records, list):
        raise ValueError("parity delta records must be an array")
    ids: set[str] = set()
    targets: set[tuple[str, str, str]] = set()
    for record in records:
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id or record_id in ids:
            raise ValueError(f"duplicate or missing parity delta id: {record_id!r}")
        ids.add(record_id)
        target = record.get("target", {})
        exact = (record.get("formId"), target.get("dimension"), target.get("differenceKey"))
        if exact in targets or any(not isinstance(value, str) or not value for value in exact):
            raise ValueError(f"duplicate or incomplete exact delta target: {exact!r}")
        targets.add(exact)
        if not _semantic_target_exists(root, record):
            raise ValueError(f"{record_id} semantic target is absent from emitted form artifacts")
        references = record.get("evidenceReferences")
        if not isinstance(references, list) or not references:
            raise ValueError(f"{record_id} has no evidence reference")
        reference_ids: set[str] = set()
        for reference in references:
            if reference.get("repository") != verification.get("repository") or reference.get(
                "revision"
            ) != verification.get("revision"):
                raise ValueError(f"{record_id} evidence does not use the verified source pin")
            path = reference.get("path")
            if path not in verified:
                raise ValueError(f"{record_id} evidence path is absent from the verification receipt")
            used_verified_paths.add(path)
            reference_ids.add(reference.get("id"))
        assertion = record.get("differentialAssertion", {})
        if assertion.get("evidenceReferenceId") not in reference_ids or not assertion.get("testId"):
            raise ValueError(f"{record_id} has no exercising differential assertion")
        source_support = record.get("sourceSupport", {})
        support_references = source_support.get("evidenceReferences")
        if source_support.get("status") not in {"unverified", "partial", "verified"} or not isinstance(
            support_references, list
        ):
            raise ValueError(f"{record_id} has invalid source-support state")
        if source_support.get("status") == "verified" and not support_references:
            raise ValueError(f"{record_id} verified source support has no evidence")
        if source_support.get("status") == "unverified" and support_references:
            raise ValueError(f"{record_id} unverified source support cannot cite verified evidence")
        for reference in support_references:
            if reference.get("repository") != "https://github.com/mikec-ai/grants-form-spec.git":
                raise ValueError(f"{record_id} source support is not a producer evidence reference")
            revision = reference.get("revision")
            path = reference.get("path")
            if not re.fullmatch(r"[0-9a-f]{40}", str(revision)) or not isinstance(path, str):
                raise ValueError(f"{record_id} source support lacks an exact revision and path")
            verified_at_revision = subprocess.run(
                ["git", "cat-file", "-e", f"{revision}:{path}"],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
            )
            if verified_at_revision.returncode != 0:
                raise ValueError(f"{record_id} source evidence is absent at its pinned revision")
        review = record.get("review", {})
        status = review.get("status")
        decision_evidence = review.get("decisionEvidence")
        if status not in {"proposed", "accepted", "rejected"}:
            raise ValueError(f"{record_id} has unsupported review status {status!r}")
        if record.get("classification") == "unresolved_mismatch" and status == "accepted":
            raise ValueError(f"{record_id} cannot accept an unresolved mismatch")
        if status == "accepted" and record.get("classification") == "unclassified":
            raise ValueError(f"{record_id} accepted review lacks a resolved classification")
        if status == "accepted":
            if not review.get("reviewer") or not review.get("reviewedAt") or not decision_evidence:
                raise ValueError(
                    f"{record_id} accepted review lacks reviewer, timestamp, or decision evidence"
                )
            if not isinstance(decision_evidence, list) or len(decision_evidence) != 1:
                raise ValueError(f"{record_id} accepted review requires exactly one decision artifact")
            decision_reference = decision_evidence[0]
            decision_key = (
                decision_reference.get("repository"),
                decision_reference.get("revision"),
                decision_reference.get("path"),
            )
            if decision_key in used_decisions:
                raise ValueError(f"{record_id} reuses a decision artifact")
            artifact = verified_decisions.get(decision_key)
            if artifact is None:
                raise ValueError(
                    f"{record_id} decision evidence is absent from the offline verification receipt"
                )
            expected = {
                "id": decision_reference.get("id"),
                "ledgerRecordId": record_id,
                "formId": record.get("formId"),
                "target": record.get("target"),
                "classification": record.get("classification"),
                "decision": "accepted",
                "reviewer": review.get("reviewer"),
                "reviewedAt": review.get("reviewedAt"),
            }
            stale = sorted(key for key, value in expected.items() if artifact.get(key) != value)
            if stale:
                raise ValueError(
                    f"{record_id} decision artifact is stale for ledger fields: {stale}"
                )
            used_decisions.add(decision_key)
        elif decision_evidence:
            raise ValueError(f"{record_id} non-accepted review cannot claim decision evidence")
        if (
            record.get("classification") == "authoritative_source_correction"
            and source_support.get("status") != "verified"
        ):
            raise ValueError(
                f"{record_id} authoritative source correction lacks verified source support"
            )
        if status == "proposed" and (review.get("reviewer") or review.get("reviewedAt")):
            raise ValueError(f"{record_id} proposed review cannot claim completed review")
    unused_verified_paths = sorted(set(verified) - used_verified_paths)
    if unused_verified_paths:
        raise ValueError(f"evidence verification receipt has unused paths: {unused_verified_paths}")
    unused_decisions = sorted(set(verified_decisions) - used_decisions)
    if unused_decisions:
        raise ValueError(f"parity decision receipt has unused artifacts: {unused_decisions}")
    return ledger


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        ledger = validate_ledger(ROOT, args.ledger)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    digest = hashlib.sha256(args.ledger.read_bytes()).hexdigest()
    print(
        "parity_delta_ledger:\n"
        "  status: valid\n"
        f"  records: {len(ledger['records'])}\n"
        f"  sha256: {digest}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
