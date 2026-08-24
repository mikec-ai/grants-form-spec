import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace QuestionBank.PrimaryOrg;

/** Enter the applicant organization's website, if applicable. */
@Question.meta(#{ id: "primary-org/website" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization, TagName.details)
@UI.label("Web Address")
@format("uri-reference")
@minLength(1)
scalar PrimaryOrgWebsite extends string;

/** Enter the legal name of the applicant that will undertake the assistance activity. */
@Question.meta(#{ id: "primary-org/legal-name" })
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization, TagName.name)
@UI.label("Legal Name")
scalar LegalName extends OrganizationName;

/** Enter the address of the applicant. */
@Question.meta(#{ id: "primary-org/address" })
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.address)
@UI.label("Address")
@Validation.requiredPaths("street1", "city", "country")
@Validation.requiredPathWhen("state", "country", CountryCode.USA)
@Validation.requiredPathWhen("zipCode", "country", CountryCode.USA)
model QuestionPrimaryOrgAddress extends QuestionAddress {}

/** UEI of the applicant organization. */
@Question.meta(#{ id: "primary-org/uei" })
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.identifier, TagName.organization)
@UI.label("SAM UEI")
@minLength(12)
@maxLength(12)
scalar SamUei extends string;

/** Enter either TIN or EIN as assigned by the Internal Revenue Service. */
@Question.meta(#{ id: "primary-org/ein" })
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.identifier, TagName.organization)
@UI.label("EIN/TIN")
@minLength(9)
@maxLength(30)
scalar EmployerIdentificationNumber extends string;

/** Identify the applicant organizational unit undertaking the assistance activity. */
@Question.meta(#{ id: "primary-org/organizational-unit" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization, TagName.name)
model QuestionOrganizationalUnit {
  /** Enter the name of primary organizational department, service, laboratory, or equivalent level within the organization which will undertake the assistance activity. */
  @UI.label("Department Name")
  @minLength(1)
  @maxLength(30)
  departmentName?: string;

  /** Enter the name of primary organizational division, office, or major subdivision which will undertake the assistance activity. */
  @UI.label("Division Name")
  @minLength(1)
  @maxLength(100)
  divisionName?: string;
}

// Both SF-424 and SF-424-Short ask this with the same twenty-four codes and the same
// cardinality. The list is shared; the wording and the "other" box stay with each form,
// because the forms word them differently.
@summary("Type of Applicant")
@doc("The applicant's category, from the Executive Order 12372 list.")
enum ApplicantTypeCode {
  A: "A: State Government",
  B: "B: County Government",
  C: "C: City or Township Government",
  D: "D: Special District Government",
  E: "E: Regional Organization",
  F: "F: U.S. Territory or Possession",
  G: "G: Independent School District",
  H: "H: Public/state Controlled Institution of Higher Education",
  I: "I: Indian/Native American Tribal Government (Federally Recognized)",
  J: "J: Indian/Native American Tribal Government (Other than Federally Recognized)",
  K: "K: Indian/Native American Tribally Designated Organization",
  L: "L: Public/Indian Housing Authority",
  M: "M: Nonprofit with 501C3 IRS Status (Other than Institution of Higher Education)",
  N: "N: Nonprofit without 501C3 IRS Status (Other than Institution of Higher Education)",
  O: "O: Private Institution of Higher Education",
  P: "P: Individual",
  Q: "Q: For-Profit Organization (Other than Small Business)",
  R: "R: Small Business",
  S: "S: Hispanic-serving Institution",
  T: "T: Historically Black Colleges and Universities (HBCUs)",
  U: "U: Tribally Controlled Colleges and Universities (TCCUs)",
  V: "V: Alaska Native and Native Hawaiian Serving Institutions",
  W: "W: Non-domestic (non-US) Entity",
  X: "X: Other (specify)",
}

/** Select the applicant's single primary category. */
@Question.meta(#{ id: "primary-org/applicant-type-code" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization, TagName.role)
model QuestionApplicantTypeCode {
  @UI.label("Type of Applicant")
  applicantTypeCode: ApplicantTypeCode;
}

// The answer is a list, so the question is the list: one to three codes, which is what both
// forms asking it require. Each form supplies its own wording for *how* to choose.
/** The applicant's category or categories. */
@Question.meta(#{ id: "primary-org/applicant-type" })
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization, TagName.role)
@UI.label("Type of Applicant")
@minItems(1)
@maxItems(3)
model ApplicantTypes is ApplicantTypeCode[];

/** Enter the applicant type here if you selected "Other (specify)" for Type of applicant. */
@Question.meta(#{ id: "primary-org/applicant-type-other" })
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization, TagName.role)
@UI.label("Type of Applicant Other Explanation")
@minLength(0)
@maxLength(30)
scalar ApplicantTypeOther extends string;
