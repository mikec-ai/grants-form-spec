#!/usr/bin/env python3
"""Inventory exact R&R Budget DAT conditions without interpreting their wording.

The input is the deterministic behavior-enriched JSONL projection produced by the
research crosswalk. Classification is deliberately exact and closed: an unknown
condition fails instead of being assigned to the nearest-looking pattern.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from collections import Counter


CONTRACT = "grants-form-dat-condition-inventory/v1"
DAT_SHA256 = "c85158ce7ddcc756d6e8a55a050e00b4a95cdfc8d9a2d91b7bd94c7f8bdb1035"
DAT_URI = "https://apply07.grants.gov/apply/forms/sample/RR_Budget_3_0-V3.0_F770.xls"
DAT_PROVENANCE = (
    f"sha256:{DAT_SHA256} work/form-metadata/RR_Budget_3_0-V3.0_F770.xls"
)
EXTRACTION_REPOSITORY = "https://github.com/mikec-ai/grants-question-crosswalk"
EXTRACTION_REVISION = "dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef"
EXTRACTION_ARTIFACT = "artifacts/proof/grantsgov-RRBudget-enriched.jsonl"

CALCULATED_PREFIX = "Calculated, readonly."
ROW_REQUIRED = "Required if any data is entered in this row."
PAIRED_REQUIRED = {
    "Required if Cost is entered in following question.",
    "Required if Description is entered in preceding question Can equal zero dollars.",
    "Required if EquipmentItem is entered.",
    "Required if FundsRequested is entered.",
    "Can equal zero dollars. For any instance, Funds is Required if corresponding Description is non-null.",
}
ATTACHMENT_POSITIVE = {
    "One possible attachment per budget period. Required if TotalFundForAttachedEquipment is entered and greater than zero.",
    "One possible attachment per budget period. Required if TotalFundForAttachedKeyPersons is entered and greater than zero.",
    "Required and must be greater than zero if an AdditionalEquipmentsAttachment exists.",
    "Required and must be greater than zero if an AttachedKeyPersons attachment exists.",
}
CROSS_SECTION_MINIMUM = (
    'All instances (lines 8-17) descriptions are always active. Data entry is not sequential '
    'and users can fill data as needed. If data is entered in E-5-1 "Other" for Section E - '
    "Participant/Trainee Costs, a minimum of one row is required to be filled out from line item 8-17."
)
PATTERN_DETAILS = {
    "calculated-output-materialization": {
        "operatorPattern": "prerequisites-present-implies-calculated-output-materialized",
        "pathScope": "calculated output and named prerequisites",
    },
    "optional-row-required-members": {
        "operatorPattern": "optional-object-present-implies-members-required",
        "pathScope": "members of one repeating-row object",
    },
    "optional-object-paired-requiredness": {
        "operatorPattern": "one-member-present-implies-paired-member-required",
        "pathScope": "members of one optional object",
    },
    "attachment-total-positive-bidirectional": {
        "operatorPattern": "attachment-present-iff-total-present-and-positive",
        "pathScope": "attachment and XSD decimal-string total",
    },
    "cross-section-minimum-one-row": {
        "operatorPattern": "source-value-present-implies-minimum-one-target-object",
        "pathScope": "one Section E field to ten distinct Section F objects",
    },
}


def classify_condition(condition: str) -> tuple[str, str]:
    """Return an exact class and disposition; unknown text is never approximated."""
    if condition.startswith(CALCULATED_PREFIX):
        return "calculated-output-materialization", "represented-by-existing-declaration"
    if condition == ROW_REQUIRED:
        return "optional-row-required-members", "represented-by-existing-declaration"
    if condition in PAIRED_REQUIRED:
        return "optional-object-paired-requiredness", "represented-by-existing-declaration"
    if condition in ATTACHMENT_POSITIVE:
        return "attachment-total-positive-bidirectional", "source-bound-uncompiled"
    if condition == CROSS_SECTION_MINIMUM:
        return (
            "cross-section-minimum-one-row",
            "compiled-by-at-least-one-path-when-present",
        )
    raise ValueError(f"unclassified exact DAT condition: {condition!r}")


def load_occurrences(path: pathlib.Path) -> tuple[list[dict], dict[str, int]]:
    occurrences: list[dict] = []
    all_behaviors = 0
    calculated_behaviors = 0
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        row = json.loads(raw)
        for behavior in row.get("behaviors", []):
            all_behaviors += 1
            if behavior.get("input_role") == "calculated":
                calculated_behaviors += 1
            condition = behavior.get("condition") or ""
            if not condition:
                continue
            provenance = behavior.get("provenance", [])
            if provenance != [DAT_PROVENANCE]:
                raise ValueError(
                    f"line {line_number} behavior {behavior.get('behavior_key')} has unexpected provenance"
                )
            class_id, disposition = classify_condition(condition)
            occurrences.append({
                "behaviorKey": behavior["behavior_key"],
                "occurrencePath": row["path"],
                "fieldNumber": behavior["field_number"],
                "fieldId": behavior["field_id"],
                "inputRole": behavior["input_role"],
                "implementation": behavior["implementation"],
                "dataType": behavior["data_type"],
                "condition": condition,
                "conditionClass": class_id,
                "implementationDisposition": disposition,
                "sourceId": "grantsgov-rr-budget-dat-3.0-f770",
                "sourceUri": DAT_URI,
                "sourceVersion": "3.0",
                "sourceSha256": DAT_SHA256,
                "sourceProvenance": DAT_PROVENANCE,
                "extractionRevision": EXTRACTION_REVISION,
                "extractionArtifact": EXTRACTION_ARTIFACT,
            })
    occurrences.sort(key=lambda row: (row["fieldNumber"], row["occurrencePath"], row["behaviorKey"]))
    return occurrences, {
        "extractedBehaviorOccurrences": all_behaviors,
        "calculatedBehaviorOccurrences": calculated_behaviors,
    }


def inventory(input_path: pathlib.Path) -> dict:
    occurrences, source_counts = load_occurrences(input_path)
    unique_keys = {row["behaviorKey"] for row in occurrences}
    calculated_conditions = [row for row in occurrences if row["inputRole"] == "calculated"]
    by_class = Counter(row["conditionClass"] for row in occurrences)
    by_disposition = Counter(row["implementationDisposition"] for row in occurrences)
    patterns = []
    for class_id, count in sorted(by_class.items()):
        class_rows = [row for row in occurrences if row["conditionClass"] == class_id]
        patterns.append({
            "conditionClass": class_id,
            **PATTERN_DETAILS[class_id],
            "occurrenceCount": count,
            "uniqueRecordCount": len({row["behaviorKey"] for row in class_rows}),
            "exactConditionTexts": sorted({row["condition"] for row in class_rows}),
            "implementationDisposition": class_rows[0]["implementationDisposition"],
        })
    return {
        "contract": CONTRACT,
        "source": {
            "id": "grantsgov-rr-budget-dat-3.0-f770",
            "type": "dat",
            "uri": DAT_URI,
            "sha256": DAT_SHA256,
            "formVersion": "3.0",
        },
        "extraction": {
            "repository": EXTRACTION_REPOSITORY,
            "revision": EXTRACTION_REVISION,
            "artifact": EXTRACTION_ARTIFACT,
            "inputSha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        },
        "counts": {
            **source_counts,
            "nonEmptyConditionOccurrences": len(occurrences),
            "uniqueConditionRecords": len(unique_keys),
            "repeatedPathOccurrences": len(occurrences) - len(unique_keys),
            "calculatedConditions": len(calculated_conditions),
            "uniqueConditionTexts": len({row["condition"] for row in occurrences}),
            "byClass": dict(sorted(by_class.items())),
            "byDisposition": dict(sorted(by_disposition.items())),
        },
        "genericPrimitiveDecision": {
            "status": "partial-generic-primitive",
            "reason": (
                "Fifty source occurrences are already represented by optional-object member "
                "requiredness or the existing calculated-output materialization declaration. "
                "Ten path occurrences of one cross-section rule compile through the bounded "
                "atLeastOnePathWhenPresent contract. The remaining four attachment/total rules "
                "require a positive comparison over an XSD numeric-string wire type and remain "
                "explicitly unavailable pending a consumer-validated numeric-string contract."
            ),
        },
        "reviewStatus": "unreviewed",
        "patterns": patterns,
        "occurrences": occurrences,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify exact R&R Budget DAT condition records.")
    parser.add_argument("--input", type=pathlib.Path, required=True, help="Behavior-enriched JSONL input.")
    parser.add_argument("--out", type=pathlib.Path, required=True, help="Machine-readable JSON output.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = inventory(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"rr_budget_dat_conditions: failed\n  error: {exc}", file=sys.stderr)
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    counts = result["counts"]
    print("rr_budget_dat_conditions:")
    print("  status: classified")
    print(f"  non_empty_occurrences: {counts['nonEmptyConditionOccurrences']}")
    print(f"  unique_records: {counts['uniqueConditionRecords']}")
    print(f"  calculated_records: {counts['calculatedBehaviorOccurrences']}")
    print(f"  calculated_conditions: {counts['calculatedConditions']}")
    print(f"  output: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
