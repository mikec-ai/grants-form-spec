from __future__ import annotations

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

from scripts.promote_crosswalk import export_packet


ROOT = Path(__file__).parents[1]
CROSSWALK = ROOT.parent / "grants-question-crosswalk-mp-cover"
CROSSWALK_REVISION = "4312f6504b060e2b9ffdbd2307fc41130c3123a0"


def load(path: Path) -> object:
    return json.loads(path.read_text())


def objects(value: object):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


class PHSAssignmentRequestTests(unittest.TestCase):
    def test_promotion_packet_is_pinned_and_semantics_remain_proposed(self) -> None:
        if not (CROSSWALK / ".git").exists():
            self.skipTest("pinned crosswalk checkout is unavailable")
        packet = export_packet(CROSSWALK, "PHSAssignmentRequest", CROSSWALK_REVISION)
        self.assertEqual(
            packet["metrics"],
            {
                "sourceRecords": 14,
                "sourceBehaviors": 24,
                "applicantBehaviorRecords": 13,
                "presentationBehaviorRecords": 11,
                "runtimeRules": 13,
                "semanticProposals": 14,
                "acceptedSemanticMappings": 0,
                "openReviewGates": 26,
            },
        )
        self.assertEqual(
            packet["extraction"]["sourceSetSha256"],
            "63ef51469ecffd0b7a39bd58f827ebe88bc60e8d368ed0789e4608a862660b4b",
        )
        self.assertTrue(all(not row["publishable"] for row in packet["semanticProposals"]))

    def test_form_compiles_as_thirteen_optional_fixed_slots_using_five_blocks(self) -> None:
        root = ROOT / "dist/forms/phs-assignment-request"
        schema = load(root / "schema.json")
        ui = load(root / "sgg/ui-schema.json")
        rules = load(root / "sgg/rule-schema.json")
        manifest = load(root / "manifest.json")
        index = load(root / "index.json")

        self.assertEqual(schema.get("required", []), [])
        self.assertEqual(len(schema["properties"]), 13)
        refs = Counter(node["$ref"] for node in schema["properties"].values())
        self.assertEqual(sorted(refs.values()), [1, 1, 3, 3, 5])
        self.assertEqual(rules, None)
        occurrences = index["fieldOccurrences"]
        self.assertEqual(len(occurrences), 13)
        self.assertEqual(
            {occurrence["responseRole"] for occurrence in occurrences},
            {"applicantInput"},
        )
        self.assertEqual(
            [section["name"] for section in ui],
            ["awardingComponents", "studySections", "rationale", "expertise", "excludedReviewers"],
        )
        fields = [node for node in objects(ui) if node.get("type") == "field"]
        self.assertEqual(len(fields), 13)
        self.assertEqual(
            {node["definition"] for node in fields if node.get("widget") == "TextArea"},
            {"/properties/rationaleSuggestions", "/properties/notReview"},
        )
        self.assertEqual(
            manifest["form"],
            {
                "id": "phs-assignment-request",
                "legacyFormId": 833,
                "formName": "PHS Assignment Request Form",
                "shortFormName": "PHS_AssignmentRequestForm_4_0",
                "formVersion": "4.0",
                "agencyCode": "GRANTS_GOV",
                "ombNumber": "0925-0001",
            },
        )

    def test_question_blocks_preserve_exact_source_limits_without_invented_enums(self) -> None:
        base = ROOT / "dist/question-bank/review-routing"
        expected = {
            "suggested-awarding-component": 7,
            "suggested-study-section": 20,
            "assignment-suggestion-rationale": 1000,
            "reviewer-expertise": 40,
            "excluded-reviewer-request": 1000,
        }
        for block, maximum in expected.items():
            with self.subTest(block=block):
                schema = load(base / block / "schema.json")
                self.assertEqual(schema["type"], "string")
                self.assertEqual(schema["maxLength"], maximum)
                self.assertNotIn("enum", schema)
                self.assertNotIn("pattern", schema)

    def test_provenance_pins_xsd_dat_xfa_and_instructions(self) -> None:
        evidence = load(ROOT / "dist/forms/phs-assignment-request/evidence.json")
        sources = {source["type"]: source for source in evidence["sources"]}
        self.assertEqual(sources["xsd"]["sha256"], "7e697ee33ea6f72271c0d74fc48c61f4f81faa242a712a4c73e7898f6c4ab976")
        self.assertEqual(sources["dat"]["sha256"], "e08625bf4ebaee23a66e1ef85346c83e86726a58e36a6c5705f66fffaf867255")
        self.assertEqual(sources["pdf"]["sha256"], "0fdcbdd7bc136ae2872b76fc61a6cb719d8d02d9a1967257a7c9c2e957e4680a")
        self.assertEqual(sources["instructions"]["sha256"], "6aef68689060890e9c3cc650a040ea8b36f893527049e582b9474032368b1120")
        self.assertEqual(sources["instructions"]["nativeVersion"], "Forms I")
        instruction_capture_path = (
            ROOT / "research/phs-assignment-request/nih-forms-i-g600-instructions.json"
        )
        instruction_capture = load(instruction_capture_path)
        self.assertEqual(
            hashlib.sha256(instruction_capture_path.read_bytes()).hexdigest(),
            sources["instructions"]["sha256"],
        )
        self.assertEqual(instruction_capture["source"]["retrievedDate"], "2026-08-23")
        self.assertIn("no OCR used", instruction_capture["transformation"]["normalization"])
        self.assertEqual(
            instruction_capture["source"]["sha256"],
            "e12101cdc12d38cfc9942744e25aec93e28d0a0bee1465cbf615e7187cb64c54",
        )
        self.assertEqual(instruction_capture["knownSourceConflict"]["status"], "unresolved")
        self.assertIn("B10", instruction_capture["knownSourceConflict"]["detail"])
        self.assertIn("BP10", instruction_capture["knownSourceConflict"]["detail"])

        expected_paths = {
            "suggestedAwardingComponent1": "SuggestedAwardingComponent1",
            "suggestedAwardingComponent2": "SuggestedAwardingComponent2",
            "suggestedAwardingComponent3": "SuggestedAwardingComponent3",
            "suggestedStudySection1": "SuggestedStudySection1",
            "suggestedStudySection2": "SuggestedStudySection2",
            "suggestedStudySection3": "SuggestedStudySection3",
            "rationaleSuggestions": "RationaleSuggestions",
            "expertise1": "Expertise1",
            "expertise2": "Expertise2",
            "expertise3": "Expertise3",
            "expertise4": "Expertise4",
            "expertise5": "Expertise5",
            "notReview": "NotReview",
        }
        review = evidence["semanticReview"]
        self.assertEqual(review["status"], "proposed")
        self.assertEqual(len(review["mappings"]), 13)
        self.assertEqual(
            {
                mapping["canonicalPointer"]: mapping["sourcePath"]
                for mapping in review["mappings"]
            },
            {
                f"#/properties/{canonical}":
                f"PHS_AssignmentRequestForm_4_0.{source}"
                for canonical, source in expected_paths.items()
            },
        )
        self.assertTrue(
            all(
                mapping["sourceId"] == "phs-assignment-request-xsd-v4-0"
                and mapping["status"] == "proposed"
                and "no cross-form semantic equivalence" in mapping["note"]
                for mapping in review["mappings"]
            )
        )
        self.assertEqual(sum(mapping["status"] == "accepted" for mapping in review["mappings"]), 0)
        self.assertEqual(evidence["behaviorEvidence"], [])


if __name__ == "__main__":
    unittest.main()
