from __future__ import annotations

import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from conformance.grants_gov_xml import render_profile_xml


ROOT = Path(__file__).parents[1]


def load(path: Path) -> object:
    return json.loads(path.read_text())


def objects(value: object):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


class PHSAdditionalIndirectCostsTests(unittest.TestCase):
    def test_exact_xsd_and_dat_authorities_remain_pinned(self) -> None:
        evidence = load(
            ROOT / "evidence/forms/phs-additional-indirect-costs/evidence.json"
        )
        sources = {source["id"]: source for source in evidence["sources"]}
        self.assertEqual(
            sources["source-dat-b0d0411dbb97"]["sha256"],
            "b0d0411dbb9794ba031b45dfaa4a94f735aad42311409a77bf44a0810196d3dd",
        )
        self.assertEqual(
            sources["source-xsd-ba38a3500b02"]["sha256"],
            "ba38a3500b025b0414edbcdbffe80dc12165ceb7a7fb657012d450b2e9682b66",
        )
        self.assertEqual(evidence["semanticReview"], {"status": "unreviewed", "mappings": []})
        audit = load(ROOT / "research/phs-additional-indirect-costs/source-audit.json")
        self.assertEqual(audit["sources"]["pdf"]["reviewState"], "not_acquired")
        self.assertEqual(audit["sources"]["pdf"]["reviewedPages"], [])

    def test_form_compiles_nested_periods_calculations_and_attachment(self) -> None:
        root = ROOT / "dist/forms/phs-additional-indirect-costs"
        schema = load(root / "schema.json")
        ui = load(root / "sgg/ui-schema.json")
        rules = load(root / "sgg/rule-schema.json")
        fields = [row for row in objects(ui) if row.get("type") == "field"]
        lists = [row for row in objects(ui) if row.get("type") == "fieldList"]
        calculations = [
            row["gg_pre_population"]
            for row in objects(rules)
            if "gg_pre_population" in row
        ]

        self.assertEqual(schema["properties"]["budgetYears"]["minItems"], 1)
        self.assertEqual(schema["properties"]["budgetYears"]["maxItems"], 10)
        period = load(
            ROOT
            / "dist/question-bank/budget/additional-indirect-costs/period/schema.json"
        )
        indirect_costs = period["$defs"]["PHSAdditionalIndirectCostsForPeriod"]
        rows = indirect_costs["properties"]["indirectCost"]
        self.assertEqual(rows["minItems"], 1)
        self.assertEqual(rows["maxItems"], 4)
        self.assertEqual(len(lists), 2)
        self.assertEqual(len(calculations), 2)
        self.assertEqual(sorted(rule["order"] for rule in calculations), [1, 2])
        self.assertEqual(
            rules["budgetYears"]["indirectCosts"]["totalIndirectCosts"]
            ["gg_pre_population"]["fields"],
            ["@THIS.indirectCost[*].fundRequested"],
        )
        self.assertEqual(
            rules["budgetYears"]["budgetPeriodEndDate"]["gg_validation"],
            {"rule": "date_not_before", "fields": ["@THIS.budgetPeriodStartDate"]},
        )
        self.assertEqual(
            sum(
                row.get("gg_validation", {}).get("rule") == "attachment"
                for row in objects(rules)
            ),
            1,
        )
        calculated_definitions = {
            row["definition"]
            for row in fields
            if row["definition"].endswith(
                (
                    "/totalIndirectCosts",
                    "/cumulativeTotalFundsRequestedIndirectCost",
                )
            )
        }
        self.assertEqual(len(calculated_definitions), 2)

    def test_xml_projection_renders_all_budget_periods_and_cumulative_total(self) -> None:
        profile = load(
            ROOT
            / "dist/forms/phs-additional-indirect-costs/targets/grants-gov-xml.json"
        )
        response = {
            "budgetYears": [
                {
                    "budgetPeriodStartDate": "2026-01-01",
                    "budgetPeriodEndDate": "2026-12-31",
                    "indirectCosts": {
                        "indirectCost": [
                            {
                                "costType": "Modified Total Direct Costs",
                                "rate": "10.00",
                                "base": "1000.00",
                                "fundRequested": "100.00",
                            }
                        ],
                        "totalIndirectCosts": "100.00",
                    },
                },
                {
                    "budgetPeriodStartDate": "2027-01-01",
                    "budgetPeriodEndDate": "2027-12-31",
                    "indirectCosts": {
                        "indirectCost": [
                            {
                                "costType": "Salary and Wages",
                                "fundRequested": "200.00",
                            }
                        ],
                        "totalIndirectCosts": "200.00",
                    },
                },
            ],
            "budgetSummary": {
                "cumulativeTotalFundsRequestedIndirectCost": "300.00"
            },
        }
        root = ET.fromstring(render_profile_xml(profile, response))
        namespace = {"f": profile["namespaces"]["default"]}
        self.assertEqual(len(root.findall("f:BudgetYear", namespace)), 2)
        self.assertEqual(
            root.findtext(
                "f:BudgetSummary/f:CumulativeTotalFundsRequestedIndirectCost",
                namespaces=namespace,
            ),
            "300.00",
        )


if __name__ == "__main__":
    unittest.main()
