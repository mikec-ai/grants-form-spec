from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from conformance.grants_gov_xml import ExactXsdFixture, PinnedXsdFile, render_profile_xml, validate_exact_xsd


ROOT = Path(__file__).parents[1]
FORM_NS = "http://apply.grants.gov/forms/PHS398_CoverPageSupplement_5_0-V5.0"
GLOB_LIB_NS = "http://apply.grants.gov/system/GlobalLibrary-V2.0"
PROFILE = json.loads((ROOT / "dist/forms/phs398-cover-page-supplement/targets/grants-gov-xml.json").read_text())
FORM_XSD = ROOT / "tests/fixtures/grants-gov-xsd/phs398-cover-page-supplement-5.0/PHS398_CoverPageSupplement_5_0-V5.0.xsd"
SHARED = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
FILES = {
    "PHS398_CoverPageSupplement_5_0-V5.0.xsd": (FORM_XSD, "ec538c9bb5fd233c36ac73ca567d31e60779ee3df2f3c7b456d9395b3ec2dc26"),
    "Attachments-V1.0.xsd": (SHARED / "Attachments-V1.0.xsd", "ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d"),
    "Global-V1.0.xsd": (SHARED / "Global-V1.0.xsd", "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb"),
    "GlobalLibrary-V2.0.xsd": (SHARED / "GlobalLibrary-V2.0.xsd", "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8"),
    "UniversalCodes-V2.0.xsd": (SHARED / "UniversalCodes-V2.0.xsd", "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a"),
}
XSD_SET = ExactXsdFixture(
    entrypoint="PHS398_CoverPageSupplement_5_0-V5.0.xsd",
    files=tuple(PinnedXsdFile(name, path, digest) for name, (path, digest) in FILES.items()),
    official_sha256="ec538c9bb5fd233c36ac73ca567d31e60779ee3df2f3c7b456d9395b3ec2dc26",
)


def attachment(name: str) -> dict[str, str]:
    return {
        "fileName": name,
        "mimeType": "application/pdf",
        "fileLocation": f"files/{name}",
        "hashValue": hashlib.sha256(name.encode()).hexdigest(),
    }


def minimal() -> dict[str, object]:
    return {
        "programIncome": {"anticipated": "N: No"},
        "humanEmbryonicStemCells": {"involved": "N: No"},
        "humanFetalTissue": {"involved": "N: No"},
    }


class PHS398CoverPageSupplementXmlTests(unittest.TestCase):
    def assert_valid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_minimal_wire_root_namespace_version_and_sequence(self) -> None:
        xml = render_profile_xml(PROFILE, minimal())
        root = ET.fromstring(xml)
        self.assertEqual(root.tag, f"{{{FORM_NS}}}PHS398_CoverPageSupplement_5_0")
        self.assertEqual(root.attrib, {f"{{{FORM_NS}}}FormVersion": "5.0"})
        self.assertEqual([child.tag.rsplit("}", 1)[-1] for child in root], ["ProgramIncome", "StemCells", "isHumanFetalTissueInvolved"])
        self.assert_valid(xml)

    def test_all_fields_preserve_exact_wire_order_and_values(self) -> None:
        response = {
            "vertebrateAnimals": {"animalEuthanized": "Y: Yes", "avmaConsistent": "N: No", "methodDescription": "Scientific justification"},
            "programIncome": {"anticipated": "Y: Yes", "periods": [{"budgetPeriod": 1, "anticipatedAmount": "12.34", "source": "Licensing"}]},
            "humanEmbryonicStemCells": {"involved": "Y: Yes", "specificLineUnavailable": "N: No", "cellLines": ["0001", "0123"]},
            "humanFetalTissue": {"involved": "Y: Yes", "complianceAssurance": "assurance", "irbConsentForm": "consent"},
            "inventionsAndPatents": {"inventions": "Y: Yes", "previouslyReported": "N: No"},
            "changes": {"changeOfProjectDirector": "Y: Yes", "changeOfRecipientOrganization": "Y: Yes"},
            "formerProjectDirector": {"prefix": "Dr", "firstName": "Ada", "middleName": "M", "lastName": "Lovelace", "suffix": "III"},
            "formerOrganizationName": "Former Research Institute",
        }
        files = {"assurance": attachment("HFTComplianceAssurance.pdf"), "consent": attachment("HFTSampleIRBConsentForm.pdf")}
        xml = render_profile_xml(PROFILE, response, files)
        root = ET.fromstring(xml)
        self.assertEqual(
            [child.tag.rsplit("}", 1)[-1] for child in root],
            ["VertebrateAnimals", "ProgramIncome", "IncomeBudgetPeriod", "StemCells", "isHumanFetalTissueInvolved", "ComplianceAssurance", "HFTIRBConsentForm", "IsInventionsAndPatents", "IsPreviouslyReported", "IsChangeOfPDPI", "FormerPD_Name", "IsChangeOfInstitution", "FormerInstitutionName"],
        )
        self.assertEqual([node.text for node in root.findall(f".//{{{FORM_NS}}}CellLines")], ["0001", "0123"])
        former = root.find(f"{{{FORM_NS}}}FormerPD_Name")
        self.assertIsNotNone(former)
        self.assertEqual([child.tag.rsplit("}", 1)[-1] for child in former], ["PrefixName", "FirstName", "MiddleName", "LastName", "SuffixName"])
        self.assertTrue(all(child.tag.startswith(f"{{{GLOB_LIB_NS}}}") for child in former))
        self.assert_valid(xml)

    def test_wire_enforces_income_and_cell_line_maxima(self) -> None:
        response = minimal()
        response["programIncome"] = {"anticipated": "Y: Yes", "periods": [{"budgetPeriod": (i % 10) + 1, "anticipatedAmount": "1.00", "source": "S"} for i in range(10)]}
        response["humanEmbryonicStemCells"] = {"involved": "Y: Yes", "cellLines": [f"{i:04d}" for i in range(200)]}
        self.assert_valid(render_profile_xml(PROFILE, response))

        response["programIncome"]["periods"].append({"budgetPeriod": 1, "anticipatedAmount": "1.00", "source": "S"})
        result = validate_exact_xsd(render_profile_xml(PROFILE, response), XSD_SET, profile=PROFILE)
        self.assertNotEqual(result.returncode, 0)
        response["programIncome"]["periods"].pop()
        response["humanEmbryonicStemCells"]["cellLines"].append("0200")
        result = validate_exact_xsd(render_profile_xml(PROFILE, response), XSD_SET, profile=PROFILE)
        self.assertNotEqual(result.returncode, 0)

    def test_exact_xsd_envelope_preserves_known_applicant_constraint_conflicts(self) -> None:
        response = minimal()
        response["programIncome"] = {"anticipated": "Y: Yes", "periods": [{"budgetPeriod": 1, "anticipatedAmount": "0", "source": ""}]}
        response["humanEmbryonicStemCells"] = {"involved": "Y: Yes", "cellLines": [""]}
        self.assert_valid(render_profile_xml(PROFILE, response))


if __name__ == "__main__":
    unittest.main()
