from __future__ import annotations

import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from conformance.grants_gov_xml import ExactXsdFixture, PinnedXsdFile, render_profile_xml, validate_exact_xsd


ROOT = Path(__file__).parents[1]
FORM_NS = "http://apply.grants.gov/forms/Project_AbstractSummary_2_0-V2.0"
FORM_XSD = ROOT / "tests/fixtures/grants-gov-xsd/project-abstract-summary-2.0/Project_AbstractSummary_2_0-V2.0.xsd"
SHARED = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
PROFILE = json.loads(
    (ROOT / "dist/forms/project-abstract-summary/targets/grants-gov-xml.json").read_text()
)
FILES = {
    "Project_AbstractSummary_2_0-V2.0.xsd": (
        FORM_XSD,
        "3022f177a7f0ebb9a1888e9b8a4a644ed2ba7857a775d2d05642a9fbd1cc008f",
    ),
    "Attachments-V1.0.xsd": (
        SHARED / "Attachments-V1.0.xsd",
        "ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d",
    ),
    "Global-V1.0.xsd": (
        SHARED / "Global-V1.0.xsd",
        "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb",
    ),
    "GlobalLibrary-V2.0.xsd": (
        SHARED / "GlobalLibrary-V2.0.xsd",
        "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
    ),
    "UniversalCodes-V2.0.xsd": (
        SHARED / "UniversalCodes-V2.0.xsd",
        "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
    ),
}
XSD_SET = ExactXsdFixture(
    entrypoint="Project_AbstractSummary_2_0-V2.0.xsd",
    files=tuple(PinnedXsdFile(name, path, digest) for name, (path, digest) in FILES.items()),
    official_sha256="3022f177a7f0ebb9a1888e9b8a4a644ed2ba7857a775d2d05642a9fbd1cc008f",
)


def minimal() -> dict[str, str]:
    return {
        "fundingOpportunityNumber": "HHS-2026-EXAMPLE",
        "applicantName": "Example Research Organization",
        "projectTitle": "A concise project title",
        "projectAbstract": "A plain-language summary of the proposed project.",
    }


class ProjectAbstractSummaryXmlTests(unittest.TestCase):
    def assert_valid(self, response: dict[str, str]) -> bytes:
        xml = render_profile_xml(PROFILE, response)
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return xml

    def test_minimal_wire_root_namespace_version_and_required_sequence(self) -> None:
        root = ET.fromstring(self.assert_valid(minimal()))
        self.assertEqual(root.tag, f"{{{FORM_NS}}}Project_AbstractSummary_2_0")
        self.assertEqual(root.attrib, {f"{{{FORM_NS}}}FormVersion": "2.0"})
        self.assertEqual(
            [child.tag.rsplit("}", 1)[-1] for child in root],
            ["FundingOpportunityNumber", "OrganizationName", "ProjectTitle", "ProjectAbstract"],
        )

    def test_full_response_preserves_optional_cfda_wire_name_order_and_values(self) -> None:
        response = minimal() | {"assistanceListingNumber": "93.001"}
        root = ET.fromstring(self.assert_valid(response))
        self.assertEqual(
            [(child.tag.rsplit("}", 1)[-1], child.text) for child in root],
            [
                ("FundingOpportunityNumber", "HHS-2026-EXAMPLE"),
                ("CFDANumber", "93.001"),
                ("OrganizationName", "Example Research Organization"),
                ("ProjectTitle", "A concise project title"),
                ("ProjectAbstract", "A plain-language summary of the proposed project."),
            ],
        )

    def test_exact_xsd_rejects_source_boundaries(self) -> None:
        for field, value in (
            ("fundingOpportunityNumber", "F" * 41),
            ("assistanceListingNumber", "9" * 16),
            ("applicantName", "O" * 61),
            ("projectTitle", "T" * 251),
            ("projectAbstract", "A" * 4001),
        ):
            with self.subTest(field=field):
                response = minimal() | {field: value}
                result = validate_exact_xsd(
                    render_profile_xml(PROFILE, response), XSD_SET, profile=PROFILE
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("maxLength", result.stderr)


if __name__ == "__main__":
    unittest.main()
