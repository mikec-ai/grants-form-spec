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
FORM_NS = "http://apply.grants.gov/forms/CD511-V1.1"
XSD_FIXTURE = ROOT / "tests/fixtures/grants-gov-xsd/cd511-1.1/CD511-V1.1.xsd"
DEPENDENCIES = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
NORMALIZED_XSD_SHA256 = "39288644f29c625fa1e0ec657c8bf9323d3e3a2dd0fd3007994342e65411fdac"
OFFICIAL_XSD_SHA256 = "f13c05b8e62fe1e7cf0198053f79fdd34efe4b7d10b56974d27a7dd45d013fde"
DEPENDENCY_NAMES = [
    "Attachments-V1.0.xsd",
    "Global-V1.0.xsd",
    "GlobalLibrary-V2.0.xsd",
    "UniversalCodes-V2.0.xsd",
]


def qname(profile: dict[str, Any], prefix: str | None, name: str) -> str:
    return f"{{{profile['namespaces'][prefix or 'default']}}}{name}"


def add_fields(
    parent: ET.Element,
    profile: dict[str, Any],
    fields: dict[str, Any],
    response: dict[str, Any],
) -> None:
    for name, node in fields.items():
        value = response.get(name)
        if value is None:
            continue
        child = ET.SubElement(parent, qname(profile, node.get("namespace"), node["element"]))
        if node["kind"] == "value":
            child.text = str(value)
        elif node["kind"] == "object":
            add_fields(child, profile, node["fields"], value)
        else:
            raise AssertionError(f"unsupported CD-511 mapping kind: {node['kind']}")


def render_xml(response: dict[str, Any]) -> bytes:
    profile = json.loads(
        (ROOT / "dist/forms/cd511/targets/grants-gov-xml.json").read_text()
    )
    ET.register_namespace("cd511", profile["namespaces"]["default"])
    ET.register_namespace("globLib", profile["namespaces"]["globLib"])
    root = ET.Element(qname(profile, "default", profile["root"]["element"]))
    for name, value in profile["root"]["attributes"].items():
        root.set(qname(profile, "default", name), str(value))
    add_fields(root, profile, profile["mapping"]["fields"], response)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def validate_exact_xsd(xml: bytes) -> subprocess.CompletedProcess[str]:
    xmllint = shutil.which("xmllint")
    if xmllint is None:
        raise AssertionError("xmllint is required to validate the pinned official XSD fixture")
    if hashlib.sha256(XSD_FIXTURE.read_bytes()).hexdigest() != NORMALIZED_XSD_SHA256:
        raise AssertionError("normalized CD-511 XSD fixture digest mismatch")
    profile = json.loads(
        (ROOT / "dist/forms/cd511/targets/grants-gov-xml.json").read_text()
    )
    if profile["xsd"]["sha256"] != OFFICIAL_XSD_SHA256:
        raise AssertionError("official CD-511 XSD source digest mismatch")

    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        paths = {"CD511-V1.1.xsd": XSD_FIXTURE}
        paths.update({name: DEPENDENCIES / name for name in DEPENDENCY_NAMES})
        for name, path in paths.items():
            source = path.read_text()
            for dependency in DEPENDENCY_NAMES:
                source = source.replace(
                    f"https://apply07.grants.gov/apply/system/schemas/{dependency}",
                    dependency,
                )
            (temp / name).write_text(source)
        xml_path = temp / "response.xml"
        xml_path.write_bytes(xml)
        return subprocess.run(
            ["xmllint", "--noout", "--schema", str(temp / "CD511-V1.1.xsd"), str(xml_path)],
            text=True,
            capture_output=True,
            check=False,
        )


class CD511XmlTests(unittest.TestCase):
    def test_full_response_validates_against_pinned_xsd(self) -> None:
        response = {
            "applicantName": "Research Organization",
            "awardNumber": "AWARD-123",
            "projectName": "Portable Forms",
            "contactPerson": {"firstName": "Alex", "lastName": "Applicant"},
            "contactPersonTitle": "Director",
            "signature": "Alex Applicant",
            "submittedDate": "2026-08-23",
        }
        xml = render_xml(response)
        validation = validate_exact_xsd(xml)
        self.assertEqual(validation.returncode, 0, validation.stderr)

        root = ET.fromstring(xml)
        self.assertEqual(root.findtext(f"{{{FORM_NS}}}OrganizationName"),
                         "Research Organization")
        self.assertEqual(root.findtext(f"{{{FORM_NS}}}AwardNumber"), "AWARD-123")
        self.assertEqual(root.findtext(f"{{{FORM_NS}}}SubmittedDate"), "2026-08-23")


if __name__ == "__main__":
    unittest.main()
