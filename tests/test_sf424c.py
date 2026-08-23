from __future__ import annotations

import json
import re
import subprocess
import unittest
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
from typing import Any


ROOT = Path(__file__).parents[1]
FORM = ROOT / "dist/forms/sf424c"
ROW_NAMES = [
    "administrativeAndLegalExpenses",
    "landStructuresRightsOfWay",
    "relocationExpenses",
    "architecturalEngineeringFees",
    "otherArchitecturalEngineeringFees",
    "projectInspectionFees",
    "siteWork",
    "demolitionAndRemoval",
    "construction",
    "equipment",
    "miscellaneous",
]


def leaves(node: dict[str, Any], path: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], dict[str, Any]]]:
    found: list[tuple[tuple[str, ...], dict[str, Any]]] = []
    for name, value in node.items():
        child_path = (*path, name)
        if isinstance(value, dict) and "gg_pre_population" in value:
            found.append((child_path, value["gg_pre_population"]))
        elif isinstance(value, dict):
            found.extend(leaves(value, child_path))
    return found


def get_at(response: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = response
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def set_at(response: dict[str, Any], path: tuple[str, ...], value: str) -> None:
    current = response
    for part in path[:-1]:
        current = current.setdefault(part, {})
    current[path[-1]] = value


def source_path(target: tuple[str, ...], source: str) -> tuple[str, ...]:
    if source.startswith("@THIS."):
        return (*target[:-1], *source.removeprefix("@THIS.").split("."))
    if source.startswith("@PARENT."):
        return (*target[:-2], *source.removeprefix("@PARENT.").split("."))
    return tuple(source.split("."))


def apply_rules(response: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(response)
    ordered = sorted(leaves(rules), key=lambda pair: (pair[1].get("order", 0), pair[0]))
    for target, rule in ordered:
        source_names = rule.get("fields") or [rule["amount"], rule["percentage"]]
        paths = [source_path(target, source) for source in source_names]
        values = [get_at(result, path) for path in paths]
        if rule.get("materialize") == "when_any_source_present" and all(value is None for value in values):
            continue
        numbers = [Decimal(str(value or 0)) for value in values]
        if rule["rule"] == "sum_monetary":
            value = sum(numbers, Decimal(0))
        elif rule["rule"] == "subtract_monetary":
            value = numbers[0] - numbers[1]
        elif rule["rule"] == "multiply_by_percentage":
            value = numbers[0] * numbers[1] / Decimal(100)
        else:
            raise AssertionError(f"unsupported test rule {rule['rule']}")
        set_at(result, target, f"{value:.2f}")
    return result


class SF424CTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads((FORM / "schema.json").read_text())
        cls.ui = json.loads((FORM / "sgg/ui-schema.json").read_text())
        cls.rules = json.loads((FORM / "sgg/rule-schema.json").read_text())
        cls.evidence = json.loads((FORM / "evidence.json").read_text())

    def test_metadata_and_source_wire_constraints_are_exact(self) -> None:
        manifest = json.loads((FORM / "manifest.json").read_text())
        self.assertEqual(
            manifest["form"],
            {
                "id": "sf424c",
                "legacyFormId": 408,
                "formName": "Budget Information for Construction Programs (SF-424C)",
                "shortFormName": "SF424C",
                "formVersion": "2.0",
                "agencyCode": "SGG",
                "ombNumber": "4040-0008",
            },
        )
        amount = json.loads(
            (ROOT / "dist/question-bank/budget/construction/administration-and-legal-expenses/schema.json").read_text()
        )["$defs"]["ConstructionEnteredAmount"]
        self.assertEqual(amount["pattern"], r"^\d{1,10}(?:[.]\d{2})?$")
        self.assertIsNotNone(re.fullmatch(amount["pattern"], "9999999999.99"))
        self.assertIsNone(re.fullmatch(amount["pattern"], "-1.00"))
        percentage = json.loads(
            (ROOT / "dist/question-bank/budget/construction/federal-share-percentage/schema.json").read_text()
        )
        self.assertEqual((percentage["minimum"], percentage["maximum"]), (0, 100))

    def test_form_composes_distinct_semantic_cost_questions(self) -> None:
        budget = self.schema["$defs"]["ConstructionBudgetInformation"]["properties"]
        refs = {name: node["$ref"] for name, node in budget.items()}
        self.assertEqual(len(budget), 16)
        self.assertEqual(len({refs[name] for name in ROW_NAMES}), 11)
        self.assertIn("administration-and-legal-expenses", refs[ROW_NAMES[0]])
        self.assertIn("other-architectural-engineering-fees", refs[ROW_NAMES[4]])
        self.assertNotEqual(refs["construction"], refs["equipment"])

    def test_ui_preserves_table_and_read_only_federal_outputs(self) -> None:
        budget, federal = self.ui
        self.assertEqual(budget["children"][0]["widget"], "Table")
        self.assertEqual(
            [child["type"] for child in federal["children"]],
            ["null", "field", "null"],
        )
        federal_schema = self.schema["properties"]["federalFunding"]["properties"]
        self.assertTrue(federal_schema["totalProjectCosts"]["readOnly"])
        self.assertTrue(federal_schema["federalFundingShare"]["readOnly"])

    def test_calculation_graph_matches_the_source_bound_oracle(self) -> None:
        rules = leaves(self.rules)
        self.assertEqual(len(rules), 24)
        self.assertTrue(
            all(rule["materialize"] == "when_any_source_present" for _, rule in rules)
        )
        response = {
            "budgetInformation": {
                **{name: {"totalCost": "100000.00", "nonAllowableCost": "10000.00"} for name in ROW_NAMES},
                "contingencies": {"totalCost": "55000.00", "nonAllowableCost": "5000.00"},
                "programIncome": {"totalCost": "10000.00", "nonAllowableCost": "0.00"},
            },
            "federalFunding": {"federalPercentageShare": 80},
        }
        actual = apply_rules(response, self.rules)
        budget = actual["budgetInformation"]
        self.assertEqual(
            budget["subtotalBeforeContingencies"],
            {"totalCost": "1100000.00", "nonAllowableCost": "110000.00", "totalAllowableCost": "990000.00"},
        )
        self.assertEqual(
            budget["subtotalAfterContingencies"],
            {"totalCost": "1155000.00", "nonAllowableCost": "115000.00", "totalAllowableCost": "1040000.00"},
        )
        self.assertEqual(
            budget["totalProjectCosts"],
            {"totalCost": "1145000.00", "nonAllowableCost": "115000.00", "totalAllowableCost": "1030000.00"},
        )
        self.assertEqual(
            actual["federalFunding"],
            {"totalProjectCosts": "1030000.00", "federalPercentageShare": 80, "federalFundingShare": "824000.00"},
        )

    def test_empty_draft_does_not_materialize_phantom_zeroes(self) -> None:
        self.assertEqual(apply_rules({}, self.rules), {})

    def test_provenance_is_pinned_and_semantics_remain_unpublished(self) -> None:
        sources = {source["type"]: source for source in self.evidence["sources"]}
        self.assertEqual(sources["xsd"]["sha256"], "a3ec5d6bae8173fce080709a8071787293dbe6271415d905d230c584c200982a")
        self.assertEqual(sources["dat"]["sha256"], "ea1b09223ab556110579bbdbf285195459824f765b6c928822fe6c1cd8f445e1")
        self.assertEqual(sources["implementation"]["sha256"], "4cbb1ba9b2241e81bf8d6bb2f90d7772d1d1de42703dae611385aa7dcba54c2e")
        self.assertEqual(len(self.evidence["behaviorEvidence"]), 24)
        rule_targets = {".".join(path) for path, _ in leaves(self.rules)}
        evidence_targets = {
            item["canonicalPath"] for item in self.evidence["behaviorEvidence"]
        }
        official_source_ids = {
            source["id"]
            for source in self.evidence["sources"]
            if source["type"] != "implementation"
        }
        self.assertEqual(evidence_targets, rule_targets)
        self.assertTrue(
            all(
                item["sourceId"] in official_source_ids
                for item in self.evidence["behaviorEvidence"]
            )
        )
        self.assertTrue(
            all(
                item["sourceId"] != "sgg-sf424c-oracle-f6affacd"
                for item in self.evidence["behaviorEvidence"]
            )
        )
        self.assertIn("federalFunding.totalProjectCosts", evidence_targets)
        self.assertNotIn("federalFunding.federalPercentageShare", evidence_targets)
        review = self.evidence["semanticReview"]
        self.assertEqual(review["status"], "proposed")
        self.assertEqual(len(review["mappings"]), 18)
        self.assertTrue(all(item["status"] == "proposed" for item in review["mappings"]))
        self.assertTrue(all("reviewedBy" not in item for item in review["mappings"]))

        result = subprocess.run(
            ["python3", str(ROOT / "scripts/analyze.py"), "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        analysis = json.loads(result.stdout)
        rows = [row for row in analysis["formQuestionWorkbook"] if row["formId"] == "sf424c"]
        self.assertEqual(len(rows), 18)
        self.assertTrue(all(row["mappingStatus"] == "proposed" for row in rows))
        self.assertTrue(all(not row["publishable"] for row in rows))
        self.assertEqual(analysis["reviewedAsks"]["sf424c"], [])


if __name__ == "__main__":
    unittest.main()
