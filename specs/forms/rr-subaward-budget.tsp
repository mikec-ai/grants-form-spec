import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/research-budget/index.tsp";

using SimplerForms;
using QuestionBank.ResearchBudget;

namespace Forms.RRSubawardBudget;

enum RRSubawardBudgetSection {
  subawardBudgets: "Subaward budgets",
}

/** R&R Subaward Budget Attachment(s) Form, Grants.gov form version 3.0. */
@Form.meta(#{
  id: "rr-subaward-budget",
  formId: "67450974-a273-5bb8-86e5-b88d8a68c732",
  legacyFormId: 776,
  formName: "[Draft] R&R Subaward Budget Attachment(s) Form",
  shortFormName: "RR_SubawardBudget_3_0",
  formVersion: "3.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0001",
  formType: "RRSubawardBudget",
  sggVersion: "1.0",
})
@UI.sections(RRSubawardBudgetSection)
model RRSubawardBudget {
  /** Add up to ten structured Research & Related budgets for subaward organizations. */
  @UI.label("Subaward Budgets")
  @UI.section(RRSubawardBudgetSection.subawardBudgets)
  @maxItems(10)
  budgetAttachments?: ResearchBudgetDetails[];
}
