from __future__ import annotations

import json
import copy
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FORM = ROOT / "dist/forms/sbir-sttr-information"


def load(path: Path) -> object:
    return json.loads(path.read_text())


class SbirSttrInformationTests(unittest.TestCase):
    def test_identity_constraints_and_exact_vocabulary(self) -> None:
        manifest = load(FORM / "manifest.json")
        schema = load(FORM / "schema.json")
        self.assertEqual(manifest["form"]["legacyFormId"], 787)
        self.assertEqual(manifest["form"]["formVersion"], "3.0")
        self.assertEqual(manifest["form"]["shortFormName"], "SBIR_STTR_Information_3_0")
        sbc = load(ROOT / "dist/question-bank/sbir-sttr/sbc-control-id/schema.json")
        employees = load(ROOT / "dist/question-bank/sbir-sttr/anticipated-employee-count/schema.json")
        uei = load(ROOT / "dist/question-bank/sbir-sttr/nonprofit-research-partner-uei/schema.json")
        eligibility = load(ROOT / "dist/question-bank/sbir-sttr/small-business-eligibility-certification/schema.json")
        self.assertEqual(sbc["pattern"], "^[0-9]{9}$")
        self.assertEqual(employees["minimum"], 1)
        self.assertEqual(employees["maximum"], 999)
        self.assertEqual(uei["minLength"], 12)
        self.assertEqual(uei["maxLength"], 12)
        enum_ref = eligibility["properties"]["value"]["$ref"]
        self.assertEqual(eligibility["$defs"][enum_ref.rsplit("/", 1)[-1]]["enum"], ["Y: Yes", "N: No"])
        employee_index = load(ROOT / "dist/question-bank/sbir-sttr/anticipated-employee-count/index.json")
        taba_index = load(ROOT / "dist/question-bank/sbir-sttr/taba-funding-request/index.json")
        self.assertEqual(employee_index["tags"], ["count"])
        self.assertEqual(taba_index["tags"], ["details"])

    def test_twenty_seven_distinct_semantic_questions_and_only_attachment_capture_reuse(self) -> None:
        index = load(FORM / "index.json")
        block_ids = {
            block_id
            for row in index["fieldOccurrences"]
            for block_id in row["blockIds"]
            if block_id.startswith("sbir-sttr/")
        }
        self.assertEqual(len(block_ids), 27)
        self.assertNotIn("primary-org/uei", block_ids)
        occurrences = {row["path"]: row for row in index["fieldOccurrences"]}
        for path in [
            "/nonDomesticPerformanceExplanation",
            "/commercializationPlan",
            "/commercializationHistory",
        ]:
            self.assertIn("generics/attachment", occurrences[path]["blockIds"])
        self.assertEqual(
            occurrences["/nonprofitResearchPartnerUei"]["blockIds"],
            ["sbir-sttr/nonprofit-research-partner-uei"],
        )
        self.assertTrue(all(row["responseRole"] == "applicantInput" for row in occurrences.values()))

    def test_simple_conditions_compile_and_clear_remove_or_policy_rules_do_not(self) -> None:
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

        ui = controlled_rules(load(FORM / "ui.json"))
        expected = {
            "#/properties/otherAgency": {"scope": "#/properties/agency/properties/value", "schema": {"const": "Other"}},
            "#/properties/federalSubcontractorNames": {"scope": "#/properties/federalSubcontractsIncluded/properties/value", "schema": {"const": "Y: Yes"}},
            "#/properties/nonDomesticPerformanceExplanation": {"scope": "#/properties/domesticPerformance/properties/value", "schema": {"const": "N: No"}},
            "#/properties/equivalentWorkFederalAgencies": {"scope": "#/properties/equivalentFederalWork/properties/value", "schema": {"const": "Y: Yes"}},
            "#/properties/phaseIIAwardsReceived/properties/value": {"scope": "#/properties/programType/properties/value", "schema": {"enum": ["SBIR", "Both"]}},
            "#/properties/commercializationHistory": {"scope": "#/properties/phaseIIAwardsReceived/properties/value", "schema": {"const": "Y: Yes"}},
            "#/properties/pdpiPrimaryEmployment/properties/value": {"scope": "#/properties/programType/properties/value", "schema": {"enum": ["SBIR", "Both"]}},
            "#/properties/pdpiAppointmentAndEffort/properties/value": {"scope": "#/properties/programType/properties/value", "schema": {"enum": ["STTR", "Both"]}},
            "#/properties/jointPerformancePercentage/properties/value": {"scope": "#/properties/programType/properties/value", "schema": {"enum": ["STTR", "Both"]}},
            "#/properties/nonprofitResearchPartnerUei": {"scope": "#/properties/programType/properties/value", "schema": {"enum": ["STTR", "Both"]}},
        }
        self.assertEqual(set(ui), set(expected))
        for target, condition in expected.items():
            self.assertEqual(ui[target], {"effect": "ENABLE", "condition": condition})
        evidence = load(FORM / "evidence.json")
        self.assertEqual(len(evidence["behaviorEvidence"]), 16)
        self.assertEqual(
            len([row for row in evidence["behaviorEvidence"] if row["executionStatus"] == "compiled"]),
            10,
        )
        unresolved = [row for row in evidence["behaviorEvidence"] if row["executionStatus"] == "source-bound-uncompiled"]
        self.assertEqual(
            {row["sourcePath"] for row in unresolved},
            {"A-6", "E-1", "F-02-1", "F-04-1", "F-05-1", "F-08-1"},
        )
        self.assertIn("commercializationPlan", " ".join(row["canonicalPath"] for row in unresolved))
        self.assertNotIn("gg_calculation", json.dumps(load(FORM / "sgg/rule-schema.json")))

    def test_all_eleven_required_condition_transitions_validate_canonical_payloads(self) -> None:
        full = {
            "agency": {"value": "Other"},
            "otherAgency": "NASA",
            "sbcControlId": "123456789",
            "programType": {"value": "Both"},
            "applicationType": {"value": "Fast-Track"},
            "phaseILetterOfIntentNumber": "LOI-123",
            "agencyTopicSubtopic": "TOPIC-1",
            "smallBusinessEligibility": {"value": "Y: Yes"},
            "numberOfEmployees": 12,
            "vcocOwnership": {"value": "N: No"},
            "facultyStudentOwnership": {"value": "N: No"},
            "federalSubcontractsIncluded": {"value": "Y: Yes"},
            "federalSubcontractorNames": "Federal Laboratory",
            "hubzoneLocation": {"value": "N: No"},
            "domesticPerformance": {"value": "N: No"},
            "nonDomesticPerformanceExplanation": "11111111-1111-4111-8111-111111111111",
            "equivalentFederalWork": {"value": "Y: Yes"},
            "equivalentWorkFederalAgencies": "DOE",
            "disclosurePermission": {"value": "N: No"},
            "tabaFundingRequest": {"value": "N: No"},
            "commercializationPlan": "22222222-2222-4222-8222-222222222222",
            "phaseIIAwardsReceived": {"value": "Y: Yes"},
            "commercializationHistory": "33333333-3333-4333-8333-333333333333",
            "pdpiPrimaryEmployment": {"value": "Y: Yes"},
            "pdpiAppointmentAndEffort": {"value": "Y: Yes"},
            "jointPerformancePercentage": {"value": "Y: Yes"},
            "nonprofitResearchPartnerUei": "ABCDEFGHIJKL",
        }
        transitions = [
            ("otherAgency", ("agency", "value"), "Other", "HHS"),
            ("agencyTopicSubtopic", ("agency", "value"), "DOE", "HHS"),
            ("federalSubcontractorNames", ("federalSubcontractsIncluded", "value"), "Y: Yes", "N: No"),
            ("nonDomesticPerformanceExplanation", ("domesticPerformance", "value"), "N: No", "Y: Yes"),
            ("equivalentWorkFederalAgencies", ("equivalentFederalWork", "value"), "Y: Yes", "N: No"),
            ("phaseIIAwardsReceived", ("programType", "value"), "SBIR", "STTR"),
            ("commercializationHistory", ("phaseIIAwardsReceived", "value"), "Y: Yes", "N: No"),
            ("pdpiPrimaryEmployment", ("programType", "value"), "SBIR", "STTR"),
            ("pdpiAppointmentAndEffort", ("programType", "value"), "STTR", "SBIR"),
            ("jointPerformancePercentage", ("programType", "value"), "STTR", "SBIR"),
            ("nonprofitResearchPartnerUei", ("programType", "value"), "STTR", "SBIR"),
        ]
        cases: list[dict[str, object]] = []
        for target, controller, required_value, optional_value in transitions:
            required_payload = copy.deepcopy(full)
            required_payload[controller[0]][controller[1]] = required_value
            del required_payload[target]
            cases.append({"name": f"{target}-required", "payload": required_payload, "valid": False})
            optional_payload = copy.deepcopy(full)
            optional_payload[controller[0]][controller[1]] = optional_value
            del optional_payload[target]
            cases.append({"name": f"{target}-optional", "payload": optional_payload, "valid": True})

        script = r"""
const fs = require('fs'); const path = require('path');
const Ajv = require('ajv/dist/2020'); const addFormats = require('ajv-formats');
function schemas(dir) { return fs.readdirSync(dir, {withFileTypes:true}).flatMap(
  entry => entry.isDirectory() ? schemas(path.join(dir, entry.name)) : (entry.name === 'schema.json' ? [path.join(dir, entry.name)] : [])
); }
const root = process.argv[1]; const ajv = new Ajv({strict:false, allErrors:true}); addFormats(ajv);
for (const file of schemas(path.join(root, 'dist/question-bank'))) {
  const schema = JSON.parse(fs.readFileSync(file));
  ajv.addSchema(schema, '/' + path.relative(path.join(root, 'dist'), file));
}
const validate = ajv.compile(JSON.parse(fs.readFileSync(path.join(root, 'dist/forms/sbir-sttr-information/schema.json'))));
for (const test of JSON.parse(process.argv[2])) {
  const actual = validate(test.payload);
  if (actual !== test.valid) {
    console.error(JSON.stringify({name:test.name, expected:test.valid, actual, errors:validate.errors})); process.exit(1);
  }
}
"""
        subprocess.run(
            ["node", "-e", script, str(ROOT), json.dumps(cases)], cwd=ROOT,
            text=True, capture_output=True, check=True,
        )

    def test_exact_sources_no_ocr_and_all_human_gates_remain_open(self) -> None:
        evidence = load(FORM / "evidence.json")
        sources = {row["id"]: row for row in evidence["sources"]}
        self.assertEqual(sources["sbir-sttr-xsd-v3-0"]["sha256"], "32ed46a450c1b77d9ef64ebf2a4086ab90b076aa2d3cdfedfab8c00324adcebf")
        self.assertEqual(sources["sbir-sttr-dat-f787"]["sha256"], "c0e8d91e583b9f7e6339cc6239f1e4d51e9d93299b893b34efd1bbbc435c6e9b")
        self.assertEqual(sources["sbir-sttr-grants-gov-xfa-pdf-v3-0"]["sha256"], "bd36dbc83d8fcfcd309cd45236d496a5f34f1401b4cf51d5aaeac2f22e45ce1e")
        audit = load(ROOT / "research/sbir-sttr-information/source-audit.json")
        self.assertFalse(audit["method"]["ocrUsed"])
        self.assertEqual(audit["inventory"]["xsdApplicantQuestions"], 27)
        self.assertEqual(audit["inventory"]["calculations"], 0)
        self.assertEqual(audit["executionPartitions"]["portableJsonSchema"]["compiledConditionalRequiredTargets"], 11)
        self.assertEqual(audit["executionPartitions"]["consumerConditionProjection"]["compiledEnablementTargets"], 10)
        self.assertEqual(audit["privacySecurityBoundary"]["status"], "unresolved-human-consumer-gate")
        self.assertEqual(audit["accessibilityBoundary"]["status"], "unresolved-human-consumer-gate")
        self.assertEqual(audit["releaseBoundary"]["status"], "unresolved-human-release-gate")

    def test_all_twenty_seven_semantic_identities_have_direct_proposed_source_mappings(self) -> None:
        evidence = load(FORM / "evidence.json")
        mappings = evidence["semanticReview"]["mappings"]
        self.assertEqual(len(mappings), 27)
        self.assertEqual(len({row["canonicalPointer"] for row in mappings}), 27)
        self.assertEqual(len({row["sourcePath"] for row in mappings}), 27)
        self.assertEqual({row["sourceId"] for row in mappings}, {"sbir-sttr-xsd-v3-0"})
        self.assertEqual({row["status"] for row in mappings}, {"proposed"})
        self.assertEqual(
            {row["canonicalPointer"] for row in mappings},
            {f"#/properties/{name}" for name in load(FORM / "schema.json")["properties"]},
        )

    def test_analysis_reports_proposed_semantics_and_capture_mechanism_separately(self) -> None:
        result = subprocess.run(
            ["python3", "scripts/analyze.py", "--json"], cwd=ROOT,
            text=True, capture_output=True, check=True,
        )
        report = json.loads(result.stdout)
        asks = set(report["asks"]["sbir-sttr-information"])
        self.assertEqual(len([item for item in asks if item.startswith("sbir-sttr/")]), 27)
        self.assertNotIn("generics/attachment", asks)
        self.assertEqual(
            set(report["usesCaptureMechanisms"]["sbir-sttr-information"]),
            {"generics/attachment"},
        )
        self.assertEqual(load(FORM / "evidence.json")["semanticReview"]["status"], "proposed")


if __name__ == "__main__":
    unittest.main()
