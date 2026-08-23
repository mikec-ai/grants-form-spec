from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).parents[1]
AUDIT_ROOT = ROOT / "research/sf424d-family"
FIXTURE_ROOT = ROOT / "tests/fixtures/grants-gov-xsd/sf424d-family-1.1"
XSD_NS = "http://www.w3.org/2001/XMLSchema"
XSD_HASHES = {
    "SF424D-V1.1.xsd": "22026ea7130a01b8674e1c3ce1668e1b57d5be65498b5a76042eb80d38de77f1",
    "Individual_SF424D-V1.1.xsd": "52187d42b9ca30cf1f2f95de50be13bbd9ae333ede4b843e8c43b23db4489356",
    "Mandatory_SF424D-V1.1.xsd": "6685f2c19329db0ee959e2453cbcaf749e9bb2d7f45cb96892d9a4e71d87f68d",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode()


def xsd_type(path: Path, name: str) -> ET.Element:
    root = ET.parse(path).getroot()
    result = root.find(f"{{{XSD_NS}}}complexType[@name='{name}']")
    if result is None:
        raise AssertionError(f"missing XSD complex type {name} in {path.name}")
    return result


class Sf424dFamilyAuditTests(unittest.TestCase):
    def test_all_three_active_profiles_have_pinned_official_sources(self) -> None:
        audit = load(AUDIT_ROOT / "official-source-audit.json")
        profiles = {profile["id"]: profile for profile in audit["profiles"]}

        self.assertEqual(set(profiles), {"sf424d", "sf424d-individual", "sf424d-mandatory"})
        self.assertEqual({profile["status"] for profile in profiles.values()}, {"Active"})
        self.assertEqual({profile["formVersion"] for profile in profiles.values()}, {"1.1"})
        self.assertEqual({profile["ombNumber"] for profile in profiles.values()}, {"4040-0009"})
        self.assertEqual(
            {profile["ombExpirationDate"] for profile in profiles.values()},
            {"2028-06-30"},
        )
        for profile in profiles.values():
            self.assertEqual(
                set(profile["artifacts"]),
                {"xsd", "dat", "instructions", "samplePdf", "readOnlyPdf"},
            )
            for source in profile["artifacts"].values():
                self.assertTrue(source["uri"].startswith("https://"))
                self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")

    def test_pinned_xsd_fixtures_are_exact_official_bytes(self) -> None:
        for name, expected in XSD_HASHES.items():
            self.assertEqual(sha256(FIXTURE_ROOT / name), expected)

    def test_policy_is_one_versioned_bundle_not_twenty_questions(self) -> None:
        audit = load(AUDIT_ROOT / "official-source-audit.json")
        policy = load(AUDIT_ROOT / audit["sharedPolicy"]["artifact"])
        texts = [item["text"] for item in policy["items"]]

        self.assertEqual(policy["status"], "source-bound-unreviewed")
        self.assertEqual(policy["itemCount"], 20)
        self.assertEqual([item["ordinal"] for item in policy["items"]], list(range(1, 21)))
        self.assertEqual(
            hashlib.sha256(canonical_json(texts)).hexdigest(),
            audit["sharedPolicy"]["canonicalTextArraySha256"],
        )
        self.assertTrue(audit["sharedPolicy"]["identicalAcrossProfiles"])

    def test_profile_ownership_differences_are_explicit(self) -> None:
        audit = load(AUDIT_ROOT / "official-source-audit.json")
        profiles = {profile["id"]: profile for profile in audit["profiles"]}

        self.assertEqual(
            profiles["sf424d"]["presentation"],
            {
                "applicantLabel": "Applicant Organization",
                "representativeTitleRole": "prefilled",
                "applicantOrganizationRole": "prefilled",
            },
        )
        self.assertEqual(
            profiles["sf424d-individual"]["presentation"],
            {
                "applicantLabel": "Applicant Name",
                "representativeTitleRole": "applicantInput",
                "applicantOrganizationRole": "applicantInput",
            },
        )
        self.assertEqual(
            profiles["sf424d-mandatory"]["presentation"],
            {
                "applicantLabel": "Applicant Organization",
                "representativeTitleRole": "prefilled",
                "applicantOrganizationRole": "prefilled",
            },
        )
        shared = {field["canonicalName"]: field for field in audit["sharedFields"]}
        self.assertEqual(shared["signature"]["responseRole"], "systemValue")
        self.assertEqual(shared["signedDate"]["responseRole"], "systemValue")
        self.assertTrue(all(field["requiredByDat"] for field in shared.values()))

    def test_individual_and_mandatory_wire_shapes_differ_only_by_namespace(self) -> None:
        individual = (FIXTURE_ROOT / "Individual_SF424D-V1.1.xsd").read_text()
        mandatory = (FIXTURE_ROOT / "Mandatory_SF424D-V1.1.xsd").read_text()
        individual = individual.replace("Individual_SF424D", "PROFILE")
        mandatory = mandatory.replace("Mandatory_SF424D", "PROFILE")
        self.assertEqual(individual, mandatory)

    def test_base_and_variant_version_wiring_stays_declarative(self) -> None:
        base = xsd_type(FIXTURE_ROOT / "SF424D-V1.1.xsd", "AssurancesType")
        individual = xsd_type(
            FIXTURE_ROOT / "Individual_SF424D-V1.1.xsd", "AssurancesType"
        )
        mandatory = xsd_type(
            FIXTURE_ROOT / "Mandatory_SF424D-V1.1.xsd", "AssurancesType"
        )

        def child_refs(node: ET.Element) -> list[str]:
            sequence = node.find(f"{{{XSD_NS}}}sequence")
            assert sequence is not None
            return [element.attrib["ref"] for element in sequence]

        self.assertEqual(
            child_refs(base),
            [
                "glob:FormVersionIdentifier",
                "SF424D:AuthorizedRepresentative",
                "SF424D:ApplicantOrganizationName",
                "SF424D:SubmittedDate",
            ],
        )
        self.assertEqual(
            [ref.split(":", 1)[1] for ref in child_refs(individual)],
            ["AuthorizedRepresentative", "ApplicantOrganizationName", "SubmittedDate"],
        )
        self.assertEqual(
            [ref.split(":", 1)[1] for ref in child_refs(mandatory)],
            ["AuthorizedRepresentative", "ApplicantOrganizationName", "SubmittedDate"],
        )

        base_attributes = [node.attrib for node in base.findall(f"{{{XSD_NS}}}attribute")]
        variant_attributes = [
            node.attrib for node in individual.findall(f"{{{XSD_NS}}}attribute")
        ]
        self.assertIn(
            {"ref": "glob:coreSchemaVersion", "use": "required", "fixed": "1.1"},
            base_attributes,
        )
        self.assertIn(
            {
                "name": "FormVersion",
                "type": "globLib:FormVersionDataType",
                "use": "required",
                "fixed": "1.1",
            },
            variant_attributes,
        )


if __name__ == "__main__":
    unittest.main()
