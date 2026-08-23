import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/research-budget/index.tsp";

using SimplerForms;
using QuestionBank.ResearchBudget;

namespace Forms.RRSubawardBudget30;

enum RRSubawardBudget30Section {
  subawardBudgets: "Subaward budgets",
}

/**
 * R&R Subaward Budget Attachment(s) Form 5 YR 30 ATT, Grants.gov form version 3.0.
 * The source wrapper's ATT1-ATT30 strings are technical capture slots, not thirty
 * distinct semantic questions. This declaration models the structured subaward
 * budgets they carry. Its portable target profile declares the Grants.gov wire shape;
 * consumer-specific execution remains adapter-owned.
 */
@Form.meta(#{
  id: "rr-subaward-budget-30",
  legacyFormId: 782,
  formName: "[Draft] R&R Subaward Budget Attachment(s) Form 30",
  shortFormName: "RR_SubawardBudget30_3_0",
  formVersion: "3.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0001",
})
@UI.sections(RRSubawardBudget30Section)
model RRSubawardBudget30 {
  /** Add up to thirty structured five-year R&R budgets for subaward organizations. */
  @UI.label("Subaward Budgets")
  @UI.section(RRSubawardBudget30Section.subawardBudgets)
  @maxItems(30)
  budgetAttachments?: ResearchBudgetDetails[];
}
