from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.promote_crosswalk import export_packet


ROOT = Path(__file__).parents[1]
CROSSWALK = ROOT.parent / "grants-question-crosswalk"
CROSSWALK_REVISION = "4312f6504b060e2b9ffdbd2307fc41130c3123a0"


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


class SflllTests(unittest.TestCase):
    def test_factory_evidence_is_pinned_and_semantic_reuse_remains_review_gated(self) -> None:
        if not (CROSSWALK / ".git").exists():
            self.skipTest("pinned crosswalk checkout is unavailable")

        packet = export_packet(CROSSWALK, "SFLLL", CROSSWALK_REVISION)
        self.assertEqual(packet["metrics"], {
            "sourceRecords": 76,
            "sourceBehaviors": 86,
            "applicantBehaviorRecords": 63,
            "presentationBehaviorRecords": 15,
            "runtimeRules": 16,
            "semanticProposals": 76,
            "acceptedSemanticMappings": 0,
            "openReviewGates": 85,
        })
        self.assertEqual(
            packet["extraction"]["sourceSetSha256"],
            "86c5849f65a3f3d8fcdc7da17cfa6070c185008eae9916184e7d6c32cd098b05",
        )
        self.assertTrue(all(not row["publishable"] for row in packet["semanticProposals"]))

    def test_form_compiles_conditions_repetition_and_lifecycle_rules_declaratively(self) -> None:
        root = ROOT / "dist/forms/sflll"
        schema = load(root / "schema.json")
        ui = load(root / "sgg/ui-schema.json")
        rules = load(root / "sgg/rule-schema.json")
        profile = load(root / "targets/grants-gov-xml.json")
        evidence = load(root / "evidence.json")

        self.assertEqual(schema["required"], [
            "reportingOrganization",
            "federalAgencyDepartment",
            "lobbyingRegistrant",
            "individualsPerformingServices",
            "signatureBlock",
        ])
        filing_schema = load(
            ROOT / "dist/question-bank/federal-action/disclosure-filing-details/schema.json"
        )
        self.assertEqual(filing_schema["required"], [
            "federalActionType",
            "federalActionStatus",
            "reportType",
            "reportingEntityType",
        ])
        self.assertEqual(schema["properties"]["individualsPerformingServices"]["minItems"], 1)
        self.assertEqual(schema["properties"]["individualsPerformingServices"]["maxItems"], 10)
        self.assertEqual(filing_schema["properties"]["tier"]["minimum"], 0)
        self.assertEqual(filing_schema["properties"]["tier"]["maximum"], 99)
        number_schema = load(ROOT / "dist/question-bank/federal-action/number/schema.json")
        self.assertEqual(number_schema["maxLength"], 110)
        award_schema = load(ROOT / "dist/question-bank/federal-action/award-amount/schema.json")
        self.assertEqual(award_schema["maxLength"], 16)
        self.assertEqual(
            {
                next(iter(branch["if"]["properties"]))
                for branch in schema["allOf"]
                if "if" in branch
            },
            {"reportType", "reportingEntityType"},
        )

        field_rows = [row for row in objects(ui) if row.get("type") in {"field", "null"}]
        material_fields = [
            row for row in field_rows
            if row["definition"].startswith("/properties/materialChange/")
        ]
        prime_fields = [
            row for row in field_rows
            if row["definition"].startswith("/properties/primeOrganization/")
        ]
        self.assertEqual(len(material_fields), 3)
        self.assertEqual(len(prime_fields), 7)
        self.assertTrue(all(row["conditional"]["when"]["ref"]["pointer"] == "/reportType"
                            for row in material_fields))
        self.assertTrue(all(row["conditional"]["when"]["ref"]["pointer"] == "/reportingEntityType"
                            for row in prime_fields))
        field_list = next(row for row in objects(ui) if row.get("type") == "fieldList")
        self.assertEqual(field_list["name"], "individualsPerformingServices")
        self.assertTrue(field_list["validateBeforeAdd"])

        self.assertEqual(
            rules["signatureBlock"]["signedDate"]["gg_post_population"]["rule"],
            "current_date",
        )
        self.assertEqual(
            rules["signatureBlock"]["signature"]["gg_post_population"]["rule"],
            "signature",
        )
        self.assertEqual(
            rules["federalAgencyDepartment"]["gg_pre_population"]["rule"],
            "agency_name",
        )

        report_entity = profile["mapping"]["fields"]["reportEntity"]
        self.assertEqual(report_entity["attributes"]["ReportEntityType"], {
            "source": "/reportingEntityType",
        })
        self.assertEqual(
            report_entity["fields"]["reportEntityIsPrime"]["valueMap"],
            {"Prime": "Y: Yes", "SubAwardee": "N: No"},
        )
        self.assertEqual(
            report_entity["fields"]["primeOrganization"]["fields"]
            ["wireEntityType"]["fields"]["entityType"]["constant"],
            "Prime",
        )
        self.assertEqual(evidence["extraction"]["revision"], CROSSWALK_REVISION)
        self.assertEqual(evidence["semanticReview"]["status"], "proposed")
        self.assertTrue(all(row["status"] == "proposed"
                            for row in evidence["semanticReview"]["mappings"]))


if __name__ == "__main__":
    unittest.main()
