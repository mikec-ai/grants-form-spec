import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/phs-career-development/index.tsp";
import "../question-bank/research-plan/index.tsp";

using SimplerForms;
using QuestionBank.PHSCareerDevelopment;
using QuestionBank.ResearchPlan;

namespace Forms.PHS398CareerDevelopmentSupplemental;

enum PHS398CareerDevelopmentSection {
  introduction: "Introduction",
  candidate: "Candidate Section",
  researchPlan: "Research Plan Section",
  otherCandidate: "Other Candidate Information Section",
  mentor: "Mentor, Co-Mentor, Consultant, Collaborators Section",
  environment: "Environment and Institutional Commitment to the Candidate Section",
  otherResearchPlan: "Other Research Plan Section",
  appendix: "Appendix",
  citizenship: "Citizenship",
}

/** PHS 398 Career Development Award Supplemental Form, Grants.gov FID 799, version 6.0. */
@Form.meta(#{
  id: "phs398-career-development-supplemental",
  legacyFormId: 799,
  formName: "PHS 398 Career Development Award Supplemental Form",
  shortFormName: "PHS398_CareerDevelopmentAwardSup_6_0",
  formVersion: "6.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "0925-0001",
})
@UI.sections(PHS398CareerDevelopmentSection)
model PHS398CareerDevelopmentSupplemental {
  // Application type is owned by the package's R&R SF-424. Keep this exact
  // Revision/Resubmission gate source-bound until cross-form conditions exist.
  @UI.label("1. Introduction to Application (for Resubmission and Revision applications)")
  @UI.section(PHS398CareerDevelopmentSection.introduction)
  @UI.widget(WidgetName.Attachment)
  introduction?: ResearchPlanIntroduction;

  @UI.label("2. Candidate Information and Goals for Career Development")
  @UI.section(PHS398CareerDevelopmentSection.candidate)
  @UI.widget(WidgetName.Attachment)
  candidateInformationAndGoals?: CareerCandidateInformationAndGoals;

  @UI.label("3. Specific Aims")
  @UI.section(PHS398CareerDevelopmentSection.researchPlan)
  @UI.widget(WidgetName.Attachment)
  specificAims?: ResearchPlanSpecificAims;

  @UI.label("4. Research Strategy")
  @UI.section(PHS398CareerDevelopmentSection.researchPlan)
  @UI.widget(WidgetName.Attachment)
  researchStrategy: ResearchPlanStrategy;

  // Application type is package state; preserve the Renewal/Resubmission gate as evidence.
  @UI.label("5. Progress Report Publication List (for Renewal applications)")
  @UI.section(PHS398CareerDevelopmentSection.researchPlan)
  @UI.widget(WidgetName.Attachment)
  progressReportPublicationList?: ResearchPlanProgressReportPublicationList;

  @UI.label("6. Training in the Responsible Conduct of Research")
  @UI.section(PHS398CareerDevelopmentSection.researchPlan)
  @UI.widget(WidgetName.Attachment)
  responsibleConductOfResearch?: CareerResponsibleConductOfResearch;

  @UI.label("7. Candidate's Plan to Provide Mentoring")
  @UI.section(PHS398CareerDevelopmentSection.otherCandidate)
  @UI.widget(WidgetName.Attachment)
  mentoringPlan?: CareerCandidateMentoringPlan;

  @UI.label("8. Plans and Statements of Mentor and Co-Mentor(s)")
  @UI.section(PHS398CareerDevelopmentSection.mentor)
  @UI.widget(WidgetName.Attachment)
  statementsOfSupport?: CareerMentorStatements;

  @UI.label("9. Letters of Support from Collaborators, Contributors, and Consultants")
  @UI.section(PHS398CareerDevelopmentSection.mentor)
  @UI.widget(WidgetName.Attachment)
  lettersOfSupport?: ResearchPlanLettersOfSupport;

  @UI.label("10. Description of Institutional Environment")
  @UI.section(PHS398CareerDevelopmentSection.environment)
  @UI.widget(WidgetName.Attachment)
  institutionalEnvironment?: CareerInstitutionalEnvironment;

  @UI.label("11. Institutional Commitment to Candidate's Research Career Development")
  @UI.section(PHS398CareerDevelopmentSection.environment)
  @UI.widget(WidgetName.Attachment)
  institutionalCommitment?: CareerInstitutionalCommitment;

  @UI.label("12. Description of Candidate's Contribution to Program Goals")
  @UI.section(PHS398CareerDevelopmentSection.environment)
  @UI.widget(WidgetName.Attachment)
  candidateContribution?: CareerCandidateContribution;

  // Requiredness depends on R&R Other Project Information package state.
  @UI.label("13. Vertebrate Animals")
  @UI.section(PHS398CareerDevelopmentSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  vertebrateAnimals?: ResearchPlanVertebrateAnimalsDocument;

  @UI.label("14. Select Agent Research")
  @UI.section(PHS398CareerDevelopmentSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  selectAgentResearch?: ResearchPlanSelectAgentResearch;

  @UI.label("15. Consortium/Contractual Arrangements")
  @UI.section(PHS398CareerDevelopmentSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  consortiumContractualArrangements?: ResearchPlanConsortiumContractualArrangements;

  @UI.label("16. Resource Sharing")
  @UI.section(PHS398CareerDevelopmentSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  resourceSharingPlans?: ResearchPlanResourceSharingPlans;

  @UI.label("17. Other Plan(s)")
  @UI.section(PHS398CareerDevelopmentSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  otherPlans?: ResearchPlanOtherPlans;

  @UI.label("18. Authentication of Key Biological and/or Chemical Resources")
  @UI.section(PHS398CareerDevelopmentSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  keyResourceAuthentication?: ResearchPlanKeyResourceAuthentication;

  // The XSD permits 100 records; the DAT and Forms I instructions cap applicants at 10.
  @UI.label("19. Appendix")
  @UI.section(PHS398CareerDevelopmentSection.appendix)
  @UI.widget(WidgetName.AttachmentArray)
  @maxItems(10)
  appendix?: ResearchPlanAppendixDocument[];

  @UI.label("20. Citizenship")
  @UI.section(PHS398CareerDevelopmentSection.citizenship)
  citizenship: QuestionCareerCandidateCitizenship;
}
