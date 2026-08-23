from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from conformance.grants_gov_xml import (
    ExactXsdFixture,
    PinnedXsdFile,
    render_profile_xml,
    validate_exact_xsd,
)


ROOT = Path(__file__).parents[1]
FORM_NS = "http://apply.grants.gov/forms/SF424C_2_0-V2.0"
XSD_FIXTURE = ROOT / "tests/fixtures/grants-gov-xsd/sf424c-2.0/SF424C_2_0-V2.0.xsd"
DEPENDENCIES = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
NORMALIZED_XSD_SHA256 = "9bffc07cef30336d4a6b320d6569bc5a93c4e48b4889c0de7cf7e46cab090af1"
OFFICIAL_XSD_SHA256 = "a3ec5d6bae8173fce080709a8071787293dbe6271415d905d230c584c200982a"
DEPENDENCY_NAMES = ["Global-V1.0.xsd", "GlobalLibrary-V2.0.xsd", "UniversalCodes-V2.0.xsd"]
PROFILE = json.loads(
    (ROOT / "dist/forms/sf424c/targets/grants-gov-xml.json").read_text()
)
XSD_SET = ExactXsdFixture(
    entrypoint="SF424C_2_0-V2.0.xsd",
    files=(
        PinnedXsdFile("SF424C_2_0-V2.0.xsd", XSD_FIXTURE, NORMALIZED_XSD_SHA256),
        *(
            PinnedXsdFile(
                name,
                DEPENDENCIES / name,
                {
                    "Global-V1.0.xsd": "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb",
                    "GlobalLibrary-V2.0.xsd": "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8",
                    "UniversalCodes-V2.0.xsd": "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a",
                }[name],
            )
            for name in DEPENDENCY_NAMES
        ),
    ),
    official_sha256=OFFICIAL_XSD_SHA256,
)


def full_response() -> dict[str, Any]:
    rows = {
        "administrativeAndLegalExpenses": {"totalCost": "100.00", "nonAllowableCost": "10.00", "totalAllowableCost": "90.00"},
        "landStructuresRightsOfWay": {"totalCost": "200.00", "nonAllowableCost": "20.00", "totalAllowableCost": "180.00"},
        "relocationExpenses": {"totalCost": "300.00", "nonAllowableCost": "30.00", "totalAllowableCost": "270.00"},
        "architecturalEngineeringFees": {"totalCost": "400.00", "nonAllowableCost": "40.00", "totalAllowableCost": "360.00"},
        "otherArchitecturalEngineeringFees": {"totalCost": "500.00", "nonAllowableCost": "50.00", "totalAllowableCost": "450.00"},
        "projectInspectionFees": {"totalCost": "600.00", "nonAllowableCost": "60.00", "totalAllowableCost": "540.00"},
        "siteWork": {"totalCost": "700.00", "nonAllowableCost": "70.00", "totalAllowableCost": "630.00"},
        "demolitionAndRemoval": {"totalCost": "800.00", "nonAllowableCost": "80.00", "totalAllowableCost": "720.00"},
        "construction": {"totalCost": "900.00", "nonAllowableCost": "90.00", "totalAllowableCost": "810.00"},
        "equipment": {"totalCost": "1000.00", "nonAllowableCost": "100.00", "totalAllowableCost": "900.00"},
        "miscellaneous": {"totalCost": "1100.00", "nonAllowableCost": "110.00", "totalAllowableCost": "990.00"},
        "subtotalBeforeContingencies": {"totalCost": "6600.00", "nonAllowableCost": "660.00", "totalAllowableCost": "5940.00"},
        "contingencies": {"totalCost": "100.00", "nonAllowableCost": "0.00", "totalAllowableCost": "100.00"},
        "subtotalAfterContingencies": {"totalCost": "6700.00", "nonAllowableCost": "660.00", "totalAllowableCost": "6040.00"},
        "programIncome": {"totalCost": "40.00", "nonAllowableCost": "0.00", "totalAllowableCost": "40.00"},
        "totalProjectCosts": {"totalCost": "6660.00", "nonAllowableCost": "660.00", "totalAllowableCost": "6000.00"},
    }
    return {
        "budgetInformation": rows,
        "federalFunding": {
            "totalProjectCosts": "6000.00",
            "federalPercentageShare": 80,
            "federalFundingShare": "4800.00",
        },
    }


class SF424CXmlTests(unittest.TestCase):
    def assert_partial_budget_valid(
        self, response: dict[str, Any], expected_optional_element: str | None
    ) -> None:
        xml = render_profile_xml(PROFILE, response)
        validation = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(validation.returncode, 0, validation.stderr)
        root = ET.fromstring(xml)
        project_costs = root.find(f"{{{FORM_NS}}}ProjectCosts")
        self.assertIsNotNone(project_costs)
        assert project_costs is not None
        names = [child.tag.removeprefix(f"{{{FORM_NS}}}") for child in project_costs]
        self.assertIn("CostSubtotalBeforeContingencies", names)
        self.assertIn("CostSubtotalAfterContingencies", names)
        if expected_optional_element is not None:
            self.assertIn(expected_optional_element, names)

    def test_full_response_validates_against_pinned_official_xsd(self) -> None:
        xml = render_profile_xml(PROFILE, full_response())
        validation = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(validation.returncode, 0, validation.stderr)

        root = ET.fromstring(xml)
        self.assertEqual(root.get(f"{{{FORM_NS}}}programType"), "Construction")
        self.assertEqual(root.get(f"{{{FORM_NS}}}FormVersion"), "2.0")
        project_costs = root.find(f"{{{FORM_NS}}}ProjectCosts")
        self.assertIsNotNone(project_costs)
        assert project_costs is not None
        self.assertEqual(
            [child.tag.removeprefix(f"{{{FORM_NS}}}") for child in project_costs],
            [
                "AdministrationCost", "LandCost", "RelocationCost", "ArchitecturalCost",
                "OtherArchitecturalCost", "InspectionFeesCost", "SiteWorkCost", "DemolitionCost",
                "ConstructionCost", "EquipmentCost", "Miscellaneous", "CostSubtotalBeforeContingencies",
                "Contingencies", "CostSubtotalAfterContingencies", "ProgramIncome", "TotalProjectCosts",
            ],
        )
        self.assertEqual(root.findtext(f"{{{FORM_NS}}}FederalFundingShareValue"), "4800.00")

    def test_flattened_federal_fields_emit_without_ui_only_eligible_cost_copy(self) -> None:
        xml = render_profile_xml(
            PROFILE,
            {"federalFunding": {"totalProjectCosts": "6000.00", "federalPercentageShare": 75, "federalFundingShare": "4500.00"}}
        )
        validation = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(validation.returncode, 0, validation.stderr)
        root = ET.fromstring(xml)
        self.assertIsNone(root.find(f"{{{FORM_NS}}}ProjectCosts"))
        self.assertEqual(root.findtext(f"{{{FORM_NS}}}FederalFundingPercentageShareValue"), "75")
        self.assertEqual(root.findtext(f"{{{FORM_NS}}}FederalFundingShareValue"), "4500.00")
        self.assertNotIn(b"totalProjectCosts", xml)

    def test_contingencies_only_budget_emits_required_subtotal_containers(self) -> None:
        self.assert_partial_budget_valid(
            {"budgetInformation": {"contingencies": {"totalCost": "25.00"}}},
            "Contingencies",
        )

    def test_program_income_only_budget_emits_required_subtotal_containers(self) -> None:
        self.assert_partial_budget_valid(
            {"budgetInformation": {"programIncome": {"totalCost": "10.00"}}},
            "ProgramIncome",
        )

    def test_empty_budget_object_emits_required_subtotal_containers(self) -> None:
        self.assert_partial_budget_valid({"budgetInformation": {}}, None)


if __name__ == "__main__":
    unittest.main()
