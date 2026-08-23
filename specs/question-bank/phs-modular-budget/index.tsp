import "@simpler-grants/form-spec";
import "../index.tsp";
import "../budget/index.tsp";
import "../research-budget/index.tsp";

using SimplerForms;
using QuestionBank.Budget;
using QuestionBank.ResearchBudget;

/** Reusable questions introduced by the PHS 398 modular budget. */
namespace QuestionBank.PHSModularBudget;

/** One indirect-cost rate and base used in a modular budget period. */
model PHSModularIndirectCostItem {
  /** Describe the type of indirect cost. */
  @UI.label("Indirect (F&A) Type")
  @maxLength(64)
  indirectCostType: string;

  /** Enter the indirect-cost rate as a percentage. */
  @UI.label("Indirect (F&A) Rate (%)")
  indirectCostRate?: ResearchBudgetIndirectRate;

  /** Enter the amount to which the indirect-cost rate applies. */
  @UI.label("Indirect (F&A) Base ($)")
  indirectCostBase?: ResearchBudgetAmount14;

  /** Enter the indirect-cost funds requested for this rate. */
  @UI.label("Funds Requested ($)")
  indirectCostFundsRequested: ResearchBudgetAmount14;
}

/** Direct costs requested for one modular budget period. */
model PHSModularDirectCosts {
  /** Enter direct costs excluding consortium indirect costs. */
  @UI.label("Direct Cost less Consortium Indirect (F&A)")
  @UI.helpText("The source form presents modular values from $0 to $250,000. Exact option-to-wire encoding remains a review gate.")
  directCostLessConsortiumFandA: ResearchBudgetAmount14;

  /** Enter consortium indirect costs. */
  @UI.label("Consortium Indirect (F&A)")
  consortiumFandA?: ResearchBudgetAmount14;

  /** Total direct costs requested for the period. */
  @UI.label("Total Funds Requested for Direct Costs")
  @Validation.computed(
    Op.Sum,
    PHSModularDirectCosts.directCostLessConsortiumFandA,
    PHSModularDirectCosts.consortiumFandA
  )
  @Validation.evaluationOrder(3)
  @UI.readOnly
  totalDirectCosts: ResearchBudgetTotalAmount15;
}

/** Indirect costs requested for one modular budget period. */
model PHSModularIndirectCosts {
  /** List the indirect-cost rates and requested amounts for the period. */
  @UI.label("Indirect (F&A) Costs")
  @maxItems(4)
  indirectCostItems?: PHSModularIndirectCostItem[];

  /** Enter the cognizant federal agency, point of contact, and telephone number. */
  @UI.label("Cognizant Agency (Agency Name, POC Name and Phone Number)")
  @maxLength(180)
  cognizantFederalAgency?: string;

  /** Enter the indirect-cost rate agreement date. */
  @UI.label("Indirect (F&A) Rate Agreement Date")
  indirectCostAgreementDate?: plainDate;

  /** Total indirect costs requested for the period. */
  @UI.label("Total Funds Requested for Indirect Costs")
  @Validation.computedFrom(Op.Sum, "indirectCostItems[*].indirectCostFundsRequested")
  @Validation.evaluationOrder(4)
  @UI.readOnly
  totalIndirectCosts?: ResearchBudgetTotalAmount15;
}

/** A dated period in a PHS 398 modular budget. */
@Question.meta(#{ id: "budget/phs398-modular/period" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money, TagName.date)
@UI.label("Budget Period")
model QuestionPHSModularBudgetPeriod {
  /** Enter the budget period start date. */
  @UI.label("Start Date")
  budgetPeriodStartDate?: plainDate;

  /** Enter the budget period end date. */
  @UI.label("End Date")
  @UI.helpText("The end date cannot be earlier than the start date. Cross-field date comparison remains a runtime review gate.")
  budgetPeriodEndDate?: plainDate;

  /** Enter the direct costs requested for this period. */
  @UI.label("Direct Costs")
  directCosts: PHSModularDirectCosts;

  /** Enter the indirect costs requested for this period. */
  @UI.label("Indirect Costs")
  indirectCosts?: PHSModularIndirectCosts;

  /** Total direct and indirect costs requested for the period. */
  @UI.label("Total Direct and Indirect Costs")
  @Validation.computedFrom(Op.Sum, "directCosts.totalDirectCosts", "indirectCosts.totalIndirectCosts")
  @Validation.evaluationOrder(7)
  @UI.readOnly
  totalDirectAndIndirectCosts: ResearchBudgetTotalAmount15;
}

/** Cumulative totals across all PHS 398 modular budget periods. */
@Question.meta(#{ id: "budget/phs398-modular/cumulative-summary" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
model QuestionPHSModularBudgetCumulativeSummary {
  /** Cumulative direct costs excluding consortium indirect costs. */
  @UI.label("Cumulative Direct Cost less Consortium Indirect (F&A)")
  @Validation.computedFrom(Op.Sum, "../periods[*].directCosts.directCostLessConsortiumFandA")
  @Validation.evaluationOrder(2)
  @UI.readOnly
  cumulativeDirectCostLessConsortiumFandA: ResearchBudgetTotalAmount15;

  /** Cumulative consortium indirect costs. */
  @UI.label("Cumulative Consortium Indirect (F&A)")
  @Validation.computedFrom(Op.Sum, "../periods[*].directCosts.consortiumFandA")
  @Validation.evaluationOrder(1)
  @UI.readOnly
  cumulativeConsortiumFandA?: ResearchBudgetTotalAmount15;

  /** Cumulative total direct costs. */
  @UI.label("Cumulative Total Direct Costs")
  @Validation.computedFrom(Op.Sum, "../periods[*].directCosts.totalDirectCosts")
  @Validation.evaluationOrder(5)
  @UI.readOnly
  cumulativeTotalDirectCosts: ResearchBudgetTotalAmount15;

  /** Cumulative total indirect costs. */
  @UI.label("Cumulative Total Indirect Costs")
  @Validation.computedFrom(Op.Sum, "../periods[*].indirectCosts.totalIndirectCosts")
  @Validation.evaluationOrder(6)
  @UI.readOnly
  cumulativeTotalIndirectCosts?: ResearchBudgetTotalAmount15;

  /** Cumulative total direct and indirect costs. */
  @UI.label("Cumulative Total Direct and Indirect Costs")
  @Validation.computedFrom(Op.Sum, "../periods[*].totalDirectAndIndirectCosts")
  @Validation.evaluationOrder(8)
  @UI.readOnly
  cumulativeTotalDirectAndIndirectCosts: ResearchBudgetTotalAmount15;
}

/** Provide the personnel justification for the modular budget. */
@Question.meta(#{ id: "budget/phs398-modular/personnel-justification" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money, TagName.attachment)
scalar PHSModularPersonnelJustification extends BudgetJustification;

/** Provide the consortium justification for the modular budget. */
@Question.meta(#{ id: "budget/phs398-modular/consortium-justification" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money, TagName.attachment)
scalar PHSModularConsortiumJustification extends BudgetJustification;

/** Provide an additional narrative justification for the modular budget. */
@Question.meta(#{ id: "budget/phs398-modular/additional-narrative-justification" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.money, TagName.attachment)
scalar PHSModularAdditionalNarrativeJustification extends BudgetJustification;
