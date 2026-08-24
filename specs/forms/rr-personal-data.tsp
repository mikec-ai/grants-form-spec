import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/personal-data/index.tsp";

using SimplerForms;
using QuestionBank.PersonalData;

namespace Forms.RRPersonalData;

enum RRPersonalDataSection {
  /** Requested demographic information is voluntary, kept confidential, separated from the application after receipt, and excluded from review. */
  projectDirector: "Project Director / Principal Investigator",
  /** Add personal data for no more than four Co-Project Directors/Co-Principal Investigators. */
  coProjectDirectors: "Co-Project Directors / Co-Principal Investigators",
}

/** Research & Related Personal Data, Grants.gov FID 357, version 1.2. */
@Form.meta(#{
  id: "rr-personal-data",
  legacyFormId: 357,
  formName: "Research & Related Personal Data",
  shortFormName: "RR_PersonalData_1_2",
  formVersion: "1.2",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0001",
})
@UI.sections(RRPersonalDataSection)
model RRPersonalData {
  /** Provide the required name and any voluntary demographic information for the PD/PI. */
  @UI.label("Project Director / Principal Investigator")
  @UI.section(RRPersonalDataSection.projectDirector)
  projectDirector: QuestionProjectDirectorPersonalData;

  /** Optionally add personal data for up to four co-PDs/co-PIs. */
  @UI.label("Co-Project Directors / Co-Principal Investigators")
  @UI.section(RRPersonalDataSection.coProjectDirectors)
  @Sgg.fieldList(#{ validateBeforeAdd: true })
  @maxItems(4)
  coProjectDirectors?: QuestionCoProjectDirectorPersonalData[];
}
