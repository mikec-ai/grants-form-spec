from __future__ import annotations

import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from conformance.grants_gov_xml import (
    ExactXsdFixture,
    PinnedXsdFile,
    render_profile_xml,
    validate_exact_xsd,
)


ROOT = Path(__file__).parents[1]
FORM_NS = "http://apply.grants.gov/forms/PHS_AssignmentRequestForm_4_0-V4.0"
XSD_FIXTURE = ROOT / "tests/fixtures/grants-gov-xsd/phs-assignment-request-4.0/PHS_AssignmentRequestForm_4_0-V4.0.xsd"
DEPENDENCIES = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
XSD_HASHES = {
    "PHS_AssignmentRequestForm_4_0-V4.0.xsd": "7e697ee33ea6f72271c0d74fc48c61f4f81faa242a712a4c73e7898f6c4ab976",
    "GlobalLibrary-V2.0.xsd": "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
    "UniversalCodes-V2.0.xsd": "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
}
PROFILE = json.loads(
    (ROOT / "dist/forms/phs-assignment-request/targets/grants-gov-xml.json").read_text()
)
XSD_SET = ExactXsdFixture(
    entrypoint="PHS_AssignmentRequestForm_4_0-V4.0.xsd",
    files=tuple(
        PinnedXsdFile(
            name,
            XSD_FIXTURE if name.startswith("PHS_Assignment") else DEPENDENCIES / name,
            digest,
        )
        for name, digest in XSD_HASHES.items()
    ),
    official_sha256=XSD_HASHES["PHS_AssignmentRequestForm_4_0-V4.0.xsd"],
)


class PHSAssignmentRequestXmlTests(unittest.TestCase):
    def test_empty_optional_form_validates_against_exact_xsd(self) -> None:
        xml = render_profile_xml(PROFILE, {})
        validation = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(validation.returncode, 0, validation.stderr)

        root = ET.fromstring(xml)
        self.assertEqual(root.tag, f"{{{FORM_NS}}}PHS_AssignmentRequestForm_4_0")
        self.assertEqual(root.attrib[f"{{{FORM_NS}}}FormVersion"], "4.0")
        self.assertEqual(list(root), [])

    def test_full_boundary_response_preserves_fixed_wire_order_and_validates(self) -> None:
        response = {
            "suggestedAwardingComponent1": "NCI",
            "suggestedAwardingComponent2": "NHLBI",
            "suggestedAwardingComponent3": "NIAID",
            "suggestedStudySection1": "AIRT",
            "suggestedStudySection2": "ZRG1HDMR",
            "suggestedStudySection3": "B" * 20,
            "rationaleSuggestions": "R" * 1000,
            "expertise1": "E" * 40,
            "expertise2": "Genomics",
            "expertise3": "Immunology",
            "expertise4": "Clinical trials",
            "expertise5": "Biostatistics",
            "notReview": "N" * 1000,
        }
        xml = render_profile_xml(PROFILE, response)
        validation = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(validation.returncode, 0, validation.stderr)

        root = ET.fromstring(xml)
        self.assertEqual(
            [child.tag.removeprefix(f"{{{FORM_NS}}}") for child in root],
            [
                "SuggestedAwardingComponent1",
                "SuggestedAwardingComponent2",
                "SuggestedAwardingComponent3",
                "SuggestedStudySection1",
                "SuggestedStudySection2",
                "SuggestedStudySection3",
                "RationaleSuggestions",
                "Expertise1",
                "Expertise2",
                "Expertise3",
                "Expertise4",
                "Expertise5",
                "NotReview",
            ],
        )

    def test_over_limit_value_is_rejected_by_exact_xsd(self) -> None:
        xml = render_profile_xml(PROFILE, {"suggestedAwardingComponent1": "TOO-LONG"})
        validation = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertNotEqual(validation.returncode, 0)
        self.assertIn("maxLength", validation.stderr)


if __name__ == "__main__":
    unittest.main()
