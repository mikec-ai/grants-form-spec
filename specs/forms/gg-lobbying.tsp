import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/aor/index.tsp";
import "../question-bank/primary-org/index.tsp";

using SimplerForms;
using QuestionBank.Aor;
using QuestionBank.PrimaryOrg;

namespace Forms.GgLobbying;

/** The numbered sections of Grants.gov Lobbying Form v1.1. */
enum GgLobbyingSection {
  /** The undersigned certifies, to the best of his or her knowledge and belief, that:

(1) No Federal appropriated funds have been paid or will be paid, by or on behalf of the undersigned, to any person for influencing or attempting to influence an officer or employee of an agency, a Member of Congress, an officer or employee of Congress, or an employee of a Member of Congress in connection with the awarding of any Federal contract, the making of any Federal grant, the making of any Federal loan, the entering into of any cooperative agreement, and the extension, continuation, renewal, amendment, or modification of any Federal contract, grant, loan, or cooperative agreement

(2) If any funds other than Federal appropriated funds have been paid or will be paid to any person for influencing or attempting to influence an officer or employee of any agency, a Member of Congress, an officer or employee of Congress, or an employee of a Member of Congress in connection with this Federal contract, grant, loan, or cooperative agreement, the undersigned shall complete and submit Standard Form-LLL, ''Disclosure of Lobbying Activities,'' in accordance with its instructions.

(3) The undersigned shall require that the language of this certification be included in the award documents for all subawards at all tiers (including subcontracts, subgrants, and contracts under grants, loans, and cooperative agreements) and that all subrecipients shall certify and disclose accordingly. This certification is a material representation of fact upon which reliance was placed when this transaction was made or entered into. Submission of this certification is a prerequisite for making or entering into this transaction imposed by section 1352, title 31, U.S. Code. Any person who fails to file the required certification shall be subject to a civil penalty of not less than $10,000 and not more than $100,000 for each such failure.

Statement for Loan Guarantees and Loan Insurance

The undersigned states, to the best of his or her knowledge and belief, that:

If any funds have been paid or will be paid to any person for influencing or attempting to influence an officer or employee of any agency, a Member of Congress, an officer or employee of Congress, or an employee of a Member of Congress in connection with this commitment providing for the United States to insure or guarantee a loan, the undersigned shall complete and submit Standard Form-LLL, ''Disclosure of Lobbying Activities,'' in accordance with its instructions. Submission of this statement is a prerequisite for making or entering into this transaction imposed by section 1352, title 31, U.S. Code. Any person who fails to file the required statement shall be subject to a civil penalty of not less than $10,000 and not more than $100,000 for each such failure. */
  certification: "1. Certification for Contracts, Grants, Loans, and Cooperative Agreements",
  applicantOrganization: "2. Applicant's Organization",
  authorizedRepresentative: "3. Authorized Representative",
  signature: "4. Signature",
}

/** Grants.gov Lobbying Form, version 1.1: a certification profile distinct from SF-LLL. */
@Form.meta(#{
  id: "gg-lobbying",
  legacyFormId: 255,
  formName: "Grants.gov Lobbying Form",
  shortFormName: "GG_LobbyingForm",
  formVersion: "1.1",
  agencyCode: "SGG",
  ombNumber: "4040-0013",
})
@UI.sections(GgLobbyingSection)
model GgLobbying {
  /** Enter the legal name of the applicant's organization that will undertake the assistance activity. This is the organization that has registered with the System for Award Management (SAM). Information on registering with SAM may be obtained by visiting SAM.gov. */
  @UI.label("Applicant's Organization")
  @UI.section(GgLobbyingSection.applicantOrganization)
  organizationName: LegalName;

  /** Enter the name of the authorized representative certifying on the applicant's behalf. */
  @UI.label("Authorized Representative")
  @UI.section(GgLobbyingSection.authorizedRepresentative)
  @Validation.requiredPaths("firstName", "lastName")
  authorizedRepresentativeName: QuestionAorName;

  /** Enter the authorized representative's position title. */
  @UI.label("Title")
  @UI.section(GgLobbyingSection.authorizedRepresentative)
  authorizedRepresentativeTitle: AorTitle;

  /** Completed by Grants.gov upon submission. */
  @UI.label("Signature")
  @UI.section(GgLobbyingSection.signature)
  @UI.readOnly
  authorizedRepresentativeSignature?: AorSignature;

  /** Completed by Grants.gov upon submission. */
  @UI.label("Date")
  @UI.section(GgLobbyingSection.signature)
  @UI.readOnly
  submittedDate?: AorDateSigned;
}
