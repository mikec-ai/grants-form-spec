from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(path: Path) -> dict:
    return json.loads(path.read_text())


class SharedCardinalityTests(unittest.TestCase):
    def test_sf424_forms_reference_address_cardinality_without_copying_it(self) -> None:
        address = load(
            ROOT / "dist/question-bank/primary-org/address/schema.json"
        )

        self.assertEqual(address["required"], ["street1", "city", "country"])
        self.assertEqual(
            {
                tuple(branch["then"]["required"])
                for branch in address["allOf"]
                if "then" in branch
            },
            {("state",), ("zipCode",)},
        )

        for form_id in ("sf424", "sf424-short"):
            with self.subTest(form=form_id):
                form = load(ROOT / f"dist/forms/{form_id}/schema.json")
                applicant = form["properties"]["applicant"]

                self.assertEqual(
                    applicant["$ref"],
                    "../../question-bank/primary-org/address/schema.json",
                )
                self.assertNotIn("required", applicant)
                self.assertNotIn("allOf", applicant)

    def test_rr_personal_data_keeps_name_cardinality_in_shared_questions(self) -> None:
        for question_id in ("project-director", "co-project-director"):
            with self.subTest(question=question_id):
                question = load(
                    ROOT
                    / f"dist/question-bank/personal-data/{question_id}/schema.json"
                )
                self.assertEqual(
                    question["properties"]["name"]["required"],
                    ["firstName", "lastName"],
                )

        form = load(ROOT / "dist/forms/rr-personal-data/schema.json")
        project_director = form["properties"]["projectDirector"]
        self.assertEqual(
            project_director["$ref"],
            "../../question-bank/personal-data/project-director/schema.json",
        )
        self.assertNotIn("properties", project_director)
        self.assertNotIn("required", project_director)
        self.assertNotIn("allOf", project_director)

        co_project_directors = form["properties"]["coProjectDirectors"]
        self.assertEqual(co_project_directors["maxItems"], 4)
        repeated_item = co_project_directors["items"]
        self.assertEqual(
            repeated_item["$ref"],
            "../../question-bank/personal-data/co-project-director/schema.json",
        )
        self.assertNotIn("properties", repeated_item)
        self.assertNotIn("required", repeated_item)
        self.assertNotIn("allOf", repeated_item)


if __name__ == "__main__":
    unittest.main()
