import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/generics/index.tsp";
import "../question-bank/phs-fellowship/index.tsp";
import "../question-bank/phs398-cover-page-supplement/index.tsp";
import "../question-bank/research-application/index.tsp";
import "../question-bank/research-plan/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.PHSFellowship;
using QuestionBank.PHS398CoverPageSupplement;
using QuestionBank.ResearchApplication;
using QuestionBank.ResearchPlan;

namespace Forms.PHSFellowshipSupplemental;

enum PHSFellowshipSupplementalSection {
  introduction: "Introduction",
  candidate: "Candidate Section",
  researchTrainingPlan: "Research Training Plan",
  commitment: "Commitment to Candidate",
  otherResearchTrainingPlan: "Other Research Training Plan",
  additionalInformation: "Additional Information",
  budget: "Budget",
  appendix: "Appendix",
}

/** The fellowship occurrence of the shared stem-cell question, limited to 20 source records. */
model FellowshipHumanEmbryonicStemCells extends QuestionHumanEmbryonicStemCells {
  @UI.label("Cell Line(s)")
  @maxItems(20)
  cellLines?: HumanEmbryonicStemCellLine[];
}

/** The fellowship occurrence requires the first euthanasia answer when applicable. */
model FellowshipVertebrateAnimalEuthanasia extends QuestionVertebrateAnimalEuthanasia {
  @UI.label("Are vertebrate animals euthanized?")
  animalEuthanized: YesNoCode;
}

/** PHS Fellowship Supplemental Form, Grants.gov FID 836, version 8.0. */
@Form.meta(#{
  id: "phs-fellowship-supplemental",
  legacyFormId: 836,
  formName: "PHS Fellowship Supplemental Form",
  shortFormName: "PHS_Fellowship_Supplemental_8_0",
  formVersion: "8.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "0925-0001",
})
@UI.sections(PHSFellowshipSupplementalSection)
@UI.overrides(#{
  `budget.tuition.year1`: #{ enabledWhen: #{ path: "budget.tuition.fundsRequested", equals: YesNoCode.yes } },
  `budget.tuition.year2`: #{ enabledWhen: #{ path: "budget.tuition.fundsRequested", equals: YesNoCode.yes } },
  `budget.tuition.year3`: #{ enabledWhen: #{ path: "budget.tuition.fundsRequested", equals: YesNoCode.yes } },
  `budget.tuition.year4`: #{ enabledWhen: #{ path: "budget.tuition.fundsRequested", equals: YesNoCode.yes } },
  `budget.tuition.year5`: #{ enabledWhen: #{ path: "budget.tuition.fundsRequested", equals: YesNoCode.yes } },
  `budget.tuition.year6`: #{ enabledWhen: #{ path: "budget.tuition.fundsRequested", equals: YesNoCode.yes } },
  `budget.childcare.year1`: #{ enabledWhen: #{ path: "budget.childcare.fundsRequested", equals: YesNoCode.yes } },
  `budget.childcare.year2`: #{ enabledWhen: #{ path: "budget.childcare.fundsRequested", equals: YesNoCode.yes } },
  `budget.childcare.year3`: #{ enabledWhen: #{ path: "budget.childcare.fundsRequested", equals: YesNoCode.yes } },
  `budget.childcare.year4`: #{ enabledWhen: #{ path: "budget.childcare.fundsRequested", equals: YesNoCode.yes } },
  `budget.childcare.year5`: #{ enabledWhen: #{ path: "budget.childcare.fundsRequested", equals: YesNoCode.yes } },
  `budget.childcare.year6`: #{ enabledWhen: #{ path: "budget.childcare.fundsRequested", equals: YesNoCode.yes } },
})
model PHSFellowshipSupplemental {
  // The source enables this only for Revision or Resubmission applications. The predicate
  // belongs to the application package and remains a source-bound gate until the portable
  // application-level condition contract exists.
  @UI.label("Introduction to Application")
  @UI.section(PHSFellowshipSupplementalSection.introduction)
  @UI.widget(WidgetName.Attachment)
  introduction?: ResearchPlanIntroduction;

  @UI.label("Goals for Fellowship Training and Career")
  @UI.section(PHSFellowshipSupplementalSection.candidate)
  @UI.widget(WidgetName.Attachment)
  candidateGoals: FellowshipCandidateGoals;

  @UI.label("Activities Planned Under This Award")
  @UI.section(PHSFellowshipSupplementalSection.researchTrainingPlan)
  @UI.widget(WidgetName.Attachment)
  trainingActivities: FellowshipTrainingActivities;

  @UI.label("Research Project Specific Aims")
  @UI.section(PHSFellowshipSupplementalSection.researchTrainingPlan)
  @UI.widget(WidgetName.Attachment)
  researchProjectAims: ResearchPlanSpecificAims;

  @UI.label("Research Strategy")
  @UI.section(PHSFellowshipSupplementalSection.researchTrainingPlan)
  @UI.widget(WidgetName.Attachment)
  researchProjectStrategy: ResearchPlanStrategy;

  // The source enables this only for Renewal or Resubmission applications. Do not add a
  // form-local application type solely to make the predicate executable.
  @UI.label("Progress Report Publication List")
  @UI.section(PHSFellowshipSupplementalSection.researchTrainingPlan)
  @UI.widget(WidgetName.Attachment)
  progressReportPublicationList?: ResearchPlanProgressReportPublicationList;

  @UI.label("Training in the Responsible Conduct of Research")
  @UI.section(PHSFellowshipSupplementalSection.researchTrainingPlan)
  @UI.widget(WidgetName.Attachment)
  responsibleConductTraining: FellowshipResponsibleConductTraining;

  @UI.label("Sponsor and Co-Sponsor Statements")
  @UI.section(PHSFellowshipSupplementalSection.commitment)
  @UI.widget(WidgetName.Attachment)
  sponsorCommitment?: FellowshipSponsorCommitment;

  @UI.label("Letters of Support from Collaborators, Contributors, and Consultants")
  @UI.section(PHSFellowshipSupplementalSection.commitment)
  @UI.widget(WidgetName.Attachment)
  lettersOfSupport?: ResearchPlanLettersOfSupport;

  @UI.label("Description of Candidate's Contribution to Programmatic Goals")
  @UI.section(PHSFellowshipSupplementalSection.commitment)
  @UI.widget(WidgetName.Attachment)
  candidateContribution?: FellowshipCandidateContribution;

  @UI.label("Are Vertebrate Animals Used?")
  @UI.section(PHSFellowshipSupplementalSection.otherResearchTrainingPlan)
  vertebrateAnimalsUsed: FellowshipVertebrateAnimalsUsed;

  @UI.section(PHSFellowshipSupplementalSection.otherResearchTrainingPlan)
  @UI.enabledWhen(PHSFellowshipSupplemental.vertebrateAnimalsUsed, "Y: Yes")
  @Validation.requiredWhen(PHSFellowshipSupplemental.vertebrateAnimalsUsed, "Y: Yes")
  vertebrateAnimalEuthanasia?: FellowshipVertebrateAnimalEuthanasia;

  @UI.label("Vertebrate Animals")
  @UI.section(PHSFellowshipSupplementalSection.otherResearchTrainingPlan)
  @UI.widget(WidgetName.Attachment)
  vertebrateAnimalsDocument?: ResearchPlanVertebrateAnimalsDocument;

  @UI.label("Select Agent Research")
  @UI.section(PHSFellowshipSupplementalSection.otherResearchTrainingPlan)
  @UI.widget(WidgetName.Attachment)
  selectAgentResearch?: ResearchPlanSelectAgentResearch;

  @UI.label("Resource Sharing Plan(s)")
  @UI.section(PHSFellowshipSupplementalSection.otherResearchTrainingPlan)
  @UI.widget(WidgetName.Attachment)
  resourceSharingPlans?: ResearchPlanResourceSharingPlans;

  @UI.label("Other Plan(s)")
  @UI.section(PHSFellowshipSupplementalSection.otherResearchTrainingPlan)
  @UI.widget(WidgetName.Attachment)
  otherPlans?: ResearchPlanOtherPlans;

  @UI.label("Authentication of Key Biological and/or Chemical Resources")
  @UI.section(PHSFellowshipSupplementalSection.otherResearchTrainingPlan)
  @UI.widget(WidgetName.Attachment)
  keyResourceAuthentication?: ResearchPlanKeyResourceAuthentication;

  // The source also clears inactive stem-cell responses. Clearing is intentionally not
  // inferred from visibility; it remains a source-bound gate for a generic response rule.
  @UI.label("Human Embryonic Stem Cells")
  @UI.section(PHSFellowshipSupplementalSection.additionalInformation)
  humanEmbryonicStemCells: FellowshipHumanEmbryonicStemCells;

  @UI.label("Fellowship Candidate Information")
  @UI.section(PHSFellowshipSupplementalSection.additionalInformation)
  candidateInformation: QuestionFellowshipCandidateInformation;

  @UI.label("Fellowship Budget")
  @UI.section(PHSFellowshipSupplementalSection.budget)
  budget: QuestionFellowshipBudget;

  @UI.label("Appendix")
  @UI.section(PHSFellowshipSupplementalSection.appendix)
  @UI.widget(WidgetName.AttachmentArray)
  @maxItems(100)
  appendix?: ResearchPlanAppendixDocument[];
}
