import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/aor/index.tsp";
import "../question-bank/primary-org/index.tsp";

using SimplerForms;
using QuestionBank.Aor;
using QuestionBank.PrimaryOrg;

namespace Forms.Sf424d;

enum Sf424dSection {
  acceptance: "3. Signature",
}

/** Submission-owned fields shared by every active SF-424D assurance profile. */
model Sf424dSubmissionAcceptance {
  /** Completed by Grants.gov upon submission. */
  @UI.label("Signature of the Authorized Certifying Official")
  @UI.section(Sf424dSection.acceptance)
  @UI.readOnly
  signature?: AorSignature;

  /** Completed by Grants.gov upon submission. */
  @UI.label("Date Submitted")
  @UI.section(Sf424dSection.acceptance)
  @UI.readOnly
  signedDate?: AorDateSigned;
}

/** Identity copied from an organizational application cover and not edited here. */
model Sf424dForwardPopulatedIdentity {
  /** This must match the authorized representative title on the application cover. */
  @Response.role(ResponseRole.systemValue)
  @UI.label("Title")
  @UI.section(Sf424dSection.acceptance)
  @UI.readOnly
  title: AorTitle;

  /** This must match the legal applicant name on the application cover. */
  @Response.role(ResponseRole.systemValue)
  @UI.label("Applicant Organization")
  @UI.section(Sf424dSection.acceptance)
  @UI.readOnly
  applicantOrganization: LegalName;
}

/** Identity entered on the assurance when the Individual profile is used. */
model Sf424dIndividualIdentity {
  @Response.role(ResponseRole.applicantInput)
  @UI.label("Title")
  @UI.section(Sf424dSection.acceptance)
  title: AorTitle;

  @Response.role(ResponseRole.applicantInput)
  @UI.label("Applicant Name")
  @UI.section(Sf424dSection.acceptance)
  applicantOrganization: LegalName;
}

/** Active organizational SF-424D, Grants.gov form version 1.1 (FID 238). */
@Form.meta(#{
  id: "sf424d",
  legacyFormId: 238,
  formName: "Assurances for Construction Programs (SF-424D)",
  shortFormName: "SF424D",
  formVersion: "1.1",
  agencyCode: "SGG",
  ombNumber: "4040-0009",
})
@UI.sections(Sf424dSection)
@UI.order(
  Sf424d.signature,
  Sf424d.title,
  Sf424d.applicantOrganization,
  Sf424d.signedDate
)
model Sf424d {
  ...Sf424dSubmissionAcceptance;
  ...Sf424dForwardPopulatedIdentity;
}

/** Active Mandatory-family SF-424D, Grants.gov form version 1.1 (FID 329). */
@Form.meta(#{
  id: "mandatory-sf424d",
  legacyFormId: 329,
  formName: "Assurances for Construction Programs (SF-424D - Mandatory)",
  shortFormName: "Mandatory_SF424D",
  formVersion: "1.1",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0009",
})
@UI.sections(Sf424dSection)
@UI.order(
  MandatorySf424d.signature,
  MandatorySf424d.title,
  MandatorySf424d.applicantOrganization,
  MandatorySf424d.signedDate
)
model MandatorySf424d {
  ...Sf424dSubmissionAcceptance;
  ...Sf424dForwardPopulatedIdentity;
}

/** Active Individual-family SF-424D, Grants.gov form version 1.1 (FID 522). */
@Form.meta(#{
  id: "individual-sf424d",
  legacyFormId: 522,
  formName: "Assurances for Construction Programs (SF-424D Individual)",
  shortFormName: "Individual_SF424D",
  formVersion: "1.1",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0009",
})
@UI.sections(Sf424dSection)
@UI.order(
  IndividualSf424d.signature,
  IndividualSf424d.title,
  IndividualSf424d.applicantOrganization,
  IndividualSf424d.signedDate
)
model IndividualSf424d {
  ...Sf424dSubmissionAcceptance;
  ...Sf424dIndividualIdentity;
}
