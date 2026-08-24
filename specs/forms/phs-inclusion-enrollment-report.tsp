import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/clinical-study/index.tsp";

using SimplerForms;
using QuestionBank.ClinicalStudy;

namespace Forms.PHSInclusionEnrollmentReport;

enum PHSInclusionEnrollmentReportSection {
  report: "Inclusion Enrollment Reports",
}

/** PHS Inclusion Enrollment Report, Grants.gov FID 791, version 1.0. */
@Form.meta(#{
  id: "phs-inclusion-enrollment-report",
  legacyFormId: 791,
  formName: "PHS Inclusion Enrollment Report",
  shortFormName: "PHSInclusionEnrollmentReport",
  formVersion: "1.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "0925-0770",
})
@UI.sections(PHSInclusionEnrollmentReportSection)
model PHSInclusionEnrollmentReport {
  @minItems(1)
  @maxItems(20)
  @UI.section(PHSInclusionEnrollmentReportSection.report)
  reports: InclusionEnrollmentReport[];
}
