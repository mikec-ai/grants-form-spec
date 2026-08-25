from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FORM = ROOT / "dist/forms/phs398-career-development-supplemental"


def load(path: Path) -> object:
    return json.loads(path.read_text())


class PHS398CareerDevelopmentSupplementalTests(unittest.TestCase):
    def test_identity_shape_and_requiredness_match_pinned_sources(self) -> None:
        manifest = load(FORM / "manifest.json")
        schema = load(FORM / "schema.json")

        self.assertEqual(manifest["form"], {
            "id": "phs398-career-development-supplemental",
            "legacyFormId": 799,
            "formName": "PHS 398 Career Development Award Supplemental Form",
            "shortFormName": "PHS398_CareerDevelopmentAwardSup_6_0",
            "formVersion": "6.0",
            "agencyCode": "GRANTS_GOV",
            "ombNumber": "0925-0001",
        })
        self.assertEqual(schema["required"], ["researchStrategy", "citizenship"])
        self.assertEqual(len(schema["properties"]), 20)
        self.assertEqual(schema["properties"]["appendix"]["maxItems"], 10)

    def test_reuse_is_visible_and_new_semantics_are_portable_questions(self) -> None:
        schema = load(FORM / "schema.json")
        shared_research_plan = {
            "introduction",
            "specificAims",
            "researchStrategy",
            "progressReportPublicationList",
            "lettersOfSupport",
            "vertebrateAnimals",
            "selectAgentResearch",
            "consortiumContractualArrangements",
            "resourceSharingPlans",
            "otherPlans",
            "keyResourceAuthentication",
            "appendix",
        }
        for name in shared_research_plan:
            prop = schema["properties"][name]
            ref = prop.get("$ref") or prop["items"]["$ref"]
            self.assertIn("/question-bank/research-plan/", ref)

        self.assertEqual(
            schema["properties"]["citizenship"]["$ref"],
            "../../question-bank/candidate/citizenship-and-residency-status/schema.json",
        )
        index = load(FORM / "index.json")
        self.assertEqual(sum(1 for row in index["fieldOccurrences"] if row["leaf"]), 22)

    def test_exact_local_conditions_compile_without_fabricating_package_state(self) -> None:
        ui = load(FORM / "sgg/ui-schema.json")
        conditional = {
            field["definition"]: field["conditional"]
            for section in ui
            for field in section["children"]
            if "conditional" in field
        }
        self.assertEqual(set(conditional), {
            "/properties/citizenship/properties/nonUsCitizenStatus",
            "/properties/citizenship/properties/permanentResidentByAward",
        })
        evidence = load(FORM / "evidence.json")
        execution = {
            row["canonicalPath"]: row["executionStatus"]
            for row in evidence["behaviorEvidence"]
        }
        self.assertEqual(execution["/introduction"], "source-bound-uncompiled")
        self.assertEqual(
            execution["citizenship.nonUsCitizenStatus"], "compiled"
        )
        self.assertEqual(evidence["semanticReview"]["status"], "proposed")
        self.assertEqual(len(evidence["semanticReview"]["mappings"]), 12)

    def test_all_document_fields_use_the_generic_attachment_runtime(self) -> None:
        rules = load(FORM / "sgg/rule-schema.json")
        self.assertEqual(len(rules), 19)
        self.assertTrue(all(
            rule == {"gg_validation": {"rule": "attachment"}}
            for rule in rules.values()
        ))


if __name__ == "__main__":
    unittest.main()
