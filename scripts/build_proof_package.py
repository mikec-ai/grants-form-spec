#!/usr/bin/env python3
"""Build a compact, reproducible index of portable-form proof evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SOURCE_CONTRACT = "grants-form-proof-package-source/v1"
OUTPUT_CONTRACT = "grants-form-proof-package/v1"
REVISION = re.compile(r"^[0-9a-f]{40}$")
IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9-]*$")
CLAIM_STATUSES = {"observed_reproducible", "merged_technical_proof"}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_bytes(root: Path, revision: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = result.stderr.decode(errors="replace").strip()
        raise ValueError(f"producer evidence is not available at {revision}:{path}: {detail}")
    return result.stdout


def _require_text(record: dict[str, Any], field: str, context: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context}.{field} must be a non-empty string")
    return value


def _validate_revision(value: str, context: str) -> None:
    if not REVISION.fullmatch(value):
        raise ValueError(f"{context} must be a full 40-character lowercase Git revision")


def _github_blob(repository: str, revision: str, path: str) -> str:
    return f"{repository}/blob/{revision}/{path}"


def build_package(*, root: Path, source_path: Path, output_dir: Path) -> dict[str, Any]:
    """Validate authored claims and emit a deterministic proof manifest and index."""
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    if source.get("contract") != SOURCE_CONTRACT:
        raise ValueError(f"unsupported source contract: {source.get('contract')!r}")
    title = _require_text(source, "title", "source")
    summary = _require_text(source, "summary", "source")

    repositories = source.get("repositories")
    if not isinstance(repositories, dict):
        raise ValueError("repositories must be an object")
    producer = repositories.get("producer")
    consumer = repositories.get("consumer")
    if not isinstance(producer, dict) or not isinstance(consumer, dict):
        raise ValueError("repositories must declare producer and consumer")
    producer_url = _require_text(producer, "url", "repositories.producer")
    producer_revision = _require_text(producer, "revision", "repositories.producer")
    consumer_url = _require_text(consumer, "url", "repositories.consumer")
    _validate_revision(producer_revision, "repositories.producer.revision")

    claims = source.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ValueError("claims must be a non-empty array")
    seen_ids: set[str] = set()
    resolved_claims: list[dict[str, Any]] = []
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise ValueError(f"claims[{index}] must be an object")
        context = f"claims[{index}]"
        claim_id = _require_text(claim, "id", context)
        if not IDENTIFIER.fullmatch(claim_id):
            raise ValueError(f"{context}.id is not a stable identifier: {claim_id!r}")
        if claim_id in seen_ids:
            raise ValueError(f"duplicate claim id: {claim_id}")
        seen_ids.add(claim_id)
        _require_text(claim, "title", context)
        _require_text(claim, "statement", context)
        status = _require_text(claim, "status", context)
        if status not in CLAIM_STATUSES:
            raise ValueError(f"{context}.status is unsupported: {status!r}")
        evidence = claim.get("evidence")
        limitations = claim.get("limitations")
        reproduce = claim.get("reproduce")
        if not isinstance(evidence, list) or not evidence:
            raise ValueError(f"{context}.evidence must be a non-empty array")
        if not isinstance(limitations, list) or not limitations or not all(
            isinstance(item, str) and item.strip() for item in limitations
        ):
            raise ValueError(f"{context}.limitations must name at least one boundary")
        if not isinstance(reproduce, list) or not reproduce or not all(
            isinstance(item, str) and item.strip() for item in reproduce
        ):
            raise ValueError(f"{context}.reproduce must contain actionable steps")

        resolved_evidence: list[dict[str, Any]] = []
        for evidence_index, item in enumerate(evidence):
            if not isinstance(item, dict):
                raise ValueError(f"{context}.evidence[{evidence_index}] must be an object")
            evidence_context = f"{context}.evidence[{evidence_index}]"
            kind = _require_text(item, "kind", evidence_context)
            label = _require_text(item, "label", evidence_context)
            revision = _require_text(item, "revision", evidence_context)
            _validate_revision(revision, f"{evidence_context}.revision")
            resolved = dict(item)
            if kind == "producer_path":
                path = _require_text(item, "path", evidence_context)
                data = _git_bytes(root, revision, path)
                resolved.update(
                    {
                        "url": _github_blob(producer_url, revision, path),
                        "sha256": _sha256(data),
                        "size": len(data),
                    }
                )
            elif kind in {"producer_pull_request", "consumer_pull_request"}:
                _require_text(item, "url", evidence_context)
                state = _require_text(item, "state", evidence_context)
                if state not in {"open", "merged"}:
                    raise ValueError(f"{evidence_context}.state must be open or merged")
                expected_repository = (
                    producer_url if kind == "producer_pull_request" else consumer_url
                )
                if not item["url"].startswith(f"{expected_repository}/pull/"):
                    raise ValueError(f"{evidence_context}.url is outside its declared repository")
            else:
                raise ValueError(f"{evidence_context}.kind is unsupported: {kind!r}")
            resolved["label"] = label
            resolved_evidence.append(resolved)

        resolved_claims.append({**claim, "evidence": resolved_evidence})

    pending_inputs = source.get("pendingInputs", [])
    if not isinstance(pending_inputs, list):
        raise ValueError("pendingInputs must be an array")
    for index, item in enumerate(pending_inputs):
        if not isinstance(item, dict):
            raise ValueError(f"pendingInputs[{index}] must be an object")
        if item.get("status") != "pending":
            raise ValueError(f"pendingInputs[{index}].status must remain pending until supplied")
        _require_text(item, "expectedPath", f"pendingInputs[{index}]")
        _require_text(item, "reason", f"pendingInputs[{index}]")

    release_boundaries = source.get("releaseBoundaries")
    if not isinstance(release_boundaries, list) or not release_boundaries or not all(
        isinstance(item, str) and item.strip() for item in release_boundaries
    ):
        raise ValueError("releaseBoundaries must name at least one package-wide boundary")

    output = {
        "contract": OUTPUT_CONTRACT,
        "source": {
            "path": source_path.relative_to(root).as_posix(),
            "sha256": _sha256(source_bytes),
            "producerRepository": producer_url,
            "producerRevision": producer_revision,
            "consumerRepository": consumer_url,
        },
        "title": title,
        "summary": summary,
        "claims": resolved_claims,
        "pendingInputs": pending_inputs,
        "releaseBoundaries": release_boundaries,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "proof-manifest.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n"
    )
    (output_dir / "index.md").write_text(_render_index(output))
    return output


def _render_index(package: dict[str, Any]) -> str:
    lines = [
        f"# {package['title']}",
        "",
        package["summary"],
        "",
        f"Producer revision: `{package['source']['producerRevision']}`",
        "",
        "## Evidence-backed claims",
        "",
    ]
    for claim in package["claims"]:
        lines.extend(
            [
                f"### {claim['title']}",
                "",
                claim["statement"],
                "",
                f"Status: `{claim['status']}`",
                "",
                "Evidence:",
                "",
            ]
        )
        for evidence in claim["evidence"]:
            suffix = f" at `{evidence['revision']}`"
            if evidence.get("generatedReceipt"):
                suffix += f"; generated receipt: `{evidence['generatedReceipt']}`"
            lines.append(f"- [{evidence['label']}]({evidence['url']}){suffix}")
        lines.extend(["", "Reproduce:", ""])
        lines.extend(f"1. {step}" for step in claim["reproduce"])
        lines.extend(["", "Limitations:", ""])
        lines.extend(f"- {limitation}" for limitation in claim["limitations"])
        lines.append("")

    if package["pendingInputs"]:
        lines.extend(["## Pending inputs", ""])
        for item in package["pendingInputs"]:
            lines.append(
                f"- **{item['title']}**: `{item['status']}`. Expected at "
                f"`{item['expectedPath']}`. {item['reason']}"
            )
        lines.append("")
    lines.extend(["## Release boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in package["releaseBoundaries"])
    lines.append("")
    return "\n".join(lines)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("proof-package/v1/proof-package.json"),
        help="authored proof-package source relative to the repository root",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("build/proof-package"),
        help="generated output directory relative to the repository root",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    root = Path(__file__).resolve().parent.parent
    source_path = args.source if args.source.is_absolute() else root / args.source
    output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    try:
        package = build_package(root=root, source_path=source_path, output_dir=output_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(
        "proof_package:\n"
        "  status: built\n"
        f"  claims: {len(package['claims'])}\n"
        f"  pending_inputs: {len(package['pendingInputs'])}\n"
        f"  output_directory: {output_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
