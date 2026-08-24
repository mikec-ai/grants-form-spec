from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


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


class NifaSupplementalTests(unittest.TestCase):
    def test_form_is_eight_source_sections_with_portable_conditions(self) -> None:
        form = ROOT / "dist/forms/nifa-supplemental"
        schema = load(form / "schema.json")
        ui = load(form / "sgg/ui-schema.json")
        manifest = load(form / "manifest.json")

        self.assertEqual(
            manifest["form"],
            {
                "id": "nifa-supplemental",
                "legacyFormId": 483,
                "formName": "NIFA Supplemental Information",
                "shortFormName": "NIFA_Supplemental_Info_1_2",
                "formVersion": "1.2",
                "agencyCode": "GRANTS_GOV",
                "ombNumber": "0524-0039",
            },
        )
        self.assertEqual(len(ui), 8)
        self.assertEqual(
            schema["required"],
            ["fundingOpportunity", "program", "applicantType", "asapRecipientInformation", "keywords"],
        )
        self.assertEqual(len(schema["allOf"]), 2)
        predicates = {
            item["if"]["properties"]["applicantType"]["properties"]["applicantTypeCode"]["const"]
            for item in schema["allOf"]
        }
        self.assertEqual(
            predicates,
            {
                "H: Public/state Controlled Institution of Higher Education",
                "X: Other (specify)",
            },
        )

        fields = [item for item in objects(ui) if item.get("type") == "field"]
        additional = next(
            item
            for item in fields
            if item["definition"].endswith(
                "/additionalApplicantType/properties/additionalApplicantType"
            )
        )
        self.assertEqual(additional["conditional"]["when"]["op"], "in")
        self.assertEqual(
            additional["conditional"]["when"]["ref"]["pointer"],
            "/applicantType/applicantTypeCode",
        )
        self.assertEqual(
            len([item for item in fields if item.get("widget") == "Checkbox"]),
            12,
        )

    def test_question_lineage_has_no_form_local_escape_hatch(self) -> None:
        index = load(ROOT / "dist/forms/nifa-supplemental/index.json")
        occurrences = [row for row in index["fieldOccurrences"] if row["leaf"]]
        self.assertEqual(len(occurrences), 22)
        self.assertTrue(all(row.get("blockIds") for row in occurrences))
        applicant_type = next(row for row in occurrences if row["path"].endswith("/applicantTypeCode"))
        self.assertEqual(applicant_type["blockIds"], ["primary-org/applicant-type-code"])

    def test_provenance_and_semantics_remain_explicitly_unreviewed(self) -> None:
        evidence = load(ROOT / "dist/forms/nifa-supplemental/evidence.json")
        sources = {source["type"]: source for source in evidence["sources"]}
        self.assertEqual(
            sources["xsd"]["sha256"],
            "9fd2d43797ec5fe17a9c29f073295e1c459b13d39346b3422de036d51c1d69e2",
        )
        self.assertEqual(
            sources["dat"]["sha256"],
            "354c743d2de7187d946440065bf0df02c45b83028163e0fb020667cd367fd4d3",
        )
        self.assertEqual(
            sources["pdf"]["sha256"],
            "01aef063990fad9eda40beb8b2dc4680afba014e6e3e6a829cf72c28be0db881",
        )
        self.assertEqual(evidence["extraction"]["revision"], "4312f6504b060e2b9ffdbd2307fc41130c3123a0")
        self.assertEqual(evidence["semanticReview"]["status"], "proposed")
        self.assertEqual(len(evidence["semanticReview"]["mappings"]), 22)
        self.assertEqual(
            sum(row["status"] == "accepted" for row in evidence["semanticReview"]["mappings"]),
            0,
        )
        self.assertEqual(len(evidence["behaviorEvidence"]), 2)

    def test_emitter_measurement_is_pinned_without_claiming_review(self) -> None:
        packet_path = ROOT / "build/promotion/NIFASupplemental.promotion.json"
        if not packet_path.exists():
            self.skipTest("generated crosswalk promotion packet is unavailable")
        packet = load(packet_path)
        self.assertEqual(
            packet["metrics"],
            {
                "sourceRecords": 32,
                "sourceBehaviors": 31,
                "applicantBehaviorRecords": 22,
                "presentationBehaviorRecords": 8,
                "runtimeRules": 4,
                "semanticProposals": 32,
                "acceptedSemanticMappings": 0,
                "openReviewGates": 39,
            },
        )
        self.assertEqual(
            packet["extraction"]["sourceSetSha256"],
            "138619ea82f8e994f30be78bf8be646abc459442c24cbbb1cbfab25a69e8733f",
        )


if __name__ == "__main__":
    unittest.main()
