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
FORM_NS = "http://apply.grants.gov/forms/EPA_KeyContacts_2_0-V2.0"
GLOB_LIB_NS = "http://apply.grants.gov/system/GlobalLibrary-V2.0"
PROFILE = json.loads(
    (ROOT / "dist/forms/epa-key-contacts/targets/grants-gov-xml.json").read_text()
)
FORM_XSD = (
    ROOT
    / "tests/fixtures/grants-gov-xsd/epa-key-contacts-2.0"
    / "EPA_KeyContacts_2_0-V2.0.xsd"
)
SHARED = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
XSD_SET = ExactXsdFixture(
    entrypoint="EPA_KeyContacts_2_0-V2.0.xsd",
    files=(
        PinnedXsdFile(
            "EPA_KeyContacts_2_0-V2.0.xsd",
            FORM_XSD,
            "157a9c8a21cdc39b4c6b5df94c3745ecd4f174cb390187441de862fb35b50b01",
        ),
        PinnedXsdFile(
            "GlobalLibrary-V2.0.xsd",
            SHARED / "GlobalLibrary-V2.0.xsd",
            "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
        ),
        PinnedXsdFile(
            "UniversalCodes-V2.0.xsd",
            SHARED / "UniversalCodes-V2.0.xsd",
            "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
        ),
    ),
    official_sha256="157a9c8a21cdc39b4c6b5df94c3745ecd4f174cb390187441de862fb35b50b01",
)

# Existing Simpler's manually authored transform declares this exact wire sequence.
# The portable profile must remain differential-compatible without importing that code.
LEGACY_WIRE_ORACLE = (
    ("authorizedRepresentative", "AuthorizedRepresentative"),
    ("payee", "Payee"),
    ("administrativeContact", "AdminstrativeContact"),
    ("projectManager", "ProjectManager"),
)
CONTACT_CHILD_ORACLE = ("Name", "Title", "Address", "Phone", "Fax", "Email")


def contact(first_name: str, last_name: str) -> dict[str, object]:
    return {
        "name": {
            "prefix": "Dr",
            "firstName": first_name,
            "middleName": "Q",
            "lastName": last_name,
            "suffix": "III",
        },
        "title": "Program Contact",
        "address": {
            "street1": "1 Research Way",
            "street2": "Suite 200",
            "city": "Washington",
            "state": "DC: District of Columbia",
            "zipCode": "200011234",
            "country": "USA: UNITED STATES",
        },
        "phone": "202-555-0100",
        "fax": "202-555-0101",
        "email": f"{first_name.lower()}@example.org",
    }


class EPAKeyContactsXmlTests(unittest.TestCase):
    def assert_valid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_resolved_profile_matches_legacy_wire_oracle_without_branches(self) -> None:
        fields = PROFILE["mapping"]["fields"]
        self.assertEqual(
            tuple((source, fields[source]["element"]) for source, _ in LEGACY_WIRE_ORACLE),
            LEGACY_WIRE_ORACLE,
        )
        for source, _ in LEGACY_WIRE_ORACLE:
            self.assertEqual(tuple(fields[source]["fields"]), (
                "name", "title", "address", "phone", "fax", "email",
            ))
            self.assertEqual(fields[source]["fields"]["name"]["namespace"], "globLib")
            self.assertEqual(fields[source]["fields"]["address"]["namespace"], "globLib")

    def test_all_four_roles_preserve_exact_wire_namespaces_order_and_xsd(self) -> None:
        response = {
            source: contact(first, last)
            for (source, _), first, last in zip(
                LEGACY_WIRE_ORACLE,
                ("Ada", "Grace", "Katherine", "Dorothy"),
                ("Lovelace", "Hopper", "Johnson", "Vaughan"),
                strict=True,
            )
        }
        xml = render_profile_xml(PROFILE, response)
        root = ET.fromstring(xml)

        self.assertEqual(root.tag, f"{{{FORM_NS}}}KeyContactPersons_2_0")
        self.assertEqual(root.attrib, {f"{{{FORM_NS}}}FormVersion": "2.0"})
        self.assertEqual(
            [child.tag.rsplit("}", 1)[-1] for child in root],
            [wire for _, wire in LEGACY_WIRE_ORACLE],
        )
        for role in root:
            self.assertEqual(
                tuple(child.tag.rsplit("}", 1)[-1] for child in role),
                CONTACT_CHILD_ORACLE,
            )
            self.assertTrue(all(child.tag.startswith(f"{{{GLOB_LIB_NS}}}") for child in role))
            name = role.find(f"{{{GLOB_LIB_NS}}}Name")
            self.assertEqual(
                [child.tag.rsplit("}", 1)[-1] for child in name],
                ["PrefixName", "FirstName", "MiddleName", "LastName", "SuffixName"],
            )
            address = role.find(f"{{{GLOB_LIB_NS}}}Address")
            self.assertEqual(
                [child.tag.rsplit("}", 1)[-1] for child in address],
                ["Street1", "Street2", "City", "State", "ZipPostalCode", "Country"],
            )
        self.assert_valid(xml)

    def test_optional_roles_omit_cleanly_and_foreign_province_validates(self) -> None:
        project_manager = contact("Chien-Shiung", "Wu")
        project_manager["address"] = {
            "street1": "1 Physics Road",
            "city": "Toronto",
            "province": "Ontario",
            "zipCode": "M5V2T6",
            "country": "CAN: CANADA",
        }
        xml = render_profile_xml(PROFILE, {"projectManager": project_manager})
        root = ET.fromstring(xml)

        self.assertEqual(
            [child.tag.rsplit("}", 1)[-1] for child in root],
            ["ProjectManager"],
        )
        address = root.find(
            f"{{{FORM_NS}}}ProjectManager/{{{GLOB_LIB_NS}}}Address"
        )
        self.assertEqual(
            [child.tag.rsplit("}", 1)[-1] for child in address],
            ["Street1", "City", "Province", "ZipPostalCode", "Country"],
        )
        self.assert_valid(xml)


if __name__ == "__main__":
    unittest.main()
