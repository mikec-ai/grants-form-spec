from __future__ import annotations

import hashlib
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
FORM_NS = "http://apply.grants.gov/forms/PHS398_CareerDevelopmentAwardSup_6_0-V6.0"
ATT_NS = "http://apply.grants.gov/system/Attachments-V1.0"
PROFILE = json.loads((
    ROOT / "dist/forms/phs398-career-development-supplemental/targets/grants-gov-xml.json"
).read_text())
FORM_XSD = (
    ROOT / "tests/fixtures/grants-gov-xsd/phs398-career-development-supplemental-6.0/"
    "PHS398_CareerDevelopmentAwardSup_6_0-V6.0.xsd"
)
SHARED_XSDS = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
FILES = {
    "PHS398_CareerDevelopmentAwardSup_6_0-V6.0.xsd": (
        FORM_XSD,
        "613641fc799a5c92d47928c98ebd90fad5d348b7637005929f0c0dc4a07e95c1",
    ),
    "Attachments-V1.0.xsd": (
        SHARED_XSDS / "Attachments-V1.0.xsd",
        "ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d",
    ),
    "Global-V1.0.xsd": (
        SHARED_XSDS / "Global-V1.0.xsd",
        "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb",
    ),
    "GlobalLibrary-V2.0.xsd": (
        SHARED_XSDS / "GlobalLibrary-V2.0.xsd",
        "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
    ),
    "UniversalCodes-V2.0.xsd": (
        SHARED_XSDS / "UniversalCodes-V2.0.xsd",
        "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
    ),
}
XSD_SET = ExactXsdFixture(
    entrypoint="PHS398_CareerDevelopmentAwardSup_6_0-V6.0.xsd",
    files=tuple(PinnedXsdFile(name, path, digest) for name, (path, digest) in FILES.items()),
    official_sha256="613641fc799a5c92d47928c98ebd90fad5d348b7637005929f0c0dc4a07e95c1",
)


def attachment(number: int) -> dict[str, str]:
    return {
        "fileName": f"career-{number}.pdf",
        "mimeType": "application/pdf",
        "fileLocation": f"files/career-{number}.pdf",
        "hashValue": hashlib.sha256(f"career-{number}".encode()).hexdigest(),
    }


class PHS398CareerDevelopmentSupplementalXmlTests(unittest.TestCase):
    def assert_valid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_minimum_response_validates_against_exact_official_xsd(self) -> None:
        response = {
            "researchStrategy": "1",
            "citizenship": {"usCitizenOrNational": "Y: Yes"},
        }
        xml = render_profile_xml(PROFILE, response, {"1": attachment(1)})
        root = ET.fromstring(xml)
        self.assertEqual(
            root.tag,
            f"{{{FORM_NS}}}PHS398_CareerDevelopmentAwardSup_6_0",
        )
        self.assertEqual(root.attrib, {f"{{{FORM_NS}}}FormVersion": "6.0"})
        self.assert_valid(xml)

    def test_full_wire_shape_preserves_source_names_and_appendix_limit(self) -> None:
        response = {
            "researchStrategy": "1",
            "institutionalEnvironment": "2",
            "appendix": ["3", "4"],
            "citizenship": {
                "usCitizenOrNational": "N: No",
                "nonUsCitizenStatus": "Temporary U.S. Visa",
                "permanentResidentByAward": "Y: Yes",
            },
        }
        attachments = {str(number): attachment(number) for number in range(1, 5)}
        xml = render_profile_xml(PROFILE, response, attachments)
        root = ET.fromstring(xml)
        container = root.find(f"{{{FORM_NS}}}CareerDevelopmentAwardAttachments")
        self.assertIsNotNone(container)
        assert container is not None
        self.assertIsNotNone(container.find(f"{{{FORM_NS}}}InsitutionalEnvironment"))
        appendix = container.find(f"{{{FORM_NS}}}Appendix")
        self.assertIsNotNone(appendix)
        assert appendix is not None
        self.assertEqual(
            [child.tag for child in appendix],
            [f"{{{ATT_NS}}}AttachedFile", f"{{{ATT_NS}}}AttachedFile"],
        )
        self.assert_valid(xml)


if __name__ == "__main__":
    unittest.main()
