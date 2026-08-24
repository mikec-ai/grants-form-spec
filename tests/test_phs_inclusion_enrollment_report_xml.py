from __future__ import annotations

import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from conformance.grants_gov_xml import ExactXsdFixture, PinnedXsdFile, render_profile_xml, validate_exact_xsd


ROOT = Path(__file__).parents[1]
FORM_NS = "http://apply.grants.gov/forms/PHSInclusionEnrollmentReport-V1.0"
PROFILE = json.loads((ROOT / "dist/forms/phs-inclusion-enrollment-report/targets/grants-gov-xml.json").read_text())
FORM_XSDS = ROOT / "tests/fixtures/grants-gov-xsd/phs-inclusion-enrollment-report-1.0"
SHARED_XSDS = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
XSD_SET = ExactXsdFixture(
    entrypoint="PHSInclusionEnrollmentReport-V1.0.xsd",
    files=(
        PinnedXsdFile("PHSInclusionEnrollmentReport-V1.0.xsd", FORM_XSDS / "PHSInclusionEnrollmentReport-V1.0.xsd", "3263bbfa8881c7d428958cf91de470cd19f0f6cbc11818c4752d5266bb0f53a4"),
        PinnedXsdFile("GlobalLibrary-V2.0.xsd", SHARED_XSDS / "GlobalLibrary-V2.0.xsd", "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8"),
        PinnedXsdFile("UniversalCodes-V2.0.xsd", SHARED_XSDS / "UniversalCodes-V2.0.xsd", "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a"),
    ),
    official_sha256="3263bbfa8881c7d428958cf91de470cd19f0f6cbc11818c4752d5266bb0f53a4",
    dependency_uri_prefixes=("https://apply07.grants.gov/apply/system/schemas/",),
)


def report(**overrides: object) -> dict[str, object]:
    return {
        "title": "Enrollment report",
        "usesExistingDatasetOrResource": "N: No",
        "locationType": "Domestic",
        **overrides,
    }


def complete_matrices() -> tuple[dict[str, object], dict[str, object]]:
    value = 0
    planned_races = ("americanIndianAlaskaNative", "asian", "nativeHawaiianPacificIslander", "blackAfricanAmerican", "white", "moreThanOneRace", "total")
    cumulative_races = (*planned_races[:-1], "unknownNotReported", "total")

    def counts(names: tuple[str, ...]) -> dict[str, int]:
        nonlocal value
        out = {}
        for name in names:
            value += 1
            out[name] = value
        return out

    planned = {
        ethnicity: {sex: counts(planned_races) for sex in ("female", "male")}
        for ethnicity in ("notHispanicLatino", "hispanicLatino")
    }
    planned["total"] = counts(planned_races)
    cumulative = {
        ethnicity: {sex: counts(cumulative_races) for sex in ("female", "male", "unknownNotReportedSex")}
        for ethnicity in ("notHispanicLatino", "hispanicLatino", "unknownNotReportedEthnicity")
    }
    cumulative["total"] = counts(cumulative_races)
    return planned, cumulative


class PHSInclusionEnrollmentReportXmlTests(unittest.TestCase):
    def assert_valid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_invalid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertNotEqual(result.returncode, 0, "source XSD unexpectedly accepted XML")

    def test_direct_report_and_country_repetition_preserve_root_namespace_and_sequence(self) -> None:
        xml = render_profile_xml(PROFILE, {"reports": [report(
            enrollmentCountries=["USA: UNITED STATES", "CAN: CANADA"],
            enrollmentLocations="University",
            comments="Comment",
        )]})
        root = ET.fromstring(xml)
        self.assertEqual(root.tag, f"{{{FORM_NS}}}PHSInclusionEnrollmentReport")
        self.assertEqual(root.attrib[f"{{{FORM_NS}}}FormVersion"], "1.0")
        row = root.find(f"{{{FORM_NS}}}InclusionEnrollmentReport")
        self.assertIsNotNone(row)
        self.assertEqual(
            [child.tag.rsplit("}", 1)[-1] for child in row],
            ["InclusionEnrollmentReportTitle", "ExistingDatasetOrResource", "EnrollmentLocationType", "EnrollmentCountry", "EnrollmentCountry", "EnrollmentLocations", "Comments"],
        )
        self.assertNotIn("IER_id", xml.decode())
        self.assert_valid(xml)

    def test_embedded_only_report_identifier_fails_closed_in_standalone_profile(self) -> None:
        with self.assertRaisesRegex(
            AssertionError,
            r"unmapped response properties at /reports/0: reportId",
        ):
            render_profile_xml(PROFILE, {"reports": [report(reportId="not-on-this-wire")]})

    def test_report_country_string_enum_and_numeric_boundaries(self) -> None:
        self.assert_invalid(render_profile_xml(PROFILE, {"reports": []}))
        self.assert_valid(render_profile_xml(PROFILE, {"reports": [report()] * 20}))
        self.assert_invalid(render_profile_xml(PROFILE, {"reports": [report()] * 21}))
        self.assert_invalid(render_profile_xml(PROFILE, {"reports": [report(title="")]}))
        self.assert_invalid(render_profile_xml(PROFILE, {"reports": [report(locationType="Neither")]}))
        self.assert_valid(render_profile_xml(PROFILE, {"reports": [report(enrollmentCountries=["USA: UNITED STATES"] * 200)]}))
        self.assert_invalid(render_profile_xml(PROFILE, {"reports": [report(enrollmentCountries=["USA: UNITED STATES"] * 201)]}))
        self.assert_invalid(render_profile_xml(PROFILE, {"reports": [report(enrollmentLocations="")]}))
        self.assert_invalid(render_profile_xml(PROFILE, {"reports": [report(comments="")]}))

        high = report(planned={"notHispanicLatino": {"female": {"asian": 999999999, "total": 9999999999}}, "total": {"total": 99999999999}})
        self.assert_valid(render_profile_xml(PROFILE, {"reports": [high]}))
        too_high = report(planned={"notHispanicLatino": {"female": {"asian": 1000000000}}})
        self.assert_invalid(render_profile_xml(PROFILE, {"reports": [too_high]}))

    def test_all_115_coordinates_are_lossless_and_uncompiled_totals_are_not_inferred(self) -> None:
        planned, cumulative = complete_matrices()
        # Deliberately inconsistent totals remain XSD-valid while all 28 DAT calculations are uncompiled.
        planned["total"]["total"] = 99999999999
        cumulative["total"]["total"] = 88888888888
        xml = render_profile_xml(PROFILE, {"reports": [report(
            enrollmentCountries=["USA: UNITED STATES"],
            enrollmentLocations="Research center",
            comments="All source fields",
            planned=planned,
            cumulativeActual=cumulative,
        )]})
        root = ET.fromstring(xml)
        matrix = root.find(f"{{{FORM_NS}}}InclusionEnrollmentReport")
        values = [
            node.text for group_name in ("Planned", "Cumulative")
            for group in [matrix.find(f"{{{FORM_NS}}}{group_name}")]
            for node in group.iter()
            if node is not group and len(node) == 0
        ]
        self.assertEqual(len(values), 115)
        self.assertIn("99999999999", values)
        self.assertIn("88888888888", values)
        self.assert_valid(xml)


if __name__ == "__main__":
    unittest.main()
