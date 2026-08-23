from __future__ import annotations

import hashlib
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


def value_field() -> dict:
    return {"element": "Value", "kind": "value", "namespace": "default"}


class XmlXsdConformanceHarnessTests(unittest.TestCase):
    def test_public_entrypoint_rejects_unsupported_contract_version(self) -> None:
        profile = profile_with({"value": value_field()})
        profile["contract"] = "grants-gov-xml-profile/v2"

        with self.assertRaisesRegex(AssertionError, "unsupported.*contract"):
            render_profile_xml(profile, {"value": "answer"})

    def test_null_constant_and_value_map_outputs_are_rejected(self) -> None:
        declarations = (
            {
                "element": "Value",
                "kind": "value",
                "namespace": "default",
                "constant": None,
            },
            {
                "element": "Value",
                "kind": "value",
                "namespace": "default",
                "source": "/choice",
                "valueMap": {"none": None},
            },
        )
        for declaration in declarations:
            with self.subTest(declaration=declaration):
                with self.assertRaisesRegex(
                    AssertionError, "declarative null emission is unsupported"
                ):
                    render_profile_xml(
                        profile_with({"value": declaration}), {"choice": "none"}
                    )

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
                official_sha256="0" * 64,
            )

            with self.assertRaisesRegex(AssertionError, "pinned XSD digest mismatch"):
                validate_exact_xsd(
                    b"<fixture/>",
                    fixture,
                    profile=profile_with({"value": value_field()}),
                )

    def test_validation_requires_exact_profile_digest_and_entrypoint_linkage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            xsd = Path(directory) / "fixture.xsd"
            xsd.write_text("<not-an-xsd/>")
            digest = hashlib.sha256(xsd.read_bytes()).hexdigest()
            fixture = ExactXsdFixture(
                entrypoint="fixture.xsd",
                files=(PinnedXsdFile("fixture.xsd", xsd, digest),),
                official_sha256=digest,
            )
            profile = profile_with({"value": value_field()})

            with self.assertRaisesRegex(AssertionError, "official XSD digest mismatch"):
                validate_exact_xsd(b"<fixture/>", fixture, profile=profile)

            profile["xsd"] = {
                "uri": "https://example.org/unrelated.xsd",
                "sha256": digest,
            }
            with self.assertRaisesRegex(
                AssertionError, "does not identify the pinned entrypoint"
            ):
                validate_exact_xsd(b"<fixture/>", fixture, profile=profile)


if __name__ == "__main__":
    unittest.main()
