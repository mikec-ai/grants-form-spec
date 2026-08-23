import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace QuestionBank.LobbyingDisclosure;

/** The paper-form sections used by the SF-LLL disclosure family. */
enum SflllSection {
  federalActionType: "1. Type of Federal Action",
  federalActionStatus: "2. Status of Federal Action",
  reportType: "3. Report Type",
  reportingEntity: "4. Name and Address of Reporting Entity",
  primeEntity: "5. If Reporting Entity in No. 4 is Subawardee, Enter Name and Address of Prime",
  federalAgency: "6. Federal Department / Agency",
  federalProgram: "7. Federal Program Name / Description",
  federalActionNumber: "8. Federal Action Number",
  awardAmount: "9. Award Amount",
  registrant: "10a. Name and Address of Lobbying Registrant",
  lobbyingIndividuals: "10b. Individuals Performing Services",
  certification: "11. Certification and Signature",
}

enum FederalActionType {
  contract: "Contract",
  grant: "Grant",
  cooperativeAgreement: "CoopAgree",
  loan: "Loan",
  loanGuarantee: "LoanGuarantee",
  loanInsurance: "LoanInsurance",
}

enum FederalActionStatus {
  bidOfferApplication: "BidOffer",
  initialAward: "InitialAward",
  postAward: "PostAward",
}

enum LobbyingReportType {
  materialChange: "MaterialChange",
  initialFiling: "InitialFiling",
}

enum ReportingEntityType {
  subAwardee: "SubAwardee",
  prime: "Prime",
}

enum MaterialChangeQuarter {
  first: "1",
  second: "2",
  third: "3",
  fourth: "4",
}

/** A four-digit year in which a material change occurred. */
@pattern("^[1-9][0-9]{3}$")
scalar MaterialChangeYear extends string;

model MaterialChangeDetails {
  @UI.label("Material Change Year")
  year: MaterialChangeYear;

  @UI.label("Material Change Quarter")
  quarter: MaterialChangeQuarter;

  @UI.label("Date of Last Report")
  lastReportDate: plainDate;
}

/** Classify the covered Federal action, filing, and reporting entity for a lobbying disclosure. */
@Question.meta(#{ id: "federal-action/disclosure-filing-details" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details, TagName.role)
model QuestionLobbyingDisclosureFilingDetails {
  /** Identify the type of covered Federal action influenced by the lobbying activity. */
  @UI.label("Type of Federal Action")
  @UI.section(SflllSection.federalActionType)
  federalActionType: FederalActionType = FederalActionType.grant;

  /** Identify the status of the covered Federal action. */
  @UI.label("Status of Federal Action")
  @UI.section(SflllSection.federalActionStatus)
  federalActionStatus: FederalActionStatus = FederalActionStatus.initialAward;

  /** Identify whether this is an initial filing or a report of a material change. */
  @UI.label("Report Type")
  @UI.section(SflllSection.reportType)
  reportType: LobbyingReportType = LobbyingReportType.initialFiling;

  @UI.label("Material Change Details")
  @UI.section(SflllSection.reportType)
  @UI.visibleWhen(QuestionLobbyingDisclosureFilingDetails.reportType, LobbyingReportType.materialChange)
  @Validation.requiredWhen(QuestionLobbyingDisclosureFilingDetails.reportType, LobbyingReportType.materialChange)
  materialChange?: MaterialChangeDetails;

  /** Select Prime when filing for the direct award or Subawardee when filing below it. */
  @UI.label("Entity Type")
  @UI.section(SflllSection.reportingEntity)
  reportingEntityType: ReportingEntityType = ReportingEntityType.prime;

  @UI.label("Tier")
  @UI.section(SflllSection.reportingEntity)
  @UI.visibleWhen(QuestionLobbyingDisclosureFilingDetails.reportingEntityType, ReportingEntityType.subAwardee)
  @minValue(0)
  @maxValue(99)
  tier?: int32;
}

/** Enter a domestic address in the exact shape accepted by the SF-LLL disclosure family. */
@Question.meta(#{ id: "generics/domestic-address" })
@Catalog.entity(EntityName.generic)
@Catalog.tag(TagName.address)
model QuestionLobbyingDomesticAddress {
  @UI.label("Street 1")
  @minLength(1)
  @maxLength(55)
  street1: string;

  @UI.label("Street 2")
  @minLength(1)
  @maxLength(55)
  street2?: string;

  @UI.label("City")
  @minLength(1)
  @maxLength(35)
  city: string;

  @UI.label("State")
  state?: StateCode;

  @UI.label("Zip / Postal Code")
  @minLength(1)
  @maxLength(30)
  zipCode?: string;
}

/** Enter the identifying number assigned to the covered Federal action. */
@Question.meta(#{ id: "federal-action/number" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@minLength(1)
@maxLength(110)
scalar LobbyingFederalActionNumber extends string;

/** Enter the amount of the covered Federal award. */
@Question.meta(#{ id: "federal-action/award-amount" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.money)
@pattern("^(?:\\d{1,15}|\\d{1,14}[.]\\d|\\d{1,13}[.]\\d{2})$")
@minLength(1)
@maxLength(16)
scalar LobbyingAwardAmount extends string;
