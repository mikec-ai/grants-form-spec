from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from conformance.grants_gov_xml import (
    ExactXsdFixture,
    PinnedXsdFile,
    render_profile_xml,
    validate_exact_xsd,
)


ROOT = Path(__file__).parents[1]
FORM_NS = "http://apply.grants.gov/forms/RR_KeyPersonExpanded_4_0-V4.0"
ATTACHMENTS_NS = "http://apply.grants.gov/system/Attachments-V1.0"
GLOBAL_NS = "http://apply.grants.gov/system/Global-V1.0"
XSD_FIXTURES = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
XSD_HASHES = {
    "RR_KeyPersonExpanded_4_0-V4.0.xsd": "c1522304f37bb91a1fc18f2b84656c570581969f9c1795d18352bc273d691b8b",
    "Attachments-V1.0.xsd": "ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d",
    "Global-V1.0.xsd": "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb",
    "GlobalLibrary-V2.0.xsd": "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
    "UniversalCodes-V2.0.xsd": "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
}
PROFILE = json.loads(
    (ROOT / "dist/forms/rr-key-person-expanded/targets/grants-gov-xml.json").read_text()
)
XSD_SET = ExactXsdFixture(
    entrypoint="RR_KeyPersonExpanded_4_0-V4.0.xsd",
    files=tuple(
        PinnedXsdFile(name, XSD_FIXTURES / name, digest)
        for name, digest in XSD_HASHES.items()
    ),
    official_sha256=XSD_HASHES["RR_KeyPersonExpanded_4_0-V4.0.xsd"],
)


def _person(first_name: str, last_name: str, *, country: str, **address: str) -> dict[str, Any]:
    return {
        "name": {"firstName": first_name, "lastName": last_name},
        "address": {
            "street1": "1 Research Way",
            "city": "Science City",
            "country": country,
            **address,
        },
        "phone": "202-555-0100",
        "email": f"{first_name.lower()}@example.org",
        "projectRole": "PD/PI",
    }


class RRKeyPersonExpandedXmlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.attachments = {
            name: {
                "fileName": f"{name}.pdf",
                "mimeType": "application/pdf",
                "fileLocation": f"https://files.example.org/{name}.pdf",
                "hashValue": "YWJj",
            }
            for name in (
                "pi-bio",
                "senior-us-bio",
                "senior-us-support",
                "senior-foreign-bio",
                "senior-foreign-support",
                "overflow-profiles",
                "overflow-bios",
                "overflow-support",
            )
        }

    def assert_attachment(
        self,
        parent: ET.Element,
        wrapper_name: str,
        leaf_name: str,
        attachment_id: str,
    ) -> None:
        wrapper_qname = f"{{{FORM_NS}}}{wrapper_name}"
        wrappers = parent.findall(wrapper_qname)
        self.assertEqual(len(wrappers), 1)
        wrapper = wrappers[0]
        leaf_qname = f"{{{FORM_NS}}}{leaf_name}"
        self.assertEqual([child.tag for child in wrapper], [leaf_qname])
        leaf = wrapper[0]
        self.assertEqual(
            [child.tag for child in leaf],
            [
                f"{{{ATTACHMENTS_NS}}}FileName",
                f"{{{ATTACHMENTS_NS}}}MimeType",
                f"{{{ATTACHMENTS_NS}}}FileLocation",
                f"{{{GLOBAL_NS}}}HashValue",
            ],
        )
        attachment = self.attachments[attachment_id]
        self.assertEqual(leaf[0].text, attachment["fileName"])
        self.assertEqual(leaf[1].text, attachment["mimeType"])
        self.assertIsNone(leaf[2].text)
        self.assertEqual(
            leaf[2].attrib,
            {f"{{{ATTACHMENTS_NS}}}href": attachment["fileLocation"]},
        )
        self.assertEqual(leaf[3].text, attachment["hashValue"])
        self.assertEqual(
            leaf[3].attrib,
            {f"{{{GLOBAL_NS}}}hashAlgorithm": "SHA-256"},
        )

    def test_pi_multiple_people_and_attachments_validate_against_exact_xsd(self) -> None:
        pi = _person(
            "Ada", "Lovelace", country="USA: UNITED STATES",
            state="CA: California", zipCode="940431234",
        )
        pi["biographicalSketch"] = "pi-bio"
        senior_us = _person(
            "Grace", "Hopper", country="USA: UNITED STATES",
            state="VA: Virginia", zipCode="222011234",
        )
        senior_us.update({
            "projectRole": "Co-Investigator",
            "biographicalSketch": "senior-us-bio",
            "currentPendingSupport": "senior-us-support",
        })
        senior_foreign = _person(
            "Katherine", "Johnson", country="CAN: CANADA",
            province="Ontario", zipCode="K1A0B1",
        )
        senior_foreign.update({
            "projectRole": "Co-Investigator",
            "biographicalSketch": "senior-foreign-bio",
            "currentPendingSupport": "senior-foreign-support",
        })
        response = {
            "principalInvestigator": pi,
            "seniorKeyPersons": [senior_us, senior_foreign],
            "additionalProfiles": "overflow-profiles",
            "additionalBiographicalSketches": "overflow-bios",
            "additionalCurrentPendingSupport": "overflow-support",
        }

        xml = render_profile_xml(PROFILE, response, self.attachments)
        root = ET.fromstring(xml)
        self.assertEqual(
            [child.tag for child in root],
            [
                f"{{{FORM_NS}}}PDPI",
                f"{{{FORM_NS}}}KeyPerson",
                f"{{{FORM_NS}}}KeyPerson",
                f"{{{FORM_NS}}}AdditionalProfilesAttached",
                f"{{{FORM_NS}}}BioSketchsAttached",
                f"{{{FORM_NS}}}SupportsAttached",
            ],
        )

        pdpis = root.findall(f"{{{FORM_NS}}}PDPI")
        self.assertEqual(len(pdpis), 1)
        self.assertEqual(
            [child.tag for child in pdpis[0]],
            [f"{{{FORM_NS}}}Profile"],
        )
        pi_profile = pdpis[0][0]
        self.assertEqual(
            [child.tag for child in pi_profile],
            [
                f"{{{FORM_NS}}}Name",
                f"{{{FORM_NS}}}Address",
                f"{{{FORM_NS}}}Phone",
                f"{{{FORM_NS}}}Email",
                f"{{{FORM_NS}}}ProjectRole",
                f"{{{FORM_NS}}}BioSketchsAttached",
            ],
        )
        self.assert_attachment(
            pi_profile, "BioSketchsAttached", "BioSketchAttached", "pi-bio"
        )

        key_people = root.findall(f"{{{FORM_NS}}}KeyPerson")
        self.assertEqual(len(key_people), 2)
        profiles: list[ET.Element] = []
        for key_person in key_people:
            self.assertEqual(
                [child.tag for child in key_person],
                [f"{{{FORM_NS}}}Profile"],
            )
            profile = key_person[0]
            profiles.append(profile)
            self.assertEqual(
                [child.tag for child in profile],
                [
                    f"{{{FORM_NS}}}Name",
                    f"{{{FORM_NS}}}Address",
                    f"{{{FORM_NS}}}Phone",
                    f"{{{FORM_NS}}}Email",
                    f"{{{FORM_NS}}}ProjectRole",
                    f"{{{FORM_NS}}}BioSketchsAttached",
                    f"{{{FORM_NS}}}SupportsAttached",
                ],
            )

        self.assert_attachment(
            profiles[0], "BioSketchsAttached", "BioSketchAttached", "senior-us-bio"
        )
        self.assert_attachment(
            profiles[0], "SupportsAttached", "SupportAttached", "senior-us-support"
        )
        self.assert_attachment(
            profiles[1],
            "BioSketchsAttached",
            "BioSketchAttached",
            "senior-foreign-bio",
        )
        self.assert_attachment(
            profiles[1],
            "SupportsAttached",
            "SupportAttached",
            "senior-foreign-support",
        )
        self.assert_attachment(
            root,
            "AdditionalProfilesAttached",
            "AdditionalProfileAttached",
            "overflow-profiles",
        )
        self.assert_attachment(
            root, "BioSketchsAttached", "BioSketchAttached", "overflow-bios"
        )
        self.assert_attachment(
            root, "SupportsAttached", "SupportAttached", "overflow-support"
        )

        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_official_xsd_rejects_state_and_province_together(self) -> None:
        pi = _person(
            "Ada", "Lovelace", country="USA: UNITED STATES",
            state="CA: California", province="California", zipCode="940431234",
        )
        pi["biographicalSketch"] = "pi-bio"

        result = validate_exact_xsd(
            render_profile_xml(PROFILE, {"principalInvestigator": pi}, self.attachments),
            XSD_SET,
            profile=PROFILE,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Province", result.stderr)

if __name__ == "__main__":
    unittest.main()
