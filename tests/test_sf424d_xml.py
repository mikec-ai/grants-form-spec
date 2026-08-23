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
FIXTURES = ROOT / "tests/fixtures/grants-gov-xsd/sf424d-family-1.1"
DEPENDENCIES = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
FORM_XSDS = {
    "sf424d": (
        "SF424D-V1.1.xsd",
        "22026ea7130a01b8674e1c3ce1668e1b57d5be65498b5a76042eb80d38de77f1",
    ),
    "mandatory-sf424d": (
        "Mandatory_SF424D-V1.1.xsd",
        "6685f2c19329db0ee959e2453cbcaf749e9bb2d7f45cb96892d9a4e71d87f68d",
    ),
    "individual-sf424d": (
        "Individual_SF424D-V1.1.xsd",
        "52187d42b9ca30cf1f2f95de50be13bbd9ae333ede4b843e8c43b23db4489356",
    ),
}
DEPENDENCY_HASHES = {
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


def _add_fields(
    parent: ET.Element,
    profile: dict[str, Any],
    fields: dict[str, Any],
    response: dict[str, Any],
    root_response: dict[str, Any],
) -> None:
    for name, node in fields.items():
        if "constant" in node:
            value = node["constant"]
        elif node["kind"] == "group":
            value = response
        elif source := node.get("source"):
            try:
                value = _pointer(root_response, source)
            except KeyError:
                continue
        else:
            value = response.get(name)
        if value is None:
            continue
        if node["kind"] == "value":
            child = ET.SubElement(parent, _qname(profile, node.get("namespace"), node["element"]))
            child.text = str(value)
        elif node["kind"] == "group":
            child = ET.SubElement(parent, _qname(profile, node.get("namespace"), node["element"]))
            _add_fields(child, profile, node["fields"], value, root_response)
        else:
            raise AssertionError(f"unsupported assurance mapping kind: {node['kind']}")


def render_xml(form_id: str, response: dict[str, Any]) -> bytes:
    profile = json.loads(
        (ROOT / f"dist/forms/{form_id}/targets/grants-gov-xml.json").read_text()
    )
    for prefix, namespace in profile["namespaces"].items():
        if prefix != "default":
            ET.register_namespace(prefix, namespace)
    root = ET.Element(_qname(profile, "default", profile["root"]["element"]))
    for name, value in profile["root"].get("attributes", {}).items():
        if ":" in name:
            prefix, local_name = name.split(":", 1)
        else:
            prefix, local_name = "default", name
        root.set(_qname(profile, prefix, local_name), str(value))
    _add_fields(root, profile, profile["mapping"]["fields"], response, response)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def validate_exact_xsd(form_id: str, xml: bytes) -> subprocess.CompletedProcess[str]:
    xmllint = shutil.which("xmllint")
    if xmllint is None:
        raise AssertionError("xmllint is required to validate the pinned official XSD fixtures")
    xsd_name, xsd_hash = FORM_XSDS[form_id]
    xsd = FIXTURES / xsd_name
    if hashlib.sha256(xsd.read_bytes()).hexdigest() != xsd_hash:
        raise AssertionError(f"pinned XSD digest mismatch for {xsd_name}")
    for name, expected in DEPENDENCY_HASHES.items():
        actual = hashlib.sha256((DEPENDENCIES / name).read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"pinned XSD dependency digest mismatch for {name}")

    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        paths = {xsd_name: xsd, **{name: DEPENDENCIES / name for name in DEPENDENCY_HASHES}}
        for name, path in paths.items():
            source = path.read_text()
            for dependency in DEPENDENCY_HASHES:
                source = source.replace(
                    f"https://apply07.grants.gov/apply/system/schemas/{dependency}",
                    dependency,
                )
            (temp / name).write_text(source)
        xml_path = temp / "response.xml"
        xml_path.write_bytes(xml)
        return subprocess.run(
            ["xmllint", "--noout", "--schema", str(temp / xsd_name), str(xml_path)],
            text=True,
            capture_output=True,
            check=False,
        )


class Sf424dXmlTests(unittest.TestCase):
    def test_all_three_profiles_validate_against_exact_official_xsds(self) -> None:
        response = {
            "signature": "Alex Authorized",
            "title": "Executive Director",
            "applicantOrganization": "Example Construction Organization",
            "signedDate": "2026-08-23",
        }
        for form_id in FORM_XSDS:
            with self.subTest(form_id=form_id):
                xml = render_xml(form_id, response)
                validation = validate_exact_xsd(form_id, xml)
                self.assertEqual(validation.returncode, 0, validation.stderr)

                profile = json.loads(
                    (ROOT / f"dist/forms/{form_id}/targets/grants-gov-xml.json").read_text()
                )
                document = ET.fromstring(xml)
                namespace = profile["namespaces"]["default"]
                self.assertEqual(
                    document.findtext(
                        f"{{{namespace}}}AuthorizedRepresentative/"
                        f"{{{namespace}}}RepresentativeName"
                    ),
                    "Alex Authorized",
                )
                self.assertEqual(
                    document.findtext(f"{{{namespace}}}ApplicantOrganizationName"),
                    "Example Construction Organization",
                )
                self.assertEqual(
                    document.findtext(f"{{{namespace}}}SubmittedDate"),
                    "2026-08-23",
                )


if __name__ == "__main__":
    unittest.main()
