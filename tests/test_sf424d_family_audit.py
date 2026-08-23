from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).parents[1]
AUDIT_ROOT = ROOT / "research/sf424d-family"
FIXTURE_ROOT = ROOT / "tests/fixtures/grants-gov-xsd/sf424d-family-1.1"
DEPENDENCY_ROOT = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
XSD_NS = "http://www.w3.org/2001/XMLSchema"
GLOBAL_NS = "http://apply.grants.gov/system/Global-V1.0"
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


def normalize_source_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


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

        self.assertEqual(set(profiles), {"sf424d", "individual-sf424d", "mandatory-sf424d"})
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

    def test_policy_equivalence_is_derived_for_each_pinned_profile(self) -> None:
        audit = load(AUDIT_ROOT / "official-source-audit.json")
        extract = load(AUDIT_ROOT / audit["sharedPolicy"]["profileExtractArtifact"])
        research = load(AUDIT_ROOT / audit["sharedPolicy"]["artifact"])
        profiles = {profile["id"]: profile for profile in audit["profiles"]}
        expected = [item["text"] for item in research["items"]]
        derived: dict[str, list[str]] = {}

        self.assertEqual(extract["status"], "source-bound-unreviewed")
        self.assertEqual(
            extract["assuranceFieldOrder"],
            [item["fieldId"] for item in extract["profiles"][0]["assuranceItems"]],
        )
        for profile in extract["profiles"]:
            form_id = profile["formId"]
            source = profile["source"]
            self.assertEqual(profile["formVersion"], profiles[form_id]["formVersion"])
            self.assertEqual(source["uri"], profiles[form_id]["artifacts"]["dat"]["uri"])
            self.assertEqual(
                source["sha256"], profiles[form_id]["artifacts"]["dat"]["sha256"]
            )
            texts = [
                normalize_source_text(item["text"])
                for item in profile["assuranceItems"]
            ]
            digest = hashlib.sha256(canonical_json(texts)).hexdigest()
            self.assertEqual(digest, profile["normalizedTextArraySha256"])
            self.assertEqual(
                digest,
                audit["sharedPolicy"]["perProfileNormalizedTextArraySha256"][form_id],
            )
            self.assertEqual(texts, expected)
            derived[form_id] = texts

        self.assertEqual(
            audit["sharedPolicy"]["equivalenceStatus"],
            "deterministic-match-unreviewed",
        )
        self.assertEqual(len({tuple(items) for items in derived.values()}), 1)

    def test_current_burden_interaction_is_preserved_but_not_silently_resolved(self) -> None:
        audit = load(AUDIT_ROOT / "official-source-audit.json")
        extract = load(AUDIT_ROOT / audit["burdenInteraction"]["profileExtractArtifact"])
        profiles = {profile["id"]: profile for profile in audit["profiles"]}
        texts = []

        for profile in extract["profiles"]:
            form_id = profile["formId"]
            burden = profile["burdenInteraction"]
            text = normalize_source_text(burden["text"])
            self.assertEqual(burden["label"], "View Burden Statement")
            self.assertEqual(
                hashlib.sha256(text.encode()).hexdigest(),
                burden["normalizedTextSha256"],
            )
            self.assertEqual(
                profile["source"]["sha256"],
                profiles[form_id]["artifacts"]["dat"]["sha256"],
            )
            self.assertIn("4040-0009", text)
            self.assertIn("30 minutes per response", text)
            self.assertIn("U.S. Department of Health & Human Services", text)
            texts.append(text)

        self.assertEqual(len(set(texts)), 1)
        self.assertEqual(
            hashlib.sha256(texts[0].encode()).hexdigest(),
            audit["burdenInteraction"]["normalizedTextSha256"],
        )
        self.assertEqual(
            audit["burdenInteraction"]["presentationDisposition"],
            "unresolved-pending-policy-owner-review",
        )
        printed = load(ROOT / "policies/construction-assurances-1.1.json")[
            "sections"
        ][0]["text"]
        self.assertIn("15 minutes per response", printed)
        self.assertNotEqual(printed, texts[0])

    def test_profile_ownership_differences_are_explicit(self) -> None:
        audit = load(AUDIT_ROOT / "official-source-audit.json")
        profiles = {profile["id"]: profile for profile in audit["profiles"]}

        self.assertEqual(
            profiles["sf424d"]["presentation"],
            {
                "applicantLabel": "Applicant Organization",
                "titleRole": "prefilled",
                "applicantOrganizationRole": "prefilled",
            },
        )
        self.assertEqual(
            profiles["individual-sf424d"]["presentation"],
            {
                "applicantLabel": "Applicant Name",
                "titleRole": "applicantInput",
                "applicantOrganizationRole": "applicantInput",
            },
        )
        self.assertEqual(
            profiles["mandatory-sf424d"]["presentation"],
            {
                "applicantLabel": "Applicant Organization",
                "titleRole": "prefilled",
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

    def test_minimal_profile_canaries_validate_against_exact_official_xsds(self) -> None:
        xmllint = shutil.which("xmllint")
        if xmllint is None:
            self.fail("xmllint is required for exact official-XSD validation")

        profiles = [
            {
                "xsd": "SF424D-V1.1.xsd",
                "namespace": "http://apply.grants.gov/forms/SF424D-V1.1",
                "versionElement": True,
                "versionAttribute": (GLOBAL_NS, "coreSchemaVersion"),
            },
            {
                "xsd": "Individual_SF424D-V1.1.xsd",
                "namespace": "http://apply.grants.gov/forms/Individual_SF424D-V1.1",
                "versionElement": False,
                "versionAttribute": (
                    "http://apply.grants.gov/forms/Individual_SF424D-V1.1",
                    "FormVersion",
                ),
            },
            {
                "xsd": "Mandatory_SF424D-V1.1.xsd",
                "namespace": "http://apply.grants.gov/forms/Mandatory_SF424D-V1.1",
                "versionElement": False,
                "versionAttribute": (
                    "http://apply.grants.gov/forms/Mandatory_SF424D-V1.1",
                    "FormVersion",
                ),
            },
        ]

        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            dependencies = ["Global-V1.0.xsd", "GlobalLibrary-V2.0.xsd", "UniversalCodes-V2.0.xsd"]
            for name in dependencies:
                source = (DEPENDENCY_ROOT / name).read_text()
                for dependency in dependencies:
                    source = source.replace(
                        f"https://apply07.grants.gov/apply/system/schemas/{dependency}",
                        dependency,
                    )
                (temp / name).write_text(source)

            for profile in profiles:
                source = (FIXTURE_ROOT / profile["xsd"]).read_text()
                for dependency in dependencies:
                    source = source.replace(
                        f"https://apply07.grants.gov/apply/system/schemas/{dependency}",
                        dependency,
                    )
                (temp / profile["xsd"]).write_text(source)

                namespace = profile["namespace"]
                root = ET.Element(f"{{{namespace}}}Assurances")
                root.set(f"{{{namespace}}}programType", "Construction")
                attribute_namespace, attribute_name = profile["versionAttribute"]
                root.set(f"{{{attribute_namespace}}}{attribute_name}", "1.1")
                if profile["versionElement"]:
                    child = ET.SubElement(root, f"{{{GLOBAL_NS}}}FormVersionIdentifier")
                    child.text = "1.1"
                xml_path = temp / f"{profile['xsd']}.xml"
                xml_path.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))

                validation = subprocess.run(
                    [xmllint, "--noout", "--schema", str(temp / profile["xsd"]), str(xml_path)],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(validation.returncode, 0, validation.stderr)


if __name__ == "__main__":
    unittest.main()
