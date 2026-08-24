from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from conformance.grants_gov_xml import ExactXsdFixture, PinnedXsdFile, render_profile_xml, validate_exact_xsd


ROOT = Path(__file__).parents[1]
FORM_NS = "http://apply.grants.gov/forms/SBIR_STTR_Information_3_0-V3.0"
ATT_NS = "http://apply.grants.gov/system/Attachments-V1.0"
PROFILE = json.loads((ROOT / "dist/forms/sbir-sttr-information/targets/grants-gov-xml.json").read_text())
FORM_XSD = ROOT / "tests/fixtures/grants-gov-xsd/sbir-sttr-information-3.0/SBIR_STTR_Information_3_0-V3.0.xsd"
SHARED = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
FILES = {
    "SBIR_STTR_Information_3_0-V3.0.xsd": (FORM_XSD, "32ed46a450c1b77d9ef64ebf2a4086ab90b076aa2d3cdfedfab8c00324adcebf"),
    "Attachments-V1.0.xsd": (SHARED / "Attachments-V1.0.xsd", "ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d"),
    "Global-V1.0.xsd": (SHARED / "Global-V1.0.xsd", "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb"),
    "GlobalLibrary-V2.0.xsd": (SHARED / "GlobalLibrary-V2.0.xsd", "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8"),
    "UniversalCodes-V2.0.xsd": (SHARED / "UniversalCodes-V2.0.xsd", "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a"),
}
XSD_SET = ExactXsdFixture(
    entrypoint="SBIR_STTR_Information_3_0-V3.0.xsd",
    files=tuple(PinnedXsdFile(name, path, digest) for name, (path, digest) in FILES.items()),
    official_sha256="32ed46a450c1b77d9ef64ebf2a4086ab90b076aa2d3cdfedfab8c00324adcebf",
)


def attachment(name: str) -> dict[str, str]:
    return {
        "fileName": name,
        "mimeType": "application/pdf",
        "fileLocation": f"files/{name}",
        "hashValue": hashlib.sha256(name.encode()).hexdigest(),
    }


def yes_no(value: str) -> dict[str, str]:
    return {"value": value}


def minimal() -> dict[str, object]:
    return {
        "agency": {"value": "HHS"},
        "sbcControlId": "123456789",
        "programType": {"value": "SBIR"},
        "applicationType": {"value": "Phase I"},
        "smallBusinessEligibility": yes_no("Y: Yes"),
        "numberOfEmployees": 12,
        "vcocOwnership": yes_no("N: No"),
        "facultyStudentOwnership": yes_no("N: No"),
        "federalSubcontractsIncluded": yes_no("N: No"),
        "hubzoneLocation": yes_no("N: No"),
        "domesticPerformance": yes_no("Y: Yes"),
        "equivalentFederalWork": yes_no("N: No"),
        "disclosurePermission": yes_no("N: No"),
        "tabaFundingRequest": yes_no("N: No"),
    }


class SbirSttrInformationXmlTests(unittest.TestCase):
    def assert_valid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_minimal_wire_root_namespace_version_and_exact_sequence(self) -> None:
        xml = render_profile_xml(PROFILE, minimal())
        root = ET.fromstring(xml)
        self.assertEqual(root.tag, f"{{{FORM_NS}}}SBIR_STTR_Information_3_0")
        self.assertEqual(root.attrib, {f"{{{FORM_NS}}}FormVersion": "3.0"})
        self.assertEqual(
            [child.tag.rsplit("}", 1)[-1] for child in root],
            ["Agency", "SBCControlID", "ProgramType", "ApplicationType", "SmallBusinessEligibility", "NumberOfEmployees", "VCOC", "FacultyStudentOwned", "SubcontractsIncluded", "LocatedInHUBZone", "DomesticPerformance", "EquivalentProposalsSubmitted", "DisclosurePermission", "TABARequest"],
        )
        self.assert_valid(xml)

    def test_fully_populated_wire_has_all_27_elements_and_three_distinct_attachments(self) -> None:
        response = minimal() | {
            "agency": {"value": "Other"},
            "otherAgency": "NASA",
            "programType": {"value": "Both"},
            "applicationType": {"value": "Fast-Track"},
            "phaseILetterOfIntentNumber": "LOI-123",
            "agencyTopicSubtopic": "TOPIC-1",
            "federalSubcontractsIncluded": yes_no("Y: Yes"),
            "federalSubcontractorNames": "Federal Laboratory",
            "domesticPerformance": yes_no("N: No"),
            "nonDomesticPerformanceExplanation": "outside-us",
            "equivalentFederalWork": yes_no("Y: Yes"),
            "equivalentWorkFederalAgencies": "DOE",
            "commercializationPlan": "plan",
            "phaseIIAwardsReceived": yes_no("Y: Yes"),
            "commercializationHistory": "history",
            "pdpiPrimaryEmployment": yes_no("Y: Yes"),
            "pdpiAppointmentAndEffort": yes_no("Y: Yes"),
            "jointPerformancePercentage": yes_no("Y: Yes"),
            "nonprofitResearchPartnerUei": "ABCDEFGHIJKL",
        }
        files = {
            "outside-us": attachment("NonDomesticExplanation.pdf"),
            "plan": attachment("CommercializationPlan.pdf"),
            "history": attachment("CommercializationHistory.pdf"),
        }
        xml = render_profile_xml(PROFILE, response, files)
        root = ET.fromstring(xml)
        self.assertEqual(len(root), 27)
        attachments = [
            root.find(f"{{{FORM_NS}}}NonDomesticPerformanceExplanation"),
            root.find(f"{{{FORM_NS}}}CommercializationPlan"),
            root.find(f"{{{FORM_NS}}}SBIR_CommercializationHistory"),
        ]
        self.assertTrue(all(node is not None for node in attachments))
        self.assertTrue(all(node.find(f"{{{ATT_NS}}}FileName") is not None for node in attachments if node is not None))
        self.assert_valid(xml)

    def test_exact_xsd_rejects_invalid_wire_vocabulary_and_bounds(self) -> None:
        response = minimal()
        response["smallBusinessEligibility"] = yes_no("Yes")
        self.assertNotEqual(validate_exact_xsd(render_profile_xml(PROFILE, response), XSD_SET, profile=PROFILE).returncode, 0)
        response = minimal()
        response["numberOfEmployees"] = 1000
        self.assertNotEqual(validate_exact_xsd(render_profile_xml(PROFILE, response), XSD_SET, profile=PROFILE).returncode, 0)
        response = minimal()
        response["nonprofitResearchPartnerUei"] = "SHORT"
        self.assertNotEqual(validate_exact_xsd(render_profile_xml(PROFILE, response), XSD_SET, profile=PROFILE).returncode, 0)


if __name__ == "__main__":
    unittest.main()
