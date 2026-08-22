import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace QuestionBank.ResearchBudget;

// A source-wire decimal, kept distinct from the applicant-facing monetary question because
// its precision pattern is a transport constraint rather than a different semantic question.
@Catalog.tag(TagName.money)
@pattern("^-?(?:\\d{1,14}|\\d{1,13}[.]\\d|\\d{1,12}[.]\\d{2})$")
@minLength(1)
@maxLength(16)
scalar ResearchBudgetDecimal extends string;

/** Whether the budget describes the applicant project or a subaward or consortium component. */
enum ResearchBudgetType {
  project: "Project",
  subawardConsortium: "Subaward/Consortium",
}

/** Cumulative totals across all research budget periods. */
@Question.meta(#{ id: "budget/research/cumulative-summary" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.order(
  ResearchBudgetBudgetSummary.cumulativeTotalFundsRequestedSeniorKeyPerson,
  ResearchBudgetBudgetSummary.cumulativeTotalFundsRequestedOtherPersonnel,
  ResearchBudgetBudgetSummary.cumulativeTotalNoOtherPersonnel,
  ResearchBudgetBudgetSummary.cumulativeTotalFundsRequestedPersonnel,
  ResearchBudgetBudgetSummary.cumulativeTotalFundsRequestedEquipment,
  ResearchBudgetBudgetSummary.cumulativeTotalFundsRequestedTravel,
  ResearchBudgetBudgetSummary.cumulativeDomesticTravelCosts,
  ResearchBudgetBudgetSummary.cumulativeForeignTravelCosts,
  ResearchBudgetBudgetSummary.cumulativeTotalFundsRequestedTraineeCosts,
  ResearchBudgetBudgetSummary.cumulativeTraineeTuitionFeesHealthInsurance,
  ResearchBudgetBudgetSummary.cumulativeTraineeStipends,
  ResearchBudgetBudgetSummary.cumulativeTraineeTravel,
  ResearchBudgetBudgetSummary.cumulativeTraineeSubsistence,
  ResearchBudgetBudgetSummary.cumulativeOtherTraineeCost,
  ResearchBudgetBudgetSummary.cumulativeNoofTrainees,
  ResearchBudgetBudgetSummary.cumulativeTotalFundsRequestedOtherDirectCosts,
  ResearchBudgetBudgetSummary.cumulativeMaterialAndSupplies,
  ResearchBudgetBudgetSummary.cumulativePublicationCosts,
  ResearchBudgetBudgetSummary.cumulativeConsultantServices,
  ResearchBudgetBudgetSummary.cumulativeAdpComputerServices,
  ResearchBudgetBudgetSummary.cumulativeSubawardConsortiumContractualCosts,
  ResearchBudgetBudgetSummary.cumulativeEquipmentFacilityRentalFees,
  ResearchBudgetBudgetSummary.cumulativeAlterationsAndRenovations,
  ResearchBudgetBudgetSummary.cumulativeOther1DirectCost,
  ResearchBudgetBudgetSummary.cumulativeOther2DirectCost,
  ResearchBudgetBudgetSummary.cumulativeOther3DirectCost,
  ResearchBudgetBudgetSummary.cumulativeOther4DirectCost,
  ResearchBudgetBudgetSummary.cumulativeOther5DirectCost,
  ResearchBudgetBudgetSummary.cumulativeOther6DirectCost,
  ResearchBudgetBudgetSummary.cumulativeOther7DirectCost,
  ResearchBudgetBudgetSummary.cumulativeOther8DirectCost,
  ResearchBudgetBudgetSummary.cumulativeOther9DirectCost,
  ResearchBudgetBudgetSummary.cumulativeOther10DirectCost,
  ResearchBudgetBudgetSummary.cumulativeTotalFundsRequestedDirectCosts,
  ResearchBudgetBudgetSummary.cumulativeTotalFundsRequestedIndirectCost,
  ResearchBudgetBudgetSummary.cumulativeTotalFundsRequestedDirectIndirectCosts,
  ResearchBudgetBudgetSummary.cumulativeFee,
  ResearchBudgetBudgetSummary.cumulativeTotalCostsFee
)
model ResearchBudgetBudgetSummary {
  @UI.label("4. ADP/Computer Services")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].otherDirectCosts.adpComputerServices")
  @Validation.evaluationOrder(23)
  @UI.readOnly
  cumulativeAdpComputerServices?: ResearchBudgetDecimal;

  @UI.label("7. Alterations and Renovations")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].otherDirectCosts.alterationsRenovations")
  @Validation.evaluationOrder(26)
  @UI.readOnly
  cumulativeAlterationsAndRenovations?: ResearchBudgetDecimal;

  @UI.label("3. Consultant Services")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].otherDirectCosts.consultantServices")
  @Validation.evaluationOrder(22)
  @UI.readOnly
  cumulativeConsultantServices?: ResearchBudgetDecimal;

  @UI.label("1. Domestic")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].travel.domesticTravelCost")
  @Validation.evaluationOrder(16)
  @UI.readOnly
  cumulativeDomesticTravelCosts?: ResearchBudgetDecimal;

  @UI.label("6. Equipment or Facility Rental/User Fees")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].otherDirectCosts.equipmentRentalFee")
  @Validation.evaluationOrder(25)
  @UI.readOnly
  cumulativeEquipmentFacilityRentalFees?: ResearchBudgetDecimal;

  @UI.label("Section J, Fee")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].fee")
  @Validation.evaluationOrder(30)
  @UI.readOnly
  cumulativeFee?: ResearchBudgetDecimal;

  @UI.label("2. Foreign")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].travel.foreignTravelCost")
  @Validation.evaluationOrder(17)
  @UI.readOnly
  cumulativeForeignTravelCosts?: ResearchBudgetDecimal;

  @UI.label("1. Materials and Supplies")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].otherDirectCosts.materialsSupplies")
  @Validation.evaluationOrder(20)
  @UI.readOnly
  cumulativeMaterialAndSupplies?: ResearchBudgetDecimal;

  @UI.label("6. Number of Participants/Trainees")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].participantTraineeSupportCosts.participantTraineeNumber")
  @Validation.evaluationOrder(18)
  @UI.readOnly
  cumulativeNoofTrainees?: int32;

  @UI.label("17. Other 10")
  @UI.readOnly
  cumulativeOther10DirectCost?: ResearchBudgetDecimal;

  @UI.label("8. Other 1")
  @UI.readOnly
  cumulativeOther1DirectCost?: ResearchBudgetDecimal;

  @UI.label("9. Other 2")
  @UI.readOnly
  cumulativeOther2DirectCost?: ResearchBudgetDecimal;

  @UI.label("10. Other 3")
  @UI.readOnly
  cumulativeOther3DirectCost?: ResearchBudgetDecimal;

  @UI.label("11. Other 4")
  @UI.readOnly
  cumulativeOther4DirectCost?: ResearchBudgetDecimal;

  @UI.label("12. Other 5")
  @UI.readOnly
  cumulativeOther5DirectCost?: ResearchBudgetDecimal;

  @UI.label("13. Other 6")
  @UI.readOnly
  cumulativeOther6DirectCost?: ResearchBudgetDecimal;

  @UI.label("14. Other 7")
  @UI.readOnly
  cumulativeOther7DirectCost?: ResearchBudgetDecimal;

  @UI.label("15. Other 8")
  @UI.readOnly
  cumulativeOther8DirectCost?: ResearchBudgetDecimal;

  @UI.label("16. Other 9")
  @UI.readOnly
  cumulativeOther9DirectCost?: ResearchBudgetDecimal;

  @UI.label("5. Other")
  @UI.readOnly
  cumulativeOtherTraineeCost?: ResearchBudgetDecimal;

  @UI.label("2. Publication Costs")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].otherDirectCosts.publicationCosts")
  @Validation.evaluationOrder(21)
  @UI.readOnly
  cumulativePublicationCosts?: ResearchBudgetDecimal;

  @UI.label("5. Subawards/Consortium/Contractual Costs")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].otherDirectCosts.subawardConsortiumContractualCosts")
  @Validation.evaluationOrder(24)
  @UI.readOnly
  cumulativeSubawardConsortiumContractualCosts?: ResearchBudgetDecimal;

  @UI.label("Section K, Total Costs and Fee (I + J)")
  @UI.readOnly
  cumulativeTotalCostsFee: ResearchBudgetDecimal;

  @UI.label("Section G, Direct Costs (A thru F)")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].directCosts")
  @Validation.evaluationOrder(27)
  @UI.readOnly
  cumulativeTotalFundsRequestedDirectCosts: ResearchBudgetDecimal;

  @UI.label("Section I, Total Direct and Indirect Costs (G + H)")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].totalCosts")
  @Validation.evaluationOrder(29)
  @UI.readOnly
  cumulativeTotalFundsRequestedDirectIndirectCosts: ResearchBudgetDecimal;

  @UI.label("Section C, Equipment")
  @UI.readOnly
  cumulativeTotalFundsRequestedEquipment?: ResearchBudgetDecimal;

  @UI.label("Section H, Indirect Costs")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].indirectCosts.totalIndirectCosts")
  @Validation.evaluationOrder(28)
  @UI.readOnly
  cumulativeTotalFundsRequestedIndirectCost?: ResearchBudgetDecimal;

  @UI.label("Section F, Other Direct Costs")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].otherDirectCosts.totalOtherDirectCost")
  @Validation.evaluationOrder(19)
  @UI.readOnly
  cumulativeTotalFundsRequestedOtherDirectCosts?: ResearchBudgetDecimal;

  @UI.label("Section B, Other Personnel")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].otherPersonnel.totalOtherPersonnelFund")
  @Validation.evaluationOrder(12)
  @UI.readOnly
  cumulativeTotalFundsRequestedOtherPersonnel?: ResearchBudgetDecimal;

  @UI.label("Total Salary, Wages and Fringe Benefits (A + B)")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].totalCompensation")
  @Validation.evaluationOrder(14)
  @UI.readOnly
  cumulativeTotalFundsRequestedPersonnel: ResearchBudgetDecimal;

  @UI.label("Section A, Senior/Key Person")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].keyPersons.totalFundForKeyPersons")
  @Validation.evaluationOrder(11)
  @UI.readOnly
  cumulativeTotalFundsRequestedSeniorKeyPerson: ResearchBudgetDecimal;

  @UI.label("Section E, Participant/Trainee Support Costs")
  @UI.readOnly
  cumulativeTotalFundsRequestedTraineeCosts?: ResearchBudgetDecimal;

  @UI.label("Section D, Travel")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].travel.totalTravelCost")
  @Validation.evaluationOrder(15)
  @UI.readOnly
  cumulativeTotalFundsRequestedTravel?: ResearchBudgetDecimal;

  @UI.label("Total Number Other Personnel")
  @Validation.computedFrom(Op.Sum, "/budgetYear[*].otherPersonnel.otherPersonnelTotalNumber")
  @Validation.evaluationOrder(13)
  @UI.readOnly
  cumulativeTotalNoOtherPersonnel?: int32;

  @UI.label("2. Stipends")
  @UI.readOnly
  cumulativeTraineeStipends?: ResearchBudgetDecimal;

  @UI.label("4. Subsistence")
  @UI.readOnly
  cumulativeTraineeSubsistence?: ResearchBudgetDecimal;

  @UI.label("3. Travel")
  @UI.readOnly
  cumulativeTraineeTravel?: ResearchBudgetDecimal;

  @UI.label("1. Tuition/Fees/Health Insurance")
  @UI.readOnly
  cumulativeTraineeTuitionFeesHealthInsurance?: ResearchBudgetDecimal;
}

@UI.label("Equipment List")
model ResearchBudgetBudgetYearEquipmentEquipmentList {
  @UI.label("Equipment Item")
  @minLength(1)
  @maxLength(64)
  equipmentItem: string;

  @UI.label("Equipment Item Funds Requested")
  fundsRequested: ResearchBudgetDecimal;
}

/** Equipment costs for one research budget period. */
@Question.meta(#{ id: "budget/research/equipment" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
model ResearchBudgetBudgetYearEquipment {
  @UI.label("Additional Equipment:")
  @UI.widget(WidgetName.Attachment)
  additionalEquipmentsAttachment?: AttachmentRef;

  @minItems(0)
  @maxItems(10)
  equipmentList?: ResearchBudgetBudgetYearEquipmentEquipmentList[];

  @UI.label("Total Equipment")
  @UI.readOnly
  totalFund: ResearchBudgetDecimal;

  @UI.label("Total funds requested for all equipment listed in the attached file")
  totalFundForAttachedEquipment?: ResearchBudgetDecimal;
}

@UI.label("Indirect Cost")
model ResearchBudgetBudgetYearIndirectCostsIndirectCost {
  @UI.label("Indirect Cost Base")
  base?: ResearchBudgetDecimal;

  @UI.label("Indirect Cost Type")
  @minLength(1)
  @maxLength(64)
  costType: string;

  @UI.label("Indirect Costs Funds Requested")
  fundRequested: ResearchBudgetDecimal;

  @UI.label("Indirect Cost Rate")
  rate?: ResearchBudgetDecimal;
}

/** Indirect cost rates and requested amounts for one research budget period. */
@Question.meta(#{ id: "budget/research/indirect-costs" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
model ResearchBudgetBudgetYearIndirectCosts {
  @minItems(1)
  @maxItems(4)
  indirectCost: ResearchBudgetBudgetYearIndirectCostsIndirectCost[];

  @UI.label("Total Indirect Costs")
  @UI.readOnly
  totalIndirectCosts: ResearchBudgetDecimal;
}

model ResearchBudgetBudgetYearKeyPersonsKeyPersonName {
  @UI.label("First Name")
  @minLength(1)
  @maxLength(35)
  firstName: string;

  @UI.label("Last Name")
  @minLength(1)
  @maxLength(60)
  lastName: string;

  @UI.label("Middle Name")
  @minLength(1)
  @maxLength(25)
  middleName?: string;

  @UI.label("Prefix")
  @minLength(1)
  @maxLength(10)
  prefixName?: string;

  @UI.label("Suffix")
  @minLength(1)
  @maxLength(10)
  suffixName?: string;
}

@UI.label("Key Person")
model ResearchBudgetBudgetYearKeyPersonsKeyPerson {
  @UI.label("Senior/Key Person Academic Months")
  academicMonths?: ResearchBudgetDecimal;

  @UI.label("Senior/Key Person Base Salary")
  baseSalary?: ResearchBudgetDecimal;

  @UI.label("Senior/Key Person Calendar Months")
  calendarMonths?: ResearchBudgetDecimal;

  @UI.label("Senior/Key Person Fringe Benefits")
  fringeBenefits: ResearchBudgetDecimal;

  @UI.label("Senior/Key Person Funds Requested")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearKeyPersonsKeyPerson.requestedSalary, ResearchBudgetBudgetYearKeyPersonsKeyPerson.fringeBenefits)
  @Validation.evaluationOrder(1)
  @UI.readOnly
  fundsRequested: ResearchBudgetDecimal;

  @UI.label("Name")
  name: ResearchBudgetBudgetYearKeyPersonsKeyPersonName;

  @UI.label("Project Role:")
  @minLength(1)
  @maxLength(100)
  projectRole: string;

  @UI.label("Senior/Key Person Requested Salary")
  requestedSalary: ResearchBudgetDecimal;

  @UI.label("Senior/Key Person Summer Months")
  summerMonths?: ResearchBudgetDecimal;
}

/** Senior and key personnel compensation for one budget period. */
@Question.meta(#{ id: "budget/research/key-personnel" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.person)
model ResearchBudgetBudgetYearKeyPersons {
  @UI.label("Additional Senior Key Persons:")
  @UI.widget(WidgetName.Attachment)
  attachedKeyPersons?: AttachmentRef;

  @minItems(1)
  @maxItems(8)
  keyPerson: ResearchBudgetBudgetYearKeyPersonsKeyPerson[];

  @UI.label("Total Funds requested for all Senior Key Persons in the attached file")
  totalFundForAttachedKeyPersons?: ResearchBudgetDecimal;

  @UI.label("Total Senior/Key Person")
  @UI.readOnly
  totalFundForKeyPersons: ResearchBudgetDecimal;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost1 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost10 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost2 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost3 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost4 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost5 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost6 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost7 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost8 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost9 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

/** Other direct costs for one research budget period. */
@Question.meta(#{ id: "budget/research/other-direct-costs" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
model ResearchBudgetBudgetYearOtherDirectCosts {
  @UI.label("4. ADP/Computer Services")
  adpComputerServices?: ResearchBudgetDecimal;

  @UI.label("7. Alterations and Renovations")
  alterationsRenovations?: ResearchBudgetDecimal;

  @UI.label("3. Consultant Services")
  consultantServices?: ResearchBudgetDecimal;

  @UI.label("6. Equipment or Facility Rental/User Fees")
  equipmentRentalFee?: ResearchBudgetDecimal;

  @UI.label("1. Materials and Supplies")
  materialsSupplies?: ResearchBudgetDecimal;

  @UI.label("Other Direct Cost1")
  otherDirectCost1?: ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost1;

  @UI.label("Other Direct Cost10")
  otherDirectCost10?: ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost10;

  @UI.label("Other Direct Cost2")
  otherDirectCost2?: ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost2;

  @UI.label("Other Direct Cost3")
  otherDirectCost3?: ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost3;

  @UI.label("Other Direct Cost4")
  otherDirectCost4?: ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost4;

  @UI.label("Other Direct Cost5")
  otherDirectCost5?: ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost5;

  @UI.label("Other Direct Cost6")
  otherDirectCost6?: ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost6;

  @UI.label("Other Direct Cost7")
  otherDirectCost7?: ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost7;

  @UI.label("Other Direct Cost8")
  otherDirectCost8?: ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost8;

  @UI.label("Other Direct Cost9")
  otherDirectCost9?: ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost9;

  @UI.label("2. Publication Costs")
  publicationCosts?: ResearchBudgetDecimal;

  @UI.label("5. Subawards/Consortium/Contractual Costs")
  subawardConsortiumContractualCosts?: ResearchBudgetDecimal;

  @UI.label("Total Other Direct Costs")
  @UI.readOnly
  totalOtherDirectCost: ResearchBudgetDecimal;
}

model ResearchBudgetBudgetYearOtherPersonnelGraduateStudents {
  @UI.label("Academic Months Graduate Students")
  academicMonths?: ResearchBudgetDecimal;

  @UI.label("Calendar Months Graduate Students")
  calendarMonths?: ResearchBudgetDecimal;

  @UI.label("Fringe Benefits Graduate Students")
  fringeBenefits: ResearchBudgetDecimal;

  @UI.label("Funds Requested Graduate Students")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearOtherPersonnelGraduateStudents.requestedSalary, ResearchBudgetBudgetYearOtherPersonnelGraduateStudents.fringeBenefits)
  @Validation.evaluationOrder(3)
  @UI.readOnly
  fundsRequested: ResearchBudgetDecimal;

  @UI.label("Number of Personnel Graduate Students")
  numberOfPersonnel: int32;

  @UI.label("Project Role Graduate Students")
  @minLength(1)
  @maxLength(100)
  projectRole: string;

  @UI.label("Requested Salary Graduate Students")
  requestedSalary: ResearchBudgetDecimal;

  @UI.label("Summer Months Graduate Students")
  summerMonths?: ResearchBudgetDecimal;
}

@UI.label("Other")
model ResearchBudgetBudgetYearOtherPersonnelOther {
  @UI.label("Academic Months Additional Project Role")
  academicMonths?: ResearchBudgetDecimal;

  @UI.label("Calendar Months Additional Project Role")
  calendarMonths?: ResearchBudgetDecimal;

  @UI.label("Fringe Benefits Additional Project Role")
  fringeBenefits: ResearchBudgetDecimal;

  @UI.label("Funds Requested Additional Project Role")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearOtherPersonnelOther.requestedSalary, ResearchBudgetBudgetYearOtherPersonnelOther.fringeBenefits)
  @Validation.evaluationOrder(6)
  @UI.readOnly
  fundsRequested: ResearchBudgetDecimal;

  @UI.label("Number of Personnel Additional Project Role")
  numberOfPersonnel: int32;

  @UI.label("Additional Project Role Description")
  @minLength(1)
  @maxLength(100)
  projectRole: string;

  @UI.label("Requested Salary Additional Project Role")
  requestedSalary: ResearchBudgetDecimal;

  @UI.label("Summer Months Additional Project Role")
  summerMonths?: ResearchBudgetDecimal;
}

model ResearchBudgetBudgetYearOtherPersonnelPostDocAssociates {
  @UI.label("Academic Months Post Doctoral Associates")
  academicMonths?: ResearchBudgetDecimal;

  @UI.label("Calendar Months Post Doctoral Associates")
  calendarMonths?: ResearchBudgetDecimal;

  @UI.label("Fringe Benefits Post Doctoral Associates")
  fringeBenefits: ResearchBudgetDecimal;

  @UI.label("Funds Requested Post Doctoral Associates")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearOtherPersonnelPostDocAssociates.requestedSalary, ResearchBudgetBudgetYearOtherPersonnelPostDocAssociates.fringeBenefits)
  @Validation.evaluationOrder(2)
  @UI.readOnly
  fundsRequested: ResearchBudgetDecimal;

  @UI.label("Number of Personnel Post Doctoral Associates")
  numberOfPersonnel: int32;

  @UI.label("Project Role Post Doctoral Associates")
  @minLength(1)
  @maxLength(100)
  projectRole: string;

  @UI.label("Requested Salary Post Doctoral Associates")
  requestedSalary: ResearchBudgetDecimal;

  @UI.label("Summer Months Post Doctoral Associates")
  summerMonths?: ResearchBudgetDecimal;
}

model ResearchBudgetBudgetYearOtherPersonnelSecretarialClerical {
  @UI.label("Academic Months Secretarial/Clerical")
  academicMonths?: ResearchBudgetDecimal;

  @UI.label("Calendar Months Secretarial/Clerical")
  calendarMonths?: ResearchBudgetDecimal;

  @UI.label("Fringe Benefits Secretarial/Clerical")
  fringeBenefits: ResearchBudgetDecimal;

  @UI.label("Funds Requested Secretarial/Clerical")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearOtherPersonnelSecretarialClerical.requestedSalary, ResearchBudgetBudgetYearOtherPersonnelSecretarialClerical.fringeBenefits)
  @Validation.evaluationOrder(5)
  @UI.readOnly
  fundsRequested: ResearchBudgetDecimal;

  @UI.label("Number of Personnel Secretarial/Clerical")
  numberOfPersonnel: int32;

  @UI.label("Project Role Secretarial/Clerical")
  @minLength(1)
  @maxLength(100)
  projectRole: string;

  @UI.label("Requested Salary Secretarial/Clerical")
  requestedSalary: ResearchBudgetDecimal;

  @UI.label("Summer Months Secretarial/Clerical")
  summerMonths?: ResearchBudgetDecimal;
}

model ResearchBudgetBudgetYearOtherPersonnelUndergraduateStudents {
  @UI.label("Academic Months Undergraduate Students")
  academicMonths?: ResearchBudgetDecimal;

  @UI.label("Calendar Months Undergraduate Students")
  calendarMonths?: ResearchBudgetDecimal;

  @UI.label("Fringe Benefits Undergraduate Students")
  fringeBenefits: ResearchBudgetDecimal;

  @UI.label("Funds Requested Undergraduate Students")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearOtherPersonnelUndergraduateStudents.requestedSalary, ResearchBudgetBudgetYearOtherPersonnelUndergraduateStudents.fringeBenefits)
  @Validation.evaluationOrder(4)
  @UI.readOnly
  fundsRequested: ResearchBudgetDecimal;

  @UI.label("Number of Personnel Undergraduate Students")
  numberOfPersonnel: int32;

  @UI.label("Project Role Undergraduate Students")
  @minLength(1)
  @maxLength(100)
  projectRole: string;

  @UI.label("Requested Salary Undergraduate Students")
  requestedSalary: ResearchBudgetDecimal;

  @UI.label("Summer Months Undergraduate Students")
  summerMonths?: ResearchBudgetDecimal;
}

/** Other personnel compensation for one budget period. */
@Question.meta(#{ id: "budget/research/other-personnel" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.person)
model ResearchBudgetBudgetYearOtherPersonnel {
  @UI.label("Graduate Students")
  graduateStudents?: ResearchBudgetBudgetYearOtherPersonnelGraduateStudents;

  @minItems(0)
  @maxItems(6)
  other?: ResearchBudgetBudgetYearOtherPersonnelOther[];

  @UI.label("Total Number Other Personnel")
  @UI.readOnly
  otherPersonnelTotalNumber: int32;

  @UI.label("Post Doc Associates")
  postDocAssociates?: ResearchBudgetBudgetYearOtherPersonnelPostDocAssociates;

  @UI.label("Secretarial Clerical")
  secretarialClerical?: ResearchBudgetBudgetYearOtherPersonnelSecretarialClerical;

  @UI.label("Total Other Personnel")
  @UI.readOnly
  totalOtherPersonnelFund?: ResearchBudgetDecimal;

  @UI.label("Undergraduate Students")
  undergraduateStudents?: ResearchBudgetBudgetYearOtherPersonnelUndergraduateStudents;
}

model ResearchBudgetBudgetYearParticipantTraineeSupportCostsOther {
  @UI.label("Other Participant/Trainee Costs")
  cost: ResearchBudgetDecimal;

  @UI.label("5. Other")
  @minLength(1)
  @maxLength(100)
  description: string;
}

/** Participant and trainee support costs for one research budget period. */
@Question.meta(#{ id: "budget/research/participant-trainee-support" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
model ResearchBudgetBudgetYearParticipantTraineeSupportCosts {
  @UI.label("Other")
  other?: ResearchBudgetBudgetYearParticipantTraineeSupportCostsOther;

  @UI.label("Number of Participants/Trainees")
  participantTraineeNumber?: int32;

  @UI.label("2. Stipends")
  stipends?: ResearchBudgetDecimal;

  @UI.label("4. Subsistence")
  subsistence?: ResearchBudgetDecimal;

  @UI.label("Total Participant/Trainee Support Costs")
  @UI.readOnly
  totalCost: ResearchBudgetDecimal;

  @UI.label("3. Travel")
  travel?: ResearchBudgetDecimal;

  @UI.label("1. Tuition/Fees/Health Insurance")
  tuitionFeeHealthInsurance?: ResearchBudgetDecimal;
}

/** Domestic and foreign travel costs for one research budget period. */
@Question.meta(#{ id: "budget/research/travel" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
model ResearchBudgetBudgetYearTravel {
  @UI.label("1. Domestic Travel Costs ( Incl. Canada, Mexico and U.S. Possessions)")
  domesticTravelCost?: ResearchBudgetDecimal;

  @UI.label("2. Foreign Travel Costs")
  foreignTravelCost?: ResearchBudgetDecimal;

  @UI.label("Total Travel Cost")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearTravel.domesticTravelCost, ResearchBudgetBudgetYearTravel.foreignTravelCost)
  @Validation.evaluationOrder(8)
  @UI.readOnly
  totalTravelCost: ResearchBudgetDecimal;
}

/** A dated research budget period with personnel, direct, indirect, and total costs. */
@Question.meta(#{ id: "budget/research/period" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Budget Period")
model ResearchBudgetBudgetYear {
  @UI.label("End Date:")
  budgetPeriodEndDate: plainDate;

  @UI.label("Start Date:")
  budgetPeriodStartDate: plainDate;

  @UI.label("Cognizant Federal Agency (Agency Name, POC Name, and POC Phone Number)")
  @minLength(1)
  @maxLength(180)
  cognizantFederalAgency?: string;

  @UI.label("Total Direct Costs (A thru F)")
  @UI.readOnly
  directCosts: ResearchBudgetDecimal;

  @UI.label("Equipment")
  equipment?: ResearchBudgetBudgetYearEquipment;

  @UI.label("Fee")
  fee?: ResearchBudgetDecimal;

  @UI.label("Indirect Costs")
  indirectCosts?: ResearchBudgetBudgetYearIndirectCosts;

  @UI.label("Key Persons")
  keyPersons: ResearchBudgetBudgetYearKeyPersons;

  @UI.label("Other Direct Costs")
  otherDirectCosts?: ResearchBudgetBudgetYearOtherDirectCosts;

  @UI.label("Other Personnel")
  otherPersonnel?: ResearchBudgetBudgetYearOtherPersonnel;

  @UI.label("Participant Trainee Support Costs")
  participantTraineeSupportCosts?: ResearchBudgetBudgetYearParticipantTraineeSupportCosts;

  @UI.label("Total Salary, Wages and Fringe Benefits (A+B)")
  @Validation.computedFrom(Op.Sum, "keyPersons.totalFundForKeyPersons", "otherPersonnel.totalOtherPersonnelFund")
  @Validation.evaluationOrder(7)
  @UI.readOnly
  totalCompensation: ResearchBudgetDecimal;

  @UI.label("Total Direct and Indirect Institutional Costs (G + H)")
  @Validation.computedFrom(Op.Sum, "directCosts", "indirectCosts.totalIndirectCosts")
  @Validation.evaluationOrder(9)
  @UI.readOnly
  totalCosts: ResearchBudgetDecimal;

  @UI.label("Total Costs and Fee (I + J)")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYear.totalCosts, ResearchBudgetBudgetYear.fee)
  @Validation.evaluationOrder(10)
  @UI.readOnly
  totalCostsFee: ResearchBudgetDecimal;

  @UI.label("Travel")
  travel?: ResearchBudgetBudgetYearTravel;
}
