from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from conformance.grants_gov_xml import (
    ExactXsdFixture,
    PinnedXsdFile,
    render_profile_xml,
    validate_exact_xsd,
)


ROOT = Path(__file__).parents[1]
FORM_NS = "http://apply.grants.gov/forms/PHSHumanSubjectsAndClinicalTrialsInfo_3_0-V3.0"
STUDY_NS = "http://apply.grants.gov/forms/HumanSubjectStudy_3_0-V3.0"
PROFILE = json.loads(
    (ROOT / "dist/forms/phs-human-subjects/targets/grants-gov-xml.json").read_text()
)
FORM_XSDS = ROOT / "tests/fixtures/grants-gov-xsd/phs-human-subjects-3.0"
SHARED_XSDS = ROOT / "tests/fixtures/grants-gov-xsd/rr-key-person-expanded-4.0"
FILES = {
    "PHSHumanSubjectsAndClinicalTrialsInfo_3_0-V3.0.xsd": (
        FORM_XSDS / "PHSHumanSubjectsAndClinicalTrialsInfo_3_0-V3.0.xsd",
        "29d859de80cc9febbd1599c28f5db9a3ec82bff26a4d32f4dbbc372effb56bf3",
    ),
    "HumanSubjectStudy_3_0-V3.0.xsd": (
        FORM_XSDS / "HumanSubjectStudy_3_0-V3.0.xsd",
        "799205dea5eddcf13f926cc39d5fc7de27c6a6cdcc68eff4d49e1b629d4351cf",
    ),
    "Attachments-V1.0.xsd": (SHARED_XSDS / "Attachments-V1.0.xsd", "ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d"),
    "Global-V1.0.xsd": (SHARED_XSDS / "Global-V1.0.xsd", "4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb"),
    "GlobalLibrary-V2.0.xsd": (SHARED_XSDS / "GlobalLibrary-V2.0.xsd", "ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8"),
    "UniversalCodes-V2.0.xsd": (SHARED_XSDS / "UniversalCodes-V2.0.xsd", "78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a"),
}
XSD_SET = ExactXsdFixture(
    entrypoint="PHSHumanSubjectsAndClinicalTrialsInfo_3_0-V3.0.xsd",
    files=tuple(PinnedXsdFile(name, path, digest) for name, (path, digest) in FILES.items()),
    official_sha256="29d859de80cc9febbd1599c28f5db9a3ec82bff26a4d32f4dbbc372effb56bf3",
    dependency_uri_prefixes=(
        "https://apply07.grants.gov/apply/system/schemas/",
        "https://apply07.grants.gov/apply/forms/schemas/",
    ),
)


def attachment(number: int) -> dict[str, str]:
    return {
        "fileName": f"human-subjects-{number}.pdf",
        "mimeType": "application/pdf",
        "fileLocation": f"files/human-subjects-{number}.pdf",
        "hashValue": hashlib.sha256(str(number).encode()).hexdigest(),
    }


class PHSHumanSubjectsXmlTests(unittest.TestCase):
    def assert_valid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_invalid(self, xml: bytes) -> None:
        result = validate_exact_xsd(xml, XSD_SET, profile=PROFILE)
        self.assertNotEqual(result.returncode, 0, "source XSD unexpectedly accepted XML")

    def test_minimal_no_human_subjects_payload_validates(self) -> None:
        xml = render_profile_xml(
            PROFILE,
            {"involvesHumanSpecimensOrData": "N: No", "involvesHumanSubjects": "N: No"},
        )
        root = ET.fromstring(xml)
        self.assertEqual(root.tag, f"{{{FORM_NS}}}PHSHumanSubjectsAndClinicalTrialsInfo_3_0")
        self.assertEqual(
            [child.tag for child in root],
            [f"{{{FORM_NS}}}InvolveHumanSpecimens", f"{{{FORM_NS}}}HumanSubjectsIndicator"],
        )
        self.assert_valid(xml)

    def test_delayed_onset_row_preserves_required_attachment_and_sequence(self) -> None:
        xml = render_profile_xml(
            PROFILE,
            {
                "involvesHumanSpecimensOrData": "N: No",
                "involvesHumanSubjects": "Y: Yes",
                "delayedOnsetStudies": [{
                    "studyTitle": "Future study",
                    "anticipatedClinicalTrial": "Y: Yes",
                    "justification": "justification",
                }],
            },
            {"justification": attachment(1)},
        )
        delayed = ET.fromstring(xml).find(f"{{{FORM_NS}}}DelayedOnsetStudy")
        self.assertIsNotNone(delayed)
        self.assertEqual(
            [child.tag.rsplit("}", 1)[-1] for child in delayed],
            ["StudyTitle", "AnticipatedClinicalTrial", "Justification"],
        )
        self.assert_valid(xml)

    def test_structured_study_and_inconsistent_enrollment_totals_validate(self) -> None:
        study = {
            "studyTitle": "Structured study",
            "exemptFromFederalRegulations": "N: No",
            "clinicalTrialQuestionnaire": {
                "humanParticipants": "Y: Yes",
                "prospectivelyAssignedIntervention": "Y: Yes",
                "evaluatesIntervention": "Y: Yes",
                "healthRelatedOutcome": "Y: Yes",
            },
            "populationCharacteristics": {
                "inclusionEnrollmentReports": [{
                    "title": "Report one",
                    "usesExistingDatasetOrResource": "N: No",
                    "locationType": "Domestic",
                    "enrollmentCountries": ["USA: UNITED STATES"],
                    "planned": {
                        "notHispanicLatino": {"female": {"asian": 9, "total": 1}},
                        "total": {"asian": 999, "total": 2},
                    },
                    "cumulativeActual": {
                        "unknownNotReportedEthnicity": {
                            "unknownNotReportedSex": {"unknownNotReported": 7, "total": 3}
                        },
                        "total": {"unknownNotReported": 111, "total": 4},
                    },
                }]
            },
        }
        xml = render_profile_xml(
            PROFILE,
            {
                "involvesHumanSpecimensOrData": "N: No",
                "involvesHumanSubjects": "Y: Yes",
                "studies": [study],
            },
        )
        root = ET.fromstring(xml)
        wrapper = root.find(f"{{{FORM_NS}}}HumanSubjectStudyAttachment")
        self.assertIsNotNone(wrapper)
        study_node = wrapper.find(f"{{{STUDY_NS}}}HumanSubjectStudy_3_0")
        self.assertIsNotNone(study_node)
        self.assertIsNotNone(study_node.find(f".//{{{STUDY_NS}}}Planned"))
        self.assertIsNotNone(study_node.find(f".//{{{STUDY_NS}}}Cumulative"))
        self.assert_valid(xml)

    def test_both_exemption_wrappers_enforce_nonempty_items(self) -> None:
        base = {"involvesHumanSpecimensOrData": "N: No", "involvesHumanSubjects": "Y: Yes"}
        # The wrapper is optional, but if present its source sequence requires at least one item.
        self.assert_valid(render_profile_xml(PROFILE, base))
        self.assert_valid(render_profile_xml(PROFILE, {**base, "exemptions": ["E1"]}))
        self.assert_invalid(render_profile_xml(PROFILE, {**base, "exemptions": []}))

        study = {
            "studyTitle": "Exempt study",
            "exemptFromFederalRegulations": "Y: Yes",
            "clinicalTrialQuestionnaire": {
                "humanParticipants": "Y: Yes",
                "prospectivelyAssignedIntervention": "N: No",
                "evaluatesIntervention": "N: No",
                "healthRelatedOutcome": "N: No",
            },
        }
        self.assert_valid(render_profile_xml(PROFILE, {**base, "studies": [{**study, "exemptionNumbers": ["E2"]}]}))
        self.assert_invalid(render_profile_xml(PROFILE, {**base, "studies": [{**study, "exemptionNumbers": []}]}))

    def test_source_bounded_strings_reject_empty_values(self) -> None:
        base = {"involvesHumanSpecimensOrData": "N: No", "involvesHumanSubjects": "N: No"}
        self.assert_invalid(render_profile_xml(PROFILE, {**base, "applicationId": ""}))
        study = {
            "studyTitle": "",
            "exemptFromFederalRegulations": "N: No",
            "clinicalTrialQuestionnaire": {
                "humanParticipants": "N: No",
                "prospectivelyAssignedIntervention": "N: No",
                "evaluatesIntervention": "N: No",
                "healthRelatedOutcome": "N: No",
            },
        }
        self.assert_invalid(render_profile_xml(PROFILE, {**base, "studies": [study]}))

    def test_comprehensive_structured_study_preserves_all_groups_and_sequence(self) -> None:
        study = {
            "studyId": "study-1",
            "studyTitle": "Comprehensive study",
            "exemptFromFederalRegulations": "Y: Yes",
            "exemptionNumbers": ["E1", "E2"],
            "clinicalTrialQuestionnaire": {
                "humanParticipants": "Y: Yes",
                "prospectivelyAssignedIntervention": "Y: Yes",
                "evaluatesIntervention": "Y: Yes",
                "healthRelatedOutcome": "Y: Yes",
            },
            "clinicalTrialsGovIdentifier": "NCT12345678",
            "populationCharacteristics": {
                "conditionsOrFocus": ["Condition one", "Condition two"],
                "eligibilityCriteria": "Adults meeting the source criteria",
                "ageLimits": {
                    "minimum": {"value": 18, "unit": "Years"},
                    "maximum": {"value": 65, "unit": "Years"},
                },
                "inclusionAcrossLifespan": "inclusionAcrossLifespan",
                "inclusionWomenMinorities": "inclusionWomenMinorities",
                "recruitmentRetentionPlan": "recruitmentRetentionPlan",
                "recruitmentStatus": "Recruiting",
                "studyTimeline": "studyTimeline",
                "firstSubjectEnrollment": {"date": "2026-01-01", "anticipatedActual": "Actual"},
                "inclusionEnrollmentReports": [{
                    "reportId": "ier-1", "title": "Enrollment report",
                    "usesExistingDatasetOrResource": "N: No", "locationType": "Domestic",
                    "enrollmentCountries": ["USA: UNITED STATES"],
                    "enrollmentLocations": "Baltimore, Maryland", "comments": "Source-aligned note",
                    "planned": {"notHispanicLatino": {"female": {"asian": 1, "total": 3}}},
                    "cumulativeActual": {"total": {"asian": 2, "total": 4, "unknownNotReported": 1}},
                }],
            },
            "protectionMonitoringPlans": {
                "protectionOfHumanSubjects": "protectionOfHumanSubjects",
                "multiSiteStudy": "Y: Yes", "singleIrbPlan": "singleIrbPlan",
                "dataSafetyMonitoringPlan": "dataSafetyMonitoringPlan",
                "monitoringBoardAppointed": "Y: Yes", "studyTeamStructure": "studyTeamStructure",
            },
            "protocolSynopsis": {
                "studyDesign": {
                    "detailedDescription": "Detailed design", "primaryPurpose": "Other",
                    "otherPrimaryPurpose": "Other purpose",
                    "interventions": [{"type": "Drug (including placebo)", "name": "Drug A", "description": "Description"}],
                    "phase": "Phase 2", "nihDefinedPhase3": "N: No",
                    "interventionModel": "Other", "otherInterventionModel": "Adaptive",
                    "masking": "Y: Yes",
                    "maskingParties": {"participant": "Y: Yes", "careProvider": "N: No", "investigator": "Y: Yes", "outcomesAssessor": "N: No"},
                    "allocation": "Randomized",
                },
                "outcomeMeasures": [{"name": "Outcome", "type": "Primary", "timeFrame": "Week 12", "description": "Primary outcome"}],
                "statisticalDesignAndPower": "statisticalDesignAndPower",
                "subjectParticipationDuration": "12 weeks", "fdaRegulatedIntervention": "Y: Yes",
                "investigationalProductAvailability": "investigationalProductAvailability",
                "applicableClinicalTrial": "Y: Yes", "disseminationPlan": "disseminationPlan",
            },
            "otherClinicalTrialAttachments": ["otherClinicalTrialAttachments"],
        }
        attachment_names = {
            "specimensExplanation", "otherRequestedInformation", "inclusionAcrossLifespan",
            "inclusionWomenMinorities", "recruitmentRetentionPlan", "studyTimeline",
            "protectionOfHumanSubjects", "singleIrbPlan", "dataSafetyMonitoringPlan",
            "studyTeamStructure", "statisticalDesignAndPower",
            "investigationalProductAvailability", "disseminationPlan",
            "otherClinicalTrialAttachments", "justification",
        }
        attachments = {name: attachment(index) for index, name in enumerate(sorted(attachment_names), 1)}
        payload = {
            "involvesHumanSpecimensOrData": "Y: Yes", "specimensExplanation": "specimensExplanation",
            "involvesHumanSubjects": "Y: Yes", "exemptFromFederalRegulations": "Y: Yes",
            "exemptions": ["E1"], "otherRequestedInformation": "otherRequestedInformation",
            "delayedOnsetStudies": [{"studyTitle": "Later study", "anticipatedClinicalTrial": "Y: Yes", "justification": "justification"}],
            "studies": [study], "applicationId": "application-1",
        }
        xml = render_profile_xml(PROFILE, payload, attachments)
        root = ET.fromstring(xml)
        study_node = root.find(f".//{{{STUDY_NS}}}HumanSubjectStudy_3_0")
        self.assertIsNotNone(study_node)
        self.assertEqual(len(study_node.findall(f".//{{{STUDY_NS}}}StudyConditions")), 2)
        self.assertEqual(len(study_node.findall(f".//{{{STUDY_NS}}}EnrollmentCountry")), 1)
        self.assertEqual(len(study_node.findall(f".//{{{STUDY_NS}}}Interventions")), 1)
        self.assertEqual(len(study_node.findall(f".//{{{STUDY_NS}}}OutcomesMeasures")), 1)
        self.assert_valid(xml)

    def test_study_and_delayed_onset_wrapper_cardinalities_are_distinct(self) -> None:
        form_schema = json.loads((ROOT / "dist/forms/phs-human-subjects/schema.json").read_text())
        self.assertEqual(form_schema["properties"]["studies"]["maxItems"], 150)
        self.assertEqual(form_schema["properties"]["delayedOnsetStudies"]["maxItems"], 150)
        study_schema = json.loads((ROOT / "dist/question-bank/clinical-study/study-record/schema.json").read_text())
        self.assertEqual(study_schema["properties"]["otherClinicalTrialAttachments"]["maxItems"], 100)

    def test_every_nested_repeat_accepts_its_maximum_and_rejects_maximum_plus_one(self) -> None:
        questionnaire = {
            "humanParticipants": "N: No", "prospectivelyAssignedIntervention": "N: No",
            "evaluatesIntervention": "N: No", "healthRelatedOutcome": "N: No",
        }

        def base_study() -> dict[str, object]:
            return {
                "studyTitle": "Boundary study",
                "exemptFromFederalRegulations": "N: No",
                "clinicalTrialQuestionnaire": questionnaire,
            }

        base = {"involvesHumanSpecimensOrData": "N: No", "involvesHumanSubjects": "Y: Yes"}

        def check_study_array(path: str, maximum: int, item: object) -> None:
            def payload(count: int) -> dict[str, object]:
                study = base_study()
                cursor: dict[str, object] = study
                parts = path.split(".")
                for part in parts[:-1]:
                    child: dict[str, object] = {}
                    cursor[part] = child
                    cursor = child
                cursor[parts[-1]] = [item for _ in range(count)]
                return {**base, "studies": [study]}

            self.assert_valid(render_profile_xml(PROFILE, payload(maximum), {
                str(value): attachment(index)
                for index, value in enumerate([item] if isinstance(item, str) else [], 1)
            }))
            self.assert_invalid(render_profile_xml(PROFILE, payload(maximum + 1), {
                str(value): attachment(index)
                for index, value in enumerate([item] if isinstance(item, str) else [], 1)
            }))

        check_study_array("populationCharacteristics.conditionsOrFocus", 20, "Condition")
        report = {
            "title": "Report", "usesExistingDatasetOrResource": "N: No", "locationType": "Domestic",
        }
        check_study_array("populationCharacteristics.inclusionEnrollmentReports", 20, report)
        report_countries = {**report, "enrollmentCountries": ["USA: UNITED STATES"] * 200}
        self.assert_valid(render_profile_xml(PROFILE, {**base, "studies": [{**base_study(), "populationCharacteristics": {"inclusionEnrollmentReports": [report_countries]}}]}))
        report_countries["enrollmentCountries"] = ["USA: UNITED STATES"] * 201
        self.assert_invalid(render_profile_xml(PROFILE, {**base, "studies": [{**base_study(), "populationCharacteristics": {"inclusionEnrollmentReports": [report_countries]}}]}))
        check_study_array("protocolSynopsis.studyDesign.interventions", 20, {
            "type": "Drug (including placebo)", "name": "Drug", "description": "Description",
        })
        check_study_array("protocolSynopsis.outcomeMeasures", 50, {
            "name": "Outcome", "type": "Primary", "timeFrame": "Week 1", "description": "Description",
        })
        check_study_array("otherClinicalTrialAttachments", 100, "other")

        minimal = base_study()
        self.assert_valid(render_profile_xml(PROFILE, {**base, "studies": [minimal] * 150}))
        self.assert_invalid(render_profile_xml(PROFILE, {**base, "studies": [minimal] * 151}))
        delayed = {"studyTitle": "Later", "justification": "justification"}
        attachments = {"justification": attachment(1)}
        self.assert_valid(render_profile_xml(PROFILE, {**base, "delayedOnsetStudies": [delayed] * 150}, attachments))
        self.assert_invalid(render_profile_xml(PROFILE, {**base, "delayedOnsetStudies": [delayed] * 151}, attachments))


if __name__ == "__main__":
    unittest.main()
