#!/usr/bin/env python3
"""Require every emitted form field to have canonical lineage or an explicit response role."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_ANALYSIS = ROOT / "build" / "analysis" / "form-analysis.json"
DEFAULT_EXCEPTIONS = ROOT / "analysis" / "unclassified-field-exceptions.v1.json"
REQUIRED_EXCEPTION_FIELDS = {
    "formId",
    "fieldPath",
    "evidenceReferences",
    "owner",
    "reason",
    "removalCondition",
}
REQUIRED_REMOVAL_FIELDS = {"criterion", "trackingReference"}
SUPERBEE_TASK = re.compile(
    r"tasks/[a-z0-9][a-z0-9._-]*(?:/[a-z0-9][a-z0-9._-]*)*"
)
GITHUB_TRACKER = re.compile(
    r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/(?:issues|pull)/[1-9][0-9]*"
)


def read_json(path: pathlib.Path) -> dict:
    try:
        value = json.loads(path.read_text())
    except FileNotFoundError as error:
        raise ValueError(f"missing file: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"JSON document must be an object: {path}")
    return value


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def decode_pointer_token(token: str, *, reference: str) -> str:
    if re.search(r"~(?![01])", token):
        raise ValueError(f"evidence reference has an invalid JSON Pointer escape: {reference}")
    return token.replace("~1", "/").replace("~0", "~")


def validate_evidence_reference(reference: str) -> None:
    if reference.count("#") != 1:
        raise ValueError(
            f"evidence reference must contain one JSON Pointer fragment: {reference}"
        )
    relative_text, pointer = reference.split("#", 1)
    relative = pathlib.PurePosixPath(relative_text)
    if (
        relative.is_absolute()
        or not relative.parts
        or relative.parts[0] != "evidence"
        or ".." in relative.parts
        or relative.suffix != ".json"
        or relative.as_posix() != relative_text
    ):
        raise ValueError(
            f"evidence reference must use a canonical evidence/*.json path: {reference}"
        )
    if not pointer.startswith("/"):
        raise ValueError(f"evidence reference must select content with a JSON Pointer: {reference}")

    evidence_root = (ROOT / "evidence").resolve()
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(evidence_root) or not path.is_file():
        raise ValueError(f"evidence reference file does not exist: {reference}")
    try:
        value: object = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        raise ValueError(f"evidence reference file is invalid JSON: {relative_text}: {error}") from error

    for raw_token in pointer[1:].split("/"):
        token = decode_pointer_token(raw_token, reference=reference)
        if isinstance(value, dict) and token in value:
            value = value[token]
            continue
        if isinstance(value, list) and re.fullmatch(r"0|[1-9][0-9]*", token):
            index = int(token)
            if index < len(value):
                value = value[index]
                continue
        raise ValueError(f"evidence reference JSON Pointer does not resolve: {reference}")


def valid_tracking_reference(reference: object) -> bool:
    if not nonempty_string(reference):
        return False
    assert isinstance(reference, str)
    if SUPERBEE_TASK.fullmatch(reference):
        return pathlib.PurePosixPath(reference).as_posix() == reference
    return GITHUB_TRACKER.fullmatch(reference) is not None


def identity(record: dict, *, label: str) -> str:
    form_id = record.get("formId")
    field_path = record.get("fieldPath")
    if not nonempty_string(form_id) or not nonempty_string(field_path):
        raise ValueError(f"every {label} must contain non-empty formId and fieldPath")
    if not field_path.startswith("/"):
        raise ValueError(f"{label} fieldPath must be a JSON pointer: {form_id}:{field_path}")
    return f"{form_id}:{field_path}"


def unclassified_identities(analysis: dict) -> set[str]:
    rows = analysis.get("unclassifiedFormFields")
    if not isinstance(rows, list):
        raise ValueError("analysis unclassifiedFormFields must be an array")
    status = analysis.get("status")
    if not isinstance(status, dict):
        raise ValueError("analysis status must be an object")
    if status.get("unclassifiedFormFieldCount") != len(rows):
        raise ValueError(
            "analysis status.unclassifiedFormFieldCount must equal unclassifiedFormFields length"
        )
    found: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("every unclassified row must be an object")
        record_id = identity(row, label="unclassified row")
        if record_id in found:
            raise ValueError(f"duplicate unclassified occurrence: {record_id}")
        found.add(record_id)
    return found


def exception_identities(document: dict) -> set[str]:
    if document.get("version") != 1:
        raise ValueError("exception document version must be 1")
    records = document.get("exceptions")
    if not isinstance(records, list):
        raise ValueError("exception document exceptions must be an array")

    found: set[str] = set()
    ordered: list[str] = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("every exception must be an object")
        missing = REQUIRED_EXCEPTION_FIELDS - set(record)
        unexpected = set(record) - REQUIRED_EXCEPTION_FIELDS
        if missing or unexpected:
            details = []
            if missing:
                details.append("missing=" + ",".join(sorted(missing)))
            if unexpected:
                details.append("unexpected=" + ",".join(sorted(unexpected)))
            raise ValueError("invalid exception fields: " + "; ".join(details))

        record_id = identity(record, label="exception")
        if record_id in found:
            raise ValueError(f"duplicate exception: {record_id}")
        found.add(record_id)
        ordered.append(record_id)

        references = record["evidenceReferences"]
        if (
            not isinstance(references, list)
            or not references
            or not all(nonempty_string(reference) for reference in references)
        ):
            raise ValueError(f"exception {record_id} requires evidenceReferences")
        if len(references) != len(set(references)):
            raise ValueError(f"exception {record_id} contains duplicate evidenceReferences")
        for reference in references:
            validate_evidence_reference(reference)
        for field in ("owner", "reason"):
            if not nonempty_string(record[field]):
                raise ValueError(f"exception {record_id} requires non-empty {field}")

        removal = record["removalCondition"]
        if not isinstance(removal, dict) or set(removal) != REQUIRED_REMOVAL_FIELDS:
            raise ValueError(
                f"exception {record_id} removalCondition must contain exactly "
                "criterion and trackingReference"
            )
        if not all(nonempty_string(removal[field]) for field in REQUIRED_REMOVAL_FIELDS):
            raise ValueError(
                f"exception {record_id} removalCondition values must be non-empty"
            )
        if not valid_tracking_reference(removal["trackingReference"]):
            raise ValueError(
                f"exception {record_id} trackingReference must be a Superbee tasks/... id or "
                "GitHub issue/pull URL"
            )

    if ordered != sorted(ordered):
        raise ValueError("exceptions must be sorted by formId and fieldPath")
    return found


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fail when an emitted leaf field lacks canonical question lineage or an explicit "
            "non-applicant response role."
        )
    )
    parser.add_argument("--analysis", type=pathlib.Path, default=DEFAULT_ANALYSIS)
    parser.add_argument("--exceptions", type=pathlib.Path, default=DEFAULT_EXCEPTIONS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        unclassified = unclassified_identities(read_json(args.analysis))
        exceptions = exception_identities(read_json(args.exceptions))
    except ValueError as error:
        print(f"classified-field-gate: invalid input: {error}", file=sys.stderr)
        return 2

    unexplained = unclassified - exceptions
    stale = exceptions - unclassified
    if unexplained or stale:
        print("classified-field-gate: failed", file=sys.stderr)
        if unexplained:
            print("  fields without canonical lineage or an approved exception:", file=sys.stderr)
            for record_id in sorted(unexplained):
                print(f"    + {record_id}", file=sys.stderr)
        if stale:
            print("  stale exceptions whose removal condition has been met:", file=sys.stderr)
            for record_id in sorted(stale):
                print(f"    - {record_id}", file=sys.stderr)
        return 1

    print("classified-field-gate:")
    print("  status: passed")
    print(f"  unclassified: {len(unclassified)}")
    print(f"  exceptions: {len(exceptions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
