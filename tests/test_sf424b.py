from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FORM_IDS = ("sf424b", "rr-sf424b", "mandatory-sf424b", "individual-sf424b")
XSD_HASHES = {
    "sf424b": "b0da616d262329e869b7c2a12146396fd8a279d2a1723521271c519f4571075d",
    "rr-sf424b": "511de9a5594a739ce596a33a92d3dec1bac2a32f193a2fe6b4799b45f29ff296",
    "mandatory-sf424b": "bcbe0010ba734ebeb0e3b6bd331a936d716b9896446231be90a11b005faf9579",
    "individual-sf424b": "1fe96cd37f1933f1c251efbbfbafae85c2e4869359f216a645024860ee29c983",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text())


class Sf424bFamilyTests(unittest.TestCase):
    def test_one_versioned_policy_is_bound_to_all_profiles(self) -> None:
        source = load(ROOT / "policies/nonconstruction-assurances-1.1.json")
        self.assertEqual(source["contract"], "policy-content/v1")
        self.assertEqual(source["id"], "grants-gov/nonconstruction-assurances")
        self.assertEqual(source["version"], "1.1")
        self.assertEqual(source["sections"][0]["presentationOrder"], ["text"])
        self.assertEqual(
            source["sections"][1]["presentationOrder"],
            ["note", "preamble", "items"],
        )
        self.assertEqual(len(source["sections"][1]["items"]), 19)
        self.assertEqual(
            [item["ordinal"] for item in source["sections"][1]["items"]],
            list(range(1, 20)),
        )

        for form_id in FORM_IDS:
            emitted = load(ROOT / f"dist/forms/{form_id}/policy-content.json")
            binding = load(ROOT / f"dist/forms/{form_id}/policy-binding.json")
            manifest = load(ROOT / f"dist/forms/{form_id}/manifest.json")
            self.assertEqual(emitted, source)
            self.assertEqual(binding["formId"], form_id)
            self.assertEqual(binding["policy"], {"id": source["id"], "version": "1.1"})
            self.assertEqual(binding["acceptance"]["event"], "submission")
            self.assertEqual(
                set(binding["acceptance"]["attestsTo"]), {"assurances"}
            )
            self.assertEqual(
                manifest["artifacts"]["policy-content.json"], "generated"
            )
            self.assertEqual(
                manifest["artifacts"]["policy-binding.json"], "generated"
            )

    def test_profile_deltas_are_declarative_and_preserve_response_ownership(self) -> None:
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

            acceptance = next(section for section in ui if section["name"] == "acceptance")
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
            if form_id == "individual-sf424b":
                self.assertNotIn("readOnly", schema["properties"]["title"])
                self.assertNotIn("readOnly", schema["properties"]["applicantOrganization"])
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

    def test_policy_projection_preserves_official_reading_order(self) -> None:
        ui = load(ROOT / "dist/forms/sf424b/sgg/ui-schema.json")
        description = next(
            section["description"]
            for section in ui
            if section["name"] == "acknowledgement"
        )
        policy = load(ROOT / "policies/nonconstruction-assurances-1.1.json")
        assurance = policy["sections"][1]
        self.assertLess(description.index(assurance["note"]), description.index(assurance["preamble"]))
        self.assertLess(description.index(assurance["preamble"]), description.index("1. "))
        self.assertEqual(description.count("\n\n"), 20)

    def test_xml_profiles_pin_official_xsds_and_wire_differences(self) -> None:
        profiles = {
            form_id: load(ROOT / f"dist/forms/{form_id}/targets/grants-gov-xml.json")
            for form_id in FORM_IDS
        }
        for form_id, profile in profiles.items():
            self.assertEqual(profile["contract"], "grants-gov-xml-profile/v1")
            self.assertEqual(profile["formId"], form_id)
            self.assertEqual(profile["xsd"]["sha256"], XSD_HASHES[form_id])
            mapping = profile["mapping"]["fields"]
            self.assertEqual(
                set(mapping) - {"formVersionIdentifier"},
                {"authorizedRepresentative", "applicantOrganization", "signedDate"},
            )

        self.assertEqual(
            profiles["sf424b"]["root"]["attributes"],
            {"programType": "Non-Construction", "glob:coreSchemaVersion": "1.1"},
        )
        self.assertIn("formVersionIdentifier", profiles["sf424b"]["mapping"]["fields"])
        self.assertEqual(
            profiles["rr-sf424b"]["root"]["attributes"],
            {"programType": "Non-Construction", "FormVersion": "1.1"},
        )
        self.assertIn("formVersionIdentifier", profiles["rr-sf424b"]["mapping"]["fields"])
        for form_id in ("mandatory-sf424b", "individual-sf424b"):
            self.assertEqual(
                profiles[form_id]["root"]["attributes"],
                {"FormVersion": "1.1", "programType": "Non-Construction"},
            )
            self.assertNotIn("formVersionIdentifier", profiles[form_id]["mapping"]["fields"])

    def test_release_gates_keep_operational_work_explicit(self) -> None:
        rr = load(ROOT / "policy-bindings/forms/rr-sf424b.json")
        self.assertEqual(rr["release"]["status"], "blocked")
        mismatch = next(
            gate for gate in rr["release"]["gates"]
            if gate["id"] == "official-xsd-version-consistency"
        )
        self.assertEqual(mismatch["status"], "blocked")
        self.assertIn("schema version attribute is 1.0", mismatch["note"])
        for form_id in FORM_IDS:
            binding = load(ROOT / f"policy-bindings/forms/{form_id}.json")
            gate_status = {gate["id"]: gate["status"] for gate in binding["release"]["gates"]}
            self.assertEqual(gate_status["policy-owner-review"], "pending")
            self.assertEqual(gate_status["accessibility-review"], "pending")
            self.assertEqual(gate_status["instructions-review"], "pending")
            self.assertEqual(gate_status["production-registration"], "pending")

    def test_evidence_pins_every_profile_and_the_legacy_oracle(self) -> None:
        expected_sources = {
            "sf424b": {
                "sf424b-xsd": XSD_HASHES["sf424b"],
                "sf424b-dat": "15944ea4df287b94e27e2f7e459c05a88e3fad74d39f2abd0bcad170c475665d",
                "sf424b-instructions": "61d72e945392ca0ae8494ab0fa6b21200f71583d5313e0843a25231d505f3ce7",
                "sf424b-pdf": "2ab0e5c91ac98824991bcfa22a283bc6e7b6b99a4f1125506e9befe57c68e51e",
                "sgg-oracle": "ca94f236d449f5e4437d03c33ebe09504fe1d02948d7bb17d16fc4a646d7d39a",
            },
            "rr-sf424b": {
                "rr-sf424b-xsd": XSD_HASHES["rr-sf424b"],
                "rr-sf424b-dat": "40d86b271c47beca5f5bcd9bfd34f6b05a555a63a58cb7a714474498e3c2731d",
                "rr-sf424b-instructions": "7403e9356b095107e64a409fd1a9ab190ca50f6fdbb6bccbdc45c33938af9216",
                "rr-sf424b-pdf": "510fcd6d6d328ba5c617f65f69af7e172aaab44695694d1068b193eca257bcd8",
            },
            "mandatory-sf424b": {
                "mandatory-sf424b-xsd": XSD_HASHES["mandatory-sf424b"],
                "mandatory-sf424b-dat": "77b0e06aefac0765b482e769ec0a5dcbea6628909e2e7a7f5965e9674355bc51",
                "mandatory-sf424b-instructions": "2084122b4d991e46b7accfbef9f041cf3e711912d586006f0109b0440d4e48e1",
                "mandatory-sf424b-pdf": "fb1fc7bb8cb2825dd400f951f2875876a36d78acb46506bc3993ce56f1ee80d1",
            },
            "individual-sf424b": {
                "individual-sf424b-xsd": XSD_HASHES["individual-sf424b"],
                "individual-sf424b-dat": "7b31671309bd4e16f2bc5e2bc040d40e8f47aace9e972e7ea1c38c19f7250adb",
                "individual-sf424b-instructions": "6d4260bf1b4aec06f68f5ef5f65f2bcfdeb70922180e5504745fba7af41d9a64",
                "individual-sf424b-pdf": "6508e0c1a57d1e28f1d4db3c663b1154d0e37d48495f7ced8beaf143d1f8958e",
            },
        }
        for form_id, expected in expected_sources.items():
            evidence = load(ROOT / f"evidence/forms/{form_id}/evidence.json")
            actual = {source["id"]: source["sha256"] for source in evidence["sources"]}
            self.assertEqual(actual, expected)
            self.assertEqual(
                evidence["extraction"]["revision"],
                "4312f6504b060e2b9ffdbd2307fc41130c3123a0",
            )
            expected_status = "unreviewed" if form_id == "rr-sf424b" else "proposed"
            self.assertEqual(evidence["semanticReview"]["status"], expected_status)


if __name__ == "__main__":
    unittest.main()
