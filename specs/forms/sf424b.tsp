import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/aor/index.tsp";
import "../question-bank/primary-org/index.tsp";

using SimplerForms;
using QuestionBank.Aor;
using QuestionBank.PrimaryOrg;

namespace Forms.Sf424b;

enum Sf424bSection {
  acceptance: "Signature",
}

/** Submission-owned fields shared by every SF-424B assurance profile. */
model Sf424bSubmissionAcceptance {
  /** Completed by Grants.gov upon submission. */
  @UI.label("Signature of the Authorized Certifying Official")
  @UI.section(Sf424bSection.acceptance)
  @UI.readOnly
  signature?: AorSignature;

  /** Completed by Grants.gov upon submission. */
  @UI.label("Date submitted")
  @UI.section(Sf424bSection.acceptance)
  @UI.readOnly
  signedDate?: AorDateSigned;
}

/** Identity copied from an organizational application cover and not edited here. */
model Sf424bForwardPopulatedIdentity {
  /** This must match the authorized representative title on the application cover. */
  @Response.role(ResponseRole.systemValue)
  @UI.label("Title")
  @UI.section(Sf424bSection.acceptance)
  @UI.readOnly
  title: AorTitle;

  /** This must match the legal applicant name on the application cover. */
  @Response.role(ResponseRole.systemValue)
  @UI.label("Applicant Organization")
  @UI.section(Sf424bSection.acceptance)
  @UI.readOnly
  applicantOrganization: LegalName;
}

/** Identity entered on the assurance when the Individual family is used. */
model Sf424bIndividualIdentity {
  @Response.role(ResponseRole.applicantInput)
  @UI.label("Title")
  @UI.section(Sf424bSection.acceptance)
  title: AorTitle;

  @Response.role(ResponseRole.applicantInput)
  @UI.label("Applicant Organization")
  @UI.section(Sf424bSection.acceptance)
  applicantOrganization: LegalName;
}

/** Active organizational SF-424B, Grants.gov form version 1.1 (FID 240). */
@Form.meta(#{
  id: "sf424b",
  legacyFormId: 240,
  formName: "Assurances for Non-Construction Programs (SF-424B)",
  shortFormName: "SF424B",
  formVersion: "1.1",
  agencyCode: "SGG",
  ombNumber: "4040-0007",
})
@UI.sections(Sf424bSection)
@UI.order(
  Sf424b.signature,
  Sf424b.title,
  Sf424b.applicantOrganization,
  Sf424b.signedDate
)
model Sf424b {
  ...Sf424bSubmissionAcceptance;
  ...Sf424bForwardPopulatedIdentity;
}

/** Active R&R SF-424B profile, Grants.gov form version 1.1 (FID 325). */
@Form.meta(#{
  id: "rr-sf424b",
  legacyFormId: 325,
  formName: "Assurances for Non-Construction Programs (SF-424B - R & R)",
  shortFormName: "RRSF424_SF424B",
  formVersion: "1.1",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0007",
})
@UI.sections(Sf424bSection)
@UI.order(
  RrSf424b.signature,
  RrSf424b.title,
  RrSf424b.applicantOrganization,
  RrSf424b.signedDate
)
model RrSf424b {
  ...Sf424bSubmissionAcceptance;
  ...Sf424bForwardPopulatedIdentity;
}

/** Active Mandatory-family SF-424B profile, Grants.gov form version 1.1 (FID 328). */
@Form.meta(#{
  id: "mandatory-sf424b",
  legacyFormId: 328,
  formName: "Assurances for Non-Construction Programs (SF-424B - Mandatory)",
  shortFormName: "Mandatory_SF424B",
  formVersion: "1.1",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0007",
})
@UI.sections(Sf424bSection)
@UI.order(
  MandatorySf424b.signature,
  MandatorySf424b.title,
  MandatorySf424b.applicantOrganization,
  MandatorySf424b.signedDate
)
model MandatorySf424b {
  ...Sf424bSubmissionAcceptance;
  ...Sf424bForwardPopulatedIdentity;
}

/** Active Individual-family SF-424B profile, Grants.gov form version 1.1 (FID 521). */
@Form.meta(#{
  id: "individual-sf424b",
  legacyFormId: 521,
  formName: "Assurances for Non-Construction Programs (SF-424B Individual)",
  shortFormName: "Individual_SF424B",
  formVersion: "1.1",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0007",
})
@UI.sections(Sf424bSection)
@UI.order(
  IndividualSf424b.signature,
  IndividualSf424b.title,
  IndividualSf424b.applicantOrganization,
  IndividualSf424b.signedDate
)
model IndividualSf424b {
  ...Sf424bSubmissionAcceptance;
  ...Sf424bIndividualIdentity;
}
