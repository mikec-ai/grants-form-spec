import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/aor/index.tsp";
import "../question-bank/generics/index.tsp";
import "../question-bank/lobbying-disclosure/index.tsp";
import "../question-bank/project/index.tsp";

using SimplerForms;
using QuestionBank.Aor;
using QuestionBank.Generics;
using QuestionBank.LobbyingDisclosure;
using QuestionBank.Project;

namespace Forms.CD511;

enum CD511Section {
  award: "1. Applicant Information",
  contactPerson: "2. Contact Person",
  signature: "3. Signature",
}

/** Department of Commerce Certification Regarding Lobbying (CD-511). */
@Form.meta(#{
  id: "cd511",
  legacyFormId: 276,
  formName: "CD511",
  shortFormName: "CD511",
  formVersion: "1.1",
  agencyCode: "SGG",
  ombNumber: "",
})
@UI.sections(CD511Section)
@Validation.atLeastOneOf(CD511.awardNumber, CD511.projectName)
model CD511 {
  /** Enter the legal name of the applicant that will undertake the assistance activity. */
  @UI.label("Name of Applicant")
  @UI.section(CD511Section.award)
  applicantName: OrganizationName;

  /** Required if Project Name is blank. */
  @UI.label("Award Number")
  @UI.section(CD511Section.award)
  @Validation.constraints(#{ maxLength: 25 })
  awardNumber?: LobbyingFederalActionNumber;

  /** Required if Award Number is blank. */
  @UI.label("Project Name")
  @UI.section(CD511Section.award)
  @Validation.constraints(#{ maxLength: 60 })
  projectName?: ProjectTitle;

  /** The duly authorized representative who certifies for the applicant. */
  @UI.label("Contact Person")
  @UI.section(CD511Section.contactPerson)
  @Validation.requiredPaths("firstName", "lastName")
  contactPerson: QuestionAorName;

  @UI.label("Title")
  @UI.section(CD511Section.contactPerson)
  contactPersonTitle: AorTitle;

  /** Completed by Grants.gov upon submission. */
  @UI.label("Signature")
  @UI.section(CD511Section.signature)
  @UI.readOnly
  signature?: AorSignature;

  /** Completed by Grants.gov upon submission. */
  @UI.label("Date")
  @UI.section(CD511Section.signature)
  @UI.readOnly
  submittedDate?: AorDateSigned;
}
