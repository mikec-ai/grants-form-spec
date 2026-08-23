from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "scripts" / "check_unclassified_baseline.py"
CANONICAL_BASELINE = json.loads(
    (ROOT / "analysis" / "unclassified-fields-baseline.v1.json").read_text()
)
INITIAL = CANONICAL_BASELINE["initial"]


class UnclassifiedFieldRatchetTests(unittest.TestCase):
    def run_check(
        self,
        current: list[str],
        resolved: list[str] | None = None,
        initial: list[str] | None = None,
    ):
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
            initial = INITIAL if initial is None else initial
            baseline.write_text(json.dumps({
                **CANONICAL_BASELINE,
                "sourceBaseline": {
                    **CANONICAL_BASELINE["sourceBaseline"],
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
        result = self.run_check(INITIAL)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"remaining: {len(INITIAL)}", result.stdout)

    def test_rejects_a_new_unclassified_occurrence(self) -> None:
        result = self.run_check(
            [*INITIAL, "new-form:/new-field"],
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("+ new-form:/new-field", result.stderr)

    def test_requires_removals_to_be_recorded(self) -> None:
        removed = INITIAL[0]
        result = self.run_check(INITIAL[1:])
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"- {removed}", result.stderr)

    def test_accepts_a_recorded_resolution_and_rejects_its_return(self) -> None:
        identity = INITIAL[0]
        resolved = self.run_check(INITIAL[1:], [identity])
        self.assertEqual(resolved.returncode, 0, resolved.stderr)

        returned = self.run_check(
            INITIAL,
            [identity],
        )
        self.assertEqual(returned.returncode, 1)
        self.assertIn(f"! {identity}", returned.stderr)

    def test_rejects_a_rewritten_initial_universe(self) -> None:
        rewritten = sorted([*INITIAL, "new-form:/new-field"])
        result = self.run_check(rewritten, initial=rewritten)
        self.assertEqual(result.returncode, 2)
        self.assertIn("pinned original universe", result.stderr)
