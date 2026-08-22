from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.promote_crosswalk import export_packet


ROOT = Path(__file__).parents[1]
CROSSWALK = ROOT.parent / "grants-question-crosswalk-mp-cover"
CROSSWALK_REVISION = "c1573287e0664d7b991e69c352038534b771189f"


class RRSF424MultiProjectCoverTests(unittest.TestCase):
    def test_promotion_packet_is_exact_and_review_gated(self) -> None:
        if not (CROSSWALK / ".git").exists():
            self.skipTest("pinned crosswalk checkout is unavailable")

        packet = export_packet(CROSSWALK, "RRSF424MPCover", CROSSWALK_REVISION)

        self.assertEqual(packet["metrics"], {
            "sourceRecords": 139,
            "sourceBehaviors": 143,
            "applicantBehaviorRecords": 123,
            "presentationBehaviorRecords": 20,
            "runtimeRules": 40,
            "semanticProposals": 139,
            "acceptedSemanticMappings": 0,
            "openReviewGates": 162,
        })
        self.assertEqual(
            packet["extraction"]["sourceSetSha256"],
            "3224ce9eac55ccc27a8cae4f257efe10b69872ef5bb6c3fa22d82c9ed4427fac",
        )
        self.assertTrue(all(not row["publishable"] for row in packet["semanticProposals"]))

    def test_source_structure_is_a_parameterized_sibling_not_a_label_match(self) -> None:
        if not (CROSSWALK / ".git").exists():
            self.skipTest("pinned crosswalk checkout is unavailable")

        standalone = export_packet(
            ROOT.parent / "Smarter-grants-management",
            "RRSF424",
            "dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef",
        )
        multi = export_packet(CROSSWALK, "RRSF424MPCover", CROSSWALK_REVISION)
        standalone_root = standalone["form"]["sourceRoot"]
        multi_root = multi["form"]["sourceRoot"]
        standalone_paths = {
            row["path"].removeprefix(standalone_root): row for row in standalone["records"]
        }
        multi_paths = {
            row["path"].removeprefix(multi_root): row for row in multi["records"]
        }

        self.assertEqual(set(standalone_paths) - set(multi_paths), {".GGTrackingID"})
        self.assertEqual(set(multi_paths) - set(standalone_paths), {".GrantsTrackingNumber"})
        self.assertEqual(len(set(standalone_paths) & set(multi_paths)), 138)
        self.assertTrue(all(
            not row["required"]
            for path, row in multi_paths.items()
            if path and row["recordKind"] != "technical_field"
        ))

    def test_emitted_form_preserves_optional_cardinality_and_typed_behavior(self) -> None:
        root = ROOT / "dist/forms/rr-sf424-multi-project-cover"
        schema = json.loads((root / "schema.json").read_text())
        ui = json.loads((root / "sgg/ui-schema.json").read_text())
        rules = json.loads((root / "sgg/rule-schema.json").read_text())
        fields = [field for section in ui for field in section["children"]]

        self.assertEqual(len(schema["properties"]), 28)
        self.assertNotIn("required", schema)
        self.assertEqual(len(ui), 21)
        self.assertEqual(len(fields), 106)
        self.assertEqual(sum("conditional" in field for field in fields), 14)
        self.assertEqual(sum(
            field.get("conditional", {}).get("then", {}).get("enabled") is True
            for field in fields
        ), 10)
        self.assertEqual(sum(
            field.get("conditional", {}).get("then", {}).get("readOnly") is True
            for field in fields
        ), 4)
        self.assertEqual(set(rules), {
            "sflllAttachment", "preApplicationAttachment", "coverLetterAttachment",
        })
        self.assertEqual(
            schema["properties"]["applicationType"]["properties"]["revisionCode"]
            ["x-encoded-checkbox-group"]["combinations"][-1],
            {"value": "BD", "members": ["B", "D"]},
        )

        evidence = json.loads((root / "evidence.json").read_text())
        self.assertEqual(evidence["semanticReview"], {"status": "unreviewed", "mappings": []})


if __name__ == "__main__":
    unittest.main()
