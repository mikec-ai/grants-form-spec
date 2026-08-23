import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/research-plan/index.tsp";

using SimplerForms;
using QuestionBank.ResearchPlan;

namespace Forms.PHS398ResearchPlan;

enum PHS398ResearchPlanSection {
  introduction: "Introduction",
  researchPlan: "Research Plan Section",
  otherResearchPlan: "Other Research Plan Section",
  appendix: "Appendix",
}

/** PHS 398 Research Plan, Grants.gov FID 797, version 5.0. */
@Form.meta(#{
  id: "phs398-research-plan",
  legacyFormId: 797,
  formName: "PHS 398 Research Plan",
  shortFormName: "PHS398_ResearchPlan_5_0",
  formVersion: "5.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "0925-0001",
})
@UI.sections(PHS398ResearchPlanSection)
model PHS398ResearchPlan {
  // Applicability depends on R&R SF-424 application type. The source-bound cross-form
  // condition is retained in the instruction evidence until application-level conditions
  // have a portable contract; no local response path is fabricated here.
  @UI.label("1. Introduction to Application (for Resubmission and Revision applications)")
  @UI.section(PHS398ResearchPlanSection.introduction)
  @UI.widget(WidgetName.Attachment)
  introduction?: ResearchPlanIntroduction;

  @UI.label("2. Specific Aims")
  @UI.section(PHS398ResearchPlanSection.researchPlan)
  @UI.widget(WidgetName.Attachment)
  specificAims?: ResearchPlanSpecificAims;

  @UI.label("3. Research Strategy")
  @UI.section(PHS398ResearchPlanSection.researchPlan)
  @UI.widget(WidgetName.Attachment)
  researchStrategy: ResearchPlanStrategy;

  // The NIH guide requires this for Renewal applications. That is an application-level
  // cross-form condition and remains source-bound outside this standalone form schema.
  @UI.label("4. Progress Report Publication List")
  @UI.section(PHS398ResearchPlanSection.researchPlan)
  @UI.widget(WidgetName.Attachment)
  progressReportPublicationList?: ResearchPlanProgressReportPublicationList;

  // This document is conditionally required from the R&R Other Project Information answer.
  // It is distinct from that form's yes/no vertebrate-animal policy question.
  @UI.label("5. Vertebrate Animals")
  @UI.section(PHS398ResearchPlanSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  vertebrateAnimals?: ResearchPlanVertebrateAnimalsDocument;

  @UI.label("6. Select Agent Research")
  @UI.section(PHS398ResearchPlanSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  selectAgentResearch?: ResearchPlanSelectAgentResearch;

  @UI.label("7. Multiple PD/PI Leadership Plan")
  @UI.section(PHS398ResearchPlanSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  multiplePdPiLeadershipPlan?: ResearchPlanMultiplePdPiLeadershipPlan;

  @UI.label("8. Consortium/Contractual Arrangements")
  @UI.section(PHS398ResearchPlanSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  consortiumContractualArrangements?: ResearchPlanConsortiumContractualArrangements;

  @UI.label("9. Letters of Support")
  @UI.section(PHS398ResearchPlanSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  lettersOfSupport?: ResearchPlanLettersOfSupport;

  @UI.label("10. Resource Sharing Plan(s)")
  @UI.section(PHS398ResearchPlanSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  resourceSharingPlans?: ResearchPlanResourceSharingPlans;

  @UI.label("11. Other Plan(s)")
  @UI.section(PHS398ResearchPlanSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  otherPlans?: ResearchPlanOtherPlans;

  @UI.label("12. Authentication of Key Biological and/or Chemical Resources")
  @UI.section(PHS398ResearchPlanSection.otherResearchPlan)
  @UI.widget(WidgetName.Attachment)
  keyResourceAuthentication?: ResearchPlanKeyResourceAuthentication;

  // The XSD container permits 100 records. The current NIH Forms I instructions and DAT
  // cap applicant submission at 10 PDF files, so the portable applicant contract is narrower.
  @UI.label("13. Appendix")
  @UI.section(PHS398ResearchPlanSection.appendix)
  @UI.widget(WidgetName.AttachmentArray)
  @maxItems(10)
  appendix?: ResearchPlanAppendixDocument[];
}
