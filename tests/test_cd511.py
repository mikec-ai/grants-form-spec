from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(path: Path) -> object:
    return json.loads(path.read_text())


class CD511Tests(unittest.TestCase):
    def test_form_is_declarative_source_bound_and_policy_projected(self) -> None:
        root = ROOT / "dist/forms/cd511"
        schema = load(root / "schema.json")
        ui = load(root / "sgg/ui-schema.json")
        rules = load(root / "sgg/rule-schema.json")
        manifest = load(root / "manifest.json")
        evidence = load(root / "evidence.json")
        policy = load(root / "policy-content.json")
        binding = load(root / "policy-binding.json")

        self.assertEqual(schema["required"], [
            "applicantName", "contactPerson", "contactPersonTitle",
        ])
        self.assertEqual(schema["allOf"], [{
            "anyOf": [
                {"required": ["awardNumber"]},
                {"required": ["projectName"]},
            ],
        }])
        self.assertEqual(schema["properties"]["awardNumber"]["maxLength"], 25)
        self.assertEqual(schema["properties"]["projectName"]["maxLength"], 60)
        self.assertEqual(
            schema["properties"]["contactPerson"]["required"],
            ["firstName", "lastName"],
        )

        self.assertEqual(
            [section["name"] for section in ui],
            ["directions1", "directions2", "directions3", "directions4",
             "award", "contactPerson", "signature"],
        )
        self.assertEqual(ui[1]["description"].splitlines()[0],
                         policy["sections"][1]["preamble"])
        self.assertTrue(ui[1]["description"].endswith(policy["sections"][1]["note"]))
        self.assertEqual(
            [child["type"] for child in ui[-1]["children"]],
            ["null", "null"],
        )
        self.assertEqual(rules["signature"]["gg_post_population"]["rule"], "signature")
        self.assertEqual(rules["submittedDate"]["gg_post_population"]["rule"], "current_date")

        self.assertEqual(binding["acceptance"]["event"], "submission")
        self.assertEqual(binding["release"]["status"], "draft")
        self.assertEqual(evidence["semanticReview"]["status"], "proposed")
        self.assertTrue(all(row["status"] == "proposed"
                            for row in evidence["semanticReview"]["mappings"]))
        self.assertEqual(
            manifest["artifacts"]["policy-binding.json"], "generated",
        )
        self.assertEqual(
            manifest["artifacts"]["targets/grants-gov-xml.json"], "generated",
        )


if __name__ == "__main__":
    unittest.main()
