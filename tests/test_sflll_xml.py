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
FORM_NS = "http://apply.grants.gov/forms/SFLLL_2_0-V2.0"
XSD_FIXTURE = ROOT / "tests/fixtures/grants-gov-xsd/sflll-2.0/SFLLL_2_0-V2.0.xsd"
DEPENDENCIES = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
XSD_HASHES = {
    "SFLLL_2_0-V2.0.xsd": "fff7449d00c715efb79d83b572bc7b1ef3e8171f6a9ba841436b26242e883664",
    "Global-V1.0.xsd": "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb",
    "GlobalLibrary-V2.0.xsd": "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
    "UniversalCodes-V2.0.xsd": "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
}


def _qname(profile: dict[str, Any], prefix: str | None, name: str) -> str:
    return f"{{{profile['namespaces'][prefix or 'default']}}}{name}"


def _pointer(response: dict[str, Any], pointer: str) -> Any:
    value: Any = response
    for step in pointer.removeprefix("/").split("/"):
        value = value[step.replace("~1", "/").replace("~0", "~")]
    return value


def _resolved_value(node: dict[str, Any], value: Any, root: dict[str, Any]) -> Any:
    if "constant" in node:
        value = node["constant"]
    elif source := node.get("source"):
        value = _pointer(root, source)
    if value_map := node.get("valueMap"):
        value = value_map[str(value)]
    return value


def _attributes(
    profile: dict[str, Any], node: dict[str, Any], root: dict[str, Any]
) -> dict[str, str]:
    result: dict[str, str] = {}
    for name, spec in node.get("attributes", {}).items():
        value = _resolved_value(spec, None, root)
        result[_qname(profile, node.get("namespace"), name)] = str(value)
    return result


def _add_node(
    parent: ET.Element,
    profile: dict[str, Any],
    node: dict[str, Any],
    value: Any,
    root: dict[str, Any],
) -> None:
    value = _resolved_value(node, value, root)
    kind = node["kind"]
    if kind == "value":
        leaf = ET.SubElement(parent, _qname(profile, node.get("namespace"), node["element"]))
        leaf.text = str(value).lower() if isinstance(value, bool) else str(value)
        return
    if kind == "group" and node.get("flatten"):
        _add_fields(parent, profile, node["fields"], value, root)
        return
    if kind in {"object", "group"}:
        child = ET.SubElement(
            parent,
            _qname(profile, node.get("namespace"), node["element"]),
            _attributes(profile, node, root),
        )
        _add_fields(child, profile, node["fields"], value, root)
        return
    if kind == "array":
        collection = ET.SubElement(
            parent,
            _qname(profile, node.get("namespace"), node["element"]),
            _attributes(profile, node, root),
        )
        for item in value:
            item_parent = ET.SubElement(
                collection,
                _qname(profile, node.get("itemNamespace"), node["itemElement"]),
            )
            _add_fields(item_parent, profile, node["items"]["fields"], item, root)
        return
    raise AssertionError(f"unsupported SF-LLL mapping kind: {kind}")


def _add_fields(
    parent: ET.Element,
    profile: dict[str, Any],
    fields: dict[str, Any],
    response: dict[str, Any],
    root: dict[str, Any],
) -> None:
    for name, node in fields.items():
        if "constant" in node or node["kind"] == "group":
            value: Any = response
        elif source := node.get("source"):
            try:
                value = _pointer(root, source)
            except KeyError:
                continue
        else:
            value = response.get(name)
        if value is not None:
            _add_node(parent, profile, node, value, root)


def render_xml(response: dict[str, Any]) -> bytes:
    profile = json.loads(
        (ROOT / "dist/forms/sflll/targets/grants-gov-xml.json").read_text()
    )
    for prefix, namespace in profile["namespaces"].items():
        if prefix not in {"default", profile["root"]["namespacePrefix"]}:
            ET.register_namespace(prefix, namespace)
    ET.register_namespace("sflll", profile["namespaces"]["default"])
    root = ET.Element(_qname(profile, "default", profile["root"]["element"]))
    for name, value in profile["root"]["attributes"].items():
        root.set(_qname(profile, "default", name), str(value))
    _add_fields(root, profile, profile["mapping"]["fields"], response, response)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def validate_exact_xsd(xml: bytes) -> subprocess.CompletedProcess[str]:
    xmllint = shutil.which("xmllint")
    if xmllint is None:
        raise AssertionError("xmllint is required to validate the pinned official XSD fixture")
    fixture_paths = {
        "SFLLL_2_0-V2.0.xsd": XSD_FIXTURE,
        **{name: DEPENDENCIES / name for name in XSD_HASHES if name != "SFLLL_2_0-V2.0.xsd"},
    }
    for name, expected in XSD_HASHES.items():
        actual = hashlib.sha256(fixture_paths[name].read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"pinned XSD digest mismatch for {name}: {actual}")
    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        for name, path in fixture_paths.items():
            source = path.read_text()
            for dependency in XSD_HASHES:
                source = source.replace(
                    f"https://apply07.grants.gov/apply/system/schemas/{dependency}",
                    dependency,
                )
            (temp / name).write_text(source)
        xml_path = temp / "response.xml"
        xml_path.write_bytes(xml)
        return subprocess.run(
            ["xmllint", "--noout", "--schema", str(temp / "SFLLL_2_0-V2.0.xsd"), str(xml_path)],
            text=True,
            capture_output=True,
            check=False,
        )


def _name(first: str, last: str) -> dict[str, str]:
    return {"firstName": first, "lastName": last}


def _organization(name: str, street: str, city: str) -> dict[str, Any]:
    return {
        "organizationName": name,
        "address": {"street1": street, "city": city, "state": "DC: District of Columbia"},
        "congressionalDistrict": "DC-000",
    }


class SflllXmlTests(unittest.TestCase):
    def test_full_material_change_subaward_response_validates_against_pinned_xsd(self) -> None:
        response = {
            "federalActionType": "Grant",
            "federalActionStatus": "PostAward",
            "reportType": "MaterialChange",
            "materialChange": {
                "year": "2026",
                "quarter": "3",
                "lastReportDate": "2026-03-31",
            },
            "reportingEntityType": "SubAwardee",
            "reportingOrganization": _organization("Subawardee Research", "10 Local Way", "Washington"),
            "tier": 0,
            "primeOrganization": _organization("Prime Research", "1 Prime Way", "Washington"),
            "federalAgencyDepartment": "Department of Research",
            "federalProgram": {
                "name": "Research Program",
                "assistanceListingNumber": "12.345",
            },
            "federalActionNumber": "AWARD-123",
            "awardAmount": "1234567890123.45",
            "lobbyingRegistrant": {
                "name": _name("Alex", "Registrant"),
                "address": {"street1": "4 Lobby Lane", "city": "Washington"},
            },
            "individualsPerformingServices": [
                {"name": _name("Jamie", "One")},
                {
                    "name": _name("Taylor", "Two"),
                    "address": {"street1": "5 Service St", "city": "Washington"},
                },
            ],
            "signatureBlock": {
                "name": _name("Sam", "Signer"),
                "title": "Director",
                "phone": "202-555-0100",
                "signedDate": "2026-08-23",
                "signature": "Sam Signer",
            },
        }
        xml = render_xml(response)
        validation = validate_exact_xsd(xml)
        self.assertEqual(validation.returncode, 0, validation.stderr)

        root = ET.fromstring(xml)
        report_entity = root.find(f"{{{FORM_NS}}}ReportEntity")
        self.assertIsNotNone(report_entity)
        assert report_entity is not None
        self.assertEqual(report_entity.attrib[f"{{{FORM_NS}}}ReportEntityType"], "SubAwardee")
        self.assertEqual(report_entity.findtext(f"{{{FORM_NS}}}ReportEntityIsPrime"), "N: No")
        prime = report_entity.find(f"{{{FORM_NS}}}PrimeIfSubawardee")
        self.assertIsNotNone(prime)
        assert prime is not None
        self.assertEqual(prime.findtext(f"{{{FORM_NS}}}EntityType"), "Prime")
        individuals = root.findall(
            f"{{{FORM_NS}}}IndividualsPerformingServices/{{{FORM_NS}}}Individual"
        )
        self.assertEqual(len(individuals), 2)


if __name__ == "__main__":
    unittest.main()
