from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FORM = ROOT / "dist/forms/phs398-cover-page-supplement"
BANK = ROOT / "dist/question-bank/hhs-research-policy"


def load(path: Path) -> object:
    return json.loads(path.read_text())


class PHS398CoverPageSupplementTests(unittest.TestCase):
    def test_identity_and_exact_applicant_constraints(self) -> None:
        manifest = load(FORM / "manifest.json")
        schema = load(FORM / "schema.json")
        self.assertEqual(manifest["form"]["legacyFormId"], 698)
        self.assertEqual(manifest["form"]["formVersion"], "5.0")
        self.assertEqual(manifest["form"]["shortFormName"], "PHS398_CoverPageSupplement_5_0")
        self.assertEqual(
            schema["required"],
            ["programIncome", "humanEmbryonicStemCells", "humanFetalTissue"],
        )
        income = load(BANK / "program-income/schema.json")
        self.assertEqual(income["properties"]["periods"]["minItems"], 1)
        self.assertEqual(income["properties"]["periods"]["maxItems"], 10)
        row = income["$defs"]["ProgramIncomePeriod"]
        self.assertEqual(row["required"], ["budgetPeriod", "anticipatedAmount", "source"])
        self.assertEqual(row["properties"]["source"]["minLength"], 1)
        stem = load(BANK / "human-embryonic-stem-cells/schema.json")
        lines = stem["properties"]["cellLines"]
        self.assertEqual(lines["maxItems"], 200)
        line_type = stem["$defs"][lines["items"]["$ref"].rsplit("/", 1)[-1]]
        self.assertEqual(line_type["pattern"], "^[0-9]{4}$")

    def test_semantic_questions_reuse_shapes_without_conflating_roles(self) -> None:
        index = load(FORM / "index.json")
        occurrences = {row["path"]: row for row in index["fieldOccurrences"]}
        former = occurrences["/formerProjectDirector/firstName"]["blockIds"]
        self.assertEqual(
            former,
            [
                "generics/person-name",
                "hhs-research-policy/former-project-director-principal-investigator",
            ],
        )
        self.assertEqual(
            occurrences["/formerOrganizationName"]["blockIds"],
            [
                "generics/organization-name",
                "hhs-research-policy/former-recipient-organization-name",
            ],
        )
        assurance = occurrences["/humanFetalTissue/complianceAssurance"]["blockIds"]
        consent = occurrences["/humanFetalTissue/irbConsentForm"]["blockIds"]
        self.assertIn("generics/attachment", assurance)
        self.assertIn("generics/attachment", consent)
        self.assertNotEqual(set(assurance), set(consent))
        self.assertTrue(all(row["responseRole"] == "applicantInput" for row in occurrences.values()))

    def test_all_24_dat_conditions_are_preserved_and_zero_calculations_claimed(self) -> None:
        evidence = load(FORM / "evidence.json")
        behaviors = evidence["behaviorEvidence"]
        dat_behaviors = [row for row in behaviors if row.get("sourceId") == "phs398-cover-dat-f698"]
        self.assertEqual(len(dat_behaviors), 24)
        self.assertTrue(all(row["ruleKind"] == "condition" for row in behaviors))
        self.assertEqual(
            {row["sourcePath"] for row in dat_behaviors},
            {
                "A-2-1", "A-3-1", "B-1-1", "B-2-1", "B-2-2", "B-2-3",
                "B-2-4", "B-2-5", "C-3-0", "C-3-2", "C-3-3", "C-3-4",
                "D-2-1", "D-2-2", "E-1-1", "E-2-1", "F-1-1", "F-1-3",
                "F-1-4", "F-1-5", "F-1-6", "F-1-7", "F-2-1", "F-2-2",
            },
        )
        unresolved = [row for row in behaviors if row["executionStatus"] == "source-bound-uncompiled"]
        self.assertGreaterEqual(len(unresolved), 8)
        self.assertIn("/inventionsAndPatents/inventions", {row["canonicalPath"] for row in unresolved})
        self.assertEqual(len([row for row in behaviors if row.get("sourceId") == "nih-forms-i-general-guide"]), 6)
        rules = load(FORM / "sgg/rule-schema.json")
        self.assertNotIn("gg_calculation", json.dumps(rules))

    def test_form_scoped_identity_conditions_are_portable_and_preserved_by_sgg(self) -> None:
        def controlled_rules(value: object) -> dict[str, dict[str, object]]:
            found: dict[str, dict[str, object]] = {}
            if isinstance(value, dict):
                scope = value.get("scope")
                rule = value.get("rule")
                if isinstance(scope, str) and isinstance(rule, dict):
                    found[scope] = rule
                for child in value.values():
                    found.update(controlled_rules(child))
            elif isinstance(value, list):
                for child in value:
                    found.update(controlled_rules(child))
            return found

        expected = {
            "#/properties/formerProjectDirector/properties/prefix": "#/properties/changes/properties/changeOfProjectDirector",
            "#/properties/formerProjectDirector/properties/firstName": "#/properties/changes/properties/changeOfProjectDirector",
            "#/properties/formerProjectDirector/properties/middleName": "#/properties/changes/properties/changeOfProjectDirector",
            "#/properties/formerProjectDirector/properties/lastName": "#/properties/changes/properties/changeOfProjectDirector",
            "#/properties/formerProjectDirector/properties/suffix": "#/properties/changes/properties/changeOfProjectDirector",
            "#/properties/formerOrganizationName": "#/properties/changes/properties/changeOfRecipientOrganization",
        }
        portable = controlled_rules(load(FORM / "ui.json"))
        for target, source in expected.items():
            self.assertEqual(portable[target], {
                "effect": "ENABLE",
                "condition": {"scope": source, "schema": {"const": "Y: Yes"}},
            })

        sgg = load(FORM / "sgg/ui-schema.json")
        sgg_expected = {target.removeprefix("#"): source for target, source in expected.items()}
        sgg_fields: dict[str, dict[str, object]] = {}
        for section in sgg:
            for field in section["children"]:
                if field.get("definition") in sgg_expected:
                    sgg_fields[field["definition"]] = field
        self.assertEqual(set(sgg_fields), set(sgg_expected))
        for target, source in sgg_expected.items():
            self.assertEqual(sgg_fields[target]["conditional"]["when"], {
                "op": "equals",
                "ref": {"scope": "root", "pointer": source.replace("#/properties/", "/").replace("/properties/", "/")},
                "value": "Y: Yes",
            })

    def test_exact_sources_no_ocr_and_bounded_operational_gates(self) -> None:
        evidence = load(FORM / "evidence.json")
        sources = {row["id"]: row for row in evidence["sources"]}
        self.assertEqual(sources["phs398-cover-xsd-v5-0"]["sha256"], "ec538c9bb5fd233c36ac73ca567d31e60779ee3df2f3c7b456d9395b3ec2dc26")
        self.assertEqual(sources["phs398-cover-dat-f698"]["sha256"], "bd467aee5184e8d13eb5867ba12370e60c9a10765d42a728ee8c28ab784f66ab")
        self.assertEqual(sources["phs398-cover-readonly-pdf-v5-0"]["sha256"], "82f9827f440018a0d3cfee25ec9f9696063143a5c618fb2dafe778ac80f183e8")
        self.assertEqual(sources["phs398-cover-xfa-pdf-v5-0"]["sha256"], "16522671505d4c3b1b5a9cbdc5218ae47de39bd3055396ae72b5d820a87e44ae")
        audit = load(ROOT / "research/phs398-cover-page-supplement/source-audit.json")
        self.assertFalse(audit["method"]["ocrUsed"])
        self.assertEqual(audit["accessibilityBoundary"]["status"], "unresolved-human-consumer-gate")
        self.assertEqual(audit["privacyBoundary"]["status"], "unresolved-human-consumer-gate")
        self.assertIn("mutual exclusion", " ".join(audit["unresolvedBehavior"]))
        self.assertIn("does not claim complete PDF", audit["parityClaim"])

    def test_analysis_reports_proposed_reuse_only(self) -> None:
        result = subprocess.run(
            ["python3", "scripts/analyze.py", "--json"], cwd=ROOT,
            text=True, capture_output=True, check=True,
        )
        report = json.loads(result.stdout)
        asks = set(report["asks"]["phs398-cover-page-supplement"])
        self.assertIn("hhs-research-policy/program-income", asks)
        self.assertIn("hhs-research-policy/former-project-director-principal-investigator", asks)
        self.assertNotIn("generics/attachment", asks)
        self.assertEqual(
            set(report["usesCaptureMechanisms"]["phs398-cover-page-supplement"]),
            {"generics/attachment"},
        )
        self.assertEqual(load(FORM / "evidence.json")["semanticReview"]["status"], "proposed")


if __name__ == "__main__":
    unittest.main()
