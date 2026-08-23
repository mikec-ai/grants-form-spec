from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


ROOT = Path(__file__).parents[1]
FORM = ROOT / "dist/forms/gg-lobbying"
FORM_NS = "http://apply.grants.gov/forms/GG_LobbyingForm-V1.1"
GLOBAL_LIBRARY_NS = "http://apply.grants.gov/system/GlobalLibrary-V2.0"
XSD = ROOT / "tests/fixtures/grants-gov-xsd/gg-lobbying-1.1/GG_LobbyingForm-V1.1.xsd"
DEPENDENCIES = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
XSD_HASH = "a41d88b19e240dbb5f9b13815c0426d2396414fc1af8d6ab6a96f35855a0a5f7"
ORACLE_REVISION = "30dd50cf0493146c32f89f78398979523e040080"
ORACLE_HASH = "bdf73a05a75b5020218f06864118f4c1e9ccc396934feaccc49e9acbbe406ad8"


def load(path: Path) -> Any:
    return json.loads(path.read_text())


def _qname(profile: dict[str, Any], prefix: str, name: str) -> str:
    return f"{{{profile['namespaces'][prefix]}}}{name}"


def render_xml(response: dict[str, Any]) -> bytes:
    profile = load(FORM / "targets/grants-gov-xml.json")
    ET.register_namespace("GG_LobbyingForm", FORM_NS)
    ET.register_namespace("globLib", GLOBAL_LIBRARY_NS)
    root = ET.Element(_qname(profile, "default", profile["root"]["element"]))
    for name, value in profile["root"]["attributes"].items():
        root.set(_qname(profile, "default", name), value)

    for field, mapping in profile["mapping"]["fields"].items():
        value = response[field]
        child = ET.SubElement(root, _qname(profile, mapping["namespace"], mapping["element"]))
        if mapping["kind"] == "value":
            child.text = value
            continue
        for nested_field, nested_mapping in mapping["fields"].items():
            nested_value = value.get(nested_field)
            if nested_value is None:
                continue
            leaf = ET.SubElement(
                child,
                _qname(profile, nested_mapping["namespace"], nested_mapping["element"]),
            )
            leaf.text = nested_value
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def validate_exact_xsd(xml: bytes) -> subprocess.CompletedProcess[str]:
    xmllint = shutil.which("xmllint")
    if xmllint is None:
        raise AssertionError("xmllint is required for the pinned XSD check")
    assert hashlib.sha256(XSD.read_bytes()).hexdigest() == XSD_HASH
    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        files = {
            "GG_LobbyingForm-V1.1.xsd": XSD,
            "Global-V1.0.xsd": DEPENDENCIES / "Global-V1.0.xsd",
            "GlobalLibrary-V2.0.xsd": DEPENDENCIES / "GlobalLibrary-V2.0.xsd",
            "UniversalCodes-V2.0.xsd": DEPENDENCIES / "UniversalCodes-V2.0.xsd",
        }
        for name, source_path in files.items():
            source = source_path.read_text()
            for dependency in files:
                source = source.replace(
                    f"https://apply07.grants.gov/apply/system/schemas/{dependency}",
                    dependency,
                )
            (temp / name).write_text(source)
        xml_path = temp / "response.xml"
        xml_path.write_bytes(xml)
        return subprocess.run(
            ["xmllint", "--noout", "--schema", str(temp / "GG_LobbyingForm-V1.1.xsd"), str(xml_path)],
            text=True,
            capture_output=True,
            check=False,
        )


class GgLobbyingTests(unittest.TestCase):
    def test_profile_reuses_reviewed_identity_and_system_primitives(self) -> None:
        schema = load(FORM / "schema.json")
        ui = load(FORM / "sgg/ui-schema.json")
        rules = load(FORM / "sgg/rule-schema.json")
        index = load(FORM / "index.json")

        self.assertEqual(schema["required"], [
            "organizationName",
            "authorizedRepresentativeName",
            "authorizedRepresentativeTitle",
        ])
        self.assertEqual(
            schema["properties"]["organizationName"]["$ref"],
            "../../question-bank/primary-org/legal-name/schema.json",
        )
        self.assertEqual(
            schema["properties"]["authorizedRepresentativeName"]["$ref"],
            "../../question-bank/aor/name/schema.json",
        )
        self.assertEqual(
            schema["properties"]["authorizedRepresentativeSignature"]["$ref"],
            "../../question-bank/aor/signature/schema.json",
        )
        self.assertEqual(rules, {
            "authorizedRepresentativeSignature": {"gg_post_population": {"rule": "signature"}},
            "submittedDate": {"gg_post_population": {"rule": "current_date"}},
        })
        occurrences = {row["path"]: row for row in index["fieldOccurrences"]}
        self.assertEqual(occurrences["/authorizedRepresentativeSignature"]["responseRole"], "systemValue")
        self.assertEqual(occurrences["/submittedDate"]["responseRole"], "systemValue")

        certification = ui[0]
        self.assertEqual(certification["name"], "certification")
        self.assertEqual(certification["children"], [])
        self.assertIn("No Federal appropriated funds", certification["description"])
        self.assertIn("Statement for Loan Guarantees and Loan Insurance", certification["description"])

    def test_profile_is_distinct_from_sflll(self) -> None:
        manifest = load(FORM / "manifest.json")
        sflll = load(ROOT / "dist/forms/sflll/manifest.json")
        self.assertEqual(manifest["form"]["legacyFormId"], 255)
        self.assertEqual(manifest["form"]["formVersion"], "1.1")
        self.assertEqual(manifest["form"]["shortFormName"], "GG_LobbyingForm")
        self.assertNotEqual(manifest["form"]["id"], sflll["form"]["id"])
        self.assertNotEqual(manifest["form"]["legacyFormId"], sflll["form"]["legacyFormId"])

    def test_official_sources_and_legacy_oracle_are_pinned(self) -> None:
        evidence = load(FORM / "evidence.json")
        sources = {row["id"]: row for row in evidence["sources"]}
        self.assertEqual(sources["grantsgov-gg-lobbying-xsd-1.1"]["sha256"], XSD_HASH)
        oracle = sources["sgg-legacy-gg-lobbying-oracle-30dd50cf"]
        self.assertIn(ORACLE_REVISION, oracle["uri"])
        self.assertEqual(oracle["nativeVersion"], ORACLE_REVISION)
        self.assertEqual(oracle["sha256"], ORACLE_HASH)
        self.assertEqual(
            evidence["extraction"]["sourceSetSha256"],
            "b545bd44a103bba32721c07e7e1dd0d708e5435b416a2ccf1005cc4de9325895",
        )
        self.assertEqual(evidence["semanticReview"]["status"], "proposed")

    def test_complete_response_validates_against_exact_official_xsd(self) -> None:
        response = {
            "organizationName": "Example Research Organization",
            "authorizedRepresentativeName": {
                "prefix": "Dr.",
                "firstName": "Ada",
                "middleName": "M",
                "lastName": "Lovelace",
                "suffix": "PhD",
            },
            "authorizedRepresentativeTitle": "Director",
            "authorizedRepresentativeSignature": "Ada Lovelace",
            "submittedDate": "2026-08-23",
        }
        xml = render_xml(response)
        validation = validate_exact_xsd(xml)
        self.assertEqual(validation.returncode, 0, validation.stderr)
        root = ET.fromstring(xml)
        self.assertEqual(root.tag, f"{{{FORM_NS}}}LobbyingForm")
        self.assertEqual(root.findtext(f"{{{FORM_NS}}}ApplicantName"), response["organizationName"])
        self.assertEqual(
            root.findtext(
                f"{{{FORM_NS}}}AuthorizedRepresentativeName/"
                f"{{{GLOBAL_LIBRARY_NS}}}FirstName"
            ),
            "Ada",
        )


if __name__ == "__main__":
    unittest.main()
