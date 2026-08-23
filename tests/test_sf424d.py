from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FORM_IDS = ("sf424d", "mandatory-sf424d", "individual-sf424d")
XSD_HASHES = {
    "sf424d": "22026ea7130a01b8674e1c3ce1668e1b57d5be65498b5a76042eb80d38de77f1",
    "mandatory-sf424d": "6685f2c19329db0ee959e2453cbcaf749e9bb2d7f45cb96892d9a4e71d87f68d",
    "individual-sf424d": "52187d42b9ca30cf1f2f95de50be13bbd9ae333ede4b843e8c43b23db4489356",
}
EXTRACTION_HASHES = {
    "sf424d": "bfbb75b5f6eaac199f1e2498c0a2cfa983380d6e16d33f453a24943892dcc67d",
    "mandatory-sf424d": "b9ec68c89b3b394718127f8e7aa21808d4700fa188f5efb020f97d28e9155d50",
    "individual-sf424d": "550b9078e0ad602ec087778a5048b824cc85d4c03852ee55dfe87bb7eebf73e7",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text())


class Sf424dFamilyTests(unittest.TestCase):
    def test_one_versioned_policy_is_bound_to_all_profiles(self) -> None:
        source = load(ROOT / "policies/construction-assurances-1.1.json")
        self.assertEqual(source["contract"], "policy-content/v1")
        self.assertEqual(source["id"], "grants-gov/construction-assurances")
        self.assertEqual(source["version"], "1.1")
        self.assertEqual(source["sections"][0]["presentationOrder"], ["text", "note"])
        self.assertEqual(
            source["sections"][1]["presentationOrder"],
            ["note", "preamble", "items"],
        )
        self.assertEqual(len(source["sections"][1]["items"]), 20)
        self.assertEqual(
            [item["ordinal"] for item in source["sections"][1]["items"]],
            list(range(1, 21)),
        )
        self.assertTrue(
            all(
                not item["text"].startswith(f"{item['ordinal']}.")
                for item in source["sections"][1]["items"]
            )
        )
        audited = load(
            ROOT / "research/sf424d-family/construction-assurances-v1.1.json"
        )
        self.assertEqual(
            [f"{item['ordinal']}. {item['text']}" for item in source["sections"][1]["items"]],
            [item["text"] for item in audited["items"]],
        )

        for form_id in FORM_IDS:
            emitted = load(ROOT / f"dist/forms/{form_id}/policy-content.json")
            binding = load(ROOT / f"dist/forms/{form_id}/policy-binding.json")
            manifest = load(ROOT / f"dist/forms/{form_id}/manifest.json")
            self.assertEqual(emitted, source)
            self.assertEqual(binding["formId"], form_id)
            self.assertEqual(binding["policy"], {"id": source["id"], "version": "1.1"})
            self.assertEqual(binding["acceptance"]["event"], "submission")
            self.assertEqual(binding["acceptance"]["attestsTo"], ["assurances"])
            self.assertEqual(manifest["artifacts"]["policy-content.json"], "generated")
            self.assertEqual(manifest["artifacts"]["policy-binding.json"], "generated")

    def test_profile_deltas_preserve_response_ownership_and_presentation(self) -> None:
        for form_id in FORM_IDS:
            schema = load(ROOT / f"dist/forms/{form_id}/schema.json")
            ui = load(ROOT / f"dist/forms/{form_id}/sgg/ui-schema.json")
            rules = load(ROOT / f"dist/forms/{form_id}/sgg/rule-schema.json")
            binding = load(ROOT / f"dist/forms/{form_id}/policy-binding.json")

            self.assertEqual(schema["required"], ["title", "applicantOrganization"])
            self.assertTrue(schema["properties"]["signature"]["readOnly"])
            self.assertTrue(schema["properties"]["signedDate"]["readOnly"])
            self.assertEqual(rules["signature"]["gg_post_population"]["rule"], "signature")
            self.assertEqual(rules["signedDate"]["gg_post_population"]["rule"], "current_date")

            self.assertEqual(
                [(section["name"], section["label"]) for section in ui],
                [
                    ("burdenStatement", "1. Burden Statement"),
                    ("directions", "2. Acknowledgement and assurances"),
                    ("acceptance", "3. Signature"),
                ],
            )
            acceptance = ui[-1]
            self.assertEqual(
                [row["definition"] for row in acceptance["children"]],
                [
                    "/properties/signature",
                    "/properties/title",
                    "/properties/applicantOrganization",
                    "/properties/signedDate",
                ],
            )
            field_by_role = {
                row["role"]: row for row in binding["acceptance"]["fields"]
            }
            if form_id == "individual-sf424d":
                self.assertNotIn("readOnly", schema["properties"]["title"])
                self.assertNotIn("readOnly", schema["properties"]["applicantOrganization"])
                self.assertEqual(schema["properties"]["applicantOrganization"]["title"], "Applicant Name")
                self.assertEqual(acceptance["children"][1]["type"], "field")
                self.assertEqual(acceptance["children"][2]["type"], "field")
                self.assertEqual(field_by_role["signerTitle"]["responseRole"], "applicantInput")
                self.assertTrue(field_by_role["signerTitle"]["editable"])
            else:
                self.assertTrue(schema["properties"]["title"]["readOnly"])
                self.assertTrue(schema["properties"]["applicantOrganization"]["readOnly"])
                self.assertEqual(acceptance["children"][1]["type"], "null")
                self.assertEqual(acceptance["children"][2]["type"], "null")
                self.assertEqual(field_by_role["signerTitle"]["responseRole"], "systemValue")
                self.assertFalse(field_by_role["signerTitle"]["editable"])

    def test_policy_projection_preserves_official_reading_order_once(self) -> None:
        ui = load(ROOT / "dist/forms/sf424d/sgg/ui-schema.json")
        description = next(section["description"] for section in ui if section["name"] == "directions")
        policy = load(ROOT / "policies/construction-assurances-1.1.json")
        assurance = policy["sections"][1]
        self.assertLess(description.index(assurance["note"]), description.index(assurance["preamble"]))
        self.assertLess(description.index(assurance["preamble"]), description.index("1. "))
        self.assertEqual(description.count("\n\n"), 21)
        for ordinal in range(1, 21):
            self.assertEqual(description.count(f"\n\n{ordinal}. "), 1)

    def test_xml_profiles_pin_official_xsds_and_wire_differences(self) -> None:
        profiles = {
            form_id: load(ROOT / f"dist/forms/{form_id}/targets/grants-gov-xml.json")
            for form_id in FORM_IDS
        }
        for form_id, profile in profiles.items():
            self.assertEqual(profile["contract"], "grants-gov-xml-profile/v1")
            self.assertEqual(profile["formId"], form_id)
            self.assertEqual(profile["xsd"]["sha256"], XSD_HASHES[form_id])
            self.assertNotIn('"$ref"', json.dumps(profile))
            self.assertEqual(
                set(profile["mapping"]["fields"]) - {"formVersionIdentifier"},
                {"authorizedRepresentative", "applicantOrganization", "signedDate"},
            )

        self.assertEqual(
            profiles["sf424d"]["root"]["attributes"],
            {"SF424D:programType": "Construction", "glob:coreSchemaVersion": "1.1"},
        )
        self.assertIn("formVersionIdentifier", profiles["sf424d"]["mapping"]["fields"])
        for form_id, prefix in (
            ("mandatory-sf424d", "Mandatory_SF424D"),
            ("individual-sf424d", "Individual_SF424D"),
        ):
            self.assertEqual(
                profiles[form_id]["root"]["attributes"],
                {
                    f"{prefix}:programType": "Construction",
                    f"{prefix}:FormVersion": "1.1",
                },
            )
            self.assertNotIn("formVersionIdentifier", profiles[form_id]["mapping"]["fields"])

    def test_release_gates_keep_operational_work_explicit(self) -> None:
        for form_id in FORM_IDS:
            binding = load(ROOT / f"policy-bindings/forms/{form_id}.json")
            self.assertEqual(binding["release"]["status"], "draft")
            gates = {gate["id"]: gate["status"] for gate in binding["release"]["gates"]}
            self.assertEqual(gates["official-source-provenance"], "passed")
            self.assertEqual(gates["cross-profile-policy-equivalence"], "passed")
            self.assertEqual(gates["semantic-review"], "pending")
            self.assertEqual(gates["accessibility-review"], "pending")
            self.assertEqual(gates["consumer-lifecycle-review"], "pending")
            self.assertEqual(gates["production-registration"], "pending")

    def test_evidence_pins_each_exact_profile_source_set(self) -> None:
        required_types = {"xsd", "dat", "instructions", "pdf"}
        for form_id in FORM_IDS:
            evidence = load(ROOT / f"evidence/forms/{form_id}/evidence.json")
            source_types = {source["type"] for source in evidence["sources"]}
            self.assertTrue(required_types.issubset(source_types))
            xsd = next(source for source in evidence["sources"] if source["id"].endswith("-xsd"))
            self.assertEqual(xsd["sha256"], XSD_HASHES[form_id])
            self.assertEqual(
                evidence["extraction"]["revision"],
                "4312f6504b060e2b9ffdbd2307fc41130c3123a0",
            )
            self.assertEqual(evidence["extraction"]["sourceSetSha256"], EXTRACTION_HASHES[form_id])
            self.assertEqual(evidence["semanticReview"]["status"], "proposed")
            self.assertEqual(len(evidence["semanticReview"]["mappings"]), 4)

        base = load(ROOT / "evidence/forms/sf424d/evidence.json")
        oracle = next(source for source in base["sources"] if source["id"] == "sgg-oracle")
        self.assertEqual(
            oracle["sha256"],
            "8236db821592dc3b36e3e95971b514af4657b3b41e781259f0797e46d091fb2a",
        )


if __name__ == "__main__":
    unittest.main()
