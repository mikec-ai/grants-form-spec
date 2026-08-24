from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FORM = ROOT / "dist/forms/sf424-short"
AUDIT = ROOT / "research/sf424-short/source-audit.json"


def load(path: Path) -> object:
    return json.loads(path.read_text())


class Sf424ShortSemanticTests(unittest.TestCase):
    PREPOPULATION_RULES = {
        "agencyName": "agency_name",
        "assistanceListingNumber": "assistance_listing_number",
        "assistanceListingProgramTitle": "assistance_listing_program_title",
        "fundingOpportunityNumber": "opportunity_number",
        "fundingOpportunityTitle": "opportunity_title",
        "samUei": "uei",
    }

    def test_six_prepopulated_fields_are_not_declared_read_only(self) -> None:
        schema = load(FORM / "schema.json")

        for field in self.PREPOPULATION_RULES:
            with self.subTest(field=field):
                self.assertNotIn("readOnly", schema["properties"][field])
                self.assertFalse(any(
                    branch.get("readOnly") is True
                    for branch in schema["properties"][field].get("allOf", [])
                ))

        for field in {
            "dateReceived",
            "aorSignature",
            "authorizedRepresentativeDateSigned",
        }:
            with self.subTest(submission_populated_field=field):
                self.assertTrue(schema["properties"][field]["readOnly"])

    def test_prepopulation_remains_while_sgg_controls_are_editable(self) -> None:
        rules = load(FORM / "sgg/rule-schema.json")
        ui = load(FORM / "sgg/ui-schema.json")
        fields = {
            child["definition"].removeprefix("/properties/"): child
            for section in ui
            for child in section["children"]
            if child.get("definition", "").removeprefix("/properties/")
            in self.PREPOPULATION_RULES
        }

        self.assertEqual(set(fields), set(self.PREPOPULATION_RULES))
        for field, rule in self.PREPOPULATION_RULES.items():
            with self.subTest(field=field):
                self.assertEqual(
                    rules[field],
                    {"gg_pre_population": {"rule": rule}},
                )
                self.assertEqual(fields[field]["type"], "field")
                self.assertNotIn("conditional", fields[field])

    def test_source_audit_preserves_each_field_disposition_and_conflict(self) -> None:
        audit = load(AUDIT)
        findings = {
            row["canonicalPath"]: row for row in audit["editabilityFindings"]
        }

        self.assertFalse(audit["method"]["ocrUsed"])
        self.assertEqual(
            audit["sourceArtifacts"]["rootXsd"]["sha256"],
            "82b0f2a0ddbbcfae4ec7e083188287fb05700e201ade3b2f69684241bf8baabd",
        )
        self.assertEqual(
            audit["sourceArtifacts"]["dat"]["sha256"],
            "a905f905928a730b10d48d0b77cbb59397edb3ad3c99770391e1e160c3fb06df",
        )
        self.assertEqual(
            set(findings),
            {f"/{field}" for field in self.PREPOPULATION_RULES},
        )
        self.assertEqual(
            findings["/samUei"]["classification"],
            "context-dependent-source-conflict",
        )
        self.assertEqual(
            {
                row["classification"]
                for path, row in findings.items()
                if path != "/samUei"
            },
            {"read-only-inferred-from-prepopulation"},
        )
        self.assertTrue(all(
            "remove" in row["declarativeDisposition"]
            and row["datFieldType"] == "Pre-populated"
            for row in findings.values()
        ))
        self.assertEqual(len(audit["sourceConflicts"]), 3)
        self.assertEqual(
            set(audit["submissionPopulatedReadOnlyFields"]),
            {
                "/dateReceived",
                "/aorSignature",
                "/authorizedRepresentativeDateSigned",
            },
        )


if __name__ == "__main__":
    unittest.main()
