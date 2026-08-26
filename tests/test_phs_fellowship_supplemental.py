from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FORM = ROOT / "dist/forms/phs-fellowship-supplemental"


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


class PHSFellowshipSupplementalTests(unittest.TestCase):
    def test_source_set_is_pinned_without_accepting_semantic_mappings(self) -> None:
        evidence = load(ROOT / "evidence/forms/phs-fellowship-supplemental/evidence.json")
        sources = {source["id"]: source for source in evidence["sources"]}

        self.assertEqual(evidence["semanticReview"], {"status": "unreviewed", "mappings": []})
        self.assertEqual(
            sources["phs-fellowship-supplemental-xsd-v8-0"]["sha256"],
            "85f8e33df4641c56f3b6b96108690f89d214de8b5c864b1d6bd1e6bf8c7cc7bc",
        )
        self.assertEqual(
            sources["phs-fellowship-supplemental-dat-f836"]["sha256"],
            "fe9c42a0ec7008f6d9076e250bb37243629a71403331b69afcbf1069929f8beb",
        )
        self.assertEqual(
            evidence["extraction"]["sourceSetSha256"],
            "ced520509653ed07d7e572edd8d7678d15901ec5b912b3bec6978688c105677f",
        )
        nrsa_records = [
            record
            for record in evidence["behaviorEvidence"]
            if record["canonicalPath"].lstrip("/").replace("/", ".")
            == "candidateInformation.currentPriorNrsaSupport.records"
        ]
        self.assertEqual(
            [(record["sourcePath"], record["executionStatus"]) for record in nrsa_records],
            [
                ("G-5-01", "compiled"),
                ("G-5-02", "source-bound-uncompiled"),
            ],
        )

    def test_form_compiles_reusable_questions_and_source_cardinalities(self) -> None:
        schema = load(FORM / "schema.json")
        ui = load(FORM / "ui.json")
        sgg_ui = load(FORM / "sgg/ui-schema.json")
        rules = load(FORM / "sgg/rule-schema.json")

        self.assertEqual(schema["properties"]["appendix"]["maxItems"], 100)
        self.assertEqual(
            schema["$defs"]["FellowshipHumanEmbryonicStemCells"]
            ["properties"]["cellLines"]["maxItems"],
            20,
        )

        tuition = load(
            ROOT / "dist/question-bank/fellowship-budget/tuition/schema.json"
        )
        childcare = load(
            ROOT / "dist/question-bank/fellowship-budget/childcare/schema.json"
        )
        year_fields = {f"year{year}" for year in range(1, 7)}
        self.assertTrue(year_fields <= set(tuition["properties"]))
        self.assertTrue(year_fields <= set(childcare["properties"]))

        # Every primitive budget control needs an explicit declarative label.
        # The consumer uses these schema titles as the accessible names for
        # nested inputs; falling back to property-name inference would move a
        # form authoring decision into the adapter.
        expected_budget_labels = {
            "institutional-base-salary": {
                "amount": "Institutional Base Salary Amount",
                "academicPeriod": "Academic Period",
                "numberOfMonths": "Number of Months",
            },
            "federal-stipend": {
                "amount": "Federal Stipend Amount",
                "numberOfMonths": "Number of Months",
            },
            "supplementation": {
                "amount": "Supplementation Amount",
                "numberOfMonths": "Number of Months",
                "type": "Type of Supplementation",
                "source": "Source of Supplementation",
            },
        }
        for question_id, labels in expected_budget_labels.items():
            question = load(
                ROOT / f"dist/question-bank/fellowship-budget/{question_id}/schema.json"
            )
            self.assertEqual(
                {
                    field_name: question["properties"][field_name].get("title")
                    for field_name in labels
                },
                labels,
            )

        attachments = [
            row
            for row in objects(rules)
            if row.get("gg_validation", {}).get("rule") == "attachment"
        ]
        calculations = [
            row["gg_pre_population"]
            for row in objects(rules)
            if "gg_pre_population" in row
        ]
        self.assertEqual(len(attachments), 17)
        self.assertEqual(len(calculations), 2)
        self.assertTrue(
            all(rule["rule"] == "sum_monetary" for rule in calculations)
        )
        self.assertTrue(
            all(rule["materialize"] == "when_any_source_present" for rule in calculations)
        )

        json_forms_enabled = [
            row
            for row in objects(ui)
            if row.get("rule", {}).get("effect") == "ENABLE"
        ]
        self.assertEqual(len(json_forms_enabled), 18)
        conditional_fields = {
            row["definition"]: row["conditional"]
            for row in objects(sgg_ui)
            if row.get("type") == "field" and "conditional" in row
        }
        enabled_scopes = set(conditional_fields)
        self.assertIn(
            "/properties/vertebrateAnimalEuthanasia/properties/animalEuthanized",
            enabled_scopes,
        )
        self.assertNotIn(
            "/properties/humanEmbryonicStemCells/properties/cellLines",
            enabled_scopes,
        )
        for year in range(1, 7):
            self.assertIn(
                f"/properties/budget/properties/tuition/properties/year{year}",
                enabled_scopes,
            )
            self.assertIn(
                f"/properties/budget/properties/childcare/properties/year{year}",
                enabled_scopes,
            )

        # The DAT applies Other Degree Type to six specific enum values. A broad
        # present/non-empty approximation would change behavior, so it must stay open.
        self.assertNotIn(
            "/properties/candidateInformation/properties/graduateDegreeSought/"
            "properties/otherDegreeTypeText",
            enabled_scopes,
        )

    def test_form_manifest_identifies_the_active_grants_gov_version(self) -> None:
        manifest = load(FORM / "manifest.json")
        profile = load(FORM / "targets/grants-gov-xml.json")

        self.assertEqual(manifest["form"]["legacyFormId"], 836)
        self.assertEqual(manifest["form"]["formVersion"], "8.0")
        self.assertEqual(profile["root"]["attributes"], {"FormVersion": "8.0"})
        self.assertEqual(
            profile["xsd"]["sha256"],
            "85f8e33df4641c56f3b6b96108690f89d214de8b5c864b1d6bd1e6bf8c7cc7bc",
        )


if __name__ == "__main__":
    unittest.main()
