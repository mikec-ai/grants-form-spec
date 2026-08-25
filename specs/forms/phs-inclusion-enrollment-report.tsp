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
// The pinned F791 DAT identifies these 28 coordinates as calculated row or
// column totals. It does not pin exact operands or blank-value semantics, so
// keep them visible and protected without compiling arithmetic.
@UI.overrides(#{
  `reports.planned.hispanicLatino.female.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.total.blackAfricanAmerican`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.total.americanIndianAlaskaNative`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.hispanicLatino.unknownNotReportedSex.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.planned.total.white`: #{ readOnly: true, visibleReadOnly: true },
  `reports.planned.notHispanicLatino.male.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.notHispanicLatino.male.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.total.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.planned.total.americanIndianAlaskaNative`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.notHispanicLatino.female.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.total.white`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.planned.total.blackAfricanAmerican`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.planned.total.asian`: #{ readOnly: true, visibleReadOnly: true },
  `reports.cumulativeActual.total.unknownNotReported`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.planned.notHispanicLatino.female.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.planned.total.total`: #{ readOnly: true, visibleReadOnly: true },
  `reports.cumulativeActual.total.asian`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.planned.hispanicLatino.male.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.total.moreThanOneRace`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.total.nativeHawaiianPacificIslander`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.hispanicLatino.male.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.unknownNotReportedEthnicity.female.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.notHispanicLatino.unknownNotReportedSex.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.planned.total.nativeHawaiianPacificIslander`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.hispanicLatino.female.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.planned.total.moreThanOneRace`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.unknownNotReportedEthnicity.unknownNotReportedSex.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `reports.cumulativeActual.unknownNotReportedEthnicity.male.total`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
})
model PHSInclusionEnrollmentReport {
  @minItems(1)
  @maxItems(20)
  @UI.section(PHSInclusionEnrollmentReportSection.report)
  reports: InclusionEnrollmentReport[];
}
