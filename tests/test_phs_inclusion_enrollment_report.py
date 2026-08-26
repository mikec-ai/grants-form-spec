from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FORM = ROOT / "dist/forms/phs-inclusion-enrollment-report"


def load(path: Path) -> object:
    return json.loads(path.read_text())


class PHSInclusionEnrollmentReportTests(unittest.TestCase):
    def test_form_shell_composes_shared_core_without_copying_the_grid(self) -> None:
        manifest = load(FORM / "manifest.json")
        schema = load(FORM / "schema.json")
        self.assertEqual(manifest["form"]["legacyFormId"], 791)
        self.assertEqual(manifest["form"]["formVersion"], "1.0")
        self.assertEqual(schema["required"], ["reports"])
        self.assertEqual(schema["properties"]["reports"]["minItems"], 1)
        self.assertEqual(schema["properties"]["reports"]["maxItems"], 20)
        self.assertEqual(
            schema["properties"]["reports"]["items"]["$ref"],
            "../../question-bank/clinical-study/inclusion-enrollment-report/schema.json",
        )

        shared = load(ROOT / "dist/question-bank/clinical-study/inclusion-enrollment-report/schema.json")
        self.assertNotIn("reportId", shared["properties"])
        self.assertNotIn("reportId", json.dumps(schema))
        embedded = (ROOT / "dist/question-bank/clinical-study/population-characteristics/schema.json").read_text()
        self.assertIn("reportId", embedded)

        source = (ROOT / "specs/question-bank/clinical-study/index.tsp").read_text()
        self.assertEqual(source.count("model PlannedEnrollmentMatrix"), 1)
        self.assertEqual(source.count("model CumulativeEnrollmentMatrix"), 1)
        self.assertNotIn("PlannedEnrollmentMatrix", (ROOT / "specs/forms/phs-inclusion-enrollment-report.tsp").read_text())

    def test_one_composite_identity_preserves_115_coordinate_occurrences(self) -> None:
        index = load(FORM / "index.json")
        occurrences = index["fieldOccurrences"]
        coordinate = [
            row for row in occurrences
            if row["leaf"] and ("/planned/" in row["path"] or "/cumulativeActual/" in row["path"])
        ]
        self.assertEqual(len(coordinate), 115)
        self.assertEqual(len({row["path"] for row in coordinate}), 115)
        self.assertTrue(all(
            row["blockIds"] == ["clinical-study/inclusion-enrollment-report"]
            for row in coordinate
        ))
        context = [
            row for row in occurrences
            if row["path"].rsplit("/", 1)[-1] in {
                "title", "usesExistingDatasetOrResource", "locationType",
                "enrollmentCountries", "enrollmentLocations", "comments",
            }
        ]
        self.assertEqual(len(context), 6)

    def test_source_behaviors_are_preserved_without_inferred_runtime_rules(self) -> None:
        evidence = load(ROOT / "evidence/forms/phs-inclusion-enrollment-report/evidence.json")
        conditions = [row for row in evidence["behaviorEvidence"] if row["ruleKind"] == "condition"]
        calculations = [row for row in evidence["behaviorEvidence"] if row["ruleKind"] == "calculation"]
        self.assertEqual(len(conditions), 8)
        self.assertEqual(len(calculations), 28)
        self.assertEqual(
            {row["sourcePath"] for row in conditions},
            {"2-04", "2-04-1", "2-04-3", "2-25-1", "2-25-3", "2-25-4", "2-25-5", "2-25-6"},
        )
        self.assertTrue(all(row["executionStatus"] == "source-bound-uncompiled" for row in conditions + calculations))
        self.assertTrue(all(row["sourceId"] == "phs-ier-dat-f791" for row in conditions + calculations))
        self.assertEqual(len({row["canonicalPath"] for row in calculations}), 28)
        self.assertIsNone(load(FORM / "sgg/rule-schema.json"))

        def read_only_paths(value: object, path: str = "") -> set[str]:
            if not isinstance(value, dict):
                return set()
            paths = {path} if value.get("readOnly") is True else set()
            properties = value.get("properties", {})
            if isinstance(properties, dict):
                for name, child in properties.items():
                    paths.update(read_only_paths(child, f"{path}/{name}"))
            items = value.get("items")
            if isinstance(items, dict):
                item_path = path if path.endswith("/[]") else f"{path}/[]"
                paths.update(read_only_paths(items, item_path))
            branch_path = f"{path}/[]" if value.get("type") == "array" else path
            for branch in value.get("allOf", []):
                paths.update(read_only_paths(branch, branch_path))
            return paths

        schema = load(FORM / "schema.json")
        self.assertEqual(
            read_only_paths(schema),
            {row["canonicalPath"] for row in calculations},
        )

        human_rules = load(ROOT / "dist/forms/phs-human-subjects/sgg/rule-schema.json")
        self.assertNotIn("gg_calculation", json.dumps(human_rules))

    def test_ui_paths_are_unique_but_accessibility_remains_an_explicit_gate(self) -> None:
        ui = load(FORM / "sgg/ui-schema.json")

        reports = ui[0]["children"][0]
        tables = [child for child in reports["children"] if child["type"] == "multiField"]
        self.assertEqual([table["name"] for table in tables], ["planned", "cumulativeActual"])
        self.assertTrue(all(table["widget"] == "Table" for table in tables))
        planned, cumulative = tables
        self.assertEqual(
            [column["columnHeader"] for column in planned["children"]["columns"]],
            [
                "Ethnicity", "Sex", "American Indian or Alaska Native", "Asian",
                "Native Hawaiian or Other Pacific Islander", "Black or African American",
                "White", "More Than One Race", "Total",
            ],
        )
        self.assertEqual(len(planned["children"]["rows"]), 5)
        self.assertEqual(len(cumulative["children"]["rows"]), 10)
        self.assertTrue(all(len(row["cells"]) == 9 for row in planned["children"]["rows"]))
        self.assertTrue(all(len(row["cells"]) == 10 for row in cumulative["children"]["rows"]))
        cells = [
            cell
            for table in tables
            for row in table["children"]["rows"]
            for cell in row["cells"]
        ]
        self.assertEqual(sum(cell["type"] == "readOnly" for cell in cells), 28)
        self.assertEqual(
            planned["children"]["rows"][0]["cells"][:2],
            [
                {"type": "plainText", "staticContent": "Not Hispanic or Latino"},
                {"type": "plainText", "staticContent": "Female"},
            ],
        )
        self.assertEqual(
            planned["children"]["rows"][-1]["cells"][:2],
            [
                {"type": "plainText", "staticContent": "Total"},
                {"type": "plainText", "staticContent": ""},
            ],
        )

        def definitions(value: object) -> list[str]:
            if isinstance(value, dict):
                own = [value["definition"]] if isinstance(value.get("definition"), str) else []
                return own + [item for child in value.values() for item in definitions(child)]
            if isinstance(value, list):
                return [item for child in value for item in definitions(child)]
            return []

        paths = definitions(ui)
        coordinate = [path for path in paths if "/planned/" in path or "/cumulativeActual/" in path]
        self.assertEqual(len(coordinate), 115)
        self.assertEqual(len(set(coordinate)), 115)
        audit = load(ROOT / "research/phs-inclusion-enrollment-report/source-audit.json")
        self.assertEqual(audit["accessibilityBoundary"]["status"], "unresolved-human-consumer-gate")
        self.assertIn("screen-reader coordinate context", audit["accessibilityBoundary"]["notVerified"])

    def test_analysis_keeps_one_question_identity_and_coordinate_shapes(self) -> None:
        result = subprocess.run(
            ["python3", "scripts/analyze.py", "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(
            report["asks"]["phs-inclusion-enrollment-report"],
            ["clinical-study/inclusion-enrollment-report"],
        )
        rows = [
            row for row in report["formQuestionAssociations"]
            if row["formId"] == "phs-inclusion-enrollment-report"
        ]
        self.assertEqual(len(rows), 121)
        self.assertEqual({row["questionId"] for row in rows}, {"clinical-study/inclusion-enrollment-report"})
        marginal = next(
            row for row in report["marginalCapabilityReuse"]
            if row["formId"] == "phs-inclusion-enrollment-report"
        )
        self.assertEqual(marginal["newQuestionCount"], 0)
        self.assertEqual(marginal["reusedQuestionCount"], 1)

    def test_physical_source_hashes_and_no_ocr_boundary(self) -> None:
        evidence = load(ROOT / "evidence/forms/phs-inclusion-enrollment-report/evidence.json")
        sources = {row["id"]: row for row in evidence["sources"]}
        self.assertEqual(sources["phs-ier-xsd-v1-0"]["sha256"], "3263bbfa8881c7d428958cf91de470cd19f0f6cbc11818c4752d5266bb0f53a4")
        self.assertEqual(sources["phs-ier-dat-f791"]["sha256"], "31927e7673d726a76a527a4cd3ea460f7b6510c41b4010c1fb15a4a2d62995f0")
        self.assertEqual(sources["phs-ier-readonly-pdf-f791"]["sha256"], "933c94b039e93ff6e16aae2c29a8c3fe779e1cce9334988b6fb2f5410ce6399f")
        self.assertEqual(sources["phs-ier-xfa-pdf-f791"]["sha256"], "e1ff215a5e8f030e7724df4c5655e1c159a651b64204e15fb9abcd060e9dda12")
        audit = load(ROOT / "research/phs-inclusion-enrollment-report/source-audit.json")
        self.assertFalse(audit["method"]["ocrUsed"])
        self.assertTrue(any("3b13a57" in row for row in audit["provenanceConflicts"]))


if __name__ == "__main__":
    unittest.main()
