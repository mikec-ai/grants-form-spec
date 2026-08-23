from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from conformance.grants_gov_xml import (
    ExactXsdFixture,
    PinnedXsdFile,
    render_profile_xml,
    validate_exact_xsd,
)


def profile_with(fields: dict) -> dict:
    return {
        "contract": "grants-gov-xml-profile/v1",
        "formId": "fixture",
        "xsd": {"uri": "https://example.org/fixture.xsd", "sha256": "0" * 64},
        "namespaces": {"default": "urn:fixture", "item": "urn:item"},
        "root": {
            "element": "Fixture",
            "namespacePrefix": "default",
            "attributes": {"version": "1"},
        },
        "mapping": {"fields": fields},
    }


class XmlXsdConformanceHarnessTests(unittest.TestCase):
    def test_collection_array_uses_one_wrapper_and_declared_item_attributes(self) -> None:
        profile = profile_with(
            {
                "rows": {
                    "element": "Rows",
                    "kind": "array",
                    "namespace": "default",
                    "itemElement": "Row",
                    "itemNamespace": "item",
                    "itemAttributes": {"version": "2"},
                    "items": {
                        "fields": {
                            "name": {
                                "element": "Name",
                                "kind": "value",
                                "namespace": "item",
                            }
                        }
                    },
                }
            }
        )

        root = ET.fromstring(
            render_profile_xml(profile, {"rows": [{"name": "one"}, {"name": "two"}]})
        )

        self.assertEqual([child.tag for child in root], ["{urn:fixture}Rows"])
        self.assertEqual(
            [child.tag for child in root[0]], ["{urn:item}Row", "{urn:item}Row"]
        )
        self.assertEqual(root[0][0].attrib, {"{urn:item}version": "2"})
        self.assertEqual([item[0].text for item in root[0]], ["one", "two"])

    def test_scalar_array_can_repeat_outer_element_and_project_each_item(self) -> None:
        profile = profile_with(
            {
                "values": {
                    "element": "Entry",
                    "kind": "array",
                    "namespace": "default",
                    "items": {
                        "node": {
                            "element": "Value",
                            "kind": "value",
                            "namespace": "item",
                        }
                    },
                }
            }
        )

        root = ET.fromstring(render_profile_xml(profile, {"values": [True, False]}))

        self.assertEqual([child.tag for child in root], ["{urn:fixture}Entry"] * 2)
        self.assertEqual([child[0].text for child in root], ["true", "false"])

    def test_digest_mismatch_fails_before_xsd_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            xsd = Path(directory) / "fixture.xsd"
            xsd.write_text("<not-an-xsd/>")
            fixture = ExactXsdFixture(
                entrypoint="fixture.xsd",
                files=(PinnedXsdFile("fixture.xsd", xsd, "0" * 64),),
            )

            with self.assertRaisesRegex(AssertionError, "pinned XSD digest mismatch"):
                validate_exact_xsd(b"<fixture/>", fixture)


if __name__ == "__main__":
    unittest.main()
