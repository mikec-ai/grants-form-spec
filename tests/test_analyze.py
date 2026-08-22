from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ANALYZER = ROOT / "scripts" / "analyze.py"


class AttachmentSemanticAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        result = subprocess.run(
            ["python3", str(ANALYZER), "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        cls.analysis = json.loads(result.stdout)

    def test_attachment_roles_are_distinct_semantic_questions(self) -> None:
        expected = {
            "project-narrative-attachments": "project/narrative",
            "budget-narrative-attachments": "budget/narrative",
            "other-narrative-attachments": "application/other-narrative",
        }
        for form_id, question_id in expected.items():
            with self.subTest(form=form_id):
                self.assertEqual(self.analysis["asks"][form_id], [question_id])
                self.assertEqual(
                    self.analysis["usesCaptureMechanisms"][form_id],
                    ["generics/attachment"],
                )

    def test_capture_mechanism_does_not_inflate_semantic_similarity(self) -> None:
        attachment_forms = {
            "project-narrative-attachments",
            "budget-narrative-attachments",
            "other-narrative-attachments",
        }
        rows = [
            row
            for row in self.analysis["pairwise"]
            if {row["formA"], row["formB"]}.issubset(attachment_forms)
        ]
        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertEqual(row["questionsInCommon"], 0)
            self.assertEqual(row["similarity"], 0.0)

    def test_associations_preserve_role_path_and_composition(self) -> None:
        semantic = [
            row
            for row in self.analysis["formQuestionAssociations"]
            if row["formId"] == "project-narrative-attachments"
        ]
        mechanism = [
            row
            for row in self.analysis["formCaptureMechanisms"]
            if row["formId"] == "project-narrative-attachments"
        ]
        self.assertEqual(
            semantic,
            [{
                "formId": "project-narrative-attachments",
                "questionId": "project/narrative",
                "path": "/attachments/[]",
                "relationship": "direct",
            }],
        )
        self.assertEqual(
            mechanism,
            [{
                "formId": "project-narrative-attachments",
                "mechanismId": "generics/attachment",
                "path": "/attachments/[]",
                "relationship": "transitive",
            }],
        )

    def test_unknown_flag_is_an_actionable_usage_error(self) -> None:
        result = subprocess.run(
            ["python3", str(ANALYZER), "--wat"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments: --wat", result.stderr)

    def test_rr_subaward_budget_reuses_every_rr_budget_question(self) -> None:
        budget = set(self.analysis["asks"]["rr-budget"])
        subaward = set(self.analysis["asks"]["rr-subaward-budget"])
        self.assertTrue(budget)
        self.assertLessEqual(budget, subaward)
        self.assertEqual(subaward - budget, {"budget/research/details"})

        row = next(
            row
            for row in self.analysis["pairwise"]
            if {row["formA"], row["formB"]} == {"rr-budget", "rr-subaward-budget"}
        )
        self.assertEqual(row["questionsInCommon"], len(budget))
        budget_share = row["shareOfA"] if row["formA"] == "rr-budget" else row["shareOfB"]
        self.assertEqual(budget_share, 1.0)


if __name__ == "__main__":
    unittest.main()
