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
FORM_NS = "http://apply.grants.gov/forms/NIFA_Supplemental_Info_1_2-V1.2"
PROFILE = json.loads(
    (ROOT / "dist/forms/nifa-supplemental/targets/grants-gov-xml.json").read_text()
)
FORM_XSD = (
    ROOT / "tests/fixtures/grants-gov-xsd/nifa-supplemental-1.2/"
    "NIFA_Supplemental_Info_1_2-V1.2.xsd"
)
SHARED_XSDS = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
FILES = {
    "NIFA_Supplemental_Info_1_2-V1.2.xsd": (
        FORM_XSD,
        "0a9461de86e7c807bcae9047ff12f1ba3f2753b5d7147caed200aab4649bf2fc",
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
    entrypoint="NIFA_Supplemental_Info_1_2-V1.2.xsd",
    files=tuple(PinnedXsdFile(name, path, digest) for name, (path, digest) in FILES.items()),
    official_sha256="9fd2d43797ec5fe17a9c29f073295e1c459b13d39346b3422de036d51c1d69e2",
)


def base_response() -> dict[str, object]:
    return {
        "fundingOpportunity": {
            "title": "Test NIFA Opportunity",
            "number": "NIFA-2026-1",
        },
        "program": {
            "programCodeName": "Agriculture Program",
            "programCode": "AG01",
        },
        "applicantType": {"applicantTypeCode": "X: Other (specify)"},
        "additionalApplicantType": {"additionalApplicantType": "Other"},
        "asapRecipientInformation": {"hasActiveAsapRecipientId": False},
        "keywords": "agriculture, portable forms",
    }


def attachment() -> dict[str, str]:
    return {
        "fileName": "conflicts.pdf",
        "mimeType": "application/pdf",
        "fileLocation": "files/conflicts.pdf",
        "hashValue": hashlib.sha256(b"conflicts").hexdigest(),
    }


class NifaSupplementalXmlTests(unittest.TestCase):
    def assert_valid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_minimal_response_preserves_order_and_validates(self) -> None:
        xml = render_profile_xml(PROFILE, base_response())
        root = ET.fromstring(xml)
        self.assertEqual(root.tag, f"{{{FORM_NS}}}NIFA_Supplemental_Info_1_2")
        self.assertEqual(
            [child.tag.split("}")[-1] for child in root],
            [
                "FundingOpportunity",
                "ProgramGroup",
                "ApplicantTypeCode",
                "AdditionalApplicantTypes",
                "ASAP_Recipient_Info",
                "KeyWords",
            ],
        )
        self.assertEqual(root.findtext(f"{{{FORM_NS}}}ASAP_Recipient_Info/{{{FORM_NS}}}ASAPID"), "N: No")
        self.assert_valid(xml)

    def test_full_response_maps_booleans_attachment_and_asap_identifier(self) -> None:
        response = base_response()
        response["supplementalApplicantTypes"] = {
            "alaskaNativeServingInstitution": True,
            "cooperativeExtensionService": False,
            "veterinarySchoolOrCollege": True,
        }
        response["asapRecipientInformation"] = {
            "hasActiveAsapRecipientId": True,
            "recipientId": "12345678",
        }
        response["conflictOfInterestList"] = "conflicts"
        xml = render_profile_xml(PROFILE, response, {"conflicts": attachment()})
        root = ET.fromstring(xml)
        supplemental = root.find(f"{{{FORM_NS}}}SupplementalApplicantType")
        assert supplemental is not None
        self.assertEqual([child.text for child in supplemental], ["Y: Yes", "N: No", "Y: Yes"])
        self.assertEqual(root.findtext(f"{{{FORM_NS}}}ASAP_Recipient_Info/{{{FORM_NS}}}ASAPID"), "Y: Yes")
        self.assertEqual(root.findtext(f"{{{FORM_NS}}}ASAP_Recipient_Info/{{{FORM_NS}}}RecipientID"), "12345678")
        self.assertIsNotNone(root.find(f"{{{FORM_NS}}}ConflictofInterestList/{{{FORM_NS}}}AttachedFile"))
        self.assert_valid(xml)

    def test_source_length_limit_is_enforced_by_exact_xsd(self) -> None:
        response = base_response()
        response["keywords"] = "x" * 101
        result = validate_exact_xsd(render_profile_xml(PROFILE, response), XSD_SET, profile=PROFILE)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
