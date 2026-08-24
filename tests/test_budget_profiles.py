from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "dist" / "forms"
QUESTIONS = ROOT / "dist" / "question-bank"


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

    def test_ten_year_thirty_subaward_profile_combines_existing_parameters(self) -> None:
        ten_year = json.loads(
            (FORMS / "rr-subaward-budget-10yr-30" / "schema.json").read_text()
        )
        budgets = ten_year["properties"]["budgetAttachments"]
        self.assertEqual(budgets["maxItems"], 30)
        self.assertEqual(
            budgets["items"]["$ref"],
            "../../question-bank/budget/research/details-10yr/schema.json",
        )
        self.assertNotIn("$defs", ten_year)
        details = json.loads(
            (QUESTIONS / "budget/research/details-10yr/schema.json").read_text()
        )
        self.assertEqual(
            details["properties"]["budgetYear"]["maxItems"],
            10,
        )
        self.assertNotIn("allOf", details)

    def test_duration_profiles_share_source_without_intersecting_cardinality(self) -> None:
        source = (ROOT / "specs/question-bank/research-budget/index.tsp").read_text()
        five_year_form = (ROOT / "specs/forms/rr-budget.tsp").read_text()
        ten_year_form = (ROOT / "specs/forms/rr-budget-10yr.tsp").read_text()

        self.assertIn("...ResearchBudgetOverview;", source)
        self.assertIn("...ResearchBudgetDetails;", five_year_form)
        self.assertIn("...ResearchBudget10YrDetails;", ten_year_form)
        self.assertNotIn("extends ResearchBudgetDetails", source)

    def test_family_profiles_inherit_exact_f770_behavior_provenance(self) -> None:
        root_evidence = json.loads((FORMS / "rr-budget" / "evidence.json").read_text())
        root_paths = {
            record["canonicalPath"]
            for record in root_evidence["behaviorEvidence"]
            if record["authority"] == "official_source"
        }
        for form_id in (
            "rr-budget",
            "rr-budget-10yr",
            "rr-subaward-budget",
            "rr-subaward-budget-30",
            "rr-subaward-budget-10yr-30",
        ):
            with self.subTest(form_id=form_id):
                evidence = json.loads((FORMS / form_id / "evidence.json").read_text())
                dat = next(
                    source
                    for source in evidence["sources"]
                    if source["id"] == "grantsgov-rr-budget-dat-3.0-f770"
                )
                self.assertEqual(
                    dat["sha256"],
                    "c85158ce7ddcc756d6e8a55a050e00b4a95cdfc8d9a2d91b7bd94c7f8bdb1035",
                )
                self.assertEqual(len(evidence["behaviorEvidence"]), 70)
                self.assertEqual(
                    {
                        record["sourceId"]
                        for record in evidence["behaviorEvidence"]
                        if record["authority"] == "official_source"
                    },
                    {"grantsgov-rr-budget-dat-3.0-f770"},
                )
                self.assertEqual(
                    evidence["semanticReview"], {"status": "unreviewed", "mappings": []}
                )
                if form_id != "rr-budget":
                    self.assertEqual(
                        {record["inheritedFrom"] for record in evidence["behaviorEvidence"]},
                        {"rr-budget"},
                    )
                prefix = (
                    "budgetAttachments[*]."
                    if form_id.startswith("rr-subaward-budget")
                    else ""
                )
                self.assertEqual(
                    {
                        record["canonicalPath"]
                        for record in evidence["behaviorEvidence"]
                        if record["authority"] == "official_source"
                    },
                    {f"{prefix}{path}" for path in root_paths},
                )
                if prefix:
                    self.assertTrue(
                        all(
                            not record["canonicalPath"].startswith("budgetYear[*]")
                            for record in evidence["behaviorEvidence"]
                        )
                    )

    def test_all_f770_conditions_are_compiled_without_semantic_acceptance(self) -> None:
        expected_condition = (
            'All instances (lines 8-17) descriptions are always active. Data entry is not '
            'sequential and users can fill data as needed. If data is entered in E-5-1 "Other" '
            'for Section E - Participant/Trainee Costs, a minimum of one row is required to be '
            'filled out from line item 8-17.'
        )
        for form_id in (
            "rr-budget",
            "rr-budget-10yr",
            "rr-subaward-budget",
            "rr-subaward-budget-30",
            "rr-subaward-budget-10yr-30",
        ):
            with self.subTest(form_id=form_id):
                evidence = json.loads((FORMS / form_id / "evidence.json").read_text())
                conditions = [
                    record
                    for record in evidence["behaviorEvidence"]
                    if record["ruleKind"] == "condition"
                ]
                self.assertEqual(len(conditions), 14)
                self.assertIn(expected_condition, {record["sourceRecord"] for record in conditions})
                self.assertEqual(
                    {record["sourcePath"] for record in conditions},
                    {"F-8-1", "A-2-1", "A-3-1", "C-2-0", "C-2-1"},
                )
                self.assertEqual({record["executionStatus"] for record in conditions}, {"compiled"})
                self.assertEqual(evidence["semanticReview"], {"status": "unreviewed", "mappings": []})


if __name__ == "__main__":
    unittest.main()
