from __future__ import annotations

import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from conformance.grants_gov_xml import ExactXsdFixture, PinnedXsdFile, render_profile_xml, validate_exact_xsd


ROOT = Path(__file__).parents[1]
FORM_NS = "http://apply.grants.gov/forms/RR_PersonalData_1_2-V1.2"
GLOB_LIB_NS = "http://apply.grants.gov/system/GlobalLibrary-V2.0"
PROFILE = json.loads((ROOT / "dist/forms/rr-personal-data/targets/grants-gov-xml.json").read_text())
FORM_XSD = ROOT / "tests/fixtures/grants-gov-xsd/rr-personal-data-1.2/RR_PersonalData_1_2-V1.2.xsd"
SHARED = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
FILES = {
    "RR_PersonalData_1_2-V1.2.xsd": (FORM_XSD, "5f766d46d573da1f6bb326bcbc13338439ba75399ad09dee2380f65e892402cb"),
    "Attachments-V1.0.xsd": (SHARED / "Attachments-V1.0.xsd", "ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d"),
    "Global-V1.0.xsd": (SHARED / "Global-V1.0.xsd", "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb"),
    "GlobalLibrary-V2.0.xsd": (SHARED / "GlobalLibrary-V2.0.xsd", "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8"),
    "UniversalCodes-V2.0.xsd": (SHARED / "UniversalCodes-V2.0.xsd", "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a"),
}
XSD_SET = ExactXsdFixture(
    entrypoint="RR_PersonalData_1_2-V1.2.xsd",
    files=tuple(PinnedXsdFile(name, path, digest) for name, (path, digest) in FILES.items()),
    official_sha256="5f766d46d573da1f6bb326bcbc13338439ba75399ad09dee2380f65e892402cb",
)


def name(first: str, last: str) -> dict[str, str]:
    return {"firstName": first, "lastName": last}


def minimal() -> dict[str, object]:
    return {"projectDirector": {"name": name("Ada", "Lovelace")}}


class RRPersonalDataXmlTests(unittest.TestCase):
    def assert_valid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_invalid(self, response: dict[str, object]) -> None:
        result = validate_exact_xsd(render_profile_xml(PROFILE, response), XSD_SET, profile=PROFILE)
        self.assertNotEqual(result.returncode, 0)

    def test_minimal_wire_root_namespace_version_and_sequence(self) -> None:
        xml = render_profile_xml(PROFILE, minimal())
        root = ET.fromstring(xml)
        self.assertEqual(root.tag, f"{{{FORM_NS}}}RR_PersonalData_1_2")
        self.assertEqual(root.attrib, {f"{{{FORM_NS}}}FormVersion": "1.2"})
        self.assertEqual([child.tag.rsplit("}", 1)[-1] for child in root], ["ProjectDirector"])
        director = root[0]
        self.assertEqual([child.tag.rsplit("}", 1)[-1] for child in director], ["Name"])
        self.assert_valid(xml)

    def test_all_fields_preserve_exact_wire_order_namespaces_and_repetitions(self) -> None:
        response = {
            "projectDirector": {
                "name": {"prefix": "Dr", "firstName": "Ada", "middleName": "M", "lastName": "Lovelace", "suffix": "III"},
                "sex": "Female",
                "race": ["Asian", "White"],
                "ethnicity": "Non-Hispanic or Latino",
                "disabilityStatus": ["Hearing", "Visual"],
                "citizenship": "US Citizen",
            },
            "coProjectDirectors": [
                {
                    "name": name("Grace", "Hopper"),
                    "sex": "Female",
                    "race": ["White"],
                    "ethnicity": "Do Not Wish to Provide",
                    "disabilityStatus": ["None"],
                    "citizenship": "US Citizen",
                },
                {"name": name("Katherine", "Johnson"), "citizenship": "Permanent Resident"},
            ],
        }
        xml = render_profile_xml(PROFILE, response)
        root = ET.fromstring(xml)
        self.assertEqual(
            [child.tag.rsplit("}", 1)[-1] for child in root],
            ["ProjectDirector", "Co-ProjectDirector", "Co-ProjectDirector"],
        )
        director = root[0]
        self.assertEqual(
            [child.tag.rsplit("}", 1)[-1] for child in director],
            ["Name", "Gender", "Race", "Race", "Ethnicity", "DisabilityStatus", "DisabilityStatus", "Citizenship"],
        )
        person_name = director.find(f"{{{FORM_NS}}}Name")
        self.assertIsNotNone(person_name)
        self.assertEqual(
            [child.tag.rsplit("}", 1)[-1] for child in person_name],
            ["PrefixName", "FirstName", "MiddleName", "LastName", "SuffixName"],
        )
        self.assertTrue(all(child.tag.startswith(f"{{{GLOB_LIB_NS}}}") for child in person_name))
        self.assertEqual([node.text for node in director.findall(f"{{{FORM_NS}}}Race")], ["Asian", "White"])
        self.assertEqual(director.find(f"{{{FORM_NS}}}Ethnicity").text, "Not Hispanic or Latino")
        co_director = root.findall(f"{{{FORM_NS}}}Co-ProjectDirector")[0]
        self.assertEqual(co_director.find(f"{{{FORM_NS}}}Ethnicity").text, "Do Not Wish To Provide")
        self.assert_valid(xml)

    def test_source_valid_free_text_name_prefix_and_suffix_round_trip(self) -> None:
        response = {
            "projectDirector": {
                "name": {"prefix": "Mx", "firstName": "Ada", "lastName": "Lovelace", "suffix": "III"}
            }
        }
        xml = render_profile_xml(PROFILE, response)
        director_name = ET.fromstring(xml).find(f"{{{FORM_NS}}}ProjectDirector/{{{FORM_NS}}}Name")
        self.assertEqual(director_name.find(f"{{{GLOB_LIB_NS}}}PrefixName").text, "Mx")
        self.assertEqual(director_name.find(f"{{{GLOB_LIB_NS}}}SuffixName").text, "III")
        self.assert_valid(xml)

    def test_exact_xsd_enforces_director_race_disability_and_repeat_maxima(self) -> None:
        response = minimal()
        response["projectDirector"]["race"] = [
            "American Indian or Alaska Native", "Asian", "Black or African American",
            "Native Hawaiian or Other Pacific Islander", "White",
        ]
        response["projectDirector"]["disabilityStatus"] = ["Hearing", "Visual", "Mobility/Orthopedic Impairment", "Other"]
        response["coProjectDirectors"] = [{"name": name(f"Co{i}", "Person")} for i in range(4)]
        self.assert_valid(render_profile_xml(PROFILE, response))

        response["coProjectDirectors"].append({"name": name("Fifth", "Person")})
        self.assert_invalid(response)
        response["coProjectDirectors"].pop()
        response["projectDirector"]["race"].append("Do Not Wish to Provide")
        self.assert_invalid(response)
        response["projectDirector"]["race"].pop()
        response["projectDirector"]["disabilityStatus"].append("None")
        self.assert_invalid(response)


if __name__ == "__main__":
    unittest.main()
