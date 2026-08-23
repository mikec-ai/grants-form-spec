from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def occurrence(form_id: str, path: str) -> dict:
    index = load(ROOT / f"dist/forms/{form_id}/index.json")
    return next(row for row in index["fieldOccurrences"] if row["path"] == path)


class ResidualReferenceQuestionTests(unittest.TestCase):
    def test_eight_fields_have_path_qualified_canonical_lineage(self) -> None:
        expected = {
            ("key-contacts", "/keyContacts/[]/projectRole"): "poc/project-role",
            ("sf424-short", "/applicantWebAddress"): "primary-org/website",
            ("sf424-short", "/projectDescription"): "project/description",
            ("sf424a", "/activityLineItems/[]/activityTitle"): "budget/activity-title",
            (
                "sf424a",
                "/activityLineItems/[]/assistanceListingNumber",
            ): "budget/activity-assistance-listing-number",
            (
                "sf424a",
                "/directChargesExplanation",
            ): "budget/direct-charges-explanation",
            (
                "sf424a",
                "/indirectChargesExplanation",
            ): "budget/indirect-charges-explanation",
            ("sf424a", "/remarks"): "budget/remarks",
        }

        for (form_id, path), block_id in expected.items():
            with self.subTest(form=form_id, path=path):
                row = occurrence(form_id, path)
                self.assertTrue(row["leaf"])
                self.assertEqual(row["blockIds"], [block_id])

    def test_key_contact_role_is_free_text_not_research_role_vocabulary(self) -> None:
        role = load(ROOT / "dist/question-bank/poc/project-role/schema.json")
        index = load(ROOT / "dist/question-bank/poc/project-role/index.json")

        self.assertEqual(role["type"], "string")
        self.assertEqual((role["minLength"], role["maxLength"]), (1, 45))
        self.assertNotIn("enum", role)
        self.assertEqual(index["entity"], "poc")
        self.assertEqual(index["tags"], ["person", "role"])
        self.assertEqual(index["responseRole"], "applicantInput")

        research = load(ROOT / "dist/question-bank/research-person/details/schema.json")
        self.assertIn("PD/PI", research["$defs"]["ResearchProjectRole"]["enum"])

    def test_sf424_short_preserves_source_shapes_and_form_use_limit(self) -> None:
        schema = load(ROOT / "dist/forms/sf424-short/schema.json")
        website = schema["properties"]["applicantWebAddress"]
        description = schema["properties"]["projectDescription"]

        self.assertEqual(
            website["$ref"], "../../question-bank/primary-org/website/schema.json"
        )
        self.assertEqual(website["maxLength"], 250)
        website_question = load(
            ROOT / "dist/question-bank/primary-org/website/schema.json"
        )
        self.assertEqual(website_question["format"], "uri-reference")
        self.assertEqual(website_question["minLength"], 1)

        self.assertEqual(
            description["$ref"], "../../question-bank/project/description/schema.json"
        )
        description_question = load(
            ROOT / "dist/question-bank/project/description/schema.json"
        )
        self.assertEqual(
            (description_question["minLength"], description_question["maxLength"]),
            (1, 1000),
        )

    def test_sf424a_preserves_repeating_row_identity_and_xsd_constraints(self) -> None:
        schema = load(ROOT / "dist/forms/sf424a/schema.json")
        rows = schema["properties"]["activityLineItems"]
        row = schema["$defs"]["ActivityLineItem"]

        self.assertEqual((rows["minItems"], rows["maxItems"]), (1, 4))
        self.assertIn("activityTitle", row["required"])
        self.assertEqual(
            row["properties"]["activityTitle"]["$ref"],
            "../../question-bank/budget/activity-title/schema.json",
        )
        self.assertEqual(
            row["properties"]["assistanceListingNumber"]["$ref"],
            "../../question-bank/budget/activity-assistance-listing-number/schema.json",
        )

        assistance_listing = load(
            ROOT
            / "dist/question-bank/budget/activity-assistance-listing-number/schema.json"
        )
        assistance_listing_index = load(
            ROOT
            / "dist/question-bank/budget/activity-assistance-listing-number/index.json"
        )
        self.assertEqual(
            (assistance_listing["minLength"], assistance_listing["maxLength"]),
            (1, 15),
        )
        self.assertNotIn("responseRole", assistance_listing_index)

        constraints = {
            "activity-title": (1, 120),
            "direct-charges-explanation": (1, 50),
            "indirect-charges-explanation": (1, 50),
            "remarks": (1, 250),
        }
        for question, expected in constraints.items():
            with self.subTest(question=question):
                question_schema = load(
                    ROOT / f"dist/question-bank/budget/{question}/schema.json"
                )
                self.assertEqual(
                    (question_schema["minLength"], question_schema["maxLength"]),
                    expected,
                )

    def test_source_mappings_remain_proposals_and_cannot_enter_published_metrics(self) -> None:
        expected_counts = {"key-contacts": 1, "sf424-short": 2, "sf424a": 5}
        for form_id, count in expected_counts.items():
            with self.subTest(form=form_id):
                evidence = load(ROOT / f"dist/forms/{form_id}/evidence.json")
                review = evidence["semanticReview"]
                self.assertEqual(review["status"], "proposed")
                self.assertEqual(len(review["mappings"]), count)
                self.assertTrue(
                    all(mapping["status"] == "proposed" for mapping in review["mappings"])
                )
                self.assertTrue(
                    all("reviewedBy" not in mapping for mapping in review["mappings"])
                )


if __name__ == "__main__":
    unittest.main()
