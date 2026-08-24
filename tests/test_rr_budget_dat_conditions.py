from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.classify_rr_budget_dat_conditions import (
    ATTACHMENT_POSITIVE,
    CROSS_SECTION_MINIMUM,
    DAT_PROVENANCE,
    DAT_SHA256,
    classify_condition,
    load_occurrences,
)


ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "analysis" / "rr-budget-dat-conditions.v1.json"
SCRIPT = ROOT / "scripts" / "classify_rr_budget_dat_conditions.py"


class RrBudgetDatConditionInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = json.loads(INVENTORY.read_text())

    def test_reconciles_calculation_and_condition_counts_without_conflating_them(self) -> None:
        self.assertEqual(
            self.inventory["counts"],
            {
                "extractedBehaviorOccurrences": 159,
                "calculatedBehaviorOccurrences": 56,
                "nonEmptyConditionOccurrences": 64,
                "uniqueConditionRecords": 46,
                "repeatedPathOccurrences": 18,
                "calculatedConditions": 20,
                "uniqueConditionTexts": 27,
                "byClass": {
                    "attachment-total-positive-bidirectional": 4,
                    "calculated-output-materialization": 20,
                    "cross-section-minimum-one-row": 10,
                    "optional-object-paired-requiredness": 14,
                    "optional-row-required-members": 16,
                },
                "byDisposition": {
                    "compiled-by-at-least-one-path-when-present": 10,
                    "compiled-by-positive-decimal-string-conditions": 4,
                    "represented-by-existing-declaration": 50,
                },
            },
        )

    def test_every_condition_occurrence_retains_exact_dat_provenance(self) -> None:
        self.assertEqual(self.inventory["reviewStatus"], "unreviewed")
        self.assertEqual(self.inventory["source"]["sha256"], DAT_SHA256)
        self.assertEqual(
            self.inventory["extraction"]["inputSha256"],
            "0f3e71fd70e470e3b2ce3e35be300bc8c7f240369a51aca855ea618c83d508bb",
        )
        occurrences = self.inventory["occurrences"]
        self.assertEqual(len(occurrences), 64)
        self.assertTrue(all(row["sourceSha256"] == DAT_SHA256 for row in occurrences))
        self.assertTrue(all(row["sourceProvenance"] == DAT_PROVENANCE for row in occurrences))
        self.assertTrue(all(row["sourceUri"] == self.inventory["source"]["uri"] for row in occurrences))
        self.assertTrue(all(row["sourceVersion"] == "3.0" for row in occurrences))
        self.assertTrue(
            all(
                row["extractionRevision"] == self.inventory["extraction"]["revision"]
                for row in occurrences
            )
        )
        self.assertTrue(all(row["condition"] for row in occurrences))
        self.assertTrue(all(row["occurrencePath"].startswith("RR_Budget_3_0.") for row in occurrences))

    def test_repeated_paths_are_only_the_two_exact_other_direct_cost_rules(self) -> None:
        by_key: dict[str, list[dict]] = {}
        for row in self.inventory["occurrences"]:
            by_key.setdefault(row["behaviorKey"], []).append(row)
        repeated = [rows for rows in by_key.values() if len(rows) > 1]
        self.assertEqual(len(repeated), 2)
        self.assertEqual({len(rows) for rows in repeated}, {10})
        self.assertEqual(
            {rows[0]["fieldNumber"] for rows in repeated},
            {"F-8-1", "F-8-2"},
        )
        for rows in repeated:
            self.assertEqual(len({row["condition"] for row in rows}), 1)
            self.assertEqual(len({row["conditionClass"] for row in rows}), 1)
            self.assertEqual(len({row["occurrencePath"] for row in rows}), 10)

    def test_only_exact_known_texts_receive_a_classification(self) -> None:
        for row in self.inventory["occurrences"]:
            self.assertEqual(
                classify_condition(row["condition"]),
                (row["conditionClass"], row["implementationDisposition"]),
            )
        with self.assertRaisesRegex(ValueError, "unclassified exact DAT condition"):
            classify_condition("Required if this wording merely looks similar.")

    def test_positive_decimal_string_boundary_is_exact_and_bounded(self) -> None:
        compiled = [
            row
            for row in self.inventory["occurrences"]
            if row["implementationDisposition"]
            == "compiled-by-positive-decimal-string-conditions"
        ]
        self.assertEqual(len(compiled), 4)
        self.assertEqual(
            {row["condition"] for row in compiled},
            ATTACHMENT_POSITIVE,
        )
        self.assertEqual(
            {row["conditionClass"] for row in compiled},
            {
                "attachment-total-positive-bidirectional",
            },
        )
        self.assertEqual(
            self.inventory["genericPrimitiveDecision"]["status"],
            "complete-generic-primitives",
        )

    def test_cross_section_rule_is_compiled_without_changing_review_status(self) -> None:
        compiled = [
            row
            for row in self.inventory["occurrences"]
            if row["implementationDisposition"]
            == "compiled-by-at-least-one-path-when-present"
        ]
        self.assertEqual(len(compiled), 10)
        self.assertEqual({row["condition"] for row in compiled}, {CROSS_SECTION_MINIMUM})
        self.assertEqual({row["behaviorKey"] for row in compiled}, {
            "behavior:sha256:558d6e3e22862b8dfefaa17770a96a96874e25f8af1e7e58d2ddd2758d0948f9"
        })
        self.assertEqual(self.inventory["reviewStatus"], "unreviewed")

    def test_pattern_summary_reconciles_to_occurrences_and_unique_records(self) -> None:
        patterns = self.inventory["patterns"]
        self.assertEqual(sum(row["occurrenceCount"] for row in patterns), 64)
        self.assertEqual(sum(row["uniqueRecordCount"] for row in patterns), 46)
        self.assertEqual(
            {row["conditionClass"] for row in patterns},
            set(self.inventory["counts"]["byClass"]),
        )
        for pattern in patterns:
            self.assertTrue(pattern["operatorPattern"])
            self.assertTrue(pattern["pathScope"])
            self.assertTrue(pattern["exactConditionTexts"])

    def test_source_loader_rejects_provenance_drift(self) -> None:
        occurrence = copy.deepcopy(self.inventory["occurrences"][0])
        source_row = {
            "path": occurrence["occurrencePath"],
            "behaviors": [{
                "behavior_key": occurrence["behaviorKey"],
                "field_number": occurrence["fieldNumber"],
                "field_id": occurrence["fieldId"],
                "input_role": occurrence["inputRole"],
                "implementation": occurrence["implementation"],
                "data_type": occurrence["dataType"],
                "condition": occurrence["condition"],
                "provenance": ["sha256:" + "0" * 64 + " changed.xls"],
            }],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "drift.jsonl"
            path.write_text(json.dumps(source_row) + "\n")
            with self.assertRaisesRegex(ValueError, "unexpected provenance"):
                load_occurrences(path)

    def test_unknown_flag_is_an_actionable_usage_error(self) -> None:
        result = subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "--input",
                "unused-input.jsonl",
                "--out",
                str(ROOT / "unused.json"),
                "--wat",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments: --wat", result.stderr)


if __name__ == "__main__":
    unittest.main()
