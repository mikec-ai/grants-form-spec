import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";
import "../budget/index.tsp";
import "../primary-org/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.Budget;
using QuestionBank.PrimaryOrg;

namespace QuestionBank.ResearchBudget;

/** The working areas shared by Research & Related budget compositions. */
enum ResearchBudgetSection {
  budgetOverview: "Budget overview",
  budgetYear: "Budget Year",
  budgetSummary: "Budget Summary",
}

// Source-wire numeric profiles. These remain distinct because the XSD assigns different
// signedness, precision, and bounds to amounts, totals, months, rates, and counts.
@Catalog.tag(TagName.money)
@pattern("^-?(?:\\d{1,14}|\\d{1,13}[.]\\d|\\d{1,12}[.]\\d{2})$")
@minLength(1)
@maxLength(16)
scalar ResearchBudgetDecimal14 extends string;

@Catalog.tag(TagName.money)
@pattern("^-?(?:\\d{1,15}|\\d{1,14}[.]\\d|\\d{1,13}[.]\\d{2})$")
@minLength(1)
@maxLength(17)
scalar ResearchBudgetDecimal15 extends string;

@Catalog.tag(TagName.money)
@pattern("^(?:\\d{1,14}|\\d{1,13}[.]\\d|\\d{1,12}[.]\\d{2})$")
@minLength(1)
@maxLength(15)
scalar ResearchBudgetAmount14 extends string;

@Catalog.tag(TagName.money)
@pattern("^(?:\\d{1,15}|\\d{1,14}[.]\\d|\\d{1,13}[.]\\d{2})$")
@minLength(1)
@maxLength(16)
scalar ResearchBudgetTotalAmount15 extends string;

@pattern("^-?(?:\\d{1,4}|\\d{1,3}[.]\\d|\\d{1,2}[.]\\d{2})$")
scalar ResearchBudgetMonth2Whole2Fraction extends string;

@pattern("^-?(?:\\d{1,5}|\\d{1,4}[.]\\d|\\d{1,3}[.]\\d{2})$")
scalar ResearchBudgetMonth3Whole2Fraction extends string;

@pattern("^(?:\\d{1,3}|\\d{1,3}[.]\\d|\\d{1,3}[.]\\d{2})$")
scalar ResearchBudgetIndirectRate extends string;

@minValue(0)
@maxValue(999)
@Catalog.tag(TagName.count)
scalar ResearchBudgetCount3 extends int32;

@minValue(0)
@maxValue(9999)
@Catalog.tag(TagName.count)
scalar ResearchBudgetCount4 extends int32;

/** Provide additional equipment details that do not fit in the structured equipment list. */
@Question.meta(#{ id: "budget/research/additional-equipment" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money, TagName.attachment)
scalar ResearchBudgetAdditionalEquipment extends AttachmentRef;

/** Provide additional senior or key-person details beyond the structured entries. */
@Question.meta(#{ id: "budget/research/additional-key-personnel" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.person, TagName.attachment)
scalar ResearchBudgetAdditionalKeyPersonnel extends AttachmentRef;

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
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.adpComputerServices")
  @Validation.evaluationOrder(19)
  @UI.readOnly
  cumulativeAdpComputerServices?: ResearchBudgetAmount14;

  @UI.label("7. Alterations and Renovations")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.alterationsRenovations")
  @Validation.evaluationOrder(20)
  @UI.readOnly
  cumulativeAlterationsAndRenovations?: ResearchBudgetAmount14;

  @UI.label("3. Consultant Services")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.consultantServices")
  @Validation.evaluationOrder(21)
  @UI.readOnly
  cumulativeConsultantServices?: ResearchBudgetAmount14;

  @UI.label("1. Domestic")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].travel.domesticTravelCost")
  @Validation.evaluationOrder(22)
  @UI.readOnly
  cumulativeDomesticTravelCosts?: ResearchBudgetAmount14;

  @UI.label("6. Equipment or Facility Rental/User Fees")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.equipmentRentalFee")
  @Validation.evaluationOrder(23)
  @UI.readOnly
  cumulativeEquipmentFacilityRentalFees?: ResearchBudgetAmount14;

  @UI.label("Section J, Fee")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].fee")
  @Validation.evaluationOrder(24)
  @UI.readOnly
  cumulativeFee?: ResearchBudgetTotalAmount15;

  @UI.label("2. Foreign")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].travel.foreignTravelCost")
  @Validation.evaluationOrder(25)
  @UI.readOnly
  cumulativeForeignTravelCosts?: ResearchBudgetAmount14;

  @UI.label("1. Materials and Supplies")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.materialsSupplies")
  @Validation.evaluationOrder(26)
  @UI.readOnly
  cumulativeMaterialAndSupplies?: ResearchBudgetAmount14;

  @UI.label("6. Number of Participants/Trainees")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].participantTraineeSupportCosts.participantTraineeNumber")
  @Validation.evaluationOrder(27)
  @UI.readOnly
  cumulativeNoofTrainees?: ResearchBudgetCount4;

  @UI.label("17. Other 10")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.otherDirectCost10.cost")
  @Validation.evaluationOrder(28)
  @UI.readOnly
  cumulativeOther10DirectCost?: ResearchBudgetAmount14;

  @UI.label("8. Other 1")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.otherDirectCost1.cost")
  @Validation.evaluationOrder(29)
  @UI.readOnly
  cumulativeOther1DirectCost?: ResearchBudgetAmount14;

  @UI.label("9. Other 2")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.otherDirectCost2.cost")
  @Validation.evaluationOrder(30)
  @UI.readOnly
  cumulativeOther2DirectCost?: ResearchBudgetAmount14;

  @UI.label("10. Other 3")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.otherDirectCost3.cost")
  @Validation.evaluationOrder(31)
  @UI.readOnly
  cumulativeOther3DirectCost?: ResearchBudgetAmount14;

  @UI.label("11. Other 4")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.otherDirectCost4.cost")
  @Validation.evaluationOrder(32)
  @UI.readOnly
  cumulativeOther4DirectCost?: ResearchBudgetAmount14;

  @UI.label("12. Other 5")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.otherDirectCost5.cost")
  @Validation.evaluationOrder(33)
  @UI.readOnly
  cumulativeOther5DirectCost?: ResearchBudgetAmount14;

  @UI.label("13. Other 6")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.otherDirectCost6.cost")
  @Validation.evaluationOrder(34)
  @UI.readOnly
  cumulativeOther6DirectCost?: ResearchBudgetAmount14;

  @UI.label("14. Other 7")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.otherDirectCost7.cost")
  @Validation.evaluationOrder(35)
  @UI.readOnly
  cumulativeOther7DirectCost?: ResearchBudgetAmount14;

  @UI.label("15. Other 8")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.otherDirectCost8.cost")
  @Validation.evaluationOrder(36)
  @UI.readOnly
  cumulativeOther8DirectCost?: ResearchBudgetAmount14;

  @UI.label("16. Other 9")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.otherDirectCost9.cost")
  @Validation.evaluationOrder(37)
  @UI.readOnly
  cumulativeOther9DirectCost?: ResearchBudgetAmount14;

  @UI.label("5. Other")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].participantTraineeSupportCosts.other.cost")
  @Validation.evaluationOrder(38)
  @UI.readOnly
  cumulativeOtherTraineeCost?: ResearchBudgetAmount14;

  @UI.label("2. Publication Costs")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.publicationCosts")
  @Validation.evaluationOrder(39)
  @UI.readOnly
  cumulativePublicationCosts?: ResearchBudgetAmount14;

  @UI.label("5. Subawards/Consortium/Contractual Costs")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.subawardConsortiumContractualCosts")
  @Validation.evaluationOrder(40)
  @UI.readOnly
  cumulativeSubawardConsortiumContractualCosts?: ResearchBudgetAmount14;

  @UI.label("Section K, Total Costs and Fee (I + J)")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].totalCostsFee")
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(41)
  @UI.readOnly
  cumulativeTotalCostsFee: ResearchBudgetTotalAmount15;

  @UI.label("Section G, Direct Costs (A thru F)")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].directCosts")
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(42)
  @UI.readOnly
  cumulativeTotalFundsRequestedDirectCosts: ResearchBudgetTotalAmount15;

  @UI.label("Section I, Total Direct and Indirect Costs (G + H)")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].totalCosts")
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(43)
  @UI.readOnly
  cumulativeTotalFundsRequestedDirectIndirectCosts: ResearchBudgetTotalAmount15;

  @UI.label("Section C, Equipment")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].equipment.totalFund")
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(44)
  @UI.readOnly
  cumulativeTotalFundsRequestedEquipment?: ResearchBudgetTotalAmount15;

  @UI.label("Section H, Indirect Costs")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].indirectCosts.totalIndirectCosts")
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(45)
  @UI.readOnly
  cumulativeTotalFundsRequestedIndirectCost?: ResearchBudgetTotalAmount15;

  @UI.label("Section F, Other Direct Costs")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherDirectCosts.totalOtherDirectCost")
  @Validation.evaluationOrder(46)
  @UI.readOnly
  cumulativeTotalFundsRequestedOtherDirectCosts?: ResearchBudgetTotalAmount15;

  @UI.label("Section B, Other Personnel")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherPersonnel.totalOtherPersonnelFund")
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(47)
  @UI.readOnly
  cumulativeTotalFundsRequestedOtherPersonnel?: ResearchBudgetTotalAmount15;

  @UI.label("Total Salary, Wages and Fringe Benefits (A + B)")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].totalCompensation")
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(48)
  @UI.readOnly
  cumulativeTotalFundsRequestedPersonnel: ResearchBudgetTotalAmount15;

  @UI.label("Section A, Senior/Key Person")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].keyPersons.totalFundForKeyPersons")
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(49)
  @UI.readOnly
  cumulativeTotalFundsRequestedSeniorKeyPerson: ResearchBudgetTotalAmount15;

  @UI.label("Section E, Participant/Trainee Support Costs")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].participantTraineeSupportCosts.totalCost")
  @Validation.evaluationOrder(50)
  @UI.readOnly
  cumulativeTotalFundsRequestedTraineeCosts?: ResearchBudgetTotalAmount15;

  @UI.label("Section D, Travel")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].travel.totalTravelCost")
  @Validation.evaluationOrder(51)
  @UI.readOnly
  cumulativeTotalFundsRequestedTravel?: ResearchBudgetTotalAmount15;

  @UI.label("Total Number Other Personnel")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].otherPersonnel.otherPersonnelTotalNumber")
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(52)
  @UI.readOnly
  cumulativeTotalNoOtherPersonnel?: ResearchBudgetCount4;

  @UI.label("2. Stipends")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].participantTraineeSupportCosts.stipends")
  @Validation.evaluationOrder(53)
  @UI.readOnly
  cumulativeTraineeStipends?: ResearchBudgetAmount14;

  @UI.label("4. Subsistence")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].participantTraineeSupportCosts.subsistence")
  @Validation.evaluationOrder(54)
  @UI.readOnly
  cumulativeTraineeSubsistence?: ResearchBudgetAmount14;

  @UI.label("3. Travel")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].participantTraineeSupportCosts.travel")
  @Validation.evaluationOrder(55)
  @UI.readOnly
  cumulativeTraineeTravel?: ResearchBudgetAmount14;

  @UI.label("1. Tuition/Fees/Health Insurance")
  @Validation.computedFrom(Op.Sum, "../budgetYear[*].participantTraineeSupportCosts.tuitionFeeHealthInsurance")
  @Validation.evaluationOrder(56)
  @UI.readOnly
  cumulativeTraineeTuitionFeesHealthInsurance?: ResearchBudgetAmount14;
}

@UI.label("Equipment List")
model ResearchBudgetBudgetYearEquipmentEquipmentList {
  @UI.label("Equipment Item")
  @minLength(1)
  @maxLength(64)
  equipmentItem: string;

  @UI.label("Equipment Item Funds Requested")
  fundsRequested: ResearchBudgetDecimal14;
}

/** Equipment costs for one research budget period. */
@Question.meta(#{ id: "budget/research/equipment" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@Validation.requiredPathWhenPositiveDecimalString(
  "additionalEquipmentsAttachment",
  "totalFundForAttachedEquipment"
)
@Validation.positiveDecimalStringWhenPathPresent(
  "totalFundForAttachedEquipment",
  "additionalEquipmentsAttachment"
)
model ResearchBudgetBudgetYearEquipment {
  @UI.label("Additional Equipment:")
  @UI.helpText("One possible attachment per budget period. Required if TotalFundForAttachedEquipment is entered and greater than zero.")
  @UI.widget(WidgetName.Attachment)
  additionalEquipmentsAttachment?: ResearchBudgetAdditionalEquipment;

  @minItems(0)
  @maxItems(10)
  equipmentList?: ResearchBudgetBudgetYearEquipmentEquipmentList[];

  @UI.label("Total Equipment")
  @Validation.computedFrom(Op.Sum, "equipmentList[*].fundsRequested", "totalFundForAttachedEquipment")
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(7)
  @UI.readOnly
  totalFund: ResearchBudgetDecimal15;

  @UI.label("Total funds requested for all equipment listed in the attached file")
  @UI.helpText("Required and must be greater than zero if an AdditionalEquipmentsAttachment exists.")
  totalFundForAttachedEquipment?: ResearchBudgetDecimal14;
}

@UI.label("Indirect Cost")
model ResearchBudgetBudgetYearIndirectCostsIndirectCost {
  @UI.label("Indirect Cost Base")
  base?: ResearchBudgetDecimal14;

  @UI.label("Indirect Cost Type")
  @minLength(1)
  @maxLength(64)
  costType: string;

  @UI.label("Indirect Costs Funds Requested")
  fundRequested: ResearchBudgetDecimal14;

  @UI.label("Indirect Cost Rate")
  rate?: ResearchBudgetIndirectRate;
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
  @Validation.computedFrom(Op.Sum, "indirectCost[*].fundRequested")
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(8)
  @UI.readOnly
  totalIndirectCosts: ResearchBudgetDecimal15;
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
  academicMonths?: ResearchBudgetMonth2Whole2Fraction;

  @UI.label("Senior/Key Person Base Salary")
  baseSalary?: ResearchBudgetDecimal14;

  @UI.label("Senior/Key Person Calendar Months")
  calendarMonths?: ResearchBudgetMonth2Whole2Fraction;

  @UI.label("Senior/Key Person Fringe Benefits")
  fringeBenefits: ResearchBudgetDecimal14;

  @UI.label("Senior/Key Person Funds Requested")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearKeyPersonsKeyPerson.requestedSalary, ResearchBudgetBudgetYearKeyPersonsKeyPerson.fringeBenefits)
  @Validation.evaluationOrder(1)
  @UI.readOnly
  fundsRequested: ResearchBudgetDecimal15;

  @UI.label("Name")
  name: ResearchBudgetBudgetYearKeyPersonsKeyPersonName;

  @UI.label("Project Role:")
  @minLength(1)
  @maxLength(100)
  projectRole: string;

  @UI.label("Senior/Key Person Requested Salary")
  requestedSalary: ResearchBudgetDecimal14;

  @UI.label("Senior/Key Person Summer Months")
  summerMonths?: ResearchBudgetMonth2Whole2Fraction;
}

/** Senior and key personnel compensation for one budget period. */
@Question.meta(#{ id: "budget/research/key-personnel" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.person)
@Validation.requiredPathWhenPositiveDecimalString(
  "attachedKeyPersons",
  "totalFundForAttachedKeyPersons"
)
@Validation.positiveDecimalStringWhenPathPresent(
  "totalFundForAttachedKeyPersons",
  "attachedKeyPersons"
)
model ResearchBudgetBudgetYearKeyPersons {
  @UI.label("Additional Senior Key Persons:")
  @UI.helpText("One possible attachment per budget period. Required if TotalFundForAttachedKeyPersons is entered and greater than zero.")
  @UI.widget(WidgetName.Attachment)
  attachedKeyPersons?: ResearchBudgetAdditionalKeyPersonnel;

  @minItems(1)
  @maxItems(8)
  keyPerson: ResearchBudgetBudgetYearKeyPersonsKeyPerson[];

  @UI.label("Total Funds requested for all Senior Key Persons in the attached file")
  @UI.helpText("Required and must be greater than zero if an AttachedKeyPersons attachment exists.")
  totalFundForAttachedKeyPersons?: ResearchBudgetDecimal15;

  @UI.label("Total Senior/Key Person")
  @Validation.computedFrom(Op.Sum, "keyPerson[*].fundsRequested", "totalFundForAttachedKeyPersons")
  @Validation.evaluationOrder(9)
  @UI.readOnly
  totalFundForKeyPersons: ResearchBudgetDecimal15;
}

/** Organization and budget identity shared by every Research & Related budget duration. */
model ResearchBudgetOverview {
  /** Unique Entity Identifier for the organization responsible for this budget. */
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
}

/** A complete five-period Research & Related budget. */
@Question.meta(#{ id: "budget/research/details" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money, TagName.details)
@UI.label("Research & Related Budget")
@UI.sections(ResearchBudgetSection)
model ResearchBudgetDetails {
  ...ResearchBudgetOverview;

  /** One to five budget periods for this project or subaward budget. */
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

/** A complete ten-period Research & Related budget. */
@Question.meta(#{ id: "budget/research/details-10yr" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money, TagName.details)
@UI.label("Research & Related Budget 10YR")
@UI.sections(ResearchBudgetSection)
model ResearchBudget10YrDetails {
  ...ResearchBudgetOverview;

  /** One to ten budget periods for this project or subaward budget. */
  @UI.label("Budget Year")
  @UI.section(ResearchBudgetSection.budgetYear)
  @minItems(1)
  @maxItems(10)
  budgetYear: ResearchBudgetBudgetYear[];

  /** Cumulative totals across every budget period. */
  @UI.label("Budget Summary")
  @UI.section(ResearchBudgetSection.budgetSummary)
  budgetSummary: ResearchBudgetBudgetSummary;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost1 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal14;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost10 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal14;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost2 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal14;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost3 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal14;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost4 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal14;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost5 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal14;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost6 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal14;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost7 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal14;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost8 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal14;

  @UI.label("Additional Other Direct Cost Description")
  @minLength(1)
  @maxLength(120)
  description: string;
}

model ResearchBudgetBudgetYearOtherDirectCostsOtherDirectCost9 {
  @UI.label("Additional Other Direct Cost Funds Requested")
  cost: ResearchBudgetDecimal14;

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
  adpComputerServices?: ResearchBudgetDecimal14;

  @UI.label("7. Alterations and Renovations")
  alterationsRenovations?: ResearchBudgetDecimal14;

  @UI.label("3. Consultant Services")
  consultantServices?: ResearchBudgetDecimal14;

  @UI.label("6. Equipment or Facility Rental/User Fees")
  equipmentRentalFee?: ResearchBudgetDecimal14;

  @UI.label("1. Materials and Supplies")
  materialsSupplies?: ResearchBudgetDecimal14;

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
  publicationCosts?: ResearchBudgetDecimal14;

  @UI.label("5. Subawards/Consortium/Contractual Costs")
  subawardConsortiumContractualCosts?: ResearchBudgetDecimal14;

  @UI.label("Total Other Direct Costs")
  @Validation.computedFrom(
    Op.Sum,
    "materialsSupplies",
    "publicationCosts",
    "consultantServices",
    "adpComputerServices",
    "subawardConsortiumContractualCosts",
    "equipmentRentalFee",
    "alterationsRenovations",
    "otherDirectCost1.cost",
    "otherDirectCost2.cost",
    "otherDirectCost3.cost",
    "otherDirectCost4.cost",
    "otherDirectCost5.cost",
    "otherDirectCost6.cost",
    "otherDirectCost7.cost",
    "otherDirectCost8.cost",
    "otherDirectCost9.cost",
    "otherDirectCost10.cost"
  )
  @Validation.evaluationOrder(10)
  @UI.readOnly
  totalOtherDirectCost: ResearchBudgetDecimal15;
}

model ResearchBudgetBudgetYearOtherPersonnelGraduateStudents {
  @UI.label("Academic Months Graduate Students")
  academicMonths?: ResearchBudgetMonth3Whole2Fraction;

  @UI.label("Calendar Months Graduate Students")
  calendarMonths?: ResearchBudgetMonth3Whole2Fraction;

  @UI.label("Fringe Benefits Graduate Students")
  fringeBenefits: ResearchBudgetDecimal14;

  @UI.label("Funds Requested Graduate Students")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearOtherPersonnelGraduateStudents.requestedSalary, ResearchBudgetBudgetYearOtherPersonnelGraduateStudents.fringeBenefits)
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(3)
  @UI.readOnly
  fundsRequested: ResearchBudgetDecimal15;

  @UI.label("Number of Personnel Graduate Students")
  numberOfPersonnel: ResearchBudgetCount3;

  @UI.label("Project Role Graduate Students")
  @minLength(1)
  @maxLength(100)
  projectRole: string;

  @UI.label("Requested Salary Graduate Students")
  requestedSalary: ResearchBudgetDecimal14;

  @UI.label("Summer Months Graduate Students")
  summerMonths?: ResearchBudgetMonth3Whole2Fraction;
}

@UI.label("Other")
model ResearchBudgetBudgetYearOtherPersonnelOther {
  @UI.label("Academic Months Additional Project Role")
  academicMonths?: ResearchBudgetMonth3Whole2Fraction;

  @UI.label("Calendar Months Additional Project Role")
  calendarMonths?: ResearchBudgetMonth3Whole2Fraction;

  @UI.label("Fringe Benefits Additional Project Role")
  fringeBenefits: ResearchBudgetDecimal14;

  @UI.label("Funds Requested Additional Project Role")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearOtherPersonnelOther.requestedSalary, ResearchBudgetBudgetYearOtherPersonnelOther.fringeBenefits)
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(6)
  @UI.readOnly
  fundsRequested: ResearchBudgetDecimal15;

  @UI.label("Number of Personnel Additional Project Role")
  numberOfPersonnel: ResearchBudgetCount3;

  @UI.label("Additional Project Role Description")
  @minLength(1)
  @maxLength(100)
  projectRole: string;

  @UI.label("Requested Salary Additional Project Role")
  requestedSalary: ResearchBudgetDecimal14;

  @UI.label("Summer Months Additional Project Role")
  summerMonths?: ResearchBudgetMonth3Whole2Fraction;
}

model ResearchBudgetBudgetYearOtherPersonnelPostDocAssociates {
  @UI.label("Academic Months Post Doctoral Associates")
  academicMonths?: ResearchBudgetMonth3Whole2Fraction;

  @UI.label("Calendar Months Post Doctoral Associates")
  calendarMonths?: ResearchBudgetMonth3Whole2Fraction;

  @UI.label("Fringe Benefits Post Doctoral Associates")
  fringeBenefits: ResearchBudgetDecimal14;

  @UI.label("Funds Requested Post Doctoral Associates")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearOtherPersonnelPostDocAssociates.requestedSalary, ResearchBudgetBudgetYearOtherPersonnelPostDocAssociates.fringeBenefits)
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(2)
  @UI.readOnly
  fundsRequested: ResearchBudgetDecimal15;

  @UI.label("Number of Personnel Post Doctoral Associates")
  numberOfPersonnel: ResearchBudgetCount3;

  @UI.label("Project Role Post Doctoral Associates")
  @minLength(1)
  @maxLength(100)
  projectRole: string;

  @UI.label("Requested Salary Post Doctoral Associates")
  requestedSalary: ResearchBudgetDecimal14;

  @UI.label("Summer Months Post Doctoral Associates")
  summerMonths?: ResearchBudgetMonth3Whole2Fraction;
}

model ResearchBudgetBudgetYearOtherPersonnelSecretarialClerical {
  @UI.label("Academic Months Secretarial/Clerical")
  academicMonths?: ResearchBudgetMonth3Whole2Fraction;

  @UI.label("Calendar Months Secretarial/Clerical")
  calendarMonths?: ResearchBudgetMonth3Whole2Fraction;

  @UI.label("Fringe Benefits Secretarial/Clerical")
  fringeBenefits: ResearchBudgetDecimal14;

  @UI.label("Funds Requested Secretarial/Clerical")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearOtherPersonnelSecretarialClerical.requestedSalary, ResearchBudgetBudgetYearOtherPersonnelSecretarialClerical.fringeBenefits)
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(5)
  @UI.readOnly
  fundsRequested: ResearchBudgetDecimal15;

  @UI.label("Number of Personnel Secretarial/Clerical")
  numberOfPersonnel: ResearchBudgetCount3;

  @UI.label("Project Role Secretarial/Clerical")
  @minLength(1)
  @maxLength(100)
  projectRole: string;

  @UI.label("Requested Salary Secretarial/Clerical")
  requestedSalary: ResearchBudgetDecimal14;

  @UI.label("Summer Months Secretarial/Clerical")
  summerMonths?: ResearchBudgetMonth3Whole2Fraction;
}

model ResearchBudgetBudgetYearOtherPersonnelUndergraduateStudents {
  @UI.label("Academic Months Undergraduate Students")
  academicMonths?: ResearchBudgetMonth3Whole2Fraction;

  @UI.label("Calendar Months Undergraduate Students")
  calendarMonths?: ResearchBudgetMonth3Whole2Fraction;

  @UI.label("Fringe Benefits Undergraduate Students")
  fringeBenefits: ResearchBudgetDecimal14;

  @UI.label("Funds Requested Undergraduate Students")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearOtherPersonnelUndergraduateStudents.requestedSalary, ResearchBudgetBudgetYearOtherPersonnelUndergraduateStudents.fringeBenefits)
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(4)
  @UI.readOnly
  fundsRequested: ResearchBudgetDecimal15;

  @UI.label("Number of Personnel Undergraduate Students")
  numberOfPersonnel: ResearchBudgetCount3;

  @UI.label("Project Role Undergraduate Students")
  @minLength(1)
  @maxLength(100)
  projectRole: string;

  @UI.label("Requested Salary Undergraduate Students")
  requestedSalary: ResearchBudgetDecimal14;

  @UI.label("Summer Months Undergraduate Students")
  summerMonths?: ResearchBudgetMonth3Whole2Fraction;
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
  @Validation.computedFrom(
    Op.Sum,
    "postDocAssociates.numberOfPersonnel",
    "graduateStudents.numberOfPersonnel",
    "undergraduateStudents.numberOfPersonnel",
    "secretarialClerical.numberOfPersonnel",
    "other[*].numberOfPersonnel"
  )
  @Validation.evaluationOrder(11)
  @UI.readOnly
  otherPersonnelTotalNumber: ResearchBudgetCount4;

  @UI.label("Post Doc Associates")
  postDocAssociates?: ResearchBudgetBudgetYearOtherPersonnelPostDocAssociates;

  @UI.label("Secretarial Clerical")
  secretarialClerical?: ResearchBudgetBudgetYearOtherPersonnelSecretarialClerical;

  @UI.label("Total Other Personnel")
  @Validation.computedFrom(
    Op.Sum,
    "postDocAssociates.fundsRequested",
    "graduateStudents.fundsRequested",
    "undergraduateStudents.fundsRequested",
    "secretarialClerical.fundsRequested",
    "other[*].fundsRequested"
  )
  @Validation.evaluationOrder(12)
  @UI.readOnly
  totalOtherPersonnelFund?: ResearchBudgetDecimal15;

  @UI.label("Undergraduate Students")
  undergraduateStudents?: ResearchBudgetBudgetYearOtherPersonnelUndergraduateStudents;
}

model ResearchBudgetBudgetYearParticipantTraineeSupportCostsOther {
  @UI.label("Other Participant/Trainee Costs")
  cost: ResearchBudgetDecimal14;

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
  participantTraineeNumber?: ResearchBudgetCount3;

  @UI.label("2. Stipends")
  stipends?: ResearchBudgetDecimal14;

  @UI.label("4. Subsistence")
  subsistence?: ResearchBudgetDecimal14;

  @UI.label("Total Participant/Trainee Support Costs")
  @Validation.computedFrom(
    Op.Sum,
    "tuitionFeeHealthInsurance",
    "stipends",
    "travel",
    "subsistence",
    "other.cost"
  )
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(13)
  @UI.readOnly
  totalCost: ResearchBudgetDecimal15;

  @UI.label("3. Travel")
  travel?: ResearchBudgetDecimal14;

  @UI.label("1. Tuition/Fees/Health Insurance")
  tuitionFeeHealthInsurance?: ResearchBudgetDecimal14;
}

/** Domestic and foreign travel costs for one research budget period. */
@Question.meta(#{ id: "budget/research/travel" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
model ResearchBudgetBudgetYearTravel {
  @UI.label("1. Domestic Travel Costs ( Incl. Canada, Mexico and U.S. Possessions)")
  domesticTravelCost?: ResearchBudgetDecimal14;

  @UI.label("2. Foreign Travel Costs")
  foreignTravelCost?: ResearchBudgetDecimal14;

  @UI.label("Total Travel Cost")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYearTravel.domesticTravelCost, ResearchBudgetBudgetYearTravel.foreignTravelCost)
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(14)
  @UI.readOnly
  totalTravelCost: ResearchBudgetDecimal15;
}

/** A dated research budget period with personnel, direct, indirect, and total costs. */
@Question.meta(#{ id: "budget/research/period" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
@UI.label("Budget Period")
@Validation.atLeastOnePathWhenPresent(
  "participantTraineeSupportCosts.other",
  "otherDirectCosts.otherDirectCost1.description",
  "otherDirectCosts.otherDirectCost2.description",
  "otherDirectCosts.otherDirectCost3.description",
  "otherDirectCosts.otherDirectCost4.description",
  "otherDirectCosts.otherDirectCost5.description",
  "otherDirectCosts.otherDirectCost6.description",
  "otherDirectCosts.otherDirectCost7.description",
  "otherDirectCosts.otherDirectCost8.description",
  "otherDirectCosts.otherDirectCost9.description",
  "otherDirectCosts.otherDirectCost10.description"
)
model ResearchBudgetBudgetYear {
  @UI.label("End Date:")
  @Validation.notBefore(ResearchBudgetBudgetYear.budgetPeriodStartDate)
  @UI.helpText("End Date cannot be before Start Date.")
  budgetPeriodEndDate: plainDate;

  @UI.label("Start Date:")
  budgetPeriodStartDate: plainDate;

  @UI.label("Cognizant Federal Agency (Agency Name, POC Name, and POC Phone Number)")
  @minLength(1)
  @maxLength(180)
  cognizantFederalAgency?: string;

  @UI.label("Total Direct Costs (A thru F)")
  @Validation.computedFrom(
    Op.Sum,
    "keyPersons.totalFundForKeyPersons",
    "otherPersonnel.totalOtherPersonnelFund",
    "equipment.totalFund",
    "travel.totalTravelCost",
    "participantTraineeSupportCosts.totalCost",
    "otherDirectCosts.totalOtherDirectCost"
  )
  @Validation.evaluationOrder(16)
  @UI.readOnly
  directCosts: ResearchBudgetDecimal15;

  @UI.label("Equipment")
  equipment?: ResearchBudgetBudgetYearEquipment;

  @UI.label("Fee")
  fee?: ResearchBudgetAmount14;

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
  @Validation.evaluationOrder(15)
  @UI.readOnly
  totalCompensation: ResearchBudgetDecimal15;

  @UI.label("Total Direct and Indirect Institutional Costs (G + H)")
  @Validation.computedFrom(Op.Sum, "directCosts", "indirectCosts.totalIndirectCosts")
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(17)
  @UI.readOnly
  totalCosts: ResearchBudgetDecimal15;

  @UI.label("Total Costs and Fee (I + J)")
  @Validation.computed(Op.Sum, ResearchBudgetBudgetYear.totalCosts, ResearchBudgetBudgetYear.fee)
  @Validation.materializeWhenAnySourcePresent
  @Validation.evaluationOrder(18)
  @UI.readOnly
  totalCostsFee: ResearchBudgetTotalAmount15;

  @UI.label("Travel")
  travel?: ResearchBudgetBudgetYearTravel;
}
