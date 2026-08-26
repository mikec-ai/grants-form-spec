from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FORM = ROOT / "dist/forms/phs-human-subjects"


def load(path: Path) -> object:
    return json.loads(path.read_text())


class PHSHumanSubjectsTests(unittest.TestCase):
    def test_identity_cardinality_and_system_owned_values(self) -> None:
        manifest = load(FORM / "manifest.json")
        overview = load(FORM / "schema.json")
        self.assertEqual(manifest["form"]["legacyFormId"], 705)
        self.assertEqual(manifest["form"]["formVersion"], "3.0")
        self.assertEqual(overview["properties"]["studies"]["maxItems"], 150)
        self.assertEqual(overview["properties"]["delayedOnsetStudies"]["maxItems"], 150)
        for name in (
            "involvesHumanSubjects",
            "exemptFromFederalRegulations",
            "exemptions",
        ):
            self.assertTrue(overview["properties"][name]["allOf"][0]["readOnly"])
        self.assertTrue(overview["properties"]["applicationId"]["readOnly"])

        ui = load(FORM / "sgg/ui-schema.json")
        overview_fields = {
            row["definition"]: row
            for row in ui[0]["children"]
        }
        for name in (
            "involvesHumanSubjects",
            "exemptFromFederalRegulations",
            "exemptions",
        ):
            self.assertEqual(overview_fields[f"/properties/{name}"]["type"], "field")

        def nodes(value: object) -> list[dict[str, object]]:
            if isinstance(value, dict):
                return [value, *[row for child in value.values() for row in nodes(child)]]
            if isinstance(value, list):
                return [row for child in value for row in nodes(child)]
            return []

        hidden = {
            str(row["definition"])
            for row in nodes(ui)
            if row.get("type") == "null" and "definition" in row
        }
        self.assertIn("/properties/applicationId", hidden)
        self.assertTrue(any(path.endswith("/properties/studyId") for path in hidden))
        self.assertTrue(any(path.endswith("/properties/reportId") for path in hidden))

    def test_applicant_labels_and_source_bound_top_level_conditions_are_projected(self) -> None:
        schema = load(FORM / "schema.json")
        self.assertEqual(
            schema["properties"]["involvesHumanSubjects"]["allOf"],
            [{
                "title": "Does the proposed project involve human subjects?",
                "readOnly": True,
            }],
        )
        self.assertEqual(
            schema["properties"]["exemptFromFederalRegulations"]["allOf"],
            [{
                "title": "Is the project exempt from federal regulations?",
                "readOnly": True,
            }],
        )
        self.assertEqual(
            schema["properties"]["exemptions"]["allOf"],
            [{"title": "Exemption Number(s)", "readOnly": True}],
        )
        self.assertEqual(
            schema["properties"]["involvesHumanSpecimensOrData"]["title"],
            "Does any proposed research involve human specimens and/or data?",
        )

        ui = load(FORM / "sgg/ui-schema.json")
        studies = ui[1]["children"][0]
        delayed = ui[2]["children"][0]
        self.assertEqual(studies["label"], "Human Subject Study")
        self.assertEqual(delayed["label"], "Delayed Onset Study")
        expected = {
            "when": {
                "op": "equals",
                "ref": {"scope": "root", "pointer": "/involvesHumanSubjects"},
                "value": "Y: Yes",
            },
            "then": {"interaction": "enabled"},
            "otherwise": {"interaction": "disabled"},
        }
        self.assertEqual(studies["conditional"], expected)
        self.assertEqual(delayed["conditional"], expected)

        nested = next(
            child
            for child in studies["children"]
            if child.get("name") == "inclusionEnrollmentReports"
        )
        self.assertEqual(nested["label"], "Inclusion Enrollment Report")

    def test_narrow_human_subject_determinations_are_reused_with_occurrence_roles(self) -> None:
        expected = {
            "involvesHumanSubjects": "research-project/human-subjects-indicator",
            "exemptFromFederalRegulations": "research-project/human-subjects-exemption-status",
            "exemptions": "research-project/human-subjects-exemption-numbers",
        }
        phs = load(FORM / "index.json")
        other = load(ROOT / "dist/forms/rr-other-project-information/index.json")
        for name, block_id in expected.items():
            phs_row = next(row for row in phs["fieldOccurrences"] if row["path"] == f"/{name}")
            self.assertIn(block_id, phs_row["blockIds"])
            self.assertEqual(phs_row["responseRole"], "systemValue")
            other_row = next(
                row
                for row in other["fieldOccurrences"]
                if row["path"] == f"/humanSubjects/{name}"
            )
            self.assertIn(block_id, other_row["blockIds"])

    def test_enrollment_is_one_semantic_composite_with_115_unique_coordinates(self) -> None:
        index = load(FORM / "index.json")
        coordinate_rows = [
            row
            for row in index["fieldOccurrences"]
            if row["leaf"]
            and "inclusionEnrollmentReports" in row["path"]
            and ("/planned/" in row["path"] or "/cumulativeActual/" in row["path"])
        ]
        self.assertEqual(len(coordinate_rows), 115)
        self.assertEqual(len({row["path"] for row in coordinate_rows}), 115)
        self.assertTrue(all(
            "clinical-study/inclusion-enrollment-report" in row["blockIds"]
            for row in coordinate_rows
        ))
        semantic_ids = {
            block_id
            for row in coordinate_rows
            for block_id in row["blockIds"]
            if block_id == "clinical-study/inclusion-enrollment-report"
        }
        self.assertEqual(semantic_ids, {"clinical-study/inclusion-enrollment-report"})

    def test_enrollment_ui_preserves_coordinate_paths_for_error_routing(self) -> None:
        ui = load(FORM / "sgg/ui-schema.json")
        fields: list[dict[str, object]] = []

        def walk(node: object) -> None:
            if isinstance(node, dict):
                if node.get("type") == "field" and "definition" in node:
                    fields.append(node)
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(ui)
        coordinates = [
            str(row["definition"])
            for row in fields
            if "inclusionEnrollmentReports" in str(row["definition"])
            and ("/planned/" in str(row["definition"]) or "/cumulativeActual/" in str(row["definition"]))
        ]
        self.assertEqual(len(coordinates), 115)
        self.assertEqual(len(set(coordinates)), 115)
        self.assertTrue(all("/properties/" in path for path in coordinates))
        self.assertTrue(any("/planned/" in path for path in coordinates))
        self.assertTrue(any("/cumulativeActual/" in path for path in coordinates))
        # Each control retains period, ethnicity, sex, and race in its pointer so a
        # generic renderer can route validation errors without a form branch. Rendering
        # accessible headers, keyboard navigation, and screen-reader context remains an
        # explicit consumer/human gate rather than a producer-side claim.
        sample = next(path for path in coordinates if path.endswith("/properties/asian"))
        self.assertIn("/planned/properties/notHispanicLatino/properties/female", sample)

    def test_total_like_coordinates_are_inputs_with_no_inferred_arithmetic(self) -> None:
        index = load(FORM / "index.json")
        rules = load(FORM / "sgg/rule-schema.json")
        coordinates = [
            row
            for row in index["fieldOccurrences"]
            if row["leaf"]
            and "inclusionEnrollmentReports" in row["path"]
            and ("/planned/" in row["path"] or "/cumulativeActual/" in row["path"])
        ]
        total_like = [
            row for row in coordinates
            if row["path"].endswith("/total") or "/total/" in row["path"]
        ]
        self.assertEqual(len(total_like), 28)
        self.assertEqual({row["responseRole"] for row in total_like}, {"applicantInput"})
        self.assertFalse(any("calculate" in value for value in rules.values()))

        # Deliberately inconsistent totals are valid under the pinned source schema shape.
        schema_path = ROOT / "dist/question-bank/clinical-study/inclusion-enrollment-report/schema.json"
        payload = {
            "title": "Example report",
            "usesExistingDatasetOrResource": "N: No",
            "locationType": "Domestic",
            "planned": {
                "notHispanicLatino": {
                    "female": {"asian": 9, "white": 4, "total": 1}
                },
                "total": {"asian": 999, "total": 2},
            },
        }
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

    def test_semantically_distinct_attachments_share_only_capture_mechanism(self) -> None:
        index = load(FORM / "index.json")
        attachments = [
            row
            for row in index["fieldOccurrences"]
            if row["leaf"] and "generics/attachment" in row["blockIds"]
        ]
        self.assertEqual(len(attachments), 15)
        semantic_roles = {
            block_id
            for row in attachments
            for block_id in row["blockIds"]
            if block_id.startswith("clinical-study/")
            and block_id not in {
                "clinical-study/application-overview",
                "clinical-study/study-record",
                "clinical-study/population-characteristics",
                "clinical-study/protection-monitoring",
                "clinical-study/protocol-synopsis",
                "clinical-study/delayed-onset-study",
            }
        }
        self.assertEqual(len(semantic_roles), 15)

    def test_exact_sources_counts_and_unresolved_gates_are_preserved(self) -> None:
        evidence = load(FORM / "evidence.json")
        sources = {row["id"]: row for row in evidence["sources"]}
        self.assertEqual(
            sources["phs-human-subjects-parent-xsd-v3-0"]["sha256"],
            "29d859de80cc9febbd1599c28f5db9a3ec82bff26a4d32f4dbbc372effb56bf3",
        )
        self.assertEqual(
            sources["human-subject-study-xsd-v3-0"]["sha256"],
            "799205dea5eddcf13f926cc39d5fc7de27c6a6cdcc68eff4d49e1b629d4351cf",
        )
        self.assertEqual(
            sources["nih-forms-i-general-application-guide"]["sha256"],
            "97b323be4e8ca90a0a5f69fe46b7762e45188088dc220efd846e008df3c13588",
        )
        self.assertNotIn("phs-human-subjects-source-audit", sources)
        audit_path = ROOT / "research/phs-human-subjects/source-audit.json"
        audit = load(audit_path)
        self.assertFalse(audit["method"]["ocrUsed"])
        self.assertEqual(len(audit["sourceBoundConditions"]), 11)
        self.assertEqual(audit["conditionDecision"]["compiledCount"], 2)
        self.assertEqual(
            audit["conditionDecision"]["compiledTargets"],
            ["studies", "delayedOnsetStudies"],
        )
        self.assertEqual(audit["inventory"]["totalLikeCoordinates"], 28)
        self.assertEqual(audit["calculationDecision"]["status"], "source-bound-unresolved")
        conditions = [
            row for row in evidence["behaviorEvidence"]
            if row["ruleKind"] == "condition"
        ]
        calculations = [
            row for row in evidence["behaviorEvidence"]
            if row["ruleKind"] == "calculation"
        ]
        self.assertEqual(len(conditions), 11)
        self.assertEqual(
            {row["sourcePath"] for row in conditions},
            {"1-07", "1-08", "1-14", "1-15-1", "1-15-2", "1-16",
             "1-19-1", "1-19-2", "1-19-3", "1-19-4", "1-20"},
        )
        compiled = {
            row["canonicalPath"]
            for row in conditions
            if row["executionStatus"] == "compiled"
        }
        self.assertEqual(compiled, {"studies", "delayedOnsetStudies"})
        self.assertEqual(
            sum(row["executionStatus"] == "source-bound-uncompiled" for row in conditions),
            9,
        )
        self.assertTrue(all(row["authority"] == "official_source" for row in conditions))
        self.assertEqual(len(calculations), 1)
        self.assertEqual(calculations[0]["authority"], "unresolved")
        self.assertIn("28 total-like", calculations[0]["reason"])
        runtime_rules = load(FORM / "sgg/rule-schema.json")
        self.assertNotIn("gg_condition", json.dumps(runtime_rules))
        self.assertNotIn("gg_calculation", json.dumps(runtime_rules))
        self.assertEqual(evidence["semanticReview"]["status"], "proposed")

    def test_source_string_and_nested_repeat_boundaries_are_exact(self) -> None:
        schemas = {
            name: load(ROOT / f"dist/question-bank/clinical-study/{name}/schema.json")
            for name in (
                "study-record", "population-characteristics", "design",
                "protocol-synopsis", "inclusion-enrollment-report",
            )
        }
        self.assertEqual(
            schemas["study-record"]["properties"]["exemptionNumbers"],
            {
                "type": "array",
                "items": {"$ref": "#/$defs/HumanSubjectExemptionCode"},
                "minItems": 1,
                "maxItems": 8,
            },
        )
        self.assertEqual(
            schemas["population-characteristics"]["properties"]["conditionsOrFocus"]["maxItems"], 20,
        )
        self.assertEqual(
            schemas["population-characteristics"]["properties"]["inclusionEnrollmentReports"]["maxItems"], 20,
        )
        self.assertEqual(schemas["design"]["properties"]["interventions"]["maxItems"], 20)
        self.assertEqual(schemas["protocol-synopsis"]["properties"]["outcomeMeasures"]["maxItems"], 50)
        self.assertEqual(
            schemas["inclusion-enrollment-report"]["properties"]["enrollmentCountries"]["maxItems"], 200,
        )
        self.assertEqual(
            schemas["study-record"]["properties"]["otherClinicalTrialAttachments"]["maxItems"], 100,
        )

        def assert_strings(node: object, path: str = "") -> None:
            if isinstance(node, dict):
                if "maxLength" in node:
                    self.assertEqual(node.get("minLength"), 1, path)
                for key, value in node.items():
                    assert_strings(value, f"{path}/{key}")
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    assert_strings(value, f"{path}/{index}")

        assert_strings(load(FORM / "schema.json"))
        for name, schema in schemas.items():
            assert_strings(schema, name)


if __name__ == "__main__":
    unittest.main()
