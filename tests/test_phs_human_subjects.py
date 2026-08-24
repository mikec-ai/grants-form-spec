from __future__ import annotations

import hashlib
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
            "humanSubjectsInvolved",
            "exemptFromFederalRegulations",
            "exemptionNumbers",
            "applicationId",
        ):
            self.assertTrue(overview["properties"][name]["readOnly"])

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
        audit_path = ROOT / "research/phs-human-subjects/source-audit.json"
        self.assertEqual(
            hashlib.sha256(audit_path.read_bytes()).hexdigest(),
            sources["phs-human-subjects-source-audit"]["sha256"],
        )
        audit = load(audit_path)
        self.assertFalse(audit["method"]["ocrUsed"])
        self.assertEqual(len(audit["sourceBoundConditions"]), 11)
        self.assertEqual(audit["conditionDecision"]["compiledCount"], 0)
        self.assertEqual(audit["inventory"]["totalLikeCoordinates"], 28)
        self.assertEqual(audit["calculationDecision"]["status"], "source-bound-unresolved")
        self.assertEqual(evidence["semanticReview"]["status"], "proposed")


if __name__ == "__main__":
    unittest.main()
