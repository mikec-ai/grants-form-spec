import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/research-budget/index.tsp";

using SimplerForms;
using QuestionBank.ResearchBudget;

namespace Forms.RRSubawardBudget10Yr30;

enum RRSubawardBudget10Yr30Section {
  subawardBudgets: "Subaward budgets",
}

/**
 * R&R Subaward Budget Attachment(s) Form 10 YR 30 ATT, Grants.gov form version 3.0.
 * The source wrapper's ATT1-ATT30 strings are technical capture slots. The portable
 * declaration models the structured ten-period subaward budgets carried by those slots.
 */
@Form.meta(#{
  id: "rr-subaward-budget-10yr-30",
  formId: "8e208eec-a423-440b-9596-f71a33cec25f",
  legacyFormId: 780,
  formName: "[Draft] R&R Subaward Budget Attachment(s) Form 10 YR 30 ATT",
  shortFormName: "RR_SubawardBudget10_30_3_0",
  formVersion: "3.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0001",
  formType: "RRSubawardBudget10_30",
  sggVersion: "1.0",
})
@UI.sections(RRSubawardBudget10Yr30Section)
model RRSubawardBudget10Yr30 {
  /** Add up to thirty structured ten-year R&R budgets for subaward organizations. */
  @UI.label("Subaward Budgets")
  @UI.section(RRSubawardBudget10Yr30Section.subawardBudgets)
  @maxItems(30)
  budgetAttachments?: ResearchBudget10YrDetails[];
}
