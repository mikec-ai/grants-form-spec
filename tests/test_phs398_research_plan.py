from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FORM = ROOT / "dist/forms/phs398-research-plan"
QUESTION_ROOT = ROOT / "dist/question-bank/research-plan"


def load(path: Path) -> object:
    return json.loads(path.read_text())


class PHS398ResearchPlanTests(unittest.TestCase):
    def test_form_identity_requiredness_and_applicant_appendix_limit(self) -> None:
        manifest = load(FORM / "manifest.json")
        schema = load(FORM / "schema.json")

        self.assertEqual(manifest["form"], {
            "id": "phs398-research-plan",
            "legacyFormId": 797,
            "formName": "PHS 398 Research Plan",
            "shortFormName": "PHS398_ResearchPlan_5_0",
            "formVersion": "5.0",
            "agencyCode": "GRANTS_GOV",
            "ombNumber": "0925-0001",
        })
        self.assertEqual(schema["required"], ["researchStrategy"])
        self.assertEqual(len(schema["properties"]), 13)
        self.assertEqual(schema["properties"]["appendix"]["maxItems"], 10)
        self.assertEqual(
            schema["properties"]["appendix"]["items"],
            {"$ref": "../../question-bank/research-plan/appendix-document/schema.json"},
        )

    def test_thirteen_semantic_roles_reuse_one_attachment_capture_mechanism(self) -> None:
        schema = load(FORM / "schema.json")
        index = load(FORM / "index.json")
        role_refs = {
            prop.get("$ref") or prop["items"]["$ref"]
            for prop in schema["properties"].values()
        }
        self.assertEqual(len(role_refs), 13)

        semantic_blocks = set()
        for reference in role_refs:
            block = reference.split("/research-plan/", 1)[1].split("/schema.json", 1)[0]
            question = load(QUESTION_ROOT / block / "index.json")
            self.assertEqual(question["classification"], "semanticQuestion")
            self.assertEqual(question["composes"], ["generics/attachment"])
            self.assertEqual(question["responseRole"], "applicantInput")
            semantic_blocks.add(question["id"])
        self.assertEqual(len(semantic_blocks), 13)

        leaf_occurrences = [row for row in index["fieldOccurrences"] if row["leaf"]]
        self.assertEqual(len(leaf_occurrences), 13)
        self.assertEqual(
            {row["responseRole"] for row in leaf_occurrences}, {"applicantInput"}
        )
        self.assertTrue(all(
            "generics/attachment" in row["blockIds"]
            and len(row["blockIds"]) == 2
            for row in leaf_occurrences
        ))

    def test_ui_order_and_attachment_rules_are_generic(self) -> None:
        ui = load(FORM / "sgg/ui-schema.json")
        rules = load(FORM / "sgg/rule-schema.json")

        self.assertEqual(
            [section["name"] for section in ui],
            ["introduction", "researchPlan", "otherResearchPlan", "appendix"],
        )
        fields = [field for section in ui for field in section["children"]]
        self.assertEqual(len(fields), 13)
        self.assertEqual(
            [field["definition"] for field in fields],
            [
                "/properties/introduction",
                "/properties/specificAims",
                "/properties/researchStrategy",
                "/properties/progressReportPublicationList",
                "/properties/vertebrateAnimals",
                "/properties/selectAgentResearch",
                "/properties/multiplePdPiLeadershipPlan",
                "/properties/consortiumContractualArrangements",
                "/properties/lettersOfSupport",
                "/properties/resourceSharingPlans",
                "/properties/otherPlans",
                "/properties/keyResourceAuthentication",
                "/properties/appendix",
            ],
        )
        self.assertEqual(fields[-1]["widget"], "AttachmentArray")
        self.assertTrue(all(
            rule == {"gg_validation": {"rule": "attachment"}}
            for rule in rules.values()
        ))

    def test_sources_are_exact_and_semantic_mappings_remain_proposed(self) -> None:
        evidence = load(FORM / "evidence.json")
        sources = {source["id"]: source for source in evidence["sources"]}

        self.assertEqual(
            sources["phs398-research-plan-xsd-v5-0"]["sha256"],
            "6e7171465d1f44a16eb822f8921423ceede4fa486cb0819bc5dd327121b4bb56",
        )
        self.assertEqual(
            sources["phs398-research-plan-dat-f797"]["sha256"],
            "61af459ba15e7a4ef5ddc4856a598561ce91bccb19f34084e977edb4eb4e7c88",
        )
        self.assertEqual(
            sources["phs398-research-plan-readonly-pdf-v5-0"]["sha256"],
            "1ae85b51a0502315b0370e596660c9c9518458152af3c15f1ef1c1d35638a12b",
        )
        self.assertEqual(
            sources["phs398-research-plan-xfa-pdf-v5-0"]["sha256"],
            "587caf4945c63fd5070d28ae79d924d5a24c647231f8fdb32e17040b794b93db",
        )
        self.assertEqual(
            sources["universal-codes-xsd-v2-0"]["sha256"],
            "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
        )
        capture = ROOT / "research/phs398-research-plan/nih-forms-i-g400-instructions.json"
        self.assertEqual(
            hashlib.sha256(capture.read_bytes()).hexdigest(),
            sources["nih-forms-i-research-plan-instructions-capture"]["sha256"],
        )
        self.assertEqual(evidence["semanticReview"]["status"], "proposed")
        self.assertEqual(len(evidence["semanticReview"]["mappings"]), 13)
        self.assertTrue(all(
            mapping["status"] == "proposed"
            for mapping in evidence["semanticReview"]["mappings"]
        ))
        self.assertEqual(evidence["behaviorEvidence"], [])

    def test_cross_form_conditions_and_source_conflicts_stay_explicit(self) -> None:
        capture = load(
            ROOT / "research/phs398-research-plan/nih-forms-i-g400-instructions.json"
        )
        conditions = capture["applicationLevelConditions"]
        self.assertEqual(len(conditions), 3)
        self.assertEqual(
            {condition["targetPath"] for condition in conditions},
            {"introduction", "progressReportPublicationList", "vertebrateAnimals"},
        )
        self.assertTrue(all(
            condition["authority"] == "official_source"
            and condition["status"] == "source-bound-unresolved-cross-form"
            for condition in conditions
        ))
        intro = next(row for row in conditions if row["targetPath"] == "introduction")
        self.assertEqual(intro["values"], ["Resubmission", "Revision"])
        self.assertEqual(intro["effects"], ["enabled", "required"])

        conflicts = {row["id"]: row for row in capture["knownSourceConflicts"]}
        self.assertIn("zero through 100", conflicts["appendix-cardinality"]["xsd"])
        self.assertIn("up to 10", conflicts["appendix-cardinality"]["applicantInstructions"])
        self.assertIn("V4.0", conflicts["xsd-prefix-version"]["detail"])
        self.assertIn("V5.0", conflicts["xsd-prefix-version"]["disposition"])

        schema = load(FORM / "schema.json")
        ui = load(FORM / "sgg/ui-schema.json")
        self.assertNotIn("allOf", schema)
        self.assertFalse(any(
            "conditional" in field
            for section in ui
            for field in section["children"]
        ))


if __name__ == "__main__":
    unittest.main()
