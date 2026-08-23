from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


ROOT = Path(__file__).parents[1]
FORM_NS = "http://apply.grants.gov/forms/SF424C_2_0-V2.0"
XSD_FIXTURE = ROOT / "tests/fixtures/grants-gov-xsd/sf424c-2.0/SF424C_2_0-V2.0.xsd"
DEPENDENCIES = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
NORMALIZED_XSD_SHA256 = "9bffc07cef30336d4a6b320d6569bc5a93c4e48b4889c0de7cf7e46cab090af1"
OFFICIAL_XSD_SHA256 = "a3ec5d6bae8173fce080709a8071787293dbe6271415d905d230c584c200982a"
DEPENDENCY_NAMES = ["Global-V1.0.xsd", "GlobalLibrary-V2.0.xsd", "UniversalCodes-V2.0.xsd"]


def qname(profile: dict[str, Any], prefix: str | None, name: str) -> str:
    return f"{{{profile['namespaces'][prefix or 'default']}}}{name}"


def add_fields(
    parent: ET.Element,
    profile: dict[str, Any],
    fields: dict[str, Any],
    response: dict[str, Any],
) -> None:
    for name, node in fields.items():
        value = response.get(name)
        if value is None and node.get("emitWhenParentPresent"):
            value = {}
        if value is None:
            continue
        if node["kind"] == "group" and node.get("flatten"):
            add_fields(parent, profile, node["fields"], value)
            continue
        child = ET.SubElement(parent, qname(profile, node.get("namespace"), node["element"]))
        if node["kind"] == "value":
            child.text = str(value)
        elif node["kind"] == "object":
            add_fields(child, profile, node["fields"], value)
        else:
            raise AssertionError(f"unsupported SF-424C mapping kind: {node['kind']}")


def render_xml(response: dict[str, Any]) -> bytes:
    profile = json.loads(
        (ROOT / "dist/forms/sf424c/targets/grants-gov-xml.json").read_text()
    )
    ET.register_namespace("SF424C_2_0", profile["namespaces"]["default"])
    root = ET.Element(qname(profile, "default", profile["root"]["element"]))
    for name, value in profile["root"]["attributes"].items():
        root.set(qname(profile, "default", name), str(value))
    add_fields(root, profile, profile["mapping"]["fields"], response)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def validate_exact_xsd(xml: bytes) -> subprocess.CompletedProcess[str]:
    xmllint = shutil.which("xmllint")
    if xmllint is None:
        raise AssertionError("xmllint is required to validate the pinned official XSD fixture")
    if hashlib.sha256(XSD_FIXTURE.read_bytes()).hexdigest() != NORMALIZED_XSD_SHA256:
        raise AssertionError("normalized SF-424C XSD fixture digest mismatch")
    profile = json.loads(
        (ROOT / "dist/forms/sf424c/targets/grants-gov-xml.json").read_text()
    )
    if profile["xsd"]["sha256"] != OFFICIAL_XSD_SHA256:
        raise AssertionError("official SF-424C XSD source digest mismatch")

    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        paths = {"SF424C_2_0-V2.0.xsd": XSD_FIXTURE}
        paths.update({name: DEPENDENCIES / name for name in DEPENDENCY_NAMES})
        for name, path in paths.items():
            source = path.read_text()
            for dependency in DEPENDENCY_NAMES:
                source = source.replace(
                    f"https://apply07.grants.gov/apply/system/schemas/{dependency}",
                    dependency,
                )
            (temp / name).write_text(source)
        xml_path = temp / "response.xml"
        xml_path.write_bytes(xml)
        return subprocess.run(
            ["xmllint", "--noout", "--schema", str(temp / "SF424C_2_0-V2.0.xsd"), str(xml_path)],
            text=True,
            capture_output=True,
            check=False,
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
        xml = render_xml(response)
        validation = validate_exact_xsd(xml)
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
        xml = render_xml(full_response())
        validation = validate_exact_xsd(xml)
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
        xml = render_xml(
            {"federalFunding": {"totalProjectCosts": "6000.00", "federalPercentageShare": 75, "federalFundingShare": "4500.00"}}
        )
        validation = validate_exact_xsd(xml)
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
