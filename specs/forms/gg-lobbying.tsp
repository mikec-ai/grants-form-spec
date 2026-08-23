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
