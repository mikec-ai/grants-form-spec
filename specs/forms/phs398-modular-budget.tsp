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
  formId: "885622d5-8122-5c9c-b15a-ba429fd458fe",
  legacyFormId: 403,
  formName: "PHS 398 Modular Budget",
  shortFormName: "PHS398_ModularBudget_1_2",
  formVersion: "1.2",
  agencyCode: "GRANTS_GOV",
  ombNumber: "0925-0001",
  formType: "PHS398ModularBudget",
  sggVersion: "1.0",
})
@UI.sections(PHS398ModularBudgetSection)
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
