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
                "properties": {"zipCode": {"minLength": 9}},
            },
        }, address["allOf"])
        self.assertEqual(len(fields), 25)
        self.assertEqual(len(conditions), 5)
        self.assertEqual(sum(c["when"]["ref"]["scope"] == "item" for c in conditions), 2)
        overflow = next(
            row for row in fields
            if row["definition"] == "/properties/additionalLocations"
        )
        self.assertEqual(overflow["conditional"]["when"], {
            "op": "countAtLeast",
            "ref": {"scope": "root", "pointer": "/additionalSites"},
            "minimum": 299,
        })
        field_list = next(
            row for row in all_ui
            if row.get("type") == "fieldList" and row.get("name") == "additionalSites"
        )
        self.assertTrue(field_list["validateBeforeAdd"])
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

    def test_five_exact_dat_behaviors_are_reconciled_without_overclaiming_parity(self) -> None:
        root = ROOT / "dist/forms/performance-site"
        evidence = load(root / "evidence.json")
        records = evidence["behaviorEvidence"]

        official = [row for row in records if row["authority"] == "official_source"]
        unresolved = [row for row in records if row["authority"] == "unresolved"]
        self.assertEqual(len(official), 5)
        self.assertEqual(
            [(row["canonicalPath"], row["sourcePath"]) for row in official],
            [
                ("/primarySite/address/state", "1-07"),
                ("/primarySite/address/province", "1-08"),
                ("/additionalSites/[]/address/state", "2-08"),
                ("/additionalSites/[]/address/province", "2-08a"),
                ("additionalLocations", "3-3"),
            ],
        )
        self.assertEqual({row["sourceId"] for row in official}, {"source-1-c0747c333fb8"})
        self.assertEqual(
            [row["sourceRecord"] for row in official],
            [
                "Conditionally required if Country is US then active. If Country is not US, then inactive",
                "If Country is US then inactive. If Country is not US, then active",
                "Conditionally required if Country is US then active. If Country is not US, then inactive",
                "If Country is US then inactive. If Country is not US, then active",
                "Button becomes active only after the maximum number of sites (i.e 299) has been entered.",
            ],
        )
        self.assertEqual(
            [row["executionStatus"] for row in official],
            [
                "source-bound-uncompiled",
                "source-bound-uncompiled",
                "source-bound-uncompiled",
                "source-bound-uncompiled",
                "compiled",
            ],
        )

        self.assertEqual(len(unresolved), 4)
        self.assertEqual({row["executionStatus"] for row in unresolved}, {"compiled"})
        self.assertEqual(
            {row["canonicalPath"] for row in unresolved},
            {
                "primarySite.address.state",
                "primarySite.address.province",
                "additionalSites[*].address.state",
                "additionalSites[*].address.province",
            },
        )
        self.assertTrue(all(row["owner"] == "form-semantic-review" for row in unresolved))
        self.assertTrue(all(row["reason"] and row["removalCondition"] for row in unresolved))
        self.assertEqual(evidence["semanticReview"], {"status": "unreviewed", "mappings": []})

    def test_handoff_exposes_current_interactions_and_requiredness_gap(self) -> None:
        root = ROOT / "dist/forms/performance-site"
        schema = load(root / "schema.json")
        ui = load(root / "sgg/ui-schema.json")
        fields = {
            row["definition"]: row
            for row in objects(ui)
            if row.get("type") == "field"
        }

        expected_conditions = {
            "/properties/primarySite/properties/address/properties/state": {
                "when": {
                    "op": "equals",
                    "ref": {"scope": "root", "pointer": "/primarySite/address/country"},
                    "value": "USA: UNITED STATES",
                },
                "then": {"interaction": "enabled"},
                "otherwise": {"interaction": "disabled"},
            },
            "/properties/primarySite/properties/address/properties/province": {
                "when": {
                    "op": "equals",
                    "ref": {"scope": "root", "pointer": "/primarySite/address/country"},
                    "value": "USA: UNITED STATES",
                },
                "then": {"interaction": "readOnly"},
                "otherwise": {"interaction": "enabled"},
            },
            "/properties/additionalSites/items/properties/address/properties/state": {
                "when": {
                    "op": "equals",
                    "ref": {"scope": "item", "pointer": "/address/country"},
                    "value": "USA: UNITED STATES",
                },
                "then": {"interaction": "enabled"},
                "otherwise": {"interaction": "disabled"},
            },
            "/properties/additionalSites/items/properties/address/properties/province": {
                "when": {
                    "op": "equals",
                    "ref": {"scope": "item", "pointer": "/address/country"},
                    "value": "USA: UNITED STATES",
                },
                "then": {"interaction": "readOnly"},
                "otherwise": {"interaction": "enabled"},
            },
        }
        for definition, expected in expected_conditions.items():
            with self.subTest(definition=definition):
                self.assertEqual(fields[definition]["conditional"], expected)
        self.assertEqual(
            fields["/properties/additionalLocations"]["conditional"]["when"],
            {
                "op": "countAtLeast",
                "ref": {"scope": "root", "pointer": "/additionalSites"},
                "minimum": 299,
            },
        )

        address = schema["$defs"]["PerformanceSiteAddress"]
        self.assertFalse(any("required" in branch.get("then", {}) for branch in address["allOf"]))


if __name__ == "__main__":
    unittest.main()
