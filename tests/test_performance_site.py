from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.promote_crosswalk import export_packet


ROOT = Path(__file__).parents[1]
CROSSWALK = ROOT.parent / "grants-question-crosswalk-mp-cover"
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


class PerformanceSiteTests(unittest.TestCase):
    def test_promotion_packet_is_pinned_and_review_gated(self) -> None:
        if not (CROSSWALK / ".git").exists():
            self.skipTest("pinned crosswalk checkout is unavailable")
        packet = export_packet(CROSSWALK, "PerformanceSite", CROSSWALK_REVISION)
        self.assertEqual(packet["metrics"], {
            "sourceRecords": 34,
            "sourceBehaviors": 33,
            "applicantBehaviorRecords": 25,
            "presentationBehaviorRecords": 8,
            "runtimeRules": 9,
            "semanticProposals": 34,
            "acceptedSemanticMappings": 0,
            "openReviewGates": 40,
        })
        self.assertEqual(
            packet["extraction"]["sourceSetSha256"],
            "ba3348472c48a2fac951308c9a8f44fc078c5b014771d7e9d1a4b0521a00d879",
        )
        self.assertTrue(all(not row["publishable"] for row in packet["semanticProposals"]))

    def test_form_compiles_primary_and_repeating_sites_without_custom_code(self) -> None:
        root = ROOT / "dist/forms/performance-site"
        schema = load(root / "schema.json")
        ui = load(root / "sgg/ui-schema.json")
        rules = load(root / "sgg/rule-schema.json")
        all_ui = list(objects(ui))
        fields = [row for row in all_ui if row.get("type") == "field"]
        conditions = [row["conditional"] for row in fields if "conditional" in row]

        self.assertEqual(len(schema["properties"]), 3)
        self.assertEqual(schema["properties"]["additionalSites"]["maxItems"], 299)
        primary = schema["$defs"]["PrimaryPerformanceSiteDetails"]
        self.assertIn({
            "if": {
                "properties": {"individual": {"const": "N: No"}},
                "required": ["individual"],
            },
            "then": {"required": ["organizationName"]},
        }, primary["allOf"])
        address = schema["$defs"]["PerformanceSiteAddress"]
        self.assertIn({
            "if": {
                "properties": {"country": {"const": "USA: UNITED STATES"}},
                "required": ["country"],
            },
            "then": {
                "required": ["state", "zipCode"],
                "properties": {"zipCode": {"minLength": 9}},
            },
        }, address["allOf"])
        self.assertEqual(len(fields), 25)
        self.assertEqual(len(conditions), 4)
        self.assertEqual(sum(c["when"]["ref"]["scope"] == "item" for c in conditions), 2)
        self.assertEqual(sum(
            row.get("gg_validation", {}).get("rule") == "attachment"
            for row in objects(rules)
        ), 1)

        details = load(ROOT / "dist/question-bank/project-site/details/schema.json")
        self.assertEqual(details["$defs"]["SiteIndividualIndicator"]["enum"], ["Y: Yes", "N: No"])
        self.assertEqual(details["properties"]["congressionalDistrict"]["maxLength"], 6)
        self.assertEqual(len(details["allOf"]), 1)

        evidence = load(root / "evidence.json")
        manifest = load(root / "manifest.json")
        profile = load(root / "targets/grants-gov-xml.json")
        self.assertEqual(evidence["semanticReview"], {"status": "unreviewed", "mappings": []})
        self.assertEqual(manifest["artifacts"]["targets/grants-gov-xml.json"], "generated")
        self.assertEqual(
            profile["xsd"]["sha256"],
            "d47dbb254b112f69dc308c01dea2fe15b29114d0e3bdc5a137d3178b5af7bc6c",
        )


if __name__ == "__main__":
    unittest.main()
