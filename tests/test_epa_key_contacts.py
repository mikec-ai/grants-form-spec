from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(path: Path) -> object:
    return json.loads(path.read_text())


class EPAKeyContactsTests(unittest.TestCase):
    def test_form_reuses_one_role_qualified_contact_composition(self) -> None:
        root = ROOT / "dist/forms/epa-key-contacts"
        schema = load(root / "schema.json")
        ui = load(root / "sgg/ui-schema.json")

        self.assertNotIn("required", schema)
        self.assertEqual(list(schema["properties"]), [
            "authorizedRepresentative",
            "payee",
            "administrativeContact",
            "projectManager",
        ])
        self.assertTrue(all(
            role["$ref"] == "#/$defs/EPAKeyContactPerson"
            for role in schema["properties"].values()
        ))

        person = schema["$defs"]["EPAKeyContactPerson"]
        self.assertEqual(person["required"], ["name", "address", "phone"])
        self.assertEqual(person["properties"]["name"]["required"], [
            "firstName", "lastName",
        ])
        self.assertEqual(person["properties"]["address"]["required"], [
            "street1", "city", "country",
        ])

        self.assertEqual([section["name"] for section in ui], [
            "authorizedRepresentative",
            "payee",
            "administrativeContact",
            "projectManager",
        ])
        for section in ui:
            definitions = {child["definition"] for child in section["children"]}
            self.assertEqual(len(definitions), 15)
            self.assertFalse(any(path.endswith("/county") for path in definitions))
            self.assertFalse(any(path.endswith("/province") for path in definitions))

    def test_us_state_and_zip_requirements_are_compiled_generically(self) -> None:
        schema = load(ROOT / "dist/forms/epa-key-contacts/schema.json")
        address = schema["$defs"]["EPAKeyContactPerson"]["properties"]["address"]

        self.assertEqual(len(address["allOf"]), 2)
        self.assertEqual(
            {branch["then"]["required"][0] for branch in address["allOf"]},
            {"state", "zipCode"},
        )
        for branch in address["allOf"]:
            self.assertEqual(
                branch["if"],
                {
                    "properties": {"country": {"const": "USA: UNITED STATES"}},
                    "required": ["country"],
                },
            )

    def test_source_and_review_boundaries_remain_machine_readable(self) -> None:
        root = ROOT / "dist/forms/epa-key-contacts"
        evidence = load(root / "evidence.json")
        manifest = load(root / "manifest.json")

        self.assertEqual(evidence["semanticReview"]["status"], "proposed")
        self.assertEqual(len(evidence["semanticReview"]["mappings"]), 4)
        self.assertTrue(all(
            mapping["status"] == "proposed"
            for mapping in evidence["semanticReview"]["mappings"]
        ))
        self.assertEqual(
            evidence["extraction"]["revision"],
            "dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef",
        )
        self.assertEqual(
            {source["sha256"] for source in evidence["sources"]},
            {
                "157a9c8a21cdc39b4c6b5df94c3745ecd4f174cb390187441de862fb35b50b01",
                "bc3db7e10eb19bb679020aa11d44d4fd9213331e5814d94568281bd45a3d4d04",
                "2d90213e02a22656f7f624dd83ce49c5d162c90ae0fbc220a61cc60ad16649f8",
                "6d12ccee7bcd95f66b019d7bca7c64a13303ff4d4ad9124b95c0aa2db54633c3",
                "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
                "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
            },
        )
        compiled = [
            record for record in evidence["behaviorEvidence"]
            if record.get("executionStatus") == "compiled"
        ]
        source_bound_uncompiled = [
            record for record in evidence["behaviorEvidence"]
            if record.get("executionStatus") == "source-bound-uncompiled"
        ]
        unresolved = [
            record for record in source_bound_uncompiled
            if record["authority"] == "unresolved"
        ]
        self.assertEqual(len(compiled), 0)
        self.assertEqual(len(source_bound_uncompiled), 36)
        self.assertEqual(len(unresolved), 4)
        self.assertEqual(
            manifest["artifacts"]["targets/grants-gov-xml.json"],
            "generated",
        )


if __name__ == "__main__":
    unittest.main()
