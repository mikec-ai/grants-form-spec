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
