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
FORM_NS = "http://apply.grants.gov/forms/PHS_Fellowship_Supplemental_8_0-V8.0"
ATT_NS = "http://apply.grants.gov/system/Attachments-V1.0"
PROFILE = json.loads(
    (ROOT / "dist/forms/phs-fellowship-supplemental/targets/grants-gov-xml.json").read_text()
)
FORM_XSD = (
    ROOT
    / "tests/fixtures/grants-gov-xsd/phs-fellowship-supplemental-8.0/"
    "PHS_Fellowship_Supplemental_8_0-V8.0.xsd"
)
SHARED_XSDS = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
FILES = {
    "PHS_Fellowship_Supplemental_8_0-V8.0.xsd": (
        FORM_XSD,
        "85f8e33df4641c56f3b6b96108690f89d214de8b5c864b1d6bd1e6bf8c7cc7bc",
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
    entrypoint="PHS_Fellowship_Supplemental_8_0-V8.0.xsd",
    files=tuple(PinnedXsdFile(name, path, digest) for name, (path, digest) in FILES.items()),
    official_sha256="85f8e33df4641c56f3b6b96108690f89d214de8b5c864b1d6bd1e6bf8c7cc7bc",
)


def attachment(number: int) -> dict[str, str]:
    return {
        "fileName": f"fellowship-{number}.pdf",
        "mimeType": "application/pdf",
        "fileLocation": f"files/fellowship-{number}.pdf",
        "hashValue": hashlib.sha256(f"fellowship-{number}".encode()).hexdigest(),
    }


def required_response() -> dict[str, object]:
    return {
        "candidateGoals": "1",
        "trainingActivities": "2",
        "researchProjectAims": "3",
        "researchProjectStrategy": "4",
        "responsibleConductTraining": "5",
        "vertebrateAnimalsUsed": "N: No",
        "humanEmbryonicStemCells": {"involved": "N: No"},
        "candidateInformation": {
            "fieldOfTraining": "100 Biochemistry",
            "currentPriorNrsaSupport": {"hasSupport": "N: No"},
            "concurrentSupport": {"hasConcurrentSupport": "N: No"},
            "citizenship": {"usCitizen": "Y: Yes"},
        },
        "budget": {
            "tuition": {"fundsRequested": "N: No"},
            "childcare": {"fundsRequested": "N: No"},
        },
    }


class PHSFellowshipSupplementalXmlTests(unittest.TestCase):
    def assert_valid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_minimal_required_response_validates_against_exact_xsd(self) -> None:
        attachments = {str(number): attachment(number) for number in range(1, 6)}
        xml = render_profile_xml(PROFILE, required_response(), attachments)
        root = ET.fromstring(xml)

        self.assertEqual(
            root.tag,
            f"{{{FORM_NS}}}PHS_Fellowship_Supplemental_8_0",
        )
        self.assertEqual(root.attrib, {f"{{{FORM_NS}}}FormVersion": "8.0"})
        self.assert_valid(xml)

    def test_repeating_records_budget_and_appendix_preserve_wire_shape(self) -> None:
        response = required_response()
        response["humanEmbryonicStemCells"] = {
            "involved": "Y: Yes",
            "specificLineUnavailable": "N: No",
            "cellLines": ["0001", "0002"],
        }
        response["candidateInformation"] = {
            "fieldOfTraining": "100 Biochemistry",
            "currentPriorNrsaSupport": {
                "hasSupport": "Y: Yes",
                "records": [
                    {
                        "level": "Predoctoral",
                        "type": "Individual",
                        "startDate": "2025-01-01",
                        "endDate": "2026-01-01",
                        "grantNumber": "ABC",
                    }
                ],
            },
            "concurrentSupport": {"hasConcurrentSupport": "N: No"},
            "citizenship": {"usCitizen": "Y: Yes"},
        }
        response["budget"] = {
            "tuition": {
                "fundsRequested": "Y: Yes",
                "year1": "100.00",
                "year2": "200.00",
                "total": "300.00",
            },
            "childcare": {"fundsRequested": "N: No"},
        }
        response["appendix"] = ["6", "7"]
        attachments = {str(number): attachment(number) for number in range(1, 8)}

        xml = render_profile_xml(PROFILE, response, attachments)
        root = ET.fromstring(xml)
        appendix = root.find(f"{{{FORM_NS}}}Appendix")

        self.assertIsNotNone(appendix)
        assert appendix is not None
        self.assertEqual(len(appendix), 2)
        self.assertEqual(
            {child.tag for child in appendix},
            {f"{{{ATT_NS}}}AttachedFile"},
        )
        self.assertEqual(
            len(root.findall(f".//{{{FORM_NS}}}CellLines")),
            2,
        )
        self.assert_valid(xml)

    def test_unknown_response_data_and_attachment_references_fail_closed(self) -> None:
        response = required_response()
        response["notAQuestion"] = "must not disappear"
        with self.assertRaisesRegex(AssertionError, "unmapped response properties"):
            render_profile_xml(PROFILE, response, {})

        with self.assertRaisesRegex(AssertionError, "missing attachment fixture"):
            render_profile_xml(PROFILE, required_response(), {})


if __name__ == "__main__":
    unittest.main()
