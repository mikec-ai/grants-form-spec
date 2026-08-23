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


class RRKeyPersonExpandedTests(unittest.TestCase):
    def test_promotion_packet_preserves_broad_evidence_without_false_conflict(self) -> None:
        if not (CROSSWALK / ".git").exists():
            self.skipTest("pinned crosswalk checkout is unavailable")

        packet = export_packet(CROSSWALK, "RRKeyPersonExpanded", CROSSWALK_REVISION)

        self.assertEqual(packet["metrics"], {
            "sourceRecords": 101,
            "sourceBehaviors": 67,
            "applicantBehaviorRecords": 56,
            "presentationBehaviorRecords": 8,
            "runtimeRules": 10,
            "semanticProposals": 101,
            "acceptedSemanticMappings": 0,
            "openReviewGates": 73,
        })
        self.assertEqual(
            packet["extraction"]["sourceSetSha256"],
            "8866396d99e32eeec6618ea63c52c2b205718dc481482b27ab61699ecd2efeb0",
        )
        self.assertFalse(any(
            gate["kind"] == "source_conflict" for gate in packet["reviewGates"]
        ))
        self.assertTrue(all(not row["publishable"] for row in packet["semanticProposals"]))

    def test_form_compiles_repeated_people_and_typed_conditions_generically(self) -> None:
        root = ROOT / "dist/forms/rr-key-person-expanded"
        schema = load(root / "schema.json")
        canonical_ui = load(root / "ui.json")
        ui = load(root / "sgg/ui-schema.json")
        rules = load(root / "sgg/rule-schema.json")
        all_ui = list(objects(ui))
        fields = [row for row in all_ui if row.get("type") == "field"]
        conditions = [row["conditional"] for row in fields if "conditional" in row]

        self.assertEqual(len(schema["properties"]), 5)
        self.assertEqual(schema["required"], ["principalInvestigator"])
        self.assertEqual(schema["properties"]["seniorKeyPersons"]["maxItems"], 99)
        address = schema["$defs"]["ResearchPersonAddress"]
        us_constraint = next(
            branch for branch in address["allOf"]
            if branch.get("then", {}).get("properties", {}).get("zipCode")
        )
        self.assertEqual(
            us_constraint["then"]["properties"]["zipCode"], {"minLength": 9}
        )
        self.assertEqual(
            schema["$defs"]["PrincipalInvestigatorProfile"]["properties"]
            ["projectRole"]["default"],
            "PD/PI",
        )
        self.assertEqual(len(fields), 57)
        self.assertEqual(len(conditions), 9)
        self.assertEqual(sum(c["when"]["op"] == "in" for c in conditions), 2)
        self.assertTrue(all(
            c["when"]["values"] == ["Other Professional", "Other (Specify)"]
            for c in conditions if c["when"]["op"] == "in"
        ))
        self.assertTrue(all(
            c["when"]["value"] == "USA: UNITED STATES"
            for c in conditions if c["when"]["op"] == "equals"
        ))
        repeated_conditions = [
            c for c in conditions
            if c["when"].get("ref", {}).get("scope") == "item"
        ]
        self.assertEqual(len(repeated_conditions), 3)
        self.assertEqual(
            {c["when"]["ref"]["pointer"] for c in repeated_conditions},
            {"/address/country", "/projectRole"},
        )

        overflow_fields = (
            "additionalProfiles",
            "additionalBiographicalSketches",
            "additionalCurrentPendingSupport",
        )
        overflow_definitions = {
            f"/properties/{field_name}" for field_name in overflow_fields
        }
        existing_conditions = [
            row for row in fields
            if "conditional" in row and row["definition"] not in overflow_definitions
        ]
        self.assertEqual(len(existing_conditions), 6)
        self.assertEqual(
            {
                (
                    row["definition"],
                    row["conditional"]["when"]["op"],
                    row["conditional"]["when"]["ref"]["scope"],
                    row["conditional"]["when"]["ref"]["pointer"],
                    row["conditional"]["then"]["interaction"],
                    row["conditional"]["otherwise"]["interaction"],
                )
                for row in existing_conditions
            },
            {
                (
                    "/properties/principalInvestigator/properties/address/properties/state",
                    "equals", "root", "/principalInvestigator/address/country",
                    "enabled", "disabled",
                ),
                (
                    "/properties/principalInvestigator/properties/address/properties/province",
                    "equals", "root", "/principalInvestigator/address/country",
                    "readOnly", "enabled",
                ),
                (
                    "/properties/principalInvestigator/properties/otherProjectRole",
                    "in", "root", "/principalInvestigator/projectRole",
                    "enabled", "disabled",
                ),
                (
                    "/properties/seniorKeyPersons/items/properties/address/properties/state",
                    "equals", "item", "/address/country", "enabled", "disabled",
                ),
                (
                    "/properties/seniorKeyPersons/items/properties/address/properties/province",
                    "equals", "item", "/address/country", "readOnly", "enabled",
                ),
                (
                    "/properties/seniorKeyPersons/items/properties/otherProjectRole",
                    "in", "item", "/projectRole", "enabled", "disabled",
                ),
            },
        )

        overflow_sgg = {
            row["definition"].removeprefix("/properties/"): row["conditional"]
            for row in fields if row["definition"] in overflow_definitions
        }
        self.assertEqual(set(overflow_sgg), set(overflow_fields))
        for field_name in overflow_fields:
            self.assertEqual(overflow_sgg[field_name], {
                "when": {
                    "op": "any",
                    "predicates": [
                        {
                            "op": "countAtLeast",
                            "ref": {
                                "scope": "root",
                                "pointer": "/seniorKeyPersons",
                            },
                            "minimum": 99,
                        },
                        {
                            "op": "present",
                            "ref": {
                                "scope": "root",
                                "pointer": f"/{field_name}",
                            },
                        },
                    ],
                },
                "then": {"interaction": "enabled"},
                "otherwise": {"interaction": "disabled"},
            })

        canonical_controls = {
            row["scope"].removeprefix("#/properties/"): row
            for row in canonical_ui["elements"]
        }
        for field_name in overflow_fields:
            self.assertEqual(canonical_controls[field_name]["rule"], {
                "effect": "ENABLE",
                "condition": {
                    "scope": "#",
                    "schema": {
                        "anyOf": [
                            {
                                "properties": {
                                    "seniorKeyPersons": {
                                        "type": "array",
                                        "minItems": 99,
                                    },
                                },
                                "required": ["seniorKeyPersons"],
                            },
                            {
                                "properties": {
                                    field_name: {
                                        "not": {
                                            "anyOf": [
                                                {"type": "null"},
                                                {"const": ""},
                                                {"type": "array", "maxItems": 0},
                                            ],
                                        },
                                    },
                                },
                                "required": [field_name],
                            },
                        ],
                    },
                },
            })

        rule_objects = list(objects(rules))
        self.assertEqual(sum(row.get("gg_validation", {}).get("rule") == "attachment"
                             for row in rule_objects), 7)

        role_schema = load(ROOT / "dist/question-bank/research-person/details/schema.json")
        self.assertEqual(
            role_schema["$defs"]["ResearchProjectRole"]["enum"],
            [
                "PD/PI", "Co-PD/PI", "Faculty", "Post Doctoral",
                "Post Doctoral Associate", "Post Doctoral Scholar",
                "Other Professional", "Graduate Student", "Undergraduate Student",
                "Technician", "Consultant", "Co-Investigator", "Other (Specify)",
            ],
        )
        required_branches = role_schema["allOf"]
        self.assertEqual(len(required_branches), 2)
        self.assertTrue(all(
            branch["then"]["required"] == ["otherProjectRole"]
            for branch in required_branches
        ))

        evidence = load(root / "evidence.json")
        review = evidence["semanticReview"]
        self.assertEqual(review["status"], "proposed")
        self.assertEqual(len(review["mappings"]), 3)
        self.assertTrue(all(row["status"] == "proposed" for row in review["mappings"]))
        self.assertEqual(
            {row["sourcePath"] for row in review["mappings"]},
            {
                "Form DAT!row 25 (Field # 1-17), Business Rules",
                "Form DAT!row 54 (Field # 2-17), Business Rules",
                "Form DAT!row 30 (Field # 1-22), Business Rules",
            },
        )


if __name__ == "__main__":
    unittest.main()
