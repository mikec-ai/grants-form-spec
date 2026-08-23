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
FIXTURES = ROOT / "tests/fixtures/grants-gov-xsd/sf424b-1.1"
DEPENDENCIES = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
FORM_XSDS = {
    "sf424b": (
        "SF424B-V1.1.xsd",
        "b0da616d262329e869b7c2a12146396fd8a279d2a1723521271c519f4571075d",
    ),
    "rr-sf424b": (
        "RRSF424_SF424B-V1.1.xsd",
        "511de9a5594a739ce596a33a92d3dec1bac2a32f193a2fe6b4799b45f29ff296",
    ),
    "mandatory-sf424b": (
        "Mandatory_SF424B-V1.1.xsd",
        "bcbe0010ba734ebeb0e3b6bd331a936d716b9896446231be90a11b005faf9579",
    ),
    "individual-sf424b": (
        "Individual_SF424B-V1.1.xsd",
        "1fe96cd37f1933f1c251efbbfbafae85c2e4869359f216a645024860ee29c983",
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
            child = ET.SubElement(
                parent,
                _qname(profile, node.get("namespace"), node["element"]),
            )
            child.text = str(value)
        elif node["kind"] == "group":
            child = ET.SubElement(
                parent,
                _qname(profile, node.get("namespace"), node["element"]),
            )
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


class Sf424bXmlTests(unittest.TestCase):
    def test_all_four_profiles_validate_against_exact_official_xsds(self) -> None:
        response = {
            "signature": "Alex Authorized",
            "title": "Executive Director",
            "applicantOrganization": "Example Research Organization",
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
                    document.findtext(f"{{{namespace}}}AuthorizedRepresentative/{{{namespace}}}RepresentativeName"),
                    "Alex Authorized",
                )
                self.assertEqual(
                    document.findtext(f"{{{namespace}}}ApplicantOrganizationName"),
                    "Example Research Organization",
                )
                self.assertEqual(
                    document.findtext(f"{{{namespace}}}SubmittedDate"),
                    "2026-08-23",
                )


if __name__ == "__main__":
    unittest.main()
