from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FORM = ROOT / "dist/forms/rr-personal-data"
PD_BANK = ROOT / "dist/question-bank/personal-data/project-director"
CO_PD_BANK = ROOT / "dist/question-bank/personal-data/co-project-director"


def load(path: Path) -> object:
    return json.loads(path.read_text())


class RRPersonalDataTests(unittest.TestCase):
    def test_identity_requiredness_and_collection_bounds(self) -> None:
        manifest = load(FORM / "manifest.json")
        schema = load(FORM / "schema.json")
        self.assertEqual(manifest["form"]["legacyFormId"], 357)
        self.assertEqual(manifest["form"]["formVersion"], "1.2")
        self.assertEqual(manifest["form"]["shortFormName"], "RR_PersonalData_1_2")
        self.assertEqual(manifest["form"]["ombNumber"], "4040-0001")
        self.assertEqual(schema["required"], ["projectDirector"])
        self.assertEqual(schema["properties"]["coProjectDirectors"]["maxItems"], 4)

        for bank in (PD_BANK, CO_PD_BANK):
            director = load(bank / "schema.json")
            self.assertEqual(director["required"], ["name"])
            self.assertEqual(director["properties"]["race"]["maxItems"], 5)
            self.assertEqual(director["properties"]["disabilityStatus"]["maxItems"], 4)

    def test_exact_wire_vocabularies_are_canonical_constraints(self) -> None:
        schema = load(PD_BANK / "schema.json")
        defs = schema["$defs"]
        self.assertEqual(defs["PersonalDataSex"]["enum"], ["Male", "Female", "Do Not Wish to Provide"])
        self.assertEqual(defs["PersonalDataRace"]["enum"], [
            "American Indian or Alaska Native", "Asian", "Black or African American",
            "Native Hawaiian or Other Pacific Islander", "White", "Do Not Wish to Provide",
        ])
        self.assertEqual(defs["PersonalDataEthnicity"]["enum"], [
            "Hispanic or Latino", "Non-Hispanic or Latino", "Do Not Wish to Provide",
        ])
        self.assertEqual(defs["PersonalDataDisabilityStatus"]["enum"], [
            "Hearing", "Visual", "Mobility/Orthopedic Impairment", "Other", "None",
            "Do Not Wish to Provide",
        ])
        self.assertEqual(defs["PersonalDataCitizenship"]["enum"], [
            "US Citizen", "Permanent Resident", "Other non-US Citizen", "Do Not Wish to Provide",
        ])

    def test_role_qualified_questions_share_name_capture_without_semantic_conflation(self) -> None:
        index = load(FORM / "index.json")
        occurrences = {row["path"]: row for row in index["fieldOccurrences"]}
        self.assertEqual(occurrences["/projectDirector/sex"]["blockIds"], ["personal-data/project-director"])
        self.assertEqual(
            occurrences["/coProjectDirectors/[]/sex"]["blockIds"],
            ["personal-data/co-project-director"],
        )
        self.assertEqual(
            occurrences["/projectDirector/name/firstName"]["blockIds"],
            ["generics/person-name", "personal-data/project-director"],
        )
        self.assertEqual(
            occurrences["/coProjectDirectors/[]/name/firstName"]["blockIds"],
            ["generics/person-name", "personal-data/co-project-director"],
        )
        self.assertNotEqual(
            set(occurrences["/projectDirector/sex"]["blockIds"]),
            set(occurrences["/coProjectDirectors/[]/sex"]["blockIds"]),
        )
        self.assertTrue(all(row["responseRole"] == "applicantInput" for row in occurrences.values()))

    def test_sgg_projection_preserves_widgets_notice_and_repeat_validation(self) -> None:
        sections = load(FORM / "sgg/ui-schema.json")
        pd_section, co_section = sections
        self.assertIn("voluntary", pd_section["description"])
        self.assertIn("separated from the application", pd_section["description"])
        pd_fields = {field["definition"]: field for field in pd_section["children"]}
        self.assertEqual(pd_fields["/properties/projectDirector/properties/sex"]["widget"], "Select")
        self.assertEqual(pd_fields["/properties/projectDirector/properties/race"]["widget"], "MultiSelect")
        self.assertEqual(pd_fields["/properties/projectDirector/properties/disabilityStatus"]["widget"], "MultiSelect")
        field_list = co_section["children"][0]
        self.assertEqual(field_list["type"], "fieldList")
        self.assertTrue(field_list["validateBeforeAdd"])
        co_fields = {field["definition"]: field for field in field_list["children"]}
        self.assertEqual(co_fields["/properties/coProjectDirectors/items/properties/race"]["widget"], "MultiSelect")
        self.assertEqual(co_fields["/properties/coProjectDirectors/items/properties/citizenship"]["widget"], "Select")

    def test_four_source_bound_exclusivity_rules_are_preserved_without_execution(self) -> None:
        evidence = load(FORM / "evidence.json")
        behaviors = evidence["behaviorEvidence"]
        self.assertEqual(len(behaviors), 4)
        self.assertEqual({row["ruleKind"] for row in behaviors}, {"condition"})
        self.assertEqual({row["authority"] for row in behaviors}, {"official_source"})
        self.assertEqual({row["executionStatus"] for row in behaviors}, {"source-bound-uncompiled"})
        self.assertEqual(
            {row["canonicalPath"] for row in behaviors},
            {
                "/projectDirector/race", "/projectDirector/disabilityStatus",
                "/coProjectDirectors/[]/race", "/coProjectDirectors/[]/disabilityStatus",
            },
        )
        audit = load(ROOT / "research/rr-personal-data/source-audit.json")
        behavior = audit["behaviorInventory"]
        self.assertEqual(behavior["privacyNotice"]["implementation"], "compiled into the portable section description")
        self.assertEqual(behavior["projectDirectorPrefill"]["implementation"], "source-bound-uncompiled")
        self.assertEqual(len(behavior["coProjectDirectorRepetition"]["sourceBehaviorKeys"]), 4)
        self.assertEqual(
            {row["canonicalPath"] for row in behavior["selectionConstraints"]},
            {
                "/projectDirector/race", "/projectDirector/disabilityStatus",
                "/coProjectDirectors/[]/race", "/coProjectDirectors/[]/disabilityStatus",
            },
        )
        self.assertTrue(all(row["implementation"] == "source-bound-uncompiled" for row in behavior["selectionConstraints"]))
        self.assertNotIn("gg_calculation", json.dumps(load(FORM / "sgg/rule-schema.json")))
        self.assertNotIn("conditional", json.dumps(load(FORM / "sgg/ui-schema.json")))

    def test_generic_name_accepts_source_valid_free_text_prefix_and_suffix(self) -> None:
        schema_path = ROOT / "dist/question-bank/generics/person-name/schema.json"
        payload = {"prefix": "Mx", "firstName": "Ada", "lastName": "Lovelace", "suffix": "III"}
        script = """
const fs = require('fs'); const Ajv = require('ajv/dist/2020');
const schema = JSON.parse(fs.readFileSync(process.argv[1], 'utf8'));
const payload = JSON.parse(process.argv[2]);
const validate = new Ajv({strict: false}).compile(schema);
if (!validate(payload)) { console.error(JSON.stringify(validate.errors)); process.exit(1); }
"""
        subprocess.run(
            ["node", "-e", script, str(schema_path), json.dumps(payload)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_exact_sources_no_ocr_and_bounded_operational_gates(self) -> None:
        evidence = load(FORM / "evidence.json")
        sources = {row["id"]: row for row in evidence["sources"]}
        self.assertEqual(sources["rr-personal-data-xsd-v1-2"]["sha256"], "5f766d46d573da1f6bb326bcbc13338439ba75399ad09dee2380f65e892402cb")
        self.assertEqual(sources["rr-personal-data-dat-f357"]["sha256"], "2c0eaf828c93162854bf1488e4687f0b1d85ab4d5b5ca7c922acdf87229ceaf7")
        self.assertEqual(sources["rr-personal-data-readonly-pdf-v1-2"]["sha256"], "51a52f3f8ee2528e26bbed64819d7992e4ff96645fe970676d12138aa7205417")
        self.assertEqual(sources["rr-personal-data-xfa-pdf-v1-2"]["sha256"], "2b95182ff1078f3f27c44025e9210755c6613aefa016811b69141fc04992f227")
        self.assertEqual(sources["universal-codes-xsd-v2-0"]["sha256"], "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a")
        audit = load(ROOT / "research/rr-personal-data/source-audit.json")
        self.assertFalse(audit["method"]["ocrUsed"])
        self.assertEqual(audit["inventory"]["xsdQuestionAndStructureRecords"], 25)
        self.assertEqual(audit["inventory"]["datRows"], 54)
        self.assertEqual(audit["inventory"]["calculations"], 0)
        self.assertEqual(audit["accessibilityBoundary"]["status"], "unresolved-human-consumer-gate")
        self.assertEqual(audit["privacyBoundary"]["status"], "unresolved-human-consumer-gate")
        self.assertIn("does not claim complete XFA", audit["parityClaim"])

    def test_analysis_reports_role_questions_and_capture_reuse(self) -> None:
        result = subprocess.run(
            ["python3", "scripts/analyze.py", "--json"], cwd=ROOT,
            text=True, capture_output=True, check=True,
        )
        report = json.loads(result.stdout)
        asks = set(report["asks"]["rr-personal-data"])
        self.assertEqual(
            asks,
            {"personal-data/project-director", "personal-data/co-project-director", "generics/person-name"},
        )
        self.assertEqual(report["usesCaptureMechanisms"]["rr-personal-data"], [])
        self.assertEqual(load(FORM / "evidence.json")["semanticReview"]["status"], "proposed")


if __name__ == "__main__":
    unittest.main()
