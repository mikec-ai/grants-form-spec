from __future__ import annotations

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
    def test_budget_family_emits_five_self_contained_profiles(self) -> None:
        form_ids = {
            "rr-budget",
            "rr-budget-10yr",
            "rr-subaward-budget",
            "rr-subaward-budget-30",
            "rr-subaward-budget-10yr-30",
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
            self.assertEqual(
                sorted(refs),
                [
                    "../mappings/attached-file-data-1.0.json#/fields",
                    "../mappings/research-budget-3.0.json#/fields",
                ],
            )


if __name__ == "__main__":
    unittest.main()
