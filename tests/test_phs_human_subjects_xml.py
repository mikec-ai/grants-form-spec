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

    def test_minimal_no_human_subjects_payload_validates(self) -> None:
        xml = render_profile_xml(
            PROFILE,
            {"involvesHumanSpecimensOrData": "N: No", "humanSubjectsInvolved": "N: No"},
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
                "humanSubjectsInvolved": "Y: Yes",
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
                "humanSubjectsInvolved": "Y: Yes",
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

    def test_study_and_delayed_onset_wrapper_cardinalities_are_distinct(self) -> None:
        form_schema = json.loads((ROOT / "dist/forms/phs-human-subjects/schema.json").read_text())
        self.assertEqual(form_schema["properties"]["studies"]["maxItems"], 150)
        self.assertEqual(form_schema["properties"]["delayedOnsetStudies"]["maxItems"], 150)
        study_schema = json.loads((ROOT / "dist/question-bank/clinical-study/study-record/schema.json").read_text())
        self.assertEqual(study_schema["properties"]["otherClinicalTrialAttachments"]["maxItems"], 100)


if __name__ == "__main__":
    unittest.main()
