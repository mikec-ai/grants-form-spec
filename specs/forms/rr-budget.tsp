import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/generics/index.tsp";
import "../question-bank/budget/index.tsp";
import "../question-bank/primary-org/index.tsp";
import "../question-bank/research-budget/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.Budget;
using QuestionBank.PrimaryOrg;
using QuestionBank.ResearchBudget;

namespace Forms.RRBudget;

/** The three working areas of the Research & Related Budget. */
enum ResearchBudgetSection {
  budgetOverview: "Budget overview",
  budgetYear: "Budget Year",
  budgetSummary: "Budget Summary",
}

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
  /** Unique Entity Identifier for the applicant organization. */
  @UI.label("UEI:")
  @UI.section(ResearchBudgetSection.budgetOverview)
  samUei: SamUei;

  /** Whether this is the project budget or a subaward or consortium budget. */
  @UI.label("Budget Type:")
  @UI.section(ResearchBudgetSection.budgetOverview)
  budgetType: ResearchBudgetType;

  /** Name of the organization responsible for this budget. */
  @UI.label("Enter name of Organization:")
  @UI.section(ResearchBudgetSection.budgetOverview)
  organizationName?: OrganizationName;

  /** Attach the budget justification file. */
  @UI.label("L. Budget Justification (Only attach one file.)")
  @UI.section(ResearchBudgetSection.budgetOverview)
  @UI.widget(WidgetName.Attachment)
  budgetJustificationAttachment: BudgetJustification;

  // One to five research budget periods. The item bounds carry this constraint without
  // introducing adapter-specific helper text into the portable UI contract.
  @UI.label("Budget Year")
  @UI.section(ResearchBudgetSection.budgetYear)
  @minItems(1)
  @maxItems(5)
  budgetYear: ResearchBudgetBudgetYear[];

  /** Cumulative totals across every budget period. */
  @UI.label("Budget Summary")
  @UI.section(ResearchBudgetSection.budgetSummary)
  budgetSummary: ResearchBudgetBudgetSummary;
}
