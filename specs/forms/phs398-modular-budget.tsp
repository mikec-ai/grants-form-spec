import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/phs-modular-budget/index.tsp";

using SimplerForms;
using QuestionBank.PHSModularBudget;

namespace Forms.PHS398ModularBudget;

enum PHS398ModularBudgetSection {
  periods: "Budget Periods",
  cumulative: "Cumulative Budget Information",
  justifications: "Budget Justifications",
}

/** PHS 398 Modular Budget, Grants.gov form version 1.2. */
@Form.meta(#{
  id: "phs398-modular-budget",
  legacyFormId: 403,
  formName: "PHS 398 Modular Budget",
  shortFormName: "PHS398_ModularBudget_1_2",
  formVersion: "1.2",
  agencyCode: "GRANTS_GOV",
  ombNumber: "0925-0001",
})
@UI.sections(PHS398ModularBudgetSection)
// The pinned Grants.gov behavior source identifies all eight totals as read-only,
// calculated fields. Keep the reusable questions read-only by default while making
// those outputs visible in this form's review and applicant surfaces.
@UI.overrides(#{
  `periods.directCosts.totalDirectCosts`: #{ readOnly: true, visibleReadOnly: true },
  `periods.indirectCosts.totalIndirectCosts`: #{ readOnly: true, visibleReadOnly: true },
  `periods.totalDirectAndIndirectCosts`: #{ readOnly: true, visibleReadOnly: true },
  `cumulativeBudgetInformation.cumulativeDirectCostLessConsortiumFandA`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `cumulativeBudgetInformation.cumulativeConsortiumFandA`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `cumulativeBudgetInformation.cumulativeTotalDirectCosts`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `cumulativeBudgetInformation.cumulativeTotalIndirectCosts`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
  `cumulativeBudgetInformation.cumulativeTotalDirectAndIndirectCosts`: #{
    readOnly: true,
    visibleReadOnly: true,
  },
})
model PHS398ModularBudget {
  @UI.label("Budget Period")
  @UI.section(PHS398ModularBudgetSection.periods)
  @maxItems(5)
  periods?: QuestionPHSModularBudgetPeriod[];

  @UI.label("Cumulative Budget Information")
  @UI.section(PHS398ModularBudgetSection.cumulative)
  cumulativeBudgetInformation: QuestionPHSModularBudgetCumulativeSummary;

  @UI.label("Personnel Justification")
  @UI.section(PHS398ModularBudgetSection.justifications)
  @UI.widget(WidgetName.Attachment)
  personnelJustification?: PHSModularPersonnelJustification;

  @UI.label("Consortium Justification")
  @UI.section(PHS398ModularBudgetSection.justifications)
  @UI.widget(WidgetName.Attachment)
  consortiumJustification?: PHSModularConsortiumJustification;

  @UI.label("Additional Narrative Justification")
  @UI.section(PHS398ModularBudgetSection.justifications)
  @UI.widget(WidgetName.Attachment)
  additionalNarrativeJustification?: PHSModularAdditionalNarrativeJustification;
}
