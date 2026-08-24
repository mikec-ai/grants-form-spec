from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "dist" / "forms"
QUESTIONS = ROOT / "dist" / "question-bank" / "budget" / "research"
AUDIT = ROOT / "analysis" / "rr-budget-source-content-audit.v1.json"
EVIDENCE = ROOT / "dist" / "forms" / "rr-budget" / "evidence.json"
TEN_YEAR_EVIDENCE = ROOT / "dist" / "forms" / "rr-budget-10yr" / "evidence.json"
TEN_YEAR_RUNTIME = ROOT / "dist" / "forms" / "rr-budget-10yr" / "operational-behavior.json"

DAT_SHA256 = "c85158ce7ddcc756d6e8a55a050e00b4a95cdfc8d9a2d91b7bd94c7f8bdb1035"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def collect_rules(node: object, rule_name: str) -> list[dict]:
    matches: list[dict] = []
    if isinstance(node, dict):
        validation = node.get("gg_validation")
        if isinstance(validation, dict) and validation.get("rule") == rule_name:
            matches.append(validation)
        for value in node.values():
            matches.extend(collect_rules(value, rule_name))
    elif isinstance(node, list):
        for value in node:
            matches.extend(collect_rules(value, rule_name))
    return matches


def collect_property_schemas(node: object, property_name: str) -> list[dict]:
    matches: list[dict] = []
    if isinstance(node, dict):
        properties = node.get("properties")
        if isinstance(properties, dict):
            candidate = properties.get(property_name)
            if isinstance(candidate, dict):
                matches.append(candidate)
        for value in node.values():
            matches.extend(collect_property_schemas(value, property_name))
    elif isinstance(node, list):
        for value in node:
            matches.extend(collect_property_schemas(value, property_name))
    return matches


class ResearchBudgetSourceContentTests(unittest.TestCase):
    def test_first_period_only_budget_type_and_justification_are_single_root_fields(self) -> None:
        form_schema = load(FORMS / "rr-budget" / "schema.json")
        self.assertIn("budgetType", form_schema["required"])
        self.assertIn("budgetJustificationAttachment", form_schema["required"])
        self.assertIn("budgetType", form_schema["properties"])
        self.assertIn("budgetJustificationAttachment", form_schema["properties"])

        period_schema = load(QUESTIONS / "period" / "schema.json")
        self.assertNotIn("budgetType", period_schema["properties"])
        self.assertNotIn("budgetJustificationAttachment", period_schema["properties"])

    def test_cross_form_prefill_evidence_preserves_exact_sources_and_boundaries(self) -> None:
        records = load(EVIDENCE)["operationalBehaviorEvidence"]
        self.assertEqual(len(records), 3)
        by_path = {record["canonicalPath"]: record for record in records}
        self.assertEqual(
            by_path["/samUei"]["valueSource"],
            {
                "kind": "canonical",
                "blockId": "rr-sf424",
                "path": "/applicantInfo/organizationInfo/samUei",
            },
        )
        self.assertEqual(by_path["/samUei"]["editability"], "editable")
        self.assertEqual(
            by_path["/organizationName"]["valueSource"],
            {
                "kind": "canonical",
                "blockId": "rr-sf424",
                "path": "/applicantInfo/organizationInfo/organizationName",
            },
        )
        self.assertEqual(by_path["/organizationName"]["editability"], "unspecified")
        self.assertEqual(
            by_path["/budgetYear/[]/budgetPeriodStartDate"],
            {
                "canonicalPath": "/budgetYear/[]/budgetPeriodStartDate",
                "operationKind": "prefill",
                "valueSource": {
                    "kind": "canonical",
                    "blockId": "rr-sf424",
                    "path": "/proposedProjectPeriod/proposedStartDate",
                },
                "targetSelection": {"arrayPath": "/budgetYear", "index": 0},
                "editability": "unspecified",
                "authority": "official_source",
                "executionStatus": "compiled",
                "executionPolicy": {
                    "trigger": "source-response-updated",
                    "writePolicy": "until-target-user-modified",
                    "missingSourcePolicy": "skip",
                },
                "sourceId": "grantsgov-rr-budget-dat-3.0-f770",
                "sourcePath": "0-10",
                "sourceRecord": (
                    "Prefill the Start Date for the first budget year from "
                    "ProposedStartDate on the R&R SF424. Start Date cannot be after End Date."
                ),
            },
        )

    def test_ten_year_profile_inherits_exact_compiled_prefill_contract(self) -> None:
        evidence = load(TEN_YEAR_EVIDENCE)
        records = evidence["operationalBehaviorEvidence"]
        self.assertEqual(len(records), 3)
        self.assertEqual(
            {record["sourcePath"] for record in records}, {"0-06", "0-07", "0-10"}
        )
        self.assertEqual({record["inheritedFrom"] for record in records}, {"rr-budget"})
        self.assertEqual(
            {record["sourceId"] for record in records},
            {"grantsgov-rr-budget-dat-3.0-f770"},
        )
        self.assertIn(
            "grantsgov-rr-budget-dat-3.0-f770",
            {source["id"] for source in evidence["sources"]},
        )

        runtime = load(TEN_YEAR_RUNTIME)
        self.assertEqual(runtime["contract"], "grants-form-operational-behavior/v1")
        self.assertEqual(runtime["formId"], "rr-budget-10yr")
        self.assertEqual(len(runtime["behaviors"]), 3)
        self.assertEqual(
            {behavior["executionPolicy"]["writePolicy"] for behavior in runtime["behaviors"]},
            {"until-target-user-modified"},
        )
        self.assertEqual({record["executionStatus"] for record in records}, {"compiled"})
        self.assertEqual(
            {tuple(record["executionPolicy"].items()) for record in records},
            {
                (
                    ("trigger", "source-response-updated"),
                    ("writePolicy", "until-target-user-modified"),
                    ("missingSourcePolicy", "skip"),
                )
            },
        )

    def test_fixed_personnel_roles_are_source_exact_defaults_and_read_only(self) -> None:
        schema = load(QUESTIONS / "other-personnel" / "schema.json")
        definitions = schema["$defs"]
        expected = {
            "ResearchBudgetBudgetYearOtherPersonnelPostDocAssociates": "Post Doctoral Associates",
            "ResearchBudgetBudgetYearOtherPersonnelGraduateStudents": "Graduate Students",
            "ResearchBudgetBudgetYearOtherPersonnelUndergraduateStudents": "Undergraduate Students",
            "ResearchBudgetBudgetYearOtherPersonnelSecretarialClerical": "Secretarial/Clerical",
        }

        for model_name, value in expected.items():
            with self.subTest(model_name=model_name):
                self.assertEqual(
                    definitions[model_name]["properties"]["projectRole"],
                    {
                        "type": "string",
                        "const": value,
                        "default": value,
                        "title": f"Project Role {value}",
                        "readOnly": True,
                    },
                )

        self.assertEqual(
            definitions["ResearchBudgetBudgetYearOtherPersonnelOther"]["properties"]["projectRole"],
            {
                "type": "string",
                "minLength": 1,
                "maxLength": 100,
                "title": "Additional Project Role Description",
            },
        )

        for form_id in (
            "rr-budget",
            "rr-budget-10yr",
            "rr-subaward-budget",
            "rr-subaward-budget-30",
            "rr-subaward-budget-10yr-30",
        ):
            with self.subTest(form_id=form_id):
                project_roles = collect_property_schemas(
                    load(FORMS / form_id / "schema.json"), "projectRole"
                )
                self.assertEqual(
                    [item for item in project_roles if item.get("readOnly") is True],
                    [{"readOnly": True}] * 4,
                )

    def test_attachment_pair_labels_and_help_are_exact_f770_records(self) -> None:
        equipment = load(QUESTIONS / "equipment" / "schema.json")["properties"]
        key_personnel = load(QUESTIONS / "key-personnel" / "schema.json")["properties"]

        self.assertEqual(
            equipment["additionalEquipmentsAttachment"],
            {
                "$ref": "../../../../question-bank/budget/research/additional-equipment/schema.json",
                "title": "Additional Equipment:",
                "description": (
                    "One possible attachment per budget period. Required if "
                    "TotalFundForAttachedEquipment is entered and greater than zero."
                ),
            },
        )
        self.assertEqual(
            {
                "title": equipment["totalFundForAttachedEquipment"]["title"],
                "description": equipment["totalFundForAttachedEquipment"]["description"],
            },
            {
                "title": "Total funds requested for all equipment listed in the attached file",
                "description": (
                    "Required and must be greater than zero if an "
                    "AdditionalEquipmentsAttachment exists."
                ),
            },
        )
        self.assertEqual(
            {
                "title": key_personnel["attachedKeyPersons"]["title"],
                "description": key_personnel["attachedKeyPersons"]["description"],
            },
            {
                "title": "Additional Senior Key Persons:",
                "description": (
                    "One possible attachment per budget period. Required if "
                    "TotalFundForAttachedKeyPersons is entered and greater than zero."
                ),
            },
        )
        self.assertEqual(
            {
                "title": key_personnel["totalFundForAttachedKeyPersons"]["title"],
                "description": key_personnel["totalFundForAttachedKeyPersons"]["description"],
            },
            {
                "title": "Total Funds requested for all Senior Key Persons in the attached file",
                "description": (
                    "Required and must be greater than zero if an "
                    "AttachedKeyPersons attachment exists."
                ),
            },
        )

    def test_end_date_source_rule_compiles_once_in_every_family_profile(self) -> None:
        period = load(QUESTIONS / "period" / "schema.json")["properties"]
        self.assertEqual(
            period["budgetPeriodEndDate"]["description"],
            "End Date cannot be before Start Date.",
        )

        for form_id in (
            "rr-budget",
            "rr-budget-10yr",
            "rr-subaward-budget",
            "rr-subaward-budget-30",
            "rr-subaward-budget-10yr-30",
        ):
            with self.subTest(form_id=form_id):
                rules = load(FORMS / form_id / "sgg" / "rule-schema.json")
                self.assertEqual(
                    collect_rules(rules, "date_not_before"),
                    [
                        {
                            "rule": "date_not_before",
                            "fields": ["@THIS.budgetPeriodStartDate"],
                        }
                    ],
                )

    def test_audit_keeps_source_pin_and_unresolved_boundaries_explicit(self) -> None:
        audit = load(AUDIT)
        self.assertEqual(audit["source"]["sha256"], DAT_SHA256)
        self.assertEqual(audit["source"]["nativeVersion"], "3.0")
        self.assertEqual(len(audit["implementedCorrections"]), 9)
        self.assertEqual(
            {item["sourcePath"] for item in audit["implementedCorrections"]},
            {
                "0-11",
                "A-2-1",
                "A-3-1",
                "B-1-2",
                "B-2-2",
                "B-3-2",
                "B-4-2",
                "C-2-0",
                "C-2-1",
            },
        )
        self.assertEqual(audit["semanticReview"]["status"], "unreviewed")
        self.assertEqual(
            audit["scope"]["dimensionStatus"],
            {
                "applicant-visible-labels": "partial",
                "help-and-instructions": "partial",
                "requiredness": "partial",
                "section-and-group-semantics": "bounded",
                "attachment-positive-total-pairs": "complete-for-two-source-pairs",
                "fixed-values-and-response-ownership": "complete-for-four-source-records",
                "lifecycle-and-prefill": "bounded",
            },
        )
        unresolved_dimensions = {
            item["dimension"] for item in audit["unresolved"] if "dimension" in item
        }
        self.assertEqual(
            unresolved_dimensions,
            {"applicant-visible-labels", "requiredness"},
        )
        self.assertNotIn(
            "All 64 unique non-empty DAT label strings",
            json.dumps(audit),
        )
        self.assertEqual(
            {path for item in audit["unresolved"] for path in item["sourcePaths"]},
            {"0-06", "0-07", "0-10"},
        )
        self.assertEqual(
            {item["sourcePath"] for item in audit["sourceBoundOperationalEvidence"]},
            {"0-06", "0-07", "0-10"},
        )


if __name__ == "__main__":
    unittest.main()
