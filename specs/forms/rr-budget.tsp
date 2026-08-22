import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/research-budget/index.tsp";

using SimplerForms;
using QuestionBank.ResearchBudget;

namespace Forms.RRBudget;

/** Research & Related Budget, Grants.gov form version 3.0. */
@Form.meta(#{
  id: "rr-budget",
  formId: "cfa593f7-e5ef-4ba8-82b2-c732ec65e461",
  legacyFormId: 770,
  formName: "[Draft] Research & Related Budget",
  shortFormName: "RR_Budget_3_0",
  formVersion: "3.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0001",
  formType: "RRBudget",
  sggVersion: "1.0",
})
@UI.sections(ResearchBudgetSection)
model RRBudget {
  ...ResearchBudgetDetails;
}
