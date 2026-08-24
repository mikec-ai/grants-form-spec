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
FORM_NS = "http://apply.grants.gov/forms/PHS398_ResearchPlan_5_0-V5.0"
ATT_NS = "http://apply.grants.gov/system/Attachments-V1.0"
PROFILE = json.loads(
    (ROOT / "dist/forms/phs398-research-plan/targets/grants-gov-xml.json").read_text()
)
FORM_XSD = (
    ROOT / "tests/fixtures/grants-gov-xsd/phs398-research-plan-5.0/"
    "PHS398_ResearchPlan_5_0-V5.0.xsd"
)
SHARED_XSDS = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
FILES = {
    "PHS398_ResearchPlan_5_0-V5.0.xsd": (
        FORM_XSD,
        "6e7171465d1f44a16eb822f8921423ceede4fa486cb0819bc5dd327121b4bb56",
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
    entrypoint="PHS398_ResearchPlan_5_0-V5.0.xsd",
    files=tuple(PinnedXsdFile(name, path, digest) for name, (path, digest) in FILES.items()),
    official_sha256="6e7171465d1f44a16eb822f8921423ceede4fa486cb0819bc5dd327121b4bb56",
)


SINGLETONS = [
    ("introduction", "IntroductionToApplication"),
    ("specificAims", "SpecificAims"),
    ("researchStrategy", "ResearchStrategy"),
    ("progressReportPublicationList", "ProgressReportPublicationList"),
    ("vertebrateAnimals", "VertebrateAnimals"),
    ("selectAgentResearch", "SelectAgentResearch"),
    ("multiplePdPiLeadershipPlan", "MultiplePDPILeadershipPlan"),
    ("consortiumContractualArrangements", "ConsortiumContractualArrangements"),
    ("lettersOfSupport", "LettersOfSupport"),
    ("resourceSharingPlans", "ResourceSharingPlans"),
    ("otherPlans", "OtherPlans"),
    ("keyResourceAuthentication", "KeyBiologicalAndOrChemicalResources"),
]


def attachment(number: int) -> dict[str, str]:
    return {
        "fileName": f"research-plan-{number}.pdf",
        "mimeType": "application/pdf",
        "fileLocation": f"files/research-plan-{number}.pdf",
        "hashValue": hashlib.sha256(f"research-plan-{number}".encode()).hexdigest(),
    }


class PHS398ResearchPlanXmlTests(unittest.TestCase):
    def assert_valid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_minimal_response_emits_required_wrapper_and_validates(self) -> None:
        attachments = {"strategy": attachment(1)}
        xml = render_profile_xml(
            PROFILE, {"researchStrategy": "strategy"}, attachments
        )
        root = ET.fromstring(xml)

        self.assertEqual(root.tag, f"{{{FORM_NS}}}PHS398_ResearchPlan_5_0")
        self.assertEqual(root.attrib, {f"{{{FORM_NS}}}FormVersion": "5.0"})
        self.assertEqual(
            [child.tag for child in root],
            [f"{{{FORM_NS}}}ResearchPlanAttachments"],
        )
        plan = root[0]
        self.assertEqual(
            [child.tag for child in plan], [f"{{{FORM_NS}}}ResearchStrategy"]
        )
        self.assertEqual(plan[0][0].tag, f"{{{FORM_NS}}}attFile")
        self.assert_valid(xml)

    def test_missing_research_strategy_fails_exact_xsd(self) -> None:
        xml = render_profile_xml(PROFILE, {})
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertNotEqual(result.returncode, 0)

    def test_cross_form_applicable_roles_emit_without_fake_local_condition_fields(self) -> None:
        attachments = {str(number): attachment(number) for number in range(1, 5)}
        xml = render_profile_xml(
            PROFILE,
            {
                "introduction": "1",
                "researchStrategy": "2",
                "progressReportPublicationList": "3",
                "vertebrateAnimals": "4",
            },
            attachments,
        )
        plan = ET.fromstring(xml)[0]

        self.assertEqual(
            [child.tag for child in plan],
            [
                f"{{{FORM_NS}}}IntroductionToApplication",
                f"{{{FORM_NS}}}ResearchStrategy",
                f"{{{FORM_NS}}}ProgressReportPublicationList",
                f"{{{FORM_NS}}}VertebrateAnimals",
            ],
        )
        self.assert_valid(xml)

    def test_full_applicant_payload_preserves_source_order_and_ten_appendices(self) -> None:
        attachments = {str(number): attachment(number) for number in range(1, 23)}
        response = {
            canonical: str(number)
            for number, (canonical, _) in enumerate(SINGLETONS, 1)
        }
        response["appendix"] = [str(number) for number in range(13, 23)]
        xml = render_profile_xml(PROFILE, response, attachments)
        plan = ET.fromstring(xml)[0]

        self.assertEqual(
            [child.tag for child in plan],
            [f"{{{FORM_NS}}}{wire}" for _, wire in SINGLETONS]
            + [f"{{{FORM_NS}}}Appendix"],
        )
        appendix = plan[-1]
        self.assertEqual(len(appendix), 10)
        self.assertEqual(
            {child.tag for child in appendix}, {f"{{{ATT_NS}}}AttachedFile"}
        )
        self.assertTrue(all(len(child) == 4 for child in appendix))
        self.assert_valid(xml)

    def test_xsd_technical_envelope_accepts_more_than_applicant_schema_limit(self) -> None:
        attachments = {str(number): attachment(number) for number in range(1, 13)}
        xml = render_profile_xml(
            PROFILE,
            {
                "researchStrategy": "1",
                "appendix": [str(number) for number in range(2, 13)],
            },
            attachments,
        )
        self.assertEqual(len(ET.fromstring(xml)[0][-1]), 11)
        self.assert_valid(xml)

    def test_unknown_attachment_reference_fails_closed(self) -> None:
        with self.assertRaisesRegex(AssertionError, "missing attachment fixture"):
            render_profile_xml(PROFILE, {"researchStrategy": "missing"}, {})


if __name__ == "__main__":
    unittest.main()
