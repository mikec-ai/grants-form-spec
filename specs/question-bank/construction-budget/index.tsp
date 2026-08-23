import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace QuestionBank.ConstructionBudget;

/** A non-negative construction-budget amount entered by an applicant. */
@Catalog.tag(TagName.money)
@pattern("^\\d{1,10}(?:[.]\\d{2})?$")
@minLength(1)
@maxLength(13)
scalar ConstructionEnteredAmount extends MonetaryAmount;

/** A non-negative calculated construction-budget subtotal. */
@Catalog.tag(TagName.money)
@pattern("^\\d{1,12}(?:[.]\\d{2})?$")
@minLength(1)
@maxLength(15)
scalar ConstructionTotalAmount extends string;

/** A whole-number federal share percentage between zero and one hundred. */
@Question.meta(#{ id: "budget/construction/federal-share-percentage" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Federal percentage share")
@minValue(0)
@maxValue(100)
scalar ConstructionFederalSharePercentage extends int32;

/** The three columns used to capture one construction cost classification. */
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
model ConstructionCostColumns {
  @UI.label("Total Cost")
  @Response.role(ResponseRole.applicantInput)
  totalCost?: ConstructionEnteredAmount;

  @UI.label("Costs Not Allowable for Participation")
  @Response.role(ResponseRole.applicantInput)
  nonAllowableCost?: ConstructionEnteredAmount;

  @UI.label("Total Allowable Costs (Columns a - b)")
  @Response.role(ResponseRole.calculatedOutput)
  @Validation.computed(Op.Subtract, ConstructionCostColumns.totalCost, ConstructionCostColumns.nonAllowableCost)
  @Validation.materializeWhenAnySourcePresent
  @UI.readOnly
  totalAllowableCost?: ConstructionEnteredAmount;
}

/** Enter administrative and legal expenses directly associated with the allowable activity. */
@Question.meta(#{ id: "budget/construction/administration-and-legal-expenses" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Administrative and legal expenses")
model QuestionConstructionAdministrationAndLegalExpenses { ...ConstructionCostColumns; }

/** Enter costs for land, structures, rights-of-way, appraisals, and related items. */
@Question.meta(#{ id: "budget/construction/land-structures-rights-of-way" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Land, structures, rights-of-way, appraisals, etc.")
model QuestionConstructionLandStructuresRightsOfWay { ...ConstructionCostColumns; }

/** Enter relocation expenses and payments. */
@Question.meta(#{ id: "budget/construction/relocation-expenses" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Relocation expenses and payments")
model QuestionConstructionRelocationExpenses { ...ConstructionCostColumns; }

/** Enter architectural and engineering fees. */
@Question.meta(#{ id: "budget/construction/architectural-engineering-fees" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Architectural and engineering fees")
model QuestionConstructionArchitecturalEngineeringFees { ...ConstructionCostColumns; }

/** Enter other architectural and engineering fees. */
@Question.meta(#{ id: "budget/construction/other-architectural-engineering-fees" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Other architectural and engineering fees")
model QuestionConstructionOtherArchitecturalEngineeringFees { ...ConstructionCostColumns; }

/** Enter project inspection fees. */
@Question.meta(#{ id: "budget/construction/project-inspection-fees" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Project inspection fees")
model QuestionConstructionProjectInspectionFees { ...ConstructionCostColumns; }

/** Enter site-work costs. */
@Question.meta(#{ id: "budget/construction/site-work" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Site work")
model QuestionConstructionSiteWork { ...ConstructionCostColumns; }

/** Enter demolition and removal costs. */
@Question.meta(#{ id: "budget/construction/demolition-and-removal" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Demolition and removal")
model QuestionConstructionDemolitionAndRemoval { ...ConstructionCostColumns; }

/** Enter construction costs. */
@Question.meta(#{ id: "budget/construction/construction" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Construction")
model QuestionConstructionConstruction { ...ConstructionCostColumns; }

/** Enter equipment costs. */
@Question.meta(#{ id: "budget/construction/equipment" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Equipment")
model QuestionConstructionEquipment { ...ConstructionCostColumns; }

/** Enter miscellaneous construction-project costs. */
@Question.meta(#{ id: "budget/construction/miscellaneous" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Miscellaneous")
model QuestionConstructionMiscellaneous { ...ConstructionCostColumns; }

/** Enter contingencies that the awarding agency allows for the project. */
@Question.meta(#{ id: "budget/construction/contingencies" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Contingencies")
model QuestionConstructionContingencies { ...ConstructionCostColumns; }

/** Enter project or program income to subtract from total project costs. */
@Question.meta(#{ id: "budget/construction/program-income" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Project (program) income")
model QuestionConstructionProgramIncome { ...ConstructionCostColumns; }

/** Subtotal of cost-classification lines 1 through 11. */
@Question.meta(#{ id: "budget/construction/subtotal-before-contingencies" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Subtotal (sum of lines 1-11)")
model QuestionConstructionSubtotalBeforeContingencies {
  @Response.role(ResponseRole.calculatedOutput)
  @Validation.computedFrom(
    Op.Sum,
    "../administrativeAndLegalExpenses.totalCost",
    "../landStructuresRightsOfWay.totalCost",
    "../relocationExpenses.totalCost",
    "../architecturalEngineeringFees.totalCost",
    "../otherArchitecturalEngineeringFees.totalCost",
    "../projectInspectionFees.totalCost",
    "../siteWork.totalCost",
    "../demolitionAndRemoval.totalCost",
    "../construction.totalCost",
    "../equipment.totalCost",
    "../miscellaneous.totalCost"
  )
  @Validation.materializeWhenAnySourcePresent
  @UI.readOnly
  totalCost?: ConstructionTotalAmount;

  @Response.role(ResponseRole.calculatedOutput)
  @Validation.computedFrom(
    Op.Sum,
    "../administrativeAndLegalExpenses.nonAllowableCost",
    "../landStructuresRightsOfWay.nonAllowableCost",
    "../relocationExpenses.nonAllowableCost",
    "../architecturalEngineeringFees.nonAllowableCost",
    "../otherArchitecturalEngineeringFees.nonAllowableCost",
    "../projectInspectionFees.nonAllowableCost",
    "../siteWork.nonAllowableCost",
    "../demolitionAndRemoval.nonAllowableCost",
    "../construction.nonAllowableCost",
    "../equipment.nonAllowableCost",
    "../miscellaneous.nonAllowableCost"
  )
  @Validation.materializeWhenAnySourcePresent
  @UI.readOnly
  nonAllowableCost?: ConstructionTotalAmount;

  @Response.role(ResponseRole.calculatedOutput)
  @Validation.computed(
    Op.Subtract,
    QuestionConstructionSubtotalBeforeContingencies.totalCost,
    QuestionConstructionSubtotalBeforeContingencies.nonAllowableCost
  )
  @Validation.materializeWhenAnySourcePresent
  @UI.readOnly
  totalAllowableCost?: ConstructionTotalAmount;
}

/** Subtotal after adding contingencies. */
@Question.meta(#{ id: "budget/construction/subtotal-after-contingencies" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Subtotal")
model QuestionConstructionSubtotalAfterContingencies {
  @Response.role(ResponseRole.calculatedOutput)
  @Validation.computedFrom(Op.Sum, "../subtotalBeforeContingencies.totalCost", "../contingencies.totalCost")
  @Validation.materializeWhenAnySourcePresent
  @UI.readOnly
  totalCost?: ConstructionTotalAmount;

  @Response.role(ResponseRole.calculatedOutput)
  @Validation.computedFrom(Op.Sum, "../subtotalBeforeContingencies.nonAllowableCost", "../contingencies.nonAllowableCost")
  @Validation.materializeWhenAnySourcePresent
  @UI.readOnly
  nonAllowableCost?: ConstructionTotalAmount;

  @Response.role(ResponseRole.calculatedOutput)
  @Validation.computedFrom(Op.Sum, "../subtotalBeforeContingencies.totalAllowableCost", "../contingencies.totalAllowableCost")
  @Validation.materializeWhenAnySourcePresent
  @UI.readOnly
  totalAllowableCost?: ConstructionTotalAmount;
}

/** Total project costs after subtracting project income. */
@Question.meta(#{ id: "budget/construction/total-project-costs" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Total project costs")
model QuestionConstructionTotalProjectCosts {
  @Response.role(ResponseRole.calculatedOutput)
  @Validation.computedFrom(Op.Subtract, "../subtotalAfterContingencies.totalCost", "../programIncome.totalCost")
  @Validation.materializeWhenAnySourcePresent
  @UI.readOnly
  totalCost?: ConstructionTotalAmount;

  @Response.role(ResponseRole.calculatedOutput)
  @Validation.computedFrom(Op.Subtract, "../subtotalAfterContingencies.nonAllowableCost", "../programIncome.nonAllowableCost")
  @Validation.materializeWhenAnySourcePresent
  @UI.readOnly
  nonAllowableCost?: ConstructionTotalAmount;

  @Response.role(ResponseRole.calculatedOutput)
  @Validation.computedFrom(Op.Subtract, "../subtotalAfterContingencies.totalAllowableCost", "../programIncome.totalAllowableCost")
  @Validation.materializeWhenAnySourcePresent
  @UI.readOnly
  totalAllowableCost?: ConstructionTotalAmount;
}

/** Federal assistance requested for the construction project. */
@Question.meta(#{ id: "budget/construction/federal-funding" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Federal funding")
model QuestionConstructionFederalFunding {
  /** Eligible costs copied from line 16c for display and the share calculation only. */
  @Response.role(ResponseRole.calculatedOutput)
  @Validation.computedFrom(Op.Sum, "../budgetInformation.totalProjectCosts.totalAllowableCost")
  @Validation.materializeWhenAnySourcePresent
  @UI.label("Total eligible project costs")
  @UI.readOnly
  totalProjectCosts?: ConstructionTotalAmount;

  federalPercentageShare?: ConstructionFederalSharePercentage;

  @Response.role(ResponseRole.calculatedOutput)
  @Validation.computed(
    Op.PercentOf,
    QuestionConstructionFederalFunding.totalProjectCosts,
    QuestionConstructionFederalFunding.federalPercentageShare
  )
  @Validation.materializeWhenAnySourcePresent
  @UI.label("Federal funding share")
  @UI.readOnly
  federalFundingShare?: ConstructionTotalAmount;
}
