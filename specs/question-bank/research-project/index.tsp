import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

/** Reusable policy and supporting-document questions about a research project. */
namespace QuestionBank.ResearchProject;

/** The exact yes/no wire values used by the R&R Other Project Information source. */
enum ResearchProjectYesNoCode {
  yes: "Y: Yes",
  no: "N: No",
}

/** Federal human-subject exemption identifiers supported by the source form. */
enum HumanSubjectExemptionCode {
  exemption1: "E1",
  exemption2: "E2",
  exemption3: "E3",
  exemption4: "E4",
  exemption5: "E5",
  exemption6: "E6",
  exemption7: "E7",
  exemption8: "E8",
}

/** Human-subject protections and institutional review information for the project. */
@Question.meta(#{ id: "research-project/human-subjects" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
model QuestionHumanSubjects {
  /** Does the proposed project involve human subjects? */
  @UI.label("Does the proposed project involve human subjects?")
  involvesHumanSubjects: ResearchProjectYesNoCode;

  /** Is the project exempt from federal regulations governing human subjects research? */
  @UI.label("Is the project exempt from federal regulations?")
  @UI.visibleWhen(QuestionHumanSubjects.involvesHumanSubjects, ResearchProjectYesNoCode.yes)
  @Validation.requiredWhen(QuestionHumanSubjects.involvesHumanSubjects, ResearchProjectYesNoCode.yes)
  exemptFromFederalRegulations?: ResearchProjectYesNoCode;

  /** Select each federal human-subject exemption that applies. */
  @UI.label("Exemption Number(s)")
  @UI.visibleWhen(QuestionHumanSubjects.exemptFromFederalRegulations, ResearchProjectYesNoCode.yes)
  @minItems(1)
  @maxItems(8)
  exemptions?: HumanSubjectExemptionCode[];

  /** Is institutional review board review pending? */
  @UI.label("Is IRB review pending?")
  @UI.visibleWhen(QuestionHumanSubjects.exemptFromFederalRegulations, ResearchProjectYesNoCode.no)
  @Validation.requiredWhen(QuestionHumanSubjects.exemptFromFederalRegulations, ResearchProjectYesNoCode.no)
  irbReviewPending?: ResearchProjectYesNoCode;

  /** Enter the institutional review board approval date. */
  @UI.label("IRB Approval Date")
  @UI.visibleWhen(QuestionHumanSubjects.irbReviewPending, ResearchProjectYesNoCode.no)
  @Validation.requiredWhen(QuestionHumanSubjects.irbReviewPending, ResearchProjectYesNoCode.no)
  irbApprovalDate?: plainDate;

  /** Enter the human-subject assurance number. */
  @UI.label("Human Subject Assurance Number")
  @UI.visibleWhen(QuestionHumanSubjects.involvesHumanSubjects, ResearchProjectYesNoCode.yes)
  @minLength(1)
  @maxLength(10)
  assuranceNumber?: string;
}

/** Vertebrate-animal protections and institutional review information for the project. */
@Question.meta(#{ id: "research-project/vertebrate-animals" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
model QuestionVertebrateAnimals {
  /** Does the proposed project involve vertebrate animals? */
  @UI.label("Does the proposed project involve vertebrate animals?")
  involvesVertebrateAnimals: ResearchProjectYesNoCode;

  /** Is institutional animal care and use committee review pending? */
  @UI.label("Is IACUC review pending?")
  @UI.visibleWhen(QuestionVertebrateAnimals.involvesVertebrateAnimals, ResearchProjectYesNoCode.yes)
  @Validation.requiredWhen(QuestionVertebrateAnimals.involvesVertebrateAnimals, ResearchProjectYesNoCode.yes)
  iacucReviewPending?: ResearchProjectYesNoCode;

  /** Enter the institutional animal care and use committee approval date. */
  @UI.label("IACUC Approval Date")
  @UI.visibleWhen(QuestionVertebrateAnimals.iacucReviewPending, ResearchProjectYesNoCode.no)
  @Validation.requiredWhen(QuestionVertebrateAnimals.iacucReviewPending, ResearchProjectYesNoCode.no)
  iacucApprovalDate?: plainDate;

  /** Enter the animal welfare assurance number. */
  @UI.label("Animal Welfare Assurance Number")
  @UI.visibleWhen(QuestionVertebrateAnimals.iacucReviewPending, ResearchProjectYesNoCode.no)
  @Validation.requiredWhen(QuestionVertebrateAnimals.iacucReviewPending, ResearchProjectYesNoCode.no)
  @minLength(1)
  @maxLength(9)
  assuranceNumber?: string;
}

/** Whether the application includes proprietary or privileged information. */
@Question.meta(#{ id: "research-project/proprietary-information" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
model QuestionProprietaryInformation {
  /** Does the application include proprietary or privileged information? */
  @UI.label("Does the application include proprietary or privileged information?")
  includesProprietaryInformation: ResearchProjectYesNoCode;
}

/** Environmental impact and exemption information for the project. */
@Question.meta(#{ id: "research-project/environmental-impact" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
model QuestionEnvironmentalImpact {
  /** Does the proposed project have an actual or potential impact on the environment? */
  @UI.label("Does the project have an actual or potential environmental impact?")
  hasEnvironmentalImpact: ResearchProjectYesNoCode;

  /** Explain the actual or potential environmental impact. */
  @UI.label("Environmental Impact Explanation")
  @UI.visibleWhen(QuestionEnvironmentalImpact.hasEnvironmentalImpact, ResearchProjectYesNoCode.yes)
  @Validation.requiredWhen(QuestionEnvironmentalImpact.hasEnvironmentalImpact, ResearchProjectYesNoCode.yes)
  @minLength(1)
  @maxLength(55)
  environmentalImpactExplanation?: string;

  /** Has an environmental exemption been authorized or an environmental assessment approved? */
  @UI.label("Has an environmental exemption been authorized or an environmental assessment approved?")
  @UI.visibleWhen(QuestionEnvironmentalImpact.hasEnvironmentalImpact, ResearchProjectYesNoCode.yes)
  @Validation.requiredWhen(QuestionEnvironmentalImpact.hasEnvironmentalImpact, ResearchProjectYesNoCode.yes)
  hasEnvironmentalExemptionOrAssessment?: ResearchProjectYesNoCode;

  /** Explain the environmental exemption or approved environmental assessment. */
  @UI.label("Environmental Exemption or Assessment Explanation")
  @UI.visibleWhen(QuestionEnvironmentalImpact.hasEnvironmentalExemptionOrAssessment, ResearchProjectYesNoCode.yes)
  @Validation.requiredWhen(QuestionEnvironmentalImpact.hasEnvironmentalExemptionOrAssessment, ResearchProjectYesNoCode.yes)
  @minLength(1)
  @maxLength(55)
  environmentalExemptionOrAssessmentExplanation?: string;
}

/** Historic-place designation information for the project. */
@Question.meta(#{ id: "research-project/historic-designation" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
model QuestionHistoricDesignation {
  /** Is the research performance site designated, or eligible to be designated, as a historic place? */
  @UI.label("Is the research performance site designated or eligible as a historic place?")
  hasHistoricDesignation: ResearchProjectYesNoCode;

  /** Explain the historic-place designation. */
  @UI.label("Historic Place Explanation")
  @UI.visibleWhen(QuestionHistoricDesignation.hasHistoricDesignation, ResearchProjectYesNoCode.yes)
  @Validation.requiredWhen(QuestionHistoricDesignation.hasHistoricDesignation, ResearchProjectYesNoCode.yes)
  @minLength(1)
  @maxLength(55)
  explanation?: string;
}

/** International activities and partnerships involved in the project. */
@Question.meta(#{ id: "research-project/international-activities" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
model QuestionInternationalActivities {
  /** Does the project involve activities outside the United States or partnerships with international collaborators? */
  @UI.label("Does the project involve international activities or partnerships?")
  involvesInternationalActivities: ResearchProjectYesNoCode;

  /** Identify the countries involved in the international activities or partnerships. */
  @UI.label("Countries Involved")
  @UI.visibleWhen(QuestionInternationalActivities.involvesInternationalActivities, ResearchProjectYesNoCode.yes)
  @Validation.requiredWhen(QuestionInternationalActivities.involvesInternationalActivities, ResearchProjectYesNoCode.yes)
  @minLength(1)
  @maxLength(55)
  countries?: string;

  /** Explain the international activities or partnerships. */
  @UI.label("International Activities Explanation")
  @minLength(1)
  @maxLength(55)
  explanation?: string;
}

/** Provide the project summary or abstract requested by the funding opportunity. */
@Question.meta(#{ id: "project/summary-abstract-document" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ProjectSummaryAbstractDocument extends AttachmentRef;

/** Provide the bibliography and references cited for the project. */
@Question.meta(#{ id: "project/bibliography-references" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.attachment)
scalar ProjectBibliographyReferences extends AttachmentRef;

/** Describe the facilities and other resources available to the project. */
@Question.meta(#{ id: "project/facilities-resources" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.attachment)
scalar ProjectFacilitiesResources extends AttachmentRef;

/** Describe the equipment available to the project. */
@Question.meta(#{ id: "project/equipment" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.attachment)
scalar ProjectEquipment extends AttachmentRef;

/** Provide another supporting document requested for the project. */
@Question.meta(#{ id: "project/other-supporting-document" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.attachment)
scalar ProjectOtherSupportingDocument extends AttachmentRef;
