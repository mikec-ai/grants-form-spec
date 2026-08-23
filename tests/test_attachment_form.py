from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FORM = ROOT / "dist/forms/attachment-form"
INSTRUCTIONS = (
    "Instructions: On this form, you will attach the various files that make up your "
    "grant application. Please consult with the appropriate Agency Guidelines for more "
    "information about each needed file. Please remember that any files you attach must "
    "be in the document format and named as specified in the Guidelines."
)
IMPORTANT = (
    "Important: Please attach your files in the proper sequence. See the appropriate "
    "Agency Guidelines for details."
)
ORDINALS = (
    "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth",
    "Ninth", "Tenth", "Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Fifteenth",
)


def load(path: Path) -> object:
    return json.loads(path.read_text())


class AttachmentFormTests(unittest.TestCase):
    def test_manifest_and_sources_pin_the_official_form_and_legacy_oracle(self) -> None:
        manifest = load(FORM / "manifest.json")
        evidence = load(FORM / "evidence.json")

        self.assertEqual(manifest["form"], {
            "id": "attachment-form",
            "legacyFormId": 540,
            "formName": "Attachment Form",
            "shortFormName": "AttachmentForm_1_2",
            "formVersion": "1.2",
            "agencyCode": "SGG",
            "ombNumber": "",
        })
        sources = {source["id"]: source for source in evidence["sources"]}
        self.assertEqual(
            sources["attachment-form-xsd-1.2"]["sha256"],
            "c6b7f40614a2077818f5f3b5df72959f867611b887c5b888005df8adeaa5e8e9",
        )
        self.assertEqual(
            sources["attachment-form-dat-540"]["sha256"],
            "e5d664667c014948b9cc6f35d3b0b61e26b3b9c247d42fbace3067588d013586",
        )
        self.assertEqual(
            sources["legacy-sgg-oracle-f843134"]["uri"],
            "https://github.com/HHS/simpler-grants-gov/blob/"
            "f84313418e237526adb90c5e57edef0b1bef0490/"
            "api/src/form_schema/forms/attachment_form/1/0/form_json.py",
        )
        self.assertEqual(evidence["semanticReview"], {
            "status": "unreviewed", "mappings": [],
        })

    def test_fifteen_optional_slots_compose_one_capture_mechanism(self) -> None:
        schema = load(FORM / "schema.json")
        index = load(FORM / "index.json")
        slot_index = load(
            ROOT / "dist/question-bank/generics/ordered-attachment-slot/index.json"
        )

        self.assertNotIn("required", schema)
        self.assertEqual(list(schema["properties"]), [f"att{i}" for i in range(1, 16)])
        for number, ordinal in enumerate(ORDINALS, 1):
            prop = schema["properties"][f"att{number}"]
            self.assertEqual(prop, {
                "$ref": "../../question-bank/generics/ordered-attachment-slot/schema.json",
                "description": f"{ordinal} attachment file",
                "title": f"Attachment {number}",
            })

        self.assertEqual(slot_index["classification"], "captureMechanism")
        self.assertEqual(slot_index["composes"], ["generics/attachment"])
        self.assertEqual(len(index["fieldOccurrences"]), 15)
        self.assertTrue(all(
            occurrence["blockIds"] == [
                "generics/attachment", "generics/ordered-attachment-slot",
            ]
            for occurrence in index["fieldOccurrences"]
        ))

    def test_portable_and_sgg_presentation_preserve_instructions_and_slot_order(self) -> None:
        portable = load(FORM / "ui.json")
        sgg = load(FORM / "sgg/ui-schema.json")

        self.assertEqual(portable["elements"][:2], [
            {"type": "Label", "text": INSTRUCTIONS},
            {"type": "Label", "text": IMPORTANT},
        ])
        self.assertEqual(
            [control["scope"] for control in portable["elements"][2:]],
            [f"#/properties/att{i}" for i in range(1, 16)],
        )
        self.assertEqual(sgg[:2], [
            {
                "type": "section", "name": "instructions", "label": "",
                "children": [], "description": INSTRUCTIONS,
            },
            {
                "type": "section", "name": "important", "label": "",
                "children": [], "description": IMPORTANT,
            },
        ])
        self.assertEqual(
            [section["name"] for section in sgg[2:]],
            [f"attachment{i}" for i in range(1, 16)],
        )
        for number, section in enumerate(sgg[2:], 1):
            self.assertEqual(section, {
                "type": "section",
                "name": f"attachment{number}",
                "label": f"{number}) Attachment {number}",
                "children": [{
                    "type": "field",
                    "definition": f"/properties/att{number}",
                    "widget": "Attachment",
                }],
            })

    def test_attachment_rules_match_the_pre_prototype_sgg_oracle(self) -> None:
        rules = load(FORM / "sgg/rule-schema.json")
        self.assertEqual(rules, {
            f"att{i}": {"gg_validation": {"rule": "attachment"}}
            for i in range(1, 16)
        })


if __name__ == "__main__":
    unittest.main()
