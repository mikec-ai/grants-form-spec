#!/usr/bin/env python3
"""Enforce a monotonic baseline for unexplained form-local field occurrences."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_ANALYSIS = ROOT / "build" / "analysis" / "form-analysis.json"
DEFAULT_BASELINE = ROOT / "analysis" / "unclassified-fields-baseline.v1.json"


def read_json(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as error:
        raise ValueError(f"missing file: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {path}: {error}") from error


def identities(analysis: dict) -> set[str]:
    found: set[str] = set()
    for row in analysis.get("unclassifiedFormFields", []):
        form_id = row.get("formId")
        field_path = row.get("fieldPath")
        if not isinstance(form_id, str) or not isinstance(field_path, str):
            raise ValueError("every unclassified row must contain string formId and fieldPath")
        identity = f"{form_id}:{field_path}"
        if identity in found:
            raise ValueError(f"duplicate unclassified occurrence: {identity}")
        found.add(identity)
    return found


def baseline_sets(baseline: dict) -> tuple[set[str], set[str]]:
    if baseline.get("version") != 1:
        raise ValueError("baseline version must be 1")
    initial_list = baseline.get("initial")
    resolved_list = baseline.get("resolved")
    if not isinstance(initial_list, list) or not all(isinstance(item, str) for item in initial_list):
        raise ValueError("baseline initial must be an array of strings")
    if not isinstance(resolved_list, list) or not all(isinstance(item, str) for item in resolved_list):
        raise ValueError("baseline resolved must be an array of strings")
    initial, resolved = set(initial_list), set(resolved_list)
    if len(initial) != len(initial_list):
        raise ValueError("baseline initial contains duplicate identities")
    if len(resolved) != len(resolved_list):
        raise ValueError("baseline resolved contains duplicate identities")
    if initial_list != sorted(initial_list):
        raise ValueError("baseline initial must be sorted")
    if resolved_list != sorted(resolved_list):
        raise ValueError("baseline resolved must be sorted")
    unknown_resolutions = resolved - initial
    if unknown_resolutions:
        raise ValueError(
            "baseline resolves identities absent from initial: "
            + ", ".join(sorted(unknown_resolutions))
        )
    source_baseline = baseline.get("sourceBaseline")
    if not isinstance(source_baseline, dict):
        raise ValueError("baseline sourceBaseline must be an object")
    adjusted_count = source_baseline.get("lineageAdjustedOccurrenceCount")
    if adjusted_count != len(initial):
        raise ValueError(
            "baseline sourceBaseline.lineageAdjustedOccurrenceCount must equal initial length"
        )
    return initial, resolved


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fail when unclassified form-field debt grows, returns, or disappears silently."
    )
    parser.add_argument("--analysis", type=pathlib.Path, default=DEFAULT_ANALYSIS)
    parser.add_argument("--baseline", type=pathlib.Path, default=DEFAULT_BASELINE)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        current = identities(read_json(args.analysis))
        initial, resolved = baseline_sets(read_json(args.baseline))
    except ValueError as error:
        print(f"unclassified-field-ratchet: invalid input: {error}", file=sys.stderr)
        return 2

    expected = initial - resolved
    additions = current - initial
    returned = current & resolved
    unrecorded_resolutions = expected - current
    if additions or returned or unrecorded_resolutions:
        print("unclassified-field-ratchet: failed", file=sys.stderr)
        if additions:
            print("  new unexplained occurrences:", file=sys.stderr)
            for identity in sorted(additions):
                print(f"    + {identity}", file=sys.stderr)
        if returned:
            print("  resolved occurrences that returned:", file=sys.stderr)
            for identity in sorted(returned):
                print(f"    ! {identity}", file=sys.stderr)
        if unrecorded_resolutions:
            print(
                "  removed occurrences not yet moved from initial to resolved:",
                file=sys.stderr,
            )
            for identity in sorted(unrecorded_resolutions):
                print(f"    - {identity}", file=sys.stderr)
        return 1

    print("unclassified-field-ratchet:")
    print("  status: passed")
    print(f"  initial: {len(initial)}")
    print(f"  resolved: {len(resolved)}")
    print(f"  remaining: {len(current)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
