from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "scripts" / "check_classified_form_fields.py"


class ClassifiedFormFieldGateTests(unittest.TestCase):
    def run_check(self, current: list[str], exceptions: list[dict] | None = None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis = root / "analysis.json"
            exception_file = root / "exceptions.json"
            analysis.write_text(json.dumps({
                "status": {"unclassifiedFormFieldCount": len(current)},
                "unclassifiedFormFields": [
                    {
                        "formId": record_id.split(":", 1)[0],
                        "fieldPath": record_id.split(":", 1)[1],
                    }
                    for record_id in current
                ],
            }))
            exception_file.write_text(json.dumps({
                "version": 1,
                "exceptions": exceptions or [],
            }))
            return subprocess.run(
                [
                    "python3",
                    str(CHECKER),
                    "--analysis",
                    str(analysis),
                    "--exceptions",
                    str(exception_file),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

    @staticmethod
    def exception(record_id: str) -> dict:
        form_id, field_path = record_id.split(":", 1)
        return {
            "formId": form_id,
            "fieldPath": field_path,
            "evidenceReferences": [
                "evidence/forms/sf424/evidence.json#/semanticReview/mappings/0"
            ],
            "owner": "form-authoring",
            "reason": "Pinned source evidence needs a bounded semantic decision.",
            "removalCondition": {
                "criterion": "Remove after the source-bound question identity is reviewed.",
                "trackingReference": "tasks/review-example-field",
            },
        }

    def test_accepts_zero_unclassified_fields_and_zero_exceptions(self) -> None:
        result = self.run_check([])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unclassified: 0", result.stdout)
        self.assertIn("exceptions: 0", result.stdout)

    def test_rejects_an_unclassified_field_without_an_exception(self) -> None:
        result = self.run_check(["new-form:/newField"])
        self.assertEqual(result.returncode, 1)
        self.assertIn("+ new-form:/newField", result.stderr)

    def test_accepts_a_complete_evidence_backed_exception(self) -> None:
        record_id = "new-form:/newField"
        result = self.run_check([record_id], [self.exception(record_id)])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("exceptions: 1", result.stdout)

    def test_accepts_a_github_issue_or_pull_tracking_reference(self) -> None:
        record_id = "new-form:/newField"
        for tracker in (
            "https://github.com/mikec-ai/grants-form-spec/issues/123",
            "https://github.com/mikec-ai/grants-form-spec/pull/55",
        ):
            with self.subTest(tracker=tracker):
                exception = self.exception(record_id)
                exception["removalCondition"]["trackingReference"] = tracker
                result = self.run_check([record_id], [exception])
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_an_incomplete_exception(self) -> None:
        record_id = "new-form:/newField"
        exception = self.exception(record_id)
        del exception["owner"]
        result = self.run_check([record_id], [exception])
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing=owner", result.stderr)

    def test_rejects_an_exception_without_evidence_owner_or_reason(self) -> None:
        record_id = "new-form:/newField"
        invalid_values = {
            "evidenceReferences": [],
            "owner": " ",
            "reason": "",
        }
        for field, value in invalid_values.items():
            with self.subTest(field=field):
                exception = self.exception(record_id)
                exception[field] = value
                result = self.run_check([record_id], [exception])
                self.assertEqual(result.returncode, 2)
                self.assertIn(field, result.stderr)

    def test_rejects_bogus_but_nonempty_evidence_references(self) -> None:
        record_id = "new-form:/newField"
        invalid_references = {
            "outside evidence": "documentation/architecture.md#/anything",
            "missing file": "evidence/forms/missing/evidence.json#/sources/0",
            "missing pointer": "evidence/forms/sf424/evidence.json#/missing/record",
            "invalid pointer escape": (
                "evidence/forms/sf424/evidence.json#/semanticReview/~2mappings"
            ),
        }
        for label, reference in invalid_references.items():
            with self.subTest(label=label):
                exception = self.exception(record_id)
                exception["evidenceReferences"] = [reference]
                result = self.run_check([record_id], [exception])
                self.assertEqual(result.returncode, 2)
                self.assertIn("evidence reference", result.stderr)

    def test_rejects_a_bogus_but_nonempty_tracking_reference(self) -> None:
        record_id = "new-form:/newField"
        exception = self.exception(record_id)
        exception["removalCondition"]["trackingReference"] = "follow-up-someday"
        result = self.run_check([record_id], [exception])
        self.assertEqual(result.returncode, 2)
        self.assertIn("Superbee tasks/... id or GitHub issue/pull URL", result.stderr)

    def test_rejects_an_unbounded_removal_condition(self) -> None:
        record_id = "new-form:/newField"
        exception = self.exception(record_id)
        exception["removalCondition"] = {
            "criterion": "Resolve it later.",
        }
        result = self.run_check([record_id], [exception])
        self.assertEqual(result.returncode, 2)
        self.assertIn("criterion and trackingReference", result.stderr)

    def test_rejects_a_stale_exception(self) -> None:
        record_id = "new-form:/newField"
        result = self.run_check([], [self.exception(record_id)])
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"- {record_id}", result.stderr)

    def test_rejects_unsorted_exceptions(self) -> None:
        first = "z-form:/field"
        second = "a-form:/field"
        result = self.run_check(
            [first, second],
            [self.exception(first), self.exception(second)],
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("sorted by formId and fieldPath", result.stderr)

    def test_rejects_an_inconsistent_analysis_count(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis = root / "analysis.json"
            exception_file = root / "exceptions.json"
            analysis.write_text(json.dumps({
                "status": {"unclassifiedFormFieldCount": 1},
                "unclassifiedFormFields": [],
            }))
            exception_file.write_text('{"version": 1, "exceptions": []}')
            result = subprocess.run(
                [
                    "python3",
                    str(CHECKER),
                    "--analysis",
                    str(analysis),
                    "--exceptions",
                    str(exception_file),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("must equal", result.stderr)

    def test_unknown_flags_fail_with_actionable_help(self) -> None:
        result = subprocess.run(
            ["python3", str(CHECKER), "--unknown"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments: --unknown", result.stderr)


if __name__ == "__main__":
    unittest.main()
