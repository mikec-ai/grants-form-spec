import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";
import "../primary-org/index.tsp";
import "../budget/index.tsp";
import "../research-budget/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.PrimaryOrg;
using QuestionBank.Budget;
using QuestionBank.ResearchBudget;

/** Reusable questions introduced by PHS Additional Indirect Costs. */
namespace QuestionBank.PHSAdditionalIndirectCosts;

/** Whether this is the project budget or a subaward or consortium budget. */
enum PHSAdditionalIndirectCostsBudgetType {
  project: "Project",
  subawardConsortium: "Subaward/Consortium",
}

/** One indirect-cost rate and requested amount. */
model PHSAdditionalIndirectCostItem {
  @UI.label("Indirect Cost Type")
  @maxLength(64)
  costType: string;

  @UI.label("Indirect Cost Rate (%)")
  rate?: ResearchBudgetIndirectRate;

  @UI.label("Indirect Cost Base ($)")
  base?: ResearchBudgetAmount14;

  @UI.label("Funds Requested ($)")
  fundRequested: ResearchBudgetAmount14;
}

/** Indirect costs requested for one budget period. */
model PHSAdditionalIndirectCostsForPeriod {
  @UI.label("Indirect Costs")
  @minItems(1)
  @maxItems(4)
  indirectCost: PHSAdditionalIndirectCostItem[];

  @UI.label("Total Indirect Costs")
  @Validation.computedFrom(Op.Sum, "indirectCost[*].fundRequested")
  @Validation.evaluationOrder(1)
  @UI.readOnly
  totalIndirectCosts: ResearchBudgetTotalAmount15;
}

/** A dated period of additional indirect costs. */
@Question.meta(#{ id: "budget/additional-indirect-costs/period" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money, TagName.date)
model QuestionPHSAdditionalIndirectCostsBudgetYear {
  @UI.label("UEI:")
  samUei?: SamUei;

  @UI.label("Enter name of Organization:")
  organizationName?: OrganizationName;

  @UI.label("Budget Type:")
  @UI.widget(WidgetName.Select)
  budgetType?: PHSAdditionalIndirectCostsBudgetType;

  @UI.label("Start Date")
  budgetPeriodStartDate: plainDate;

  @UI.label("End Date")
  @Validation.notBefore(QuestionPHSAdditionalIndirectCostsBudgetYear.budgetPeriodStartDate)
  @UI.helpText("End Date cannot be before Start Date.")
  budgetPeriodEndDate: plainDate;

  @UI.label("Indirect Costs")
  indirectCosts?: PHSAdditionalIndirectCostsForPeriod;
}

/** Cumulative indirect costs requested across all budget periods. */
@Question.meta(#{ id: "budget/additional-indirect-costs/cumulative-summary" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
model QuestionPHSAdditionalIndirectCostsSummary {
  @UI.label("Indirect Costs")
  @Validation.computedFrom(Op.Sum, "../budgetYears[*].indirectCosts.totalIndirectCosts")
  @Validation.evaluationOrder(2)
  @UI.readOnly
  cumulativeTotalFundsRequestedIndirectCost?: ResearchBudgetTotalAmount15;
}

/** Provide one budget justification for the entire project period. */
@Question.meta(#{ id: "budget/additional-indirect-costs/justification" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money, TagName.attachment)
scalar PHSAdditionalIndirectCostsBudgetJustification extends BudgetJustification;
