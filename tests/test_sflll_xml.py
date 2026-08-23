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
FORM_NS = "http://apply.grants.gov/forms/SFLLL_2_0-V2.0"
XSD_FIXTURE = ROOT / "tests/fixtures/grants-gov-xsd/sflll-2.0/SFLLL_2_0-V2.0.xsd"
DEPENDENCIES = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
XSD_HASHES = {
    "SFLLL_2_0-V2.0.xsd": "fff7449d00c715efb79d83b572bc7b1ef3e8171f6a9ba841436b26242e883664",
    "Global-V1.0.xsd": "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb",
    "GlobalLibrary-V2.0.xsd": "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
    "UniversalCodes-V2.0.xsd": "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
}
PROFILE = json.loads(
    (ROOT / "dist/forms/sflll/targets/grants-gov-xml.json").read_text()
)
XSD_SET = ExactXsdFixture(
    entrypoint="SFLLL_2_0-V2.0.xsd",
    files=tuple(
        PinnedXsdFile(
            name,
            XSD_FIXTURE if name == "SFLLL_2_0-V2.0.xsd" else DEPENDENCIES / name,
            digest,
        )
        for name, digest in XSD_HASHES.items()
    ),
    official_sha256=XSD_HASHES["SFLLL_2_0-V2.0.xsd"],
)


def _name(first: str, last: str) -> dict[str, str]:
    return {"firstName": first, "lastName": last}


def _organization(name: str, street: str, city: str) -> dict[str, Any]:
    return {
        "organizationName": name,
        "address": {"street1": street, "city": city, "state": "DC: District of Columbia"},
        "congressionalDistrict": "DC-000",
    }


class SflllXmlTests(unittest.TestCase):
    def test_full_material_change_subaward_response_validates_against_pinned_xsd(self) -> None:
        response = {
            "federalActionType": "Grant",
            "federalActionStatus": "PostAward",
            "reportType": "MaterialChange",
            "materialChange": {
                "year": "2026",
                "quarter": "3",
                "lastReportDate": "2026-03-31",
            },
            "reportingEntityType": "SubAwardee",
            "reportingOrganization": _organization("Subawardee Research", "10 Local Way", "Washington"),
            "tier": 0,
            "primeOrganization": _organization("Prime Research", "1 Prime Way", "Washington"),
            "federalAgencyDepartment": "Department of Research",
            "federalProgram": {
                "name": "Research Program",
                "assistanceListingNumber": "12.345",
            },
            "federalActionNumber": "AWARD-123",
            "awardAmount": "1234567890123.45",
            "lobbyingRegistrant": {
                "name": _name("Alex", "Registrant"),
                "address": {"street1": "4 Lobby Lane", "city": "Washington"},
            },
            "individualsPerformingServices": [
                {"name": _name("Jamie", "One")},
                {
                    "name": _name("Taylor", "Two"),
                    "address": {"street1": "5 Service St", "city": "Washington"},
                },
            ],
            "signatureBlock": {
                "name": _name("Sam", "Signer"),
                "title": "Director",
                "phone": "202-555-0100",
                "signedDate": "2026-08-23",
                "signature": "Sam Signer",
            },
        }
        xml = render_profile_xml(PROFILE, response)
        validation = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(validation.returncode, 0, validation.stderr)

        root = ET.fromstring(xml)
        report_entity = root.find(f"{{{FORM_NS}}}ReportEntity")
        self.assertIsNotNone(report_entity)
        assert report_entity is not None
        self.assertEqual(report_entity.attrib[f"{{{FORM_NS}}}ReportEntityType"], "SubAwardee")
        self.assertEqual(report_entity.findtext(f"{{{FORM_NS}}}ReportEntityIsPrime"), "N: No")
        prime = report_entity.find(f"{{{FORM_NS}}}PrimeIfSubawardee")
        self.assertIsNotNone(prime)
        assert prime is not None
        self.assertEqual(prime.findtext(f"{{{FORM_NS}}}EntityType"), "Prime")
        individuals = root.findall(
            f"{{{FORM_NS}}}IndividualsPerformingServices/{{{FORM_NS}}}Individual"
        )
        self.assertEqual(len(individuals), 2)


if __name__ == "__main__":
    unittest.main()
