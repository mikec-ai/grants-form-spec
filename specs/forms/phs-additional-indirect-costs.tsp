import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/phs-additional-indirect-costs/index.tsp";

using SimplerForms;
using QuestionBank.PHSAdditionalIndirectCosts;

namespace Forms.PHSAdditionalIndirectCosts;

enum PHSAdditionalIndirectCostsSection {
  periods: "Budget Periods",
  justification: "Budget Justification",
  cumulative: "Cumulative Budget",
}

/** PHS Additional Indirect Costs, Grants.gov form version 2.0. */
@Form.meta(#{
  id: "phs-additional-indirect-costs",
  legacyFormId: 739,
  formName: "PHS Additional Indirect Costs",
  shortFormName: "PHS_Additional_IndirectCosts_2_0",
  formVersion: "2.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "0925-0001",
})
@UI.sections(PHSAdditionalIndirectCostsSection)
// The pinned DAT identifies both totals as calculated and read-only. Keep those
// semantics in the reusable bank while making the outputs visible in this form.
@UI.overrides(#{
  `budgetYears.indirectCosts.totalIndirectCosts`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `budgetSummary.cumulativeTotalFundsRequestedIndirectCost`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
})
model PHSAdditionalIndirectCosts {
  @UI.label("Budget Period")
  @UI.section(PHSAdditionalIndirectCostsSection.periods)
  @minItems(1)
  @maxItems(10)
  budgetYears: QuestionPHSAdditionalIndirectCostsBudgetYear[];

  @UI.label("Budget Justification (Only attach one file.)")
  @UI.section(PHSAdditionalIndirectCostsSection.justification)
  @UI.widget(WidgetName.Attachment)
  budgetJustificationAttachment?: PHSAdditionalIndirectCostsBudgetJustification;

  @UI.label("Cumulative Budget")
  @UI.section(PHSAdditionalIndirectCostsSection.cumulative)
  budgetSummary?: QuestionPHSAdditionalIndirectCostsSummary;
}
