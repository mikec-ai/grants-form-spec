import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/generics/index.tsp";
import "../question-bank/research-application/index.tsp";
import "../question-bank/sbir-sttr/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.ResearchApplication;
using QuestionBank.SbirSttr;

namespace Forms.SbirSttrInformation;

enum SbirSttrInformationSection {
  allApplicants: "All Applicants",
  sbir: "SBIR-Specific Questions",
  sttr: "STTR-Specific Questions",
}

/** SBIR/STTR Information, Grants.gov FID 787, version 3.0. */
@Form.meta(#{
  id: "sbir-sttr-information",
  legacyFormId: 787,
  formName: "SBIR/STTR Information",
  shortFormName: "SBIR_STTR_Information_3_0",
  formVersion: "3.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0001",
})
@UI.sections(SbirSttrInformationSection)
@UI.overrides(#{
  otherAgency: #{ enabledWhen: #{ path: "agency.value", equals: SbirSttrAgencyCode.other } },
  federalSubcontractorNames: #{ enabledWhen: #{ path: "federalSubcontractsIncluded.value", equals: YesNoCode.yes } },
  nonDomesticPerformanceExplanation: #{ enabledWhen: #{ path: "domesticPerformance.value", equals: YesNoCode.no } },
  equivalentWorkFederalAgencies: #{ enabledWhen: #{ path: "equivalentFederalWork.value", equals: YesNoCode.yes } },
  `phaseIIAwardsReceived.value`: #{ enabledWhen: #{ path: "programType.value", in: #[SbirSttrProgramTypeCode.sbir, SbirSttrProgramTypeCode.both] } },
  commercializationHistory: #{ enabledWhen: #{ path: "phaseIIAwardsReceived.value", equals: YesNoCode.yes } },
  `pdpiPrimaryEmployment.value`: #{ enabledWhen: #{ path: "programType.value", in: #[SbirSttrProgramTypeCode.sbir, SbirSttrProgramTypeCode.both] } },
  `pdpiAppointmentAndEffort.value`: #{ enabledWhen: #{ path: "programType.value", in: #[SbirSttrProgramTypeCode.sttr, SbirSttrProgramTypeCode.both] } },
  `jointPerformancePercentage.value`: #{ enabledWhen: #{ path: "programType.value", in: #[SbirSttrProgramTypeCode.sttr, SbirSttrProgramTypeCode.both] } },
  nonprofitResearchPartnerUei: #{ enabledWhen: #{ path: "programType.value", in: #[SbirSttrProgramTypeCode.sttr, SbirSttrProgramTypeCode.both] } },
})
model SbirSttrInformation {
  @UI.section(SbirSttrInformationSection.allApplicants)
  agency: QuestionSbirSttrAgency;

  @UI.label("Other Agency")
  @UI.section(SbirSttrInformationSection.allApplicants)
  @Validation.requiredWhenPath("agency.value", SbirSttrAgencyCode.other)
  otherAgency?: QuestionSbirSttrOtherAgency;

  @UI.label("SBC Control ID")
  @UI.helpText("Enter the 9 digit SBC Control ID obtained from the Small Business Administration.")
  @UI.section(SbirSttrInformationSection.allApplicants)
  sbcControlId: QuestionSbcControlId;

  @UI.section(SbirSttrInformationSection.allApplicants)
  programType: QuestionSbirSttrProgramType;

  @UI.section(SbirSttrInformationSection.allApplicants)
  applicationType: QuestionSbirSttrApplicationType;

  @UI.label("Phase I Letter of Intent Number")
  @UI.section(SbirSttrInformationSection.allApplicants)
  phaseILetterOfIntentNumber?: QuestionSbirSttrPhaseILetterOfIntentNumber;

  @UI.label("Agency Topic/Subtopic")
  @UI.helpText("Enter Agency Topic/Subtopic. This field is required for DOE and otherwise optional.")
  @UI.section(SbirSttrInformationSection.allApplicants)
  @Validation.requiredWhenPath("agency.value", SbirSttrAgencyCode.doe)
  agencyTopicSubtopic?: QuestionSbirSttrAgencyTopicSubtopic;

  @UI.section(SbirSttrInformationSection.allApplicants)
  smallBusinessEligibility: QuestionSbirSttrSmallBusinessEligibility;

  @UI.label("Anticipated Number of personnel to be employed at your organization at the time of award")
  @UI.section(SbirSttrInformationSection.allApplicants)
  numberOfEmployees: QuestionSbirSttrEmployeeCount;

  @UI.section(SbirSttrInformationSection.allApplicants)
  vcocOwnership: QuestionSbirSttrVcocOwnership;

  @UI.section(SbirSttrInformationSection.allApplicants)
  facultyStudentOwnership: QuestionSbirSttrFacultyStudentOwnership;

  @UI.section(SbirSttrInformationSection.allApplicants)
  federalSubcontractsIncluded: QuestionSbirSttrFederalSubcontractsIncluded;

  @UI.label("Names of Federal Laboratories/Agencies")
  @UI.section(SbirSttrInformationSection.allApplicants)
  @Validation.requiredWhenPath("federalSubcontractsIncluded.value", YesNoCode.yes)
  federalSubcontractorNames?: QuestionSbirSttrFederalSubcontractorNames;

  @UI.section(SbirSttrInformationSection.allApplicants)
  hubzoneLocation: QuestionSbirSttrHubzoneLocation;

  @UI.section(SbirSttrInformationSection.allApplicants)
  domesticPerformance: QuestionSbirSttrDomesticPerformance;

  @UI.label("Explanation")
  @UI.helpText("If you answered No, attach an explanation of the research and development performed outside the United States.")
  @UI.section(SbirSttrInformationSection.allApplicants)
  @UI.widget(WidgetName.Attachment)
  @Validation.requiredWhenPath("domesticPerformance.value", YesNoCode.no)
  nonDomesticPerformanceExplanation?: QuestionSbirSttrNonDomesticPerformanceExplanation;

  @UI.section(SbirSttrInformationSection.allApplicants)
  equivalentFederalWork: QuestionSbirSttrEquivalentFederalWork;

  @UI.label("Names of other Federal agencies")
  @UI.section(SbirSttrInformationSection.allApplicants)
  @Validation.requiredWhenPath("equivalentFederalWork.value", YesNoCode.yes)
  equivalentWorkFederalAgencies?: QuestionSbirSttrEquivalentWorkFederalAgencies;

  @UI.section(SbirSttrInformationSection.allApplicants)
  disclosurePermission: QuestionSbirSttrDisclosurePermission;

  @UI.section(SbirSttrInformationSection.allApplicants)
  tabaFundingRequest: QuestionSbirSttrTabaFundingRequest;

  // The source-specific compound commercialization-plan rule conflicts with current NIH policy.
  @UI.label("Commercialization Plan")
  @UI.helpText("Include a Commercialization Plan in accordance with the agency announcement and agency-specific instructions. The source-specific requirement is preserved as unresolved policy evidence.")
  @UI.section(SbirSttrInformationSection.allApplicants)
  @UI.widget(WidgetName.Attachment)
  commercializationPlan?: QuestionSbirSttrCommercializationPlan;

  @UI.section(SbirSttrInformationSection.sbir)
  @Validation.requiredWhenPath("programType.value", SbirSttrProgramTypeCode.sbir)
  @Validation.requiredWhenPath("programType.value", SbirSttrProgramTypeCode.both)
  phaseIIAwardsReceived?: QuestionSbirSttrPhaseIIAwardsReceived;

  @UI.label("Commercialization History")
  @UI.helpText("If you answered Yes to the SBIR Phase II awards question, attach a company commercialization history in accordance with agency-specific instructions.")
  @UI.section(SbirSttrInformationSection.sbir)
  @UI.widget(WidgetName.Attachment)
  @Validation.requiredWhenPath("phaseIIAwardsReceived.value", YesNoCode.yes)
  commercializationHistory?: QuestionSbirSttrCommercializationHistory;

  @UI.section(SbirSttrInformationSection.sbir)
  @Validation.requiredWhenPath("programType.value", SbirSttrProgramTypeCode.sbir)
  @Validation.requiredWhenPath("programType.value", SbirSttrProgramTypeCode.both)
  pdpiPrimaryEmployment?: QuestionSbirSttrPdpiPrimaryEmployment;

  @UI.section(SbirSttrInformationSection.sttr)
  @Validation.requiredWhenPath("programType.value", SbirSttrProgramTypeCode.sttr)
  @Validation.requiredWhenPath("programType.value", SbirSttrProgramTypeCode.both)
  pdpiAppointmentAndEffort?: QuestionSbirSttrPdpiAppointmentAndEffort;

  @UI.section(SbirSttrInformationSection.sttr)
  @Validation.requiredWhenPath("programType.value", SbirSttrProgramTypeCode.sttr)
  @Validation.requiredWhenPath("programType.value", SbirSttrProgramTypeCode.both)
  jointPerformancePercentage?: QuestionSbirSttrJointPerformancePercentage;

  @UI.label("UEI of non-profit research partner for STTR")
  @UI.helpText("Enter the 12-character UEI of the non-profit research partner for STTR.")
  @UI.section(SbirSttrInformationSection.sttr)
  @Validation.requiredWhenPath("programType.value", SbirSttrProgramTypeCode.sttr)
  @Validation.requiredWhenPath("programType.value", SbirSttrProgramTypeCode.both)
  nonprofitResearchPartnerUei?: QuestionSbirSttrNonprofitResearchPartnerUei;
}
