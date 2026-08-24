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
        if status == "accepted":
            if not review.get("reviewer") or not review.get("reviewedAt") or not decision_evidence:
                raise ValueError(
                    f"{record_id} accepted review lacks reviewer, timestamp, or decision evidence"
                )
        elif status not in {"proposed", "rejected"}:
            raise ValueError(f"{record_id} has unsupported review status {status!r}")
        if record.get("classification") == "unresolved_mismatch" and status == "accepted":
            raise ValueError(f"{record_id} cannot accept an unresolved mismatch")
        if status == "proposed" and (review.get("reviewer") or review.get("reviewedAt")):
            raise ValueError(f"{record_id} proposed review cannot claim completed review")
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
