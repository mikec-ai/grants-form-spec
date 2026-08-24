from __future__ import annotations

import copy
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


def attachment() -> dict:
    return {
        "fileName": "appendix.pdf",
        "mimeType": "application/pdf",
        "fileLocation": "files/appendix.pdf",
        "hashValue": "a" * 64,
    }


def value_field() -> dict:
    return {"element": "Value", "kind": "value", "namespace": "default"}


class XmlXsdConformanceHarnessTests(unittest.TestCase):
    def test_payload_properties_must_be_consumed_by_the_declarative_mapping(self) -> None:
        profile = profile_with(
            {
                "record": {
                    "element": "Record",
                    "kind": "object",
                    "namespace": "default",
                    "fields": {
                        "name": value_field(),
                        "rows": {
                            "element": "Rows",
                            "kind": "array",
                            "namespace": "default",
                            "items": {"fields": {"name": value_field()}},
                        },
                    },
                }
            }
        )
        with self.assertRaisesRegex(AssertionError, r"unmapped response properties at /: unknown"):
            render_profile_xml(profile, {"record": {"name": "ok"}, "unknown": True})
        with self.assertRaisesRegex(AssertionError, r"at /record: unknown"):
            render_profile_xml(profile, {"record": {"name": "ok", "unknown": True}})
        with self.assertRaisesRegex(AssertionError, r"at /record/rows/0: unknown"):
            render_profile_xml(
                profile,
                {"record": {"name": "ok", "rows": [{"name": "row", "unknown": True}]}},
            )

    def test_source_overrides_consume_only_their_exact_root_payload_paths(self) -> None:
        profile = profile_with(
            {
                "copied": {
                    "element": "Copied",
                    "kind": "value",
                    "namespace": "default",
                    "source": "/control/value",
                    "attributes": {"code": {"source": "/control/code"}},
                },
                "optional": value_field(),
            }
        )
        root = ET.fromstring(
            render_profile_xml(
                profile, {"control": {"value": "answer", "code": "A"}}
            )
        )
        self.assertEqual(root[0].text, "answer")
        self.assertEqual(list(root[0].attrib.values()), ["A"])
        with self.assertRaisesRegex(AssertionError, r"at /control: unknown"):
            render_profile_xml(profile, {"control": {"value": "answer", "unknown": True}})
        with self.assertRaisesRegex(AssertionError, r"at /: copied"):
            render_profile_xml(profile, {"control": {"value": "answer"}, "copied": "shadow"})
        with self.assertRaisesRegex(AssertionError, "requires a scalar response"):
            render_profile_xml(
                profile, {"control": {"value": "answer", "code": {"bad": True}}}
            )

        profile["mapping"]["nonEmittingResponsePaths"] = ["/control/technical"]
        render_profile_xml(
            profile,
            {"control": {"value": "answer", "technical": "consumer-only"}},
        )
        with self.assertRaisesRegex(AssertionError, r"at /control: unknown"):
            render_profile_xml(
                profile,
                {"control": {"value": "answer", "technical": "ok", "unknown": True}},
            )

        for invalid in ("control/technical", "/", "/control//technical", "/control/~2"):
            with self.subTest(invalid=invalid):
                candidate = copy.deepcopy(profile)
                candidate["mapping"]["nonEmittingResponsePaths"] = [invalid]
                with self.assertRaisesRegex(AssertionError, "invalid non-emitting"):
                    render_profile_xml(candidate, {})

    def test_object_and_object_array_source_overrides_validate_declared_children(self) -> None:
        profile = profile_with(
            {
                "wireSummary": {
                    "element": "Summary",
                    "kind": "object",
                    "namespace": "default",
                    "source": "/summary",
                    "fields": {
                        "name": value_field(),
                        "rows": {
                            "element": "Rows",
                            "kind": "array",
                            "namespace": "default",
                            "items": {"fields": {"amount": value_field()}},
                        },
                    },
                },
                "wireRecords": {
                    "element": "Records",
                    "kind": "array",
                    "namespace": "default",
                    "source": "/records",
                    "items": {"fields": {"name": value_field()}},
                },
            }
        )
        response = {
            "summary": {"name": "summary", "rows": [{"amount": 1}]},
            "records": [{"name": "record"}],
        }
        root = ET.fromstring(render_profile_xml(profile, response))
        self.assertEqual(root.find("{urn:fixture}Summary/{urn:fixture}Value").text, "summary")

        nested_unknown = copy.deepcopy(response)
        nested_unknown["summary"]["unknown"] = True
        with self.assertRaisesRegex(AssertionError, r"at /summary: unknown"):
            render_profile_xml(profile, nested_unknown)

        array_unknown = copy.deepcopy(response)
        array_unknown["summary"]["rows"][0]["unknown"] = True
        with self.assertRaisesRegex(AssertionError, r"at /summary/rows/0: unknown"):
            render_profile_xml(profile, array_unknown)

        source_array_unknown = copy.deepcopy(response)
        source_array_unknown["records"][0]["unknown"] = True
        with self.assertRaisesRegex(AssertionError, r"at /records/0: unknown"):
            render_profile_xml(profile, source_array_unknown)

    def test_non_emitting_paths_must_be_disjoint_scalar_values(self) -> None:
        profile = profile_with(
            {
                "copied": {
                    "element": "Copied",
                    "kind": "value",
                    "namespace": "default",
                    "source": "/control/value",
                },
                "optional": value_field(),
            }
        )
        for paths in (
            ["/optional"],
            ["/control"],
            ["/control/value/technical"],
            ["/control/technical", "/control/technical/detail"],
        ):
            with self.subTest(paths=paths):
                candidate = copy.deepcopy(profile)
                candidate["mapping"]["nonEmittingResponsePaths"] = paths
                with self.assertRaisesRegex(AssertionError, "overlaps"):
                    render_profile_xml(candidate, {})

        profile["mapping"]["nonEmittingResponsePaths"] = ["/control/technical"]
        with self.assertRaisesRegex(AssertionError, "must be a scalar leaf"):
            render_profile_xml(
                profile,
                {"control": {"value": "answer", "technical": {"nested": True}}},
            )

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
                        profile_with({"value": declaration}),
                        {"choice": "none"} if "source" in declaration else {},
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

    def test_scalar_array_can_flatten_each_value_into_its_repeated_element(self) -> None:
        profile = profile_with(
            {
                "values": {
                    "element": "Entry",
                    "kind": "array",
                    "namespace": "default",
                    "items": {"node": {"kind": "value", "flatten": True}},
                }
            }
        )

        root = ET.fromstring(render_profile_xml(profile, {"values": [True, False]}))

        self.assertEqual([child.tag for child in root], ["{urn:fixture}Entry"] * 2)
        self.assertEqual([child.text for child in root], ["true", "false"])
        self.assertTrue(all(len(child) == 0 for child in root))

    def test_flattened_scalar_rejects_illegal_context_and_ignored_properties(self) -> None:
        with self.assertRaisesRegex(AssertionError, "only valid as an array item node"):
            render_profile_xml(
                profile_with({"value": {"kind": "value", "flatten": True}}),
                {"value": "answer"},
            )

        declaration = {
            "element": "Entry",
            "kind": "array",
            "namespace": "default",
            "items": {
                "node": {
                    "kind": "value",
                    "flatten": True,
                    "element": "Ignored",
                }
            },
        }
        with self.assertRaisesRegex(AssertionError, "cannot declare ignored properties"):
            render_profile_xml(profile_with({"values": declaration}), {"values": ["x"]})

    def test_collection_array_can_flatten_attachment_payload_into_each_item(self) -> None:
        profile = profile_with(
            {
                "appendix": {
                    "element": "Appendix",
                    "kind": "array",
                    "namespace": "default",
                    "itemElement": "AttachedFile",
                    "itemNamespace": "item",
                    "items": {
                        "node": {
                            "kind": "attachment",
                            "flatten": True,
                        }
                    },
                }
            }
        )
        profile["attachment"] = {
            "fields": {
                name: {"element": element, "namespace": "item"}
                for name, element in (
                    ("fileName", "FileName"),
                    ("mimeType", "MimeType"),
                    ("fileLocation", "FileLocation"),
                    ("hashValue", "HashValue"),
                )
            }
        }

        root = ET.fromstring(
            render_profile_xml(
                profile,
                {"appendix": ["one", "two"]},
                {"one": attachment(), "two": attachment()},
            )
        )

        self.assertEqual([child.tag for child in root], ["{urn:fixture}Appendix"])
        self.assertEqual(
            [child.tag for child in root[0]],
            ["{urn:item}AttachedFile", "{urn:item}AttachedFile"],
        )
        self.assertEqual(
            [child.tag for child in root[0][0]],
            [
                "{urn:item}FileName",
                "{urn:item}MimeType",
                "{urn:item}FileLocation",
                "{urn:item}HashValue",
            ],
        )

    def test_flattened_attachment_rejects_ignored_or_misspelled_declarations(self) -> None:
        profile = profile_with(
            {
                "appendix": {
                    "element": "Appendix",
                    "kind": "array",
                    "namespace": "default",
                    "itemElement": "AttachedFile",
                    "itemNamespace": "item",
                    "items": {
                        "node": {"kind": "attachment", "flatten": True}
                    },
                }
            }
        )
        profile["attachment"] = {
            "fields": {
                name: {"element": element, "namespace": "item"}
                for name, element in (
                    ("fileName", "FileName"),
                    ("mimeType", "MimeType"),
                    ("fileLocation", "FileLocation"),
                    ("hashValue", "HashValue"),
                )
            }
        }
        mutations = (
            {"element": "AttachedFile"},
            {"namespace": "item"},
            {"attributes": {"status": {"constant": "ignored"}}},
            {"source": "/appendix"},
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                candidate = copy.deepcopy(profile)
                candidate_node = (
                    candidate["mapping"]["fields"]["appendix"]["items"]["node"]
                )
                candidate_node.update(mutation)
                with self.assertRaisesRegex(
                    AssertionError, "flattened attachment mapping cannot declare ignored"
                ):
                    render_profile_xml(
                        candidate,
                        {"appendix": ["one"]},
                        {"one": attachment()},
                    )

        typo = copy.deepcopy(profile)
        typo_node = typo["mapping"]["fields"]["appendix"]["items"]["node"]
        del typo_node["flatten"]
        typo_node["flaten"] = True
        with self.assertRaisesRegex(AssertionError, "unsupported.*flaten"):
            render_profile_xml(typo, {"appendix": ["one"]}, {"one": attachment()})

    def test_flattened_attachment_rejects_illegal_contexts(self) -> None:
        top_level = profile_with(
            {"file": {"kind": "attachment", "flatten": True}}
        )
        with self.assertRaisesRegex(
            AssertionError, "only valid as an array item node"
        ):
            render_profile_xml(top_level, {"file": "one"}, {"one": attachment()})

        missing_item_element = profile_with(
            {
                "appendix": {
                    "element": "Appendix",
                    "kind": "array",
                    "namespace": "default",
                    "items": {
                        "node": {"kind": "attachment", "flatten": True}
                    },
                }
            }
        )
        with self.assertRaisesRegex(
            AssertionError, "with a declared itemElement"
        ):
            render_profile_xml(
                missing_item_element,
                {"appendix": ["one"]},
                {"one": attachment()},
            )

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
