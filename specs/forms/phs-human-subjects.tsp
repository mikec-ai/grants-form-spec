import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/clinical-study/index.tsp";

using SimplerForms;
using QuestionBank.ClinicalStudy;

namespace Forms.PHSHumanSubjects;

enum PHSHumanSubjectsSection {
  overview: "Use of Human Specimens and/or Data",
  studies: "Human Subject Study Records",
  delayedOnset: "Delayed Onset Studies",
}

/** PHS Human Subjects and Clinical Trials Information, Grants.gov FID 705, version 3.0. */
@Form.meta(#{
  id: "phs-human-subjects",
  legacyFormId: 705,
  formName: "PHS Human Subjects and Clinical Trials Information",
  shortFormName: "PHSHumanSubjectsAndClinicalTrialsInfo_3_0",
  formVersion: "3.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "0925-0001",
})
@UI.sections(PHSHumanSubjectsSection)
@Response.role(ResponseRole.systemValue)
@UI.overrides(#{
  `involvesHumanSubjects`: #{ readOnly: true, visibleReadOnly: true, section: "overview" },
  `exemptFromFederalRegulations`: #{ readOnly: true, visibleReadOnly: true, section: "overview" },
  `exemptions`: #{ readOnly: true, visibleReadOnly: true, section: "overview" },
})
model PHSHumanSubjects extends QuestionBank.ResearchProject.HumanSubjectDeterminations {
  @UI.section(PHSHumanSubjectsSection.overview)
  involvesHumanSpecimensOrData: QuestionInvolvesHumanSpecimensOrData;
  @UI.section(PHSHumanSubjectsSection.overview)
  specimensExplanation?: HumanSpecimensExplanation;
  @UI.section(PHSHumanSubjectsSection.overview)
  otherRequestedInformation?: HumanSubjectsOtherRequestedInformation;
  @maxItems(150)
  @UI.section(PHSHumanSubjectsSection.studies)
  studies?: HumanSubjectStudyRecord[];
  @maxItems(150)
  @UI.section(PHSHumanSubjectsSection.delayedOnset)
  delayedOnsetStudies?: DelayedOnsetStudy[];
  @Response.role(ResponseRole.systemValue)
  @UI.readOnly
  @maxLength(40)
  @minLength(1)
  @UI.section(PHSHumanSubjectsSection.overview)
  applicationId?: string;
}
