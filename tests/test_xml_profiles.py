from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DIST_FORMS = ROOT / "dist/forms"
SOURCE = ROOT / "targets/grants-gov-xml"


def _json(path: Path) -> Any:
    return json.loads(path.read_text())


class GrantsGovXmlProfileTests(unittest.TestCase):
    def test_factored_profiles_remain_byte_identical_to_the_source_bound_baseline(self) -> None:
        expected = {
            "rr-budget": "b519089485c79277dd6eb21363624895eebfde882f5e2224b268692d606eafe3",
            "rr-sf424": "23015dd8940e677666e335d2533012865439952db03c57eea61056f8764ca9ca",
        }

        for form_id, digest in expected.items():
            artifact = DIST_FORMS / form_id / "targets/grants-gov-xml.json"
            self.assertEqual(hashlib.sha256(artifact.read_bytes()).hexdigest(), digest)

    def test_rr_sf424_factors_only_source_identical_global_library_types(self) -> None:
        source = _json(SOURCE / "mappings/rr-sf424-5.0.json")
        serialized = json.dumps(source)
        self.assertEqual(
            serialized.count("global-library-v2-human-name.json#/fields"), 3
        )
        self.assertEqual(
            serialized.count("global-library-v2-address-v3.json#/fields"), 4
        )

        evidence = _json(ROOT / "evidence/forms/rr-sf424/evidence.json")
        source_by_uri = {item["uri"]: item for item in evidence["sources"]}
        fragments = {
            "global-library-v2-human-name.json": ("globLib:HumanNameDataType", "2.0"),
            "global-library-v2-address-v3.json": ("globLib:AddressDataTypeV3", "2.0"),
            "attached-file-data-1.0.json": ("att:AttachedFileDataType", "1.0"),
        }
        for name, (expected_type, expected_version) in fragments.items():
            fragment = _json(SOURCE / "mappings" / name)
            xsd = fragment["evidence"]["xsd"]
            pinned = source_by_uri[xsd["uri"]]
            self.assertEqual(xsd["sha256"], pinned["sha256"])
            self.assertEqual(xsd["type"], expected_type)
            self.assertEqual(xsd["version"], expected_version)

    def test_all_authored_profiles_emit_self_contained_targets(self) -> None:
        form_ids = {
            "rr-budget",
            "rr-budget-10yr",
            "rr-subaward-budget",
            "rr-subaward-budget-30",
            "rr-subaward-budget-10yr-30",
            "rr-sf424",
            "performance-site",
            "rr-other-project-information",
            "phs398-modular-budget",
        }
        profiles = {
            form_id: _json(DIST_FORMS / form_id / "targets/grants-gov-xml.json")
            for form_id in form_ids
        }

        self.assertEqual(set(profiles), form_ids)
        for form_id, profile in profiles.items():
            self.assertEqual(profile["formId"], form_id)
            self.assertNotIn('"$ref"', json.dumps(profile))
            manifest = _json(DIST_FORMS / form_id / "manifest.json")
            self.assertEqual(
                manifest["artifacts"]["targets/grants-gov-xml.json"], "generated"
            )

    def test_all_profiles_reuse_one_authored_budget_mapping(self) -> None:
        shared = _json(SOURCE / "mappings/research-budget-3.0.json")["fields"]
        attachment = _json(SOURCE / "mappings/attached-file-data-1.0.json")["fields"]
        five_year = _json(DIST_FORMS / "rr-budget/targets/grants-gov-xml.json")
        ten_year = _json(DIST_FORMS / "rr-budget-10yr/targets/grants-gov-xml.json")
        self.assertEqual(five_year["mapping"]["fields"], shared)
        self.assertEqual(ten_year["mapping"]["fields"], shared)

        for form_id in (
            "rr-subaward-budget",
            "rr-subaward-budget-30",
            "rr-subaward-budget-10yr-30",
        ):
            profile = _json(DIST_FORMS / form_id / "targets/grants-gov-xml.json")
            self.assertEqual(
                profile["mapping"]["fields"]["budgetAttachments"]["items"]["fields"],
                shared,
            )
        profiles = [five_year, ten_year]
        profiles.extend(
            _json(DIST_FORMS / form_id / "targets/grants-gov-xml.json")
            for form_id in (
                "rr-subaward-budget",
                "rr-subaward-budget-30",
                "rr-subaward-budget-10yr-30",
            )
        )
        for profile in profiles:
            self.assertEqual(profile["attachment"]["fields"], attachment)

    def test_source_profiles_compose_the_shared_mapping_instead_of_copying_it(self) -> None:
        expected_refs = {
            "performance-site": [
                "../mappings/attached-file-data-1.0.json#/fields",
                "../mappings/performance-site-location-4.0.json#/fields",
                "../mappings/performance-site-location-4.0.json#/fields",
            ],
            "phs398-modular-budget": [
                "../mappings/attached-file-data-1.0.json#/fields",
                "../mappings/phs398-modular-budget-1.2.json#/fields",
            ],
            "rr-other-project-information": [
                "../mappings/attached-file-data-1.0.json#/fields",
                "../mappings/rr-other-project-information-1.4.json#/fields",
            ],
        }
        for source in sorted((SOURCE / "profiles").glob("*.json")):
            profile = _json(source)
            refs: list[str] = []

            def walk(value: Any) -> None:
                if isinstance(value, dict):
                    if "$ref" in value:
                        refs.append(value["$ref"])
                    for child in value.values():
                        walk(child)
                elif isinstance(value, list):
                    for child in value:
                        walk(child)

            walk(profile)
            default_refs = [
                "../mappings/attached-file-data-1.0.json#/fields",
                (
                    "../mappings/rr-sf424-5.0.json#/fields"
                    if profile["formId"] == "rr-sf424"
                    else "../mappings/research-budget-3.0.json#/fields"
                ),
            ]
            self.assertEqual(
                sorted(refs), sorted(expected_refs.get(profile["formId"], default_refs))
            )

    def test_rr_sf424_keeps_wire_only_grouping_out_of_the_question_model(self) -> None:
        profile = _json(DIST_FORMS / "rr-sf424/targets/grants-gov-xml.json")
        district = profile["mapping"]["fields"]["congressionalDistrict"]

        self.assertEqual(district["kind"], "group")
        self.assertEqual(district["namespace"], "default")
        self.assertEqual(
            district["fields"]["applicantCongressionalDistrict"],
            {
                "element": "ApplicantCongressionalDistrict",
                "kind": "value",
                "namespace": "default",
                "source": "/applicantCongressionalDistrict",
            },
        )
        self.assertEqual(profile["evidence"]["status"], "source-bound-unreviewed")

    def test_complex_wire_shapes_remain_declarative(self) -> None:
        other = _json(DIST_FORMS / "rr-other-project-information/targets/grants-gov-xml.json")
        human = other["mapping"]["fields"]["humanSubjects"]
        self.assertTrue(human["flatten"])
        self.assertEqual(
            human["fields"]["humanSubjectsSupplement"]["kind"],
            "group",
        )
        self.assertEqual(
            other["mapping"]["fields"]["otherAttachments"]["items"]["node"],
            {"element": "OtherAttachment", "kind": "attachment"},
        )

        modular = _json(DIST_FORMS / "phs398-modular-budget/targets/grants-gov-xml.json")
        self.assertEqual(
            modular["mapping"]["fields"]["budgetJustifications"]["kind"],
            "group",
        )


if __name__ == "__main__":
    unittest.main()
