import "@simpler-grants/form-spec";
import "../index.tsp";
import "../aor/index.tsp";
import "../generics/index.tsp";
import "../primary-org/index.tsp";

using SimplerForms;
using QuestionBank.Aor;
using QuestionBank.Generics;
using QuestionBank.PrimaryOrg;

/** Reusable questions introduced by the Research and Related application cover forms. */
namespace QuestionBank.ResearchApplication;

/** Exact R&R submission vocabulary shared by the standalone and Multi-Project covers. */
enum ResearchSubmissionType {
  preapplication: "Preapplication",
  application: "Application",
  changedCorrected: "Change/Corrected Application",
}

/** R&R application lifecycle vocabulary. */
enum ResearchApplicationTypeCode {
  new: "New",
  resubmission: "Resubmission",
  renewal: "Renewal",
  continuation: "Continuation",
  revision: "Revision",
}

/** R&R's encoded revision choices. */
enum ResearchRevisionCode {
  A: "A",
  B: "B",
  C: "C",
  D: "D",
  E: "E",
  AC: "AC",
  AD: "AD",
  BC: "BC",
  BD: "BD",
}

enum YesNoCode {
  yes: "Y: Yes",
  no: "N: No",
}

enum ResearchStateReviewCode {
  yes: "Y: Yes",
  notCovered: "Program is not covered by E.O. 12372",
  notSelected: "Program has not been selected by state for review",
}

/** Select the kind of R&R submission being made. */
@Question.meta(#{ id: "research-application/submission-type" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionResearchSubmissionType {
  @UI.label("Type of Submission")
  submissionTypeCode?: ResearchSubmissionType;
}

/** Enter the applicant's control number for an R&R application, if applicable. */
@Question.meta(#{ id: "research-application/applicant-control-identifier" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@minLength(1)
@maxLength(30)
scalar ResearchApplicantControlIdentifier extends string;

/** Enter the previously assigned Federal identifier for an R&R application. */
@Question.meta(#{ id: "research-application/previous-federal-award-identifier" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@minLength(1)
@maxLength(30)
scalar ResearchFederalAwardIdentifier extends string;

model QuestionResearchSmallBusinessType {
  @UI.label("Socially and Economically Disadvantaged")
  sociallyEconomicallyDisadvantaged?: string;

  @UI.label("Women Owned")
  womenOwned?: string;
}

/** Identify the applicant category and any R&R small-business characteristics. */
@Question.meta(#{ id: "primary-org/research-applicant-type" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization, TagName.role)
model QuestionResearchApplicantType {
  @UI.label("Applicant Type")
  applicantTypeCode?: ApplicantTypeCode;

  @UI.label("Other Applicant Type Explanation")
  @minLength(1)
  @maxLength(50)
  applicantTypeCodeOtherExplanation?: string;

  @UI.label("Small Business Organization Type")
  smallBusinessOrganizationType?: QuestionResearchSmallBusinessType;
}

/** Describe the R&R application lifecycle, revision, and other-agency submission. */
@Question.meta(#{ id: "research-application/application-type" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionResearchApplicationType {
  @UI.label("Application Type")
  applicationTypeCode?: ResearchApplicationTypeCode;

  @UI.label("Is this application being submitted to another agency?")
  isOtherAgencySubmission?: YesNoCode;

  @UI.label("Other Agency Submission Explanation")
  @minLength(1)
  @maxLength(20)
  otherAgencySubmissionExplanation?: string;

  @UI.label("Revision Code")
  @UI.encodedCheckboxGroup(#{
    choices: #[
      #{ code: "A", label: "A. Increase Award" },
      #{ code: "B", label: "B. Decrease Award" },
      #{ code: "C", label: "C. Increase Duration" },
      #{ code: "D", label: "D. Decrease Duration" },
      #{ code: "E", label: "E. Other" },
    ],
    combinations: #[
      #{ value: "A", members: #["A"] },
      #{ value: "B", members: #["B"] },
      #{ value: "C", members: #["C"] },
      #{ value: "D", members: #["D"] },
      #{ value: "E", members: #["E"] },
      #{ value: "AC", members: #["A", "C"] },
      #{ value: "AD", members: #["A", "D"] },
      #{ value: "BC", members: #["B", "C"] },
      #{ value: "BD", members: #["B", "D"] },
    ],
  })
  revisionCode?: ResearchRevisionCode;

  @UI.label("Other Revision Explanation")
  @minLength(1)
  @maxLength(45)
  revisionCodeOtherExplanation?: string;
}

/** Enter estimated funding for the complete R&R project period. */
@Question.meta(#{ id: "research-application/estimated-project-funding" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.money)
model QuestionResearchEstimatedFunding {
  @UI.label("Total Federal Funds Requested")
  @minValue(0)
  @maxValue(9999999999999.99)
  totalEstimatedAmount?: float64;

  @UI.label("Total Non-Federal Funds")
  @minValue(0)
  @maxValue(9999999999999.99)
  totalNonFederalRequested?: float64;

  @UI.label("Total Federal and Non-Federal Funds")
  @minValue(0)
  @maxValue(9999999999999.99)
  totalFederalNonFederalRequested?: float64;

  @UI.label("Estimated Program Income")
  @minValue(0)
  @maxValue(9999999999999.99)
  estimatedProgramIncome?: float64;
}

/** Record whether and when the R&R application was submitted for State review. */
@Question.meta(#{ id: "research-application/state-review" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details, TagName.date)
model QuestionResearchStateReview {
  @UI.label("State Review")
  stateReviewCodeType?: ResearchStateReviewCode;

  @UI.label("State Review Date")
  stateReviewDate?: plainDate;
}

/** The applicant organization information required by an R&R cover form. */
model ResearchApplicantOrganization {
  /** Enter the applicant organization's legal name. */
  @UI.label("Organization Name")
  organizationName?: LegalName;

  /** Enter the applicant organization's address. */
  @UI.label("Address")
  address?: QuestionAddress;

  /** Enter the department. */
  @UI.label("Department")
  @minLength(1)
  @maxLength(100)
  department?: string;

  /** Enter the division. */
  @UI.label("Division")
  @minLength(1)
  @maxLength(100)
  division?: string;

  /** The applicant organization's Unique Entity Identifier. */
  @UI.label("SAM UEI")
  samUei?: SamUei;

  // The XSD contains this second EIN leaf, but the reviewed XFA has no binding for it. The
  // top-level Employer ID is the applicant-facing answer, so preserve this source leaf without
  // rendering a duplicate question.
  @UI.omit
  @minLength(9)
  @maxLength(30)
  employerId?: string;
}

/** The person to contact about the Research and Related application. */
model ResearchApplicationContact {
  /** Enter the contact person's name. */
  @UI.label("Name")
  name?: QuestionPersonName;

  /** Enter the contact person's address. */
  @UI.label("Address")
  address?: QuestionAddress;

  /** Enter the contact person's title. */
  @UI.label("Title")
  title?: ContactTitle;

  /** Enter the daytime telephone number. */
  @UI.label("Telephone Number")
  phone?: PhoneNumber;

  /** Enter the fax number. */
  @UI.label("Fax Number")
  fax?: PhoneNumber;

  /** Enter a valid email address. */
  @UI.label("Email")
  email?: EmailAddress;
}

/** Applicant organization and application-contact information. */
@Question.meta(#{ id: "research-application/applicant" })
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization, TagName.person, TagName.details)
model QuestionResearchApplicant {
  /** Enter the applicant organization information. */
  @UI.label("Organization Information")
  organizationInfo?: ResearchApplicantOrganization;

  /** Enter the contact person for this application. */
  @UI.label("Contact Person Information")
  contactPersonInfo?: ResearchApplicationContact;
}

/** The project director or principal investigator named on the application. */
@Question.meta(#{ id: "research-application/principal-investigator" })
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.details)
model QuestionPrincipalInvestigator {
  /** Enter the project director or principal investigator's name. */
  @UI.label("Name")
  name?: QuestionPersonName;

  /** Enter the position title. */
  @UI.label("Position / Title")
  title?: ContactTitle;

  /** Enter the organization name. */
  @UI.label("Organization Name")
  organizationName?: OrganizationName;

  /** Enter the department. */
  @UI.label("Department")
  @minLength(1)
  @maxLength(100)
  department?: string;

  /** Enter the division. */
  @UI.label("Division")
  @minLength(1)
  @maxLength(100)
  division?: string;

  /** Enter the address. */
  @UI.label("Address")
  address?: QuestionAddress;

  /** Enter the daytime telephone number. */
  @UI.label("Telephone Number")
  phone?: PhoneNumber;

  /** Enter the fax number. */
  @UI.label("Fax Number")
  fax?: PhoneNumber;

  /** Enter a valid email address. */
  @UI.label("Email")
  email?: EmailAddress;
}

/** The representative authorized to submit the Research and Related application. */
@Question.meta(#{ id: "research-application/authorized-representative" })
@Catalog.entity(EntityName.authorizedRepresentative)
@Catalog.tag(TagName.person, TagName.details)
model QuestionResearchAuthorizedRepresentative {
  /** Enter the authorized representative's name. */
  @UI.label("Name")
  name?: QuestionAorName;

  /** Enter the position title. */
  @UI.label("Position / Title")
  title?: AorTitle;

  /** Enter the organization name. */
  @UI.label("Organization Name")
  organizationName?: OrganizationName;

  /** Enter the department. */
  @UI.label("Department")
  @minLength(1)
  @maxLength(100)
  department?: string;

  /** Enter the division. */
  @UI.label("Division")
  @minLength(1)
  @maxLength(100)
  division?: string;

  /** Enter the address. */
  @UI.label("Address")
  address?: QuestionAddress;

  /** Enter the daytime telephone number. */
  @UI.label("Telephone Number")
  phone?: AorPhone;

  /** Enter the fax number. */
  @UI.label("Fax Number")
  fax?: AorFax;

  /** Enter a valid email address. */
  @UI.label("Email")
  email?: AorEmail;
}

/** Attach the lobbying disclosure associated with this application, when required. */
@Question.meta(#{ id: "application/disclosure-document" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.attachment)
scalar ResearchLobbyingDisclosure extends AttachmentRef;

/** Attach the pre-application associated with this application, when required. */
@Question.meta(#{ id: "application/pre-application-document" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.attachment)
scalar ResearchPreApplication extends AttachmentRef;

/** Attach an optional cover letter for this application. */
@Question.meta(#{ id: "application/cover-letter" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.attachment)
scalar ResearchCoverLetter extends AttachmentRef;
