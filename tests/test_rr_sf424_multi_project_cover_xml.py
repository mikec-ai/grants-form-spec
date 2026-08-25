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
PROFILE = json.loads(
    (
        ROOT
        / "dist/forms/rr-sf424-multi-project-cover/targets/grants-gov-xml.json"
    ).read_text()
)
FORM_XSDS = (
    ROOT
    / "tests/fixtures/grants-gov-xsd/rr-sf424-multi-project-cover-4.0"
)
SHARED_XSDS = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
XSD_SET = ExactXsdFixture(
    entrypoint="RR_SF424_Multi_Project_Cover_4_0-V4.0.xsd",
    files=(
        PinnedXsdFile(
            "RR_SF424_Multi_Project_Cover_4_0-V4.0.xsd",
            FORM_XSDS / "RR_SF424_Multi_Project_Cover_4_0-V4.0.xsd",
            "5d5599068d721e6554fa442df88711f8d9386a5fafc18b01cb1d1becc41f84e7",
        ),
        PinnedXsdFile(
            "Attachments-V1.0.xsd",
            SHARED_XSDS / "Attachments-V1.0.xsd",
            "ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d",
        ),
        PinnedXsdFile(
            "Global-V1.0.xsd",
            SHARED_XSDS / "Global-V1.0.xsd",
            "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb",
        ),
        PinnedXsdFile(
            "GlobalLibrary-V2.0.xsd",
            SHARED_XSDS / "GlobalLibrary-V2.0.xsd",
            "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
        ),
        PinnedXsdFile(
            "UniversalCodes-V2.0.xsd",
            SHARED_XSDS / "UniversalCodes-V2.0.xsd",
            "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
        ),
    ),
    official_sha256=(
        "5d5599068d721e6554fa442df88711f8d9386a5fafc18b01cb1d1becc41f84e7"
    ),
)


class RRSF424MultiProjectCoverXmlTests(unittest.TestCase):
    def assert_xsd_valid(self, response: dict[str, object]) -> bytes:
        xml = render_profile_xml(PROFILE, response)
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return xml

    def test_empty_response_preserves_the_all_optional_root_cardinality(self) -> None:
        xml = self.assert_xsd_valid({})
        root = ET.fromstring(xml)
        self.assertEqual(list(root), [])
        self.assertEqual(
            root.attrib,
            {
                "{http://apply.grants.gov/forms/"
                "RR_SF424_Multi_Project_Cover_4_0-V4.0}FormVersion": "4.0"
            },
        )

    def test_shared_projection_emits_representative_values_in_exact_xsd_order(self) -> None:
        response = {
            "submissionTypeCode": "Application",
            "submittedDate": "2026-08-25",
            "grantsTrackingNumber": "1234567890123",
            "projectTitle": "Portable multi-project cover",
            "proposedProjectPeriod": {
                "proposedStartDate": "2026-09-01",
                "proposedEndDate": "2027-08-31",
            },
            "applicantCongressionalDistrict": "VA-008",
            "estimatedProjectFunding": {
                "totalEstimatedAmount": "100.00",
                "totalNonFederalRequested": "25.00",
                "totalFederalNonFederalRequested": "125.00",
                "estimatedProgramIncome": "0.00",
            },
            "stateReview": {
                "stateReviewCodeType": "Program is not covered by E.O. 12372"
            },
            "trustAgree": "Y: Yes",
            "aorSignature": "Authorized Representative",
            "aorSignedDate": "2026-08-25",
        }
        root = ET.fromstring(self.assert_xsd_valid(response))
        names = [child.tag.rsplit("}", 1)[-1] for child in root]
        self.assertEqual(
            names,
            [
                "SubmissionTypeCode",
                "SubmittedDate",
                "GrantsTrackingNumber",
                "ProjectTitle",
                "ProposedProjectPeriod",
                "CongressionalDistrict",
                "EstimatedProjectFunding",
                "StateReview",
                "TrustAgree",
                "AOR_Signature",
                "AOR_SignedDate",
            ],
        )

    def test_tracking_number_length_is_enforced_by_the_exact_official_xsd(self) -> None:
        xml = render_profile_xml(PROFILE, {"grantsTrackingNumber": "too-short"})
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertNotEqual(result.returncode, 0, "official XSD accepted short tracking number")


if __name__ == "__main__":
    unittest.main()
