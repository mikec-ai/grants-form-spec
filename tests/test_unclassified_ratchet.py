from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "scripts" / "check_unclassified_baseline.py"


class UnclassifiedFieldRatchetTests(unittest.TestCase):
    def run_check(self, current: list[str], initial: list[str], resolved: list[str] | None = None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis = root / "analysis.json"
            baseline = root / "baseline.json"
            analysis.write_text(json.dumps({
                "unclassifiedFormFields": [
                    {
                        "formId": identity.split(":", 1)[0],
                        "fieldPath": identity.split(":", 1)[1],
                    }
                    for identity in current
                ]
            }))
            baseline.write_text(json.dumps({
                "version": 1,
                "sourceBaseline": {
                    "lineageAdjustedOccurrenceCount": len(initial),
                },
                "initial": initial,
                "resolved": resolved or [],
            }))
            return subprocess.run(
                [
                    "python3",
                    str(CHECKER),
                    "--analysis",
                    str(analysis),
                    "--baseline",
                    str(baseline),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

    def test_accepts_the_exact_remaining_baseline(self) -> None:
        result = self.run_check(["form:/known"], ["form:/known"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("remaining: 1", result.stdout)

    def test_rejects_a_new_unclassified_occurrence(self) -> None:
        result = self.run_check(
            ["form:/known", "new-form:/new-field"],
            ["form:/known"],
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("+ new-form:/new-field", result.stderr)

    def test_requires_removals_to_be_recorded(self) -> None:
        result = self.run_check([], ["form:/known"])
        self.assertEqual(result.returncode, 1)
        self.assertIn("- form:/known", result.stderr)

    def test_accepts_a_recorded_resolution_and_rejects_its_return(self) -> None:
        resolved = self.run_check([], ["form:/known"], ["form:/known"])
        self.assertEqual(resolved.returncode, 0, resolved.stderr)

        returned = self.run_check(
            ["form:/known"],
            ["form:/known"],
            ["form:/known"],
        )
        self.assertEqual(returned.returncode, 1)
        self.assertIn("! form:/known", returned.stderr)
