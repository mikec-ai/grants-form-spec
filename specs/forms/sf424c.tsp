import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/construction-budget/index.tsp";

using SimplerForms;
using QuestionBank.ConstructionBudget;

namespace Forms.SF424C;

enum SF424CSection {
  /** Certain programs require additional computations to establish the eligible Federal share. Follow the awarding agency's instructions. */
  budget: "Budget Information for Construction Programs",
  federalFunding: "Federal Funding",
}

/** The sixteen cost-classification rows on SF-424C. */
@UI.label("Cost Classification")
model ConstructionBudgetInformation {
  administrativeAndLegalExpenses?: QuestionConstructionAdministrationAndLegalExpenses;
  landStructuresRightsOfWay?: QuestionConstructionLandStructuresRightsOfWay;
  relocationExpenses?: QuestionConstructionRelocationExpenses;
  architecturalEngineeringFees?: QuestionConstructionArchitecturalEngineeringFees;
  otherArchitecturalEngineeringFees?: QuestionConstructionOtherArchitecturalEngineeringFees;
  projectInspectionFees?: QuestionConstructionProjectInspectionFees;
  siteWork?: QuestionConstructionSiteWork;
  demolitionAndRemoval?: QuestionConstructionDemolitionAndRemoval;
  construction?: QuestionConstructionConstruction;
  equipment?: QuestionConstructionEquipment;
  miscellaneous?: QuestionConstructionMiscellaneous;
  subtotalBeforeContingencies?: QuestionConstructionSubtotalBeforeContingencies;
  contingencies?: QuestionConstructionContingencies;
  subtotalAfterContingencies?: QuestionConstructionSubtotalAfterContingencies;
  programIncome?: QuestionConstructionProgramIncome;
  totalProjectCosts?: QuestionConstructionTotalProjectCosts;
}

/** Budget Information for Construction Programs (SF-424C), Grants.gov version 2.0. */
@Form.meta(#{
  id: "sf424c",
  legacyFormId: 408,
  formName: "Budget Information for Construction Programs (SF-424C)",
  shortFormName: "SF424C",
  formVersion: "2.0",
  agencyCode: "SGG",
  ombNumber: "4040-0008",
})
@UI.sections(SF424CSection)
@Sgg.multiField(SF424CSection.budget, WidgetName.Table)
model SF424C {
  @UI.section(SF424CSection.budget)
  budgetInformation?: ConstructionBudgetInformation;

  @UI.section(SF424CSection.federalFunding)
  federalFunding?: QuestionConstructionFederalFunding;
}
