from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "dist" / "forms"


class ResearchBudgetProfileTests(unittest.TestCase):
    def test_ten_year_profile_changes_only_identity_copy_and_period_capacity(self) -> None:
        five_year = json.loads((FORMS / "rr-budget" / "schema.json").read_text())
        ten_year = json.loads((FORMS / "rr-budget-10yr" / "schema.json").read_text())

        normalized_ten_year = copy.deepcopy(ten_year)
        normalized_ten_year["$id"] = five_year["$id"]
        normalized_ten_year["description"] = five_year["description"]
        budget_year = normalized_ten_year["properties"]["budgetYear"]
        budget_year["description"] = five_year["properties"]["budgetYear"]["description"]
        budget_year["maxItems"] = 5

        self.assertEqual(normalized_ten_year, five_year)

    def test_thirty_subaward_profile_changes_only_identity_copy_and_capacity(self) -> None:
        ten_subawards = json.loads(
            (FORMS / "rr-subaward-budget" / "schema.json").read_text()
        )
        thirty_subawards = json.loads(
            (FORMS / "rr-subaward-budget-30" / "schema.json").read_text()
        )

        normalized_thirty = copy.deepcopy(thirty_subawards)
        normalized_thirty["$id"] = ten_subawards["$id"]
        normalized_thirty["description"] = ten_subawards["description"]
        budgets = normalized_thirty["properties"]["budgetAttachments"]
        budgets["description"] = ten_subawards["properties"]["budgetAttachments"]["description"]
        budgets["maxItems"] = 10

        self.assertEqual(normalized_thirty, ten_subawards)


if __name__ == "__main__":
    unittest.main()
