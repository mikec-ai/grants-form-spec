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


if __name__ == "__main__":
    unittest.main()
