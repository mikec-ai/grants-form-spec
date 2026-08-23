import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/research-budget/index.tsp";

using SimplerForms;
using QuestionBank.ResearchBudget;

namespace Forms.RRBudget10Yr;

/** Research & Related Budget 10YR, Grants.gov form version 3.0. */
@Form.meta(#{
  id: "rr-budget-10yr",
  formName: "[Draft] Research & Related Budget 10YR",
  shortFormName: "RR_Budget10_3_0",
  formVersion: "3.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0001",
})
@UI.sections(ResearchBudgetSection)
model RRBudget10Yr {
  ...ResearchBudget10YrDetails;
}
