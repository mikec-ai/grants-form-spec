from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


ROOT = Path(__file__).parents[1]
FORM_NS = "http://apply.grants.gov/forms/RR_KeyPersonExpanded_4_0-V4.0"
ATTACHMENTS_NS = "http://apply.grants.gov/system/Attachments-V1.0"
GLOBAL_NS = "http://apply.grants.gov/system/Global-V1.0"
XSD_FIXTURES = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
XSD_HASHES = {
    "RR_KeyPersonExpanded_4_0-V4.0.xsd": "c1522304f37bb91a1fc18f2b84656c570581969f9c1795d18352bc273d691b8b",
    "Attachments-V1.0.xsd": "ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d",
    "Global-V1.0.xsd": "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb",
    "GlobalLibrary-V2.0.xsd": "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
    "UniversalCodes-V2.0.xsd": "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
}


def _qname(profile: dict[str, Any], prefix: str | None, element: str) -> str:
    namespace = profile["namespaces"][prefix or "default"]
    return f"{{{namespace}}}{element}"


def _pointer(response: dict[str, Any], pointer: str) -> Any:
    value: Any = response
    for step in pointer.removeprefix("/").split("/"):
        value = value[step.replace("~1", "/").replace("~0", "~")]
    return value


def _add_attachment(
    parent: ET.Element,
    profile: dict[str, Any],
    node: dict[str, Any],
    attachment_id: str,
    attachments: dict[str, dict[str, str]],
) -> None:
    attachment = attachments[attachment_id]
    leaf_parent = parent
    if container := node.get("container"):
        leaf_parent = ET.SubElement(
            parent, _qname(profile, container["namespace"], container["element"])
        )
    leaf = ET.SubElement(
        leaf_parent, _qname(profile, node.get("namespace"), node["element"])
    )
    wire = profile["attachment"]["fields"]
    for field_name in ("fileName", "mimeType", "fileLocation", "hashValue"):
        declaration = wire[field_name]
        child = ET.SubElement(
            leaf,
            _qname(profile, declaration["namespace"], declaration["element"]),
        )
        if field_name == "fileLocation":
            child.set(
                _qname(profile, declaration["namespace"], "href"),
                attachment[field_name],
            )
        else:
            child.text = attachment[field_name]
        if field_name == "hashValue":
            child.set(_qname(profile, declaration["namespace"], "hashAlgorithm"), "SHA-256")


def _add_node(
    parent: ET.Element,
    profile: dict[str, Any],
    node: dict[str, Any],
    value: Any,
    root_response: dict[str, Any],
    attachments: dict[str, dict[str, str]],
) -> None:
    kind = node["kind"]
    if kind == "attachment":
        _add_attachment(parent, profile, node, value, attachments)
        return
    if kind == "value":
        leaf_parent = parent
        if container := node.get("container"):
            leaf_parent = ET.SubElement(
                parent, _qname(profile, container["namespace"], container["element"])
            )
        leaf = ET.SubElement(
            leaf_parent, _qname(profile, node.get("namespace"), node["element"])
        )
        leaf.text = str(value).lower() if isinstance(value, bool) else str(value)
        return
    if kind in {"object", "group"}:
        child = ET.SubElement(parent, _qname(profile, node.get("namespace"), node["element"]))
        source = _pointer(root_response, node["source"]) if node.get("source") else value
        _add_fields(child, profile, node["fields"], source, root_response, attachments)
        return
    if kind == "array":
        item_element = node.get("itemElement")
        repeat_outer = not item_element or node.get("repeatElementPerItem", False)
        collection = None
        if not repeat_outer:
            collection = ET.SubElement(
                parent, _qname(profile, node.get("namespace"), node["element"])
            )
        for item in value:
            outer = (
                ET.SubElement(parent, _qname(profile, node.get("namespace"), node["element"]))
                if repeat_outer
                else collection
            )
            assert outer is not None
            item_parent = outer
            if item_element:
                item_parent = ET.SubElement(
                    outer, _qname(profile, node.get("itemNamespace"), item_element)
                )
            _add_fields(
                item_parent, profile, node["items"]["fields"], item, root_response, attachments
            )
        return
    raise AssertionError(f"unsupported test mapping kind: {kind}")


def _add_fields(
    parent: ET.Element,
    profile: dict[str, Any],
    fields: dict[str, Any],
    response: dict[str, Any],
    root_response: dict[str, Any],
    attachments: dict[str, dict[str, str]],
) -> None:
    for name, node in fields.items():
        if node["kind"] == "group":
            value: Any = response
        elif node.get("source"):
            value = _pointer(root_response, node["source"])
        else:
            value = response.get(name)
        if value is not None:
            _add_node(parent, profile, node, value, root_response, attachments)


def render_xml(
    response: dict[str, Any], attachments: dict[str, dict[str, str]]
) -> bytes:
    profile = json.loads(
        (ROOT / "dist/forms/rr-key-person-expanded/targets/grants-gov-xml.json").read_text()
    )
    for prefix, namespace in profile["namespaces"].items():
        if prefix not in {"default", profile["root"]["namespacePrefix"]}:
            ET.register_namespace(prefix, namespace)
    ET.register_namespace("rr", profile["namespaces"]["default"])
    root = ET.Element(_qname(profile, "default", profile["root"]["element"]))
    for name, value in profile["root"]["attributes"].items():
        root.set(_qname(profile, "default", name), str(value))
    _add_fields(root, profile, profile["mapping"]["fields"], response, response, attachments)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def validate_exact_xsd(xml: bytes) -> subprocess.CompletedProcess[str]:
    xmllint = shutil.which("xmllint")
    if xmllint is None:
        raise AssertionError("xmllint is required to validate the pinned official XSD fixture")
    for name, expected in XSD_HASHES.items():
        actual = hashlib.sha256((XSD_FIXTURES / name).read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"pinned XSD digest mismatch for {name}: {actual}")
    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        for name in XSD_HASHES:
            source = (XSD_FIXTURES / name).read_text()
            for dependency in XSD_HASHES:
                source = source.replace(
                    f"https://apply07.grants.gov/apply/system/schemas/{dependency}",
                    dependency,
                )
            (temp / name).write_text(source)
        xml_path = temp / "response.xml"
        xml_path.write_bytes(xml)
        return subprocess.run(
            [xmllint, "--noout", "--schema", str(temp / "RR_KeyPersonExpanded_4_0-V4.0.xsd"), str(xml_path)],
            text=True,
            capture_output=True,
            check=False,
        )


def _person(first_name: str, last_name: str, *, country: str, **address: str) -> dict[str, Any]:
    return {
        "name": {"firstName": first_name, "lastName": last_name},
        "address": {
            "street1": "1 Research Way",
            "city": "Science City",
            "country": country,
            **address,
        },
        "phone": "202-555-0100",
        "email": f"{first_name.lower()}@example.org",
        "projectRole": "PD/PI",
    }


class RRKeyPersonExpandedXmlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.attachments = {
            name: {
                "fileName": f"{name}.pdf",
                "mimeType": "application/pdf",
                "fileLocation": f"https://files.example.org/{name}.pdf",
                "hashValue": "YWJj",
            }
            for name in (
                "pi-bio",
                "senior-us-bio",
                "senior-us-support",
                "senior-foreign-bio",
                "senior-foreign-support",
                "overflow-profiles",
                "overflow-bios",
                "overflow-support",
            )
        }

    def assert_attachment(
        self,
        parent: ET.Element,
        wrapper_name: str,
        leaf_name: str,
        attachment_id: str,
    ) -> None:
        wrapper_qname = f"{{{FORM_NS}}}{wrapper_name}"
        wrappers = parent.findall(wrapper_qname)
        self.assertEqual(len(wrappers), 1)
        wrapper = wrappers[0]
        leaf_qname = f"{{{FORM_NS}}}{leaf_name}"
        self.assertEqual([child.tag for child in wrapper], [leaf_qname])
        leaf = wrapper[0]
        self.assertEqual(
            [child.tag for child in leaf],
            [
                f"{{{ATTACHMENTS_NS}}}FileName",
                f"{{{ATTACHMENTS_NS}}}MimeType",
                f"{{{ATTACHMENTS_NS}}}FileLocation",
                f"{{{GLOBAL_NS}}}HashValue",
            ],
        )
        attachment = self.attachments[attachment_id]
        self.assertEqual(leaf[0].text, attachment["fileName"])
        self.assertEqual(leaf[1].text, attachment["mimeType"])
        self.assertIsNone(leaf[2].text)
        self.assertEqual(
            leaf[2].attrib,
            {f"{{{ATTACHMENTS_NS}}}href": attachment["fileLocation"]},
        )
        self.assertEqual(leaf[3].text, attachment["hashValue"])
        self.assertEqual(
            leaf[3].attrib,
            {f"{{{GLOBAL_NS}}}hashAlgorithm": "SHA-256"},
        )

    def test_pi_multiple_people_and_attachments_validate_against_exact_xsd(self) -> None:
        pi = _person(
            "Ada", "Lovelace", country="USA: UNITED STATES",
            state="CA: California", zipCode="940431234",
        )
        pi["biographicalSketch"] = "pi-bio"
        senior_us = _person(
            "Grace", "Hopper", country="USA: UNITED STATES",
            state="VA: Virginia", zipCode="222011234",
        )
        senior_us.update({
            "projectRole": "Co-Investigator",
            "biographicalSketch": "senior-us-bio",
            "currentPendingSupport": "senior-us-support",
        })
        senior_foreign = _person(
            "Katherine", "Johnson", country="CAN: CANADA",
            province="Ontario", zipCode="K1A0B1",
        )
        senior_foreign.update({
            "projectRole": "Co-Investigator",
            "biographicalSketch": "senior-foreign-bio",
            "currentPendingSupport": "senior-foreign-support",
        })
        response = {
            "principalInvestigator": pi,
            "seniorKeyPersons": [senior_us, senior_foreign],
            "additionalProfiles": "overflow-profiles",
            "additionalBiographicalSketches": "overflow-bios",
            "additionalCurrentPendingSupport": "overflow-support",
        }

        xml = render_xml(response, self.attachments)
        root = ET.fromstring(xml)
        self.assertEqual(
            [child.tag for child in root],
            [
                f"{{{FORM_NS}}}PDPI",
                f"{{{FORM_NS}}}KeyPerson",
                f"{{{FORM_NS}}}KeyPerson",
                f"{{{FORM_NS}}}AdditionalProfilesAttached",
                f"{{{FORM_NS}}}BioSketchsAttached",
                f"{{{FORM_NS}}}SupportsAttached",
            ],
        )

        pdpis = root.findall(f"{{{FORM_NS}}}PDPI")
        self.assertEqual(len(pdpis), 1)
        self.assertEqual(
            [child.tag for child in pdpis[0]],
            [f"{{{FORM_NS}}}Profile"],
        )
        pi_profile = pdpis[0][0]
        self.assertEqual(
            [child.tag for child in pi_profile],
            [
                f"{{{FORM_NS}}}Name",
                f"{{{FORM_NS}}}Address",
                f"{{{FORM_NS}}}Phone",
                f"{{{FORM_NS}}}Email",
                f"{{{FORM_NS}}}ProjectRole",
                f"{{{FORM_NS}}}BioSketchsAttached",
            ],
        )
        self.assert_attachment(
            pi_profile, "BioSketchsAttached", "BioSketchAttached", "pi-bio"
        )

        key_people = root.findall(f"{{{FORM_NS}}}KeyPerson")
        self.assertEqual(len(key_people), 2)
        profiles: list[ET.Element] = []
        for key_person in key_people:
            self.assertEqual(
                [child.tag for child in key_person],
                [f"{{{FORM_NS}}}Profile"],
            )
            profile = key_person[0]
            profiles.append(profile)
            self.assertEqual(
                [child.tag for child in profile],
                [
                    f"{{{FORM_NS}}}Name",
                    f"{{{FORM_NS}}}Address",
                    f"{{{FORM_NS}}}Phone",
                    f"{{{FORM_NS}}}Email",
                    f"{{{FORM_NS}}}ProjectRole",
                    f"{{{FORM_NS}}}BioSketchsAttached",
                    f"{{{FORM_NS}}}SupportsAttached",
                ],
            )

        self.assert_attachment(
            profiles[0], "BioSketchsAttached", "BioSketchAttached", "senior-us-bio"
        )
        self.assert_attachment(
            profiles[0], "SupportsAttached", "SupportAttached", "senior-us-support"
        )
        self.assert_attachment(
            profiles[1],
            "BioSketchsAttached",
            "BioSketchAttached",
            "senior-foreign-bio",
        )
        self.assert_attachment(
            profiles[1],
            "SupportsAttached",
            "SupportAttached",
            "senior-foreign-support",
        )
        self.assert_attachment(
            root,
            "AdditionalProfilesAttached",
            "AdditionalProfileAttached",
            "overflow-profiles",
        )
        self.assert_attachment(
            root, "BioSketchsAttached", "BioSketchAttached", "overflow-bios"
        )
        self.assert_attachment(
            root, "SupportsAttached", "SupportAttached", "overflow-support"
        )

        result = validate_exact_xsd(xml)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_official_xsd_rejects_state_and_province_together(self) -> None:
        pi = _person(
            "Ada", "Lovelace", country="USA: UNITED STATES",
            state="CA: California", province="California", zipCode="940431234",
        )
        pi["biographicalSketch"] = "pi-bio"

        result = validate_exact_xsd(
            render_xml({"principalInvestigator": pi}, self.attachments)
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Province", result.stderr)

    def test_array_with_item_element_defaults_to_one_collection_wrapper(self) -> None:
        profile = {"namespaces": {"default": "urn:example"}}
        node = {
            "element": "Items",
            "kind": "array",
            "itemElement": "Item",
            "itemNamespace": "default",
            "items": {
                "fields": {
                    "name": {"element": "Name", "kind": "value", "namespace": "default"}
                }
            },
        }
        root = ET.Element("root")

        _add_node(
            root,
            profile,
            node,
            [{"name": "first"}, {"name": "second"}],
            {},
            {},
        )

        self.assertEqual([child.tag for child in root], ["{urn:example}Items"])
        self.assertEqual(
            [child.tag for child in root[0]],
            ["{urn:example}Item", "{urn:example}Item"],
        )
        self.assertEqual([item[0].text for item in root[0]], ["first", "second"])


if __name__ == "__main__":
    unittest.main()
