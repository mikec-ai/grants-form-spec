import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace QuestionBank.Nifa;

/** Additional applicant category used by NIFA Supplemental Information. */
enum NifaAdditionalApplicantType {
  usdaAgency: "USDA Agency",
  otherFederalAgency: "Other Federal Agency",
  landGrant1862: "1862 Land-Grant University",
  landGrant1890: "1890 Land-Grant University (including Tuskegee University & West Virginia State University)",
  landGrant1994: "1994 Land-Grant University",
  other: "Other",
}

/** Identify the NIFA program to which the applicant is applying. */
@Question.meta(#{ id: "nifa/program" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier, TagName.title)
model QuestionNifaProgram {
  /** Enter the NIFA program name. */
  @UI.label("Program Code Name")
  @minLength(1)
  @maxLength(80)
  programCodeName: string;

  /** Enter the NIFA program code. */
  @UI.label("Program Code")
  @minLength(1)
  @maxLength(5)
  programCode: string;
}

/** Select an additional applicant category when the primary applicant type permits it. */
@Question.meta(#{ id: "nifa/additional-applicant-type" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization, TagName.role)
model QuestionNifaAdditionalApplicantType {
  @UI.label("Additional Applicant Type")
  @UI.widget(WidgetName.Select)
  additionalApplicantType: NifaAdditionalApplicantType;
}

/** Report the NIFA-specific institutional classifications that apply to the applicant. */
@Question.meta(#{ id: "nifa/supplemental-applicant-classifications" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization, TagName.role)
model QuestionNifaSupplementalApplicantTypes {
  @UI.label("Alaska Native-Serving Institution")
  @UI.widget(WidgetName.Checkbox)
  alaskaNativeServingInstitution?: boolean;

  @UI.label("Cooperative Extension Service")
  @UI.widget(WidgetName.Checkbox)
  cooperativeExtensionService?: boolean;

  @UI.label("Hispanic-Serving Institution")
  @UI.widget(WidgetName.Checkbox)
  hispanicServingInstitution?: boolean;

  @UI.label("Historically Black College or University (other than 1890)")
  @UI.widget(WidgetName.Checkbox)
  historicallyBlackCollegeOrUniversity?: boolean;

  @UI.label("Minority-Serving Institution")
  @UI.widget(WidgetName.Checkbox)
  minorityServingInstitution?: boolean;

  @UI.label("Native Hawaiian-Serving Institution")
  @UI.widget(WidgetName.Checkbox)
  nativeHawaiianServingInstitution?: boolean;

  @UI.label("Public Nonprofit Junior or Community College")
  @UI.widget(WidgetName.Checkbox)
  publicNonprofitJuniorOrCommunityCollege?: boolean;

  @UI.label("Public Secondary School")
  @UI.widget(WidgetName.Checkbox)
  publicSecondarySchool?: boolean;

  @UI.label("School of Forestry")
  @UI.widget(WidgetName.Checkbox)
  schoolOfForestry?: boolean;

  @UI.label("State Agricultural Experiment Station")
  @UI.widget(WidgetName.Checkbox)
  stateAgriculturalExperimentStation?: boolean;

  @UI.label("Tribal College (other than 1994)")
  @UI.widget(WidgetName.Checkbox)
  tribalCollege?: boolean;

  @UI.label("Veterinary School or College")
  @UI.widget(WidgetName.Checkbox)
  veterinarySchoolOrCollege?: boolean;
}

/** Identify the applicant's Automated Standard Application for Payments status. */
@Question.meta(#{ id: "nifa/asap-recipient-information" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization, TagName.identifier)
model QuestionNifaAsapRecipientInformation {
  /** Report whether the legal applicant has an active ASAP recipient identifier for NIFA awards. */
  @UI.label("Does the legal applicant have an active Automated Standard Application for Payments (ASAP) Recipient Identification Number for NIFA awards?")
  @UI.widget(WidgetName.Radio)
  hasActiveAsapRecipientId: boolean;

  /** Enter the ASAP recipient identifier corresponding to this application's organization identifiers. */
  @UI.label("ASAP Recipient ID")
  @UI.visibleWhen(QuestionNifaAsapRecipientInformation.hasActiveAsapRecipientId, true)
  @Validation.requiredWhen(QuestionNifaAsapRecipientInformation.hasActiveAsapRecipientId, true)
  @minLength(1)
  @maxLength(8)
  recipientId?: string;
}

/** Enter keywords that describe this NIFA application. */
@Question.meta(#{ id: "nifa/application-keywords" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
@minLength(1)
@maxLength(100)
scalar NifaApplicationKeywords extends string;

/** Attach the conflict-of-interest list requested by NIFA. */
@Question.meta(#{ id: "nifa/conflict-of-interest-list" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.attachment)
scalar NifaConflictOfInterestList extends AttachmentRef;
