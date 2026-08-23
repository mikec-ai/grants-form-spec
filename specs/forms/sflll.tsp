import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/generics/index.tsp";
import "../question-bank/lobbying-disclosure/index.tsp";
import "../question-bank/opportunity/index.tsp";
import "../question-bank/project/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.LobbyingDisclosure;
using QuestionBank.Opportunity;
using QuestionBank.Project;

namespace Forms.Sflll;

// SF-LLL's XSD intentionally carries a domestic address shape rather than the broader
// generic address (no country, county, or province). One local declaration is reused by
// each role without claiming that the roles themselves are interchangeable.
model SflllReportingOrganization {
  @UI.label("Organization Name")
  organizationName: OrganizationName;

  @UI.label("Address")
  address: QuestionLobbyingDomesticAddress;

  @UI.label("Congressional District")
  congressionalDistrict?: CongressionalDistrict;
}

model FederalProgramDetails {
  @UI.label("Federal Program Name / Description")
  name?: AssistanceListingTitle;

  @UI.label("Assistance Listing Number")
  assistanceListingNumber?: AssistanceListingNumber;
}

model LobbyingRegistrant {
  @UI.label("Individual Name")
  @Validation.requiredPaths("firstName", "lastName")
  name: QuestionPersonName;

  @UI.label("Address")
  address?: QuestionLobbyingDomesticAddress;
}

@UI.label("Individual")
model LobbyingServiceIndividual {
  @UI.label("Name")
  @Validation.requiredPaths("firstName", "lastName")
  name: QuestionPersonName;

  @UI.label("Address")
  address?: QuestionLobbyingDomesticAddress;
}

model SflllSignatureBlock {
  @UI.label("Name")
  @Validation.requiredPaths("firstName", "lastName")
  name: QuestionPersonName;

  @UI.label("Title")
  title?: ContactTitle;

  @UI.label("Telephone Number")
  phone?: PhoneNumber;

  /** Completed by Grants.gov upon submission. */
  @UI.label("Date Signed")
  @UI.readOnly
  signedDate?: SubmittedDate;

  /** Completed by Grants.gov upon submission. */
  @UI.label("Signature")
  @UI.readOnly
  signature?: Signature;
}

/** Disclosure of Lobbying Activities (SF-LLL), Grants.gov version 2.0. */
@Form.meta(#{
  id: "sflll",
  legacyFormId: 670,
  formName: "Disclosure of Lobbying Activities (SF-LLL)",
  shortFormName: "SFLLL_2_0",
  formVersion: "2.0",
  agencyCode: "SGG",
  ombNumber: "4040-0013",
})
@UI.sections(SflllSection)
@Sgg.prePopulate(#{
  `federalAgencyDepartment`: SggPrePop.agencyName,
  `federalProgram.assistanceListingNumber`: SggPrePop.assistanceListingNumber,
  `federalProgram.name`: SggPrePop.assistanceListingProgramTitle,
})
model Sflll extends QuestionLobbyingDisclosureFilingDetails {

  @UI.label("Reporting Entity")
  @UI.section(SflllSection.reportingEntity)
  reportingOrganization: SflllReportingOrganization;

  @UI.label("Prime Awardee")
  @UI.section(SflllSection.primeEntity)
  @UI.visibleWhen(Sflll.reportingEntityType, ReportingEntityType.subAwardee)
  @Validation.requiredWhen(Sflll.reportingEntityType, ReportingEntityType.subAwardee)
  primeOrganization?: SflllReportingOrganization;

  /** Enter the Federal department or agency making the covered award. */
  @UI.label("Federal Department / Agency")
  @UI.section(SflllSection.federalAgency)
  @Validation.constraints(#{ maxLength: 40 })
  federalAgencyDepartment: AgencyName;

  @UI.label("Federal Program")
  @UI.section(SflllSection.federalProgram)
  federalProgram?: FederalProgramDetails;

  @UI.label("Federal Action Number")
  @UI.section(SflllSection.federalActionNumber)
  federalActionNumber?: LobbyingFederalActionNumber;

  @UI.label("Award Amount")
  @UI.section(SflllSection.awardAmount)
  awardAmount?: LobbyingAwardAmount;

  @UI.label("Lobbying Registrant")
  @UI.section(SflllSection.registrant)
  lobbyingRegistrant: LobbyingRegistrant;

  @UI.label("Individuals Performing Services")
  @UI.section(SflllSection.lobbyingIndividuals)
  @Sgg.fieldList(#{ validateBeforeAdd: true })
  @minItems(1)
  @maxItems(10)
  individualsPerformingServices: LobbyingServiceIndividual[];

  /** Information supplied constitutes a material representation of fact upon which reliance was placed when the transaction was made or entered into. This disclosure is required by 31 U.S.C. 1352 and will be reported to Congress semi-annually. */
  @UI.label("Certification and Signature")
  @UI.section(SflllSection.certification)
  signatureBlock: SflllSignatureBlock;
}
