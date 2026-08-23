import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

/**
 * The five budget tables of SF-424A, each a question in its own right. Every one is asked
 * twice on that form -- once per activity and once as a total -- and the budget family
 * asks several of them again.
 *
 * Where a table's own arithmetic is intrinsic to it, it is declared here rather than on
 * the forms: a direct-charge subtotal is the sum of the object-class categories no matter
 * which form is asking.
 */
namespace QuestionBank.Budget;

/** Identify the grant program, function, or activity represented by a budget row. */
@Question.meta(#{ id: "budget/activity-title" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.title)
@UI.label("Grant program, function, or activity")
@minLength(1)
@maxLength(120)
scalar BudgetActivityTitle extends string;

/** Enter the Assistance Listing number associated with this budget activity, when applicable. */
@Question.meta(#{ id: "budget/activity-assistance-listing-number" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.identifier)
@UI.label("Assistance Listing number")
@minLength(1)
@maxLength(15)
scalar BudgetActivityAssistanceListingNumber extends string;

/** Explain direct-charge amounts that need additional context. */
@Question.meta(#{ id: "budget/direct-charges-explanation" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money, TagName.narrative)
@UI.label("Direct Charges")
@minLength(1)
@maxLength(50)
scalar DirectChargesExplanation extends string;

/** Explain the indirect rate, its base, and the resulting indirect expense. */
@Question.meta(#{ id: "budget/indirect-charges-explanation" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money, TagName.narrative)
@UI.label("Indirect Charges")
@minLength(1)
@maxLength(50)
scalar IndirectChargesExplanation extends string;

/** Provide any other explanation or comment needed for this budget. */
@Question.meta(#{ id: "budget/remarks" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money, TagName.narrative)
@UI.label("Remarks")
@minLength(1)
@maxLength(250)
scalar BudgetRemarks extends string;

/** Provide the narrative explaining and supporting the proposed budget. */
@Question.meta(#{ id: "budget/narrative" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.money, TagName.attachment)
@UI.label("Budget Narrative")
scalar BudgetNarrative extends AttachmentRef;

/** Provide the detailed justification supporting the proposed budget. */
@Question.meta(#{ id: "budget/justification" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money, TagName.attachment)
scalar BudgetJustification extends AttachmentRef;

/** Estimated unobligated and new or revised funds, federal and non-federal. */
@Question.meta(#{ id: "budget/summary" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Budget Summary")
model QuestionBudgetSummary {
  @UI.label("Estimated unobligated federal funds")
  @UI.helpText("Federal funds authorized under an award that have not yet been obligated. Enter an amount only when the application instructions require it.")
  federalEstimatedUnobligatedAmount?: MonetaryAmount;

  @UI.label("Estimated unobligated non-federal funds")
  @UI.helpText("Non-federal funds required under an award that have not yet been obligated or used. Enter an amount only when the application instructions require it.")
  nonFederalEstimatedUnobligatedAmount?: MonetaryAmount;

  @UI.label("New or revised federal budget")
  @UI.helpText("Enter federal funds needed for the upcoming period. For a supplemental application, enter the additional amount requested. For a change, enter the increase or decrease.")
  federalNewOrRevisedAmount?: MonetaryAmount;

  @UI.label("New or revised non-federal budget")
  @UI.helpText("Enter the non-federal share for the upcoming period. For a supplemental application, enter the additional contribution. For a change, enter the increase or decrease.")
  nonFederalNewOrRevisedAmount?: MonetaryAmount;

  @UI.label("Total")
  @UI.helpText("Enter the total budgeted amount for this row. This value is not calculated automatically.")
  totalAmount?: MonetaryAmount;
}

/** Funds required for each object class category. */
@Question.meta(#{ id: "budget/categories" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Budget Categories")
model QuestionBudgetCategories {
  personnelAmount?: MonetaryAmount;
  fringeBenefitsAmount?: MonetaryAmount;
  travelAmount?: MonetaryAmount;
  equipmentAmount?: MonetaryAmount;
  suppliesAmount?: MonetaryAmount;
  contractualAmount?: MonetaryAmount;
  constructionAmount?: MonetaryAmount;
  otherAmount?: MonetaryAmount;

  @Validation.computed(
    Op.Sum,
    QuestionBudgetCategories.personnelAmount,
    QuestionBudgetCategories.fringeBenefitsAmount,
    QuestionBudgetCategories.travelAmount,
    QuestionBudgetCategories.equipmentAmount,
    QuestionBudgetCategories.suppliesAmount,
    QuestionBudgetCategories.contractualAmount,
    QuestionBudgetCategories.constructionAmount,
    QuestionBudgetCategories.otherAmount
  )
  totalDirectChargeAmount?: MonetaryAmount;

  totalIndirectChargeAmount?: MonetaryAmount;

  @Validation.computed(
    Op.Sum,
    QuestionBudgetCategories.totalDirectChargeAmount,
    QuestionBudgetCategories.totalIndirectChargeAmount
  )
  totalAmount?: MonetaryAmount;

  programIncomeAmount?: MonetaryAmount;
}

/** Resources provided by the applicant, the state, or other sources. */
@Question.meta(#{ id: "budget/non-federal-resources" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Non-federal Resources")
model QuestionNonFederalResources {
  @minLength(0)
  @maxLength(120)
  grantProgram?: string;

  applicantAmount?: MonetaryAmount;
  stateAmount?: MonetaryAmount;
  otherAmount?: MonetaryAmount;

  @Validation.computed(
    Op.Sum,
    QuestionNonFederalResources.applicantAmount,
    QuestionNonFederalResources.stateAmount,
    QuestionNonFederalResources.otherAmount
  )
  totalAmount?: MonetaryAmount;
}

/** Federal funds needed for the balance of the project, by year. */
@Question.meta(#{ id: "budget/federal-fund-estimates" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Federal Fund Estimates")
model QuestionFederalFundEstimates {
  @minLength(0)
  @maxLength(120)
  grantProgram?: string;

  firstYearAmount?: MonetaryAmount;
  secondYearAmount?: MonetaryAmount;
  thirdYearAmount?: MonetaryAmount;
  fourthYearAmount?: MonetaryAmount;
}

/** Cash needed by quarter for the first year. */
@Question.meta(#{ id: "budget/forecasted-cash-needs" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Forecasted Cash Needs")
model QuestionForecastedCashNeeds {
  firstQuarterAmount?: MonetaryAmount;
  secondQuarterAmount?: MonetaryAmount;
  thirdQuarterAmount?: MonetaryAmount;
  fourthQuarterAmount?: MonetaryAmount;

  @Validation.computed(
    Op.Sum,
    QuestionForecastedCashNeeds.firstQuarterAmount,
    QuestionForecastedCashNeeds.secondQuarterAmount,
    QuestionForecastedCashNeeds.thirdQuarterAmount,
    QuestionForecastedCashNeeds.fourthQuarterAmount
  )
  totalAmount?: MonetaryAmount;
}
