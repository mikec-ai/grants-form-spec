from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "dist/forms"


def load(form_id: str, artifact: str) -> object:
    return json.loads((FORMS / form_id / artifact).read_text())


class RuleEvidenceCoverageTests(unittest.TestCase):
    def test_sf424c_calculations_are_exactly_official_source_bound(self) -> None:
        evidence = load("sf424c", "evidence.json")
        records = evidence["behaviorEvidence"]

        self.assertEqual(len(records), 24)
        self.assertEqual({record["ruleKind"] for record in records}, {"calculation"})
        self.assertEqual(
            {record["authority"] for record in records}, {"official_source"}
        )
        self.assertNotIn(
            "federalFunding.federalPercentageShare",
            {record["canonicalPath"] for record in records},
        )
        self.assertEqual(evidence["semanticReview"]["status"], "proposed")

    def test_budget_family_inherits_one_complete_explicit_disposition_set(self) -> None:
        expected_paths = {
            record["canonicalPath"]
            for record in load("rr-budget", "evidence.json")["behaviorEvidence"]
        }
        self.assertEqual(len(expected_paths), 70)

        for form_id in ("rr-budget", "rr-budget-10yr"):
            with self.subTest(form_id=form_id):
                evidence = load(form_id, "evidence.json")
                records = evidence["behaviorEvidence"]
                self.assertEqual(len(records), 70)
                self.assertEqual(
                    {record["canonicalPath"] for record in records},
                    expected_paths,
                )
                self.assertEqual(
                    sum(record["authority"] == "official_source" for record in records),
                    34,
                )
                self.assertEqual(
                    sum(record["authority"] == "unresolved" for record in records),
                    36,
                )
                self.assertEqual(
                    sum(
                        record["ruleKind"] == "condition"
                        and record["executionStatus"] == "compiled"
                        for record in records
                    ),
                    14,
                )
                self.assertEqual(
                    evidence["semanticReview"],
                    {
                        "status": "unreviewed",
                        "mappings": [],
                    },
                )

        subaward = load("rr-subaward-budget", "evidence.json")["behaviorEvidence"]
        self.assertEqual(len(subaward), 70)
        self.assertTrue(
            all(
                record["canonicalPath"].startswith("budgetAttachments[*].")
                for record in subaward
            )
        )

    def test_condition_heavy_form_separates_source_records_from_compiled_dispositions(
        self,
    ) -> None:
        evidence = load("rr-other-project-information", "evidence.json")
        records = evidence["behaviorEvidence"]
        official = [
            record for record in records if record["authority"] == "official_source"
        ]
        compiled = [
            record for record in records if record["executionStatus"] == "compiled"
        ]

        self.assertEqual(len(official), 24)
        self.assertTrue(
            all(
                record["executionStatus"] == "source-bound-uncompiled"
                for record in official
            )
        )
        self.assertEqual(len(compiled), 13)
        self.assertEqual({record["ruleKind"] for record in records}, {"condition"})
        self.assertEqual({record["authority"] for record in compiled}, {"unresolved"})
        self.assertTrue(all(record["owner"] for record in compiled))
        self.assertTrue(all(record["reason"] for record in compiled))
        self.assertTrue(all(record["removalCondition"] for record in compiled))
        self.assertEqual(
            evidence["semanticReview"],
            {
                "status": "unreviewed",
                "mappings": [],
            },
        )


if __name__ == "__main__":
    unittest.main()
