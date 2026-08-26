import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";
import "../research-project/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

/** Portable questions and dimensional structures for human-subject study records. */
namespace QuestionBank.ClinicalStudy;

enum ClinicalYesNo { yes: "Y: Yes", no: "N: No" }
enum ClinicalYesNoNotApplicable { yes: "Y: Yes", no: "N: No", notApplicable: "NA: Not Applicable" }
enum EnrollmentLocationType { domestic: "Domestic", foreign: "Foreign" }
enum EnrollmentAnticipatedActual { anticipated: "Anticipated", actual: "Actual" }
enum ClinicalRecruitmentStatus { notYetRecruiting: "Not yet recruiting", recruiting: "Recruiting", enrollingByInvitation: "Enrolling by invitation", activeNotRecruiting: "Active, not recruiting", completed: "Completed", suspended: "Suspended", terminated: "Terminated (Halted Prematurely)", withdrawn: "Withdrawn (No Participants Enrolled)" }
enum ClinicalPrimaryPurpose { treatment: "Treatment", prevention: "Prevention", diagnostics: "Diagnostics", supportiveCare: "Supportive Care", screening: "Screening", healthServicesResearch: "Health Services Research", basicScience: "Basic Science", deviceFeasibility: "Device Feasibility", other: "Other" }
enum ClinicalInterventionType { drug: "Drug (including placebo)", device: "Device (including sham)", biologicalVaccine: "Biological/Vaccine", procedureSurgery: "Procedure/Surgery", radiation: "Radiation", behavioral: "Behavioral (e.g., Psychotherapy, Lifestyle Counseling)", genetic: "Genetic (including gene transfer, stem cell and recombinant DNA)", dietarySupplement: "Dietary Supplement (e.g., vitamins, minerals)", combinationProduct: "Combination Product", diagnosticTest: "Diagnostic Test", other: "Other" }
enum ClinicalStudyPhase { earlyPhase1: "Early Phase 1 (or Phase 0)", phase1: "Phase 1", phase1Phase2: "Phase 1/2", phase2: "Phase 2", phase2Phase3: "Phase 2/3", phase3: "Phase 3", phase4: "Phase 4", notApplicable: "N/A" }
enum ClinicalInterventionModel { singleGroup: "Single Group", parallel: "Parallel", crossover: "Cross-Over", factorial: "Factorial", sequential: "Sequential", other: "Other" }
enum ClinicalAllocation { randomized: "Randomized", nonRandomized: "Non-randomized", notApplicable: "N/A" }
enum ClinicalOutcomeType { primary: "Primary", secondary: "Secondary", other: "Other" }
enum ClinicalAgeUnit { years: "Years", months: "Months", weeks: "Weeks", days: "Days", hours: "Hours", minutes: "Minutes", noLimit: "N/A (No limit)" }

@minValue(0) @maxValue(999999999) scalar ClinicalCount9 extends integer;
@minValue(0) @maxValue(9999999999) scalar ClinicalCount10 extends integer;
@minValue(0) @maxValue(99999999999) scalar ClinicalCount11 extends integer;

@maxLength(255)
@minLength(1)
scalar ClinicalConditionOrFocus extends string;

/** Whether any proposed research involves human specimens and/or data. */
@Question.meta(#{ id: "clinical-study/involves-human-specimens-or-data", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
@pattern("^(Y: Yes|N: No)$")
scalar QuestionInvolvesHumanSpecimensOrData extends string;

/** Explain use of human specimens or data that is not human-subjects research. */
@Question.meta(#{ id: "clinical-study/non-human-subjects-specimens-explanation", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar HumanSpecimensExplanation extends AttachmentRef;

/** Provide information requested by the awarding component outside study records. */
@Question.meta(#{ id: "clinical-study/other-requested-information", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar HumanSubjectsOtherRequestedInformation extends AttachmentRef;

/** Provide the justification for a delayed-onset human-subject study. */
@Question.meta(#{ id: "clinical-study/delayed-onset-justification", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar DelayedOnsetJustification extends AttachmentRef;

/** Explain inclusion of individuals across the lifespan. */
@Question.meta(#{ id: "clinical-study/inclusion-across-lifespan", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar InclusionAcrossLifespanDocument extends AttachmentRef;

/** Explain inclusion of women and racial or ethnic minority groups. */
@Question.meta(#{ id: "clinical-study/inclusion-women-minorities", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar InclusionWomenMinoritiesDocument extends AttachmentRef;

/** Provide the recruitment and retention plan. */
@Question.meta(#{ id: "clinical-study/recruitment-retention-plan", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar RecruitmentRetentionPlanDocument extends AttachmentRef;

/** Provide the study timeline. */
@Question.meta(#{ id: "clinical-study/study-timeline", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar StudyTimelineDocument extends AttachmentRef;

/** Address protection of human subjects. */
@Question.meta(#{ id: "clinical-study/protection-human-subjects", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ProtectionHumanSubjectsDocument extends AttachmentRef;

/** Provide the single-IRB plan. */
@Question.meta(#{ id: "clinical-study/single-irb-plan", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar SingleIrbPlanDocument extends AttachmentRef;

/** Provide the data and safety monitoring plan. */
@Question.meta(#{ id: "clinical-study/data-safety-monitoring-plan", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar DataSafetyMonitoringPlanDocument extends AttachmentRef;

/** Describe the overall study-team structure. */
@Question.meta(#{ id: "clinical-study/study-team-structure", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar StudyTeamStructureDocument extends AttachmentRef;

/** Provide the statistical design and power analysis. */
@Question.meta(#{ id: "clinical-study/statistical-design-power", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar StatisticalDesignPowerDocument extends AttachmentRef;

/** Describe availability of the investigational product. */
@Question.meta(#{ id: "clinical-study/investigational-product-availability", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar InvestigationalAvailabilityDocument extends AttachmentRef;

/** Provide the clinical-trial dissemination plan. */
@Question.meta(#{ id: "clinical-study/dissemination-plan", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar DisseminationPlanDocument extends AttachmentRef;

/** Provide one NOFO-authorized other clinical-trial document. */
@Question.meta(#{ id: "clinical-study/other-clinical-trial-document", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar OtherClinicalTrialDocument extends AttachmentRef;

/** Describe one delayed-onset study whose specific plans are not yet available. */
@Question.meta(#{ id: "clinical-study/delayed-onset-study", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
@UI.label("Delayed Onset Study")
model DelayedOnsetStudy {
  @maxLength(600)
  @minLength(1)
  studyTitle: string;
  anticipatedClinicalTrial?: ClinicalYesNo;
  justification: DelayedOnsetJustification;
}

/** Four source questions used together to determine whether a study is a clinical trial. */
@Question.meta(#{ id: "clinical-study/clinical-trial-questionnaire", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
model ClinicalTrialQuestionnaire {
  humanParticipants: ClinicalYesNo;
  prospectivelyAssignedIntervention: ClinicalYesNo;
  evaluatesIntervention: ClinicalYesNo;
  healthRelatedOutcome: ClinicalYesNo;
}

/** One age boundary expressed as a numeric value and source-defined unit. */
model ClinicalAgeLimit {
  @minValue(0)
  @maxValue(999)
  value?: int32;
  unit: ClinicalAgeUnit;
}

model ClinicalAgeLimits {
  minimum?: ClinicalAgeLimit;
  maximum?: ClinicalAgeLimit;
}

model FirstSubjectEnrollment {
  date: plainDate;
  anticipatedActual: EnrollmentAnticipatedActual;
}

/** Counts for the source racial categories at one ethnicity/sex coordinate. */
model PlannedRaceCounts {
  americanIndianAlaskaNative?: ClinicalCount9;
  asian?: ClinicalCount9;
  nativeHawaiianPacificIslander?: ClinicalCount9;
  blackAfricanAmerican?: ClinicalCount9;
  white?: ClinicalCount9;
  moreThanOneRace?: ClinicalCount9;
  // The source XSD and pinned parent DAT do not establish derivation. Totals remain
  // entered/observed values until exact embedded-study behavior evidence is pinned.
  total?: ClinicalCount10;
}

model CumulativeRaceCounts extends PlannedRaceCounts {
  unknownNotReported?: ClinicalCount9;
}

model PlannedTotalCounts {
  americanIndianAlaskaNative?: ClinicalCount10;
  asian?: ClinicalCount10;
  nativeHawaiianPacificIslander?: ClinicalCount10;
  blackAfricanAmerican?: ClinicalCount10;
  white?: ClinicalCount10;
  moreThanOneRace?: ClinicalCount10;
  total?: ClinicalCount11;
}

model CumulativeTotalCounts extends PlannedTotalCounts {
  unknownNotReported?: ClinicalCount10;
}

model PlannedEthnicityCounts {
  female?: PlannedRaceCounts;
  male?: PlannedRaceCounts;
}

model CumulativeEthnicityCounts {
  female?: CumulativeRaceCounts;
  male?: CumulativeRaceCounts;
  unknownNotReportedSex?: CumulativeRaceCounts;
}

model PlannedEnrollmentMatrix {
  notHispanicLatino?: PlannedEthnicityCounts;
  hispanicLatino?: PlannedEthnicityCounts;
  total?: PlannedTotalCounts;
}

model CumulativeEnrollmentMatrix {
  notHispanicLatino?: CumulativeEthnicityCounts;
  hispanicLatino?: CumulativeEthnicityCounts;
  unknownNotReportedEthnicity?: CumulativeEthnicityCounts;
  total?: CumulativeTotalCounts;
}

/** Enrollment count measure instantiated by reporting period, ethnicity, sex, and race. */
@Question.meta(#{ id: "clinical-study/inclusion-enrollment-report", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.count, TagName.details)
@UI.label("Inclusion Enrollment Report")
model InclusionEnrollmentReport {
  @maxLength(600)
  @minLength(1)
  title: string;
  usesExistingDatasetOrResource: ClinicalYesNo;
  locationType: EnrollmentLocationType;
  @maxItems(200)
  enrollmentCountries?: CountryCode[];
  @maxLength(255)
  @minLength(1)
  enrollmentLocations?: string;
  @maxLength(500)
  @minLength(1)
  comments?: string;
  planned?: PlannedEnrollmentMatrix;
  cumulativeActual?: CumulativeEnrollmentMatrix;
}

/** Embedded-study occurrence of the shared report with its source-owned technical identifier. */
@UI.label("Inclusion Enrollment Report")
model EmbeddedInclusionEnrollmentReport extends InclusionEnrollmentReport {
  @Response.role(ResponseRole.systemValue)
  @UI.readOnly
  @maxLength(40)
  @minLength(1)
  reportId?: string;
}

/** Population, eligibility, inclusion, recruitment, and enrollment information for one study. */
@Question.meta(#{ id: "clinical-study/population-characteristics", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
model StudyPopulationCharacteristics {
  @maxItems(20)
  conditionsOrFocus?: ClinicalConditionOrFocus[];
  @maxLength(15000)
  @minLength(1)
  eligibilityCriteria?: string;
  ageLimits?: ClinicalAgeLimits;
  inclusionAcrossLifespan?: InclusionAcrossLifespanDocument;
  inclusionWomenMinorities?: InclusionWomenMinoritiesDocument;
  recruitmentRetentionPlan?: RecruitmentRetentionPlanDocument;
  recruitmentStatus?: ClinicalRecruitmentStatus;
  studyTimeline?: StudyTimelineDocument;
  firstSubjectEnrollment?: FirstSubjectEnrollment;
  @maxItems(20)
  inclusionEnrollmentReports?: EmbeddedInclusionEnrollmentReport[];
}

/** Protection and monitoring plans for one human-subject study. */
@Question.meta(#{ id: "clinical-study/protection-monitoring", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details, TagName.attachment)
model ProtectionMonitoringPlans {
  protectionOfHumanSubjects?: ProtectionHumanSubjectsDocument;
  multiSiteStudy?: ClinicalYesNoNotApplicable;
  singleIrbPlan?: SingleIrbPlanDocument;
  dataSafetyMonitoringPlan?: DataSafetyMonitoringPlanDocument;
  monitoringBoardAppointed?: ClinicalYesNo;
  studyTeamStructure?: StudyTeamStructureDocument;
}

model ClinicalIntervention {
  type: ClinicalInterventionType;
  @maxLength(200)
  @minLength(1)
  name: string;
  @maxLength(1000)
  @minLength(1)
  description: string;
}

model ClinicalMaskingParties {
  participant?: ClinicalYesNo;
  careProvider?: ClinicalYesNo;
  investigator?: ClinicalYesNo;
  outcomesAssessor?: ClinicalYesNo;
}

/** Study-design fields for a clinical-trial protocol synopsis. */
@Question.meta(#{ id: "clinical-study/design", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
model ClinicalStudyDesign {
  @maxLength(32000)
  @minLength(1)
  detailedDescription?: string;
  primaryPurpose?: ClinicalPrimaryPurpose;
  @maxLength(255)
  @minLength(1)
  otherPrimaryPurpose?: string;
  @maxItems(20)
  interventions?: ClinicalIntervention[];
  phase?: ClinicalStudyPhase;
  nihDefinedPhase3?: ClinicalYesNo;
  interventionModel?: ClinicalInterventionModel;
  @maxLength(255)
  @minLength(1)
  otherInterventionModel?: string;
  masking?: ClinicalYesNo;
  maskingParties?: ClinicalMaskingParties;
  allocation?: ClinicalAllocation;
}

model ClinicalOutcomeMeasure {
  @maxLength(255)
  @minLength(1)
  name: string;
  type: ClinicalOutcomeType;
  @maxLength(255)
  @minLength(1)
  timeFrame: string;
  @maxLength(999)
  @minLength(1)
  description: string;
}

/** Protocol, outcomes, regulatory, and dissemination information for a clinical trial. */
@Question.meta(#{ id: "clinical-study/protocol-synopsis", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
model ProtocolSynopsis {
  studyDesign?: ClinicalStudyDesign;
  @maxItems(50)
  outcomeMeasures?: ClinicalOutcomeMeasure[];
  statisticalDesignAndPower?: StatisticalDesignPowerDocument;
  @maxLength(255)
  @minLength(1)
  subjectParticipationDuration?: string;
  fdaRegulatedIntervention?: ClinicalYesNo;
  investigationalProductAvailability?: InvestigationalAvailabilityDocument;
  applicableClinicalTrial?: ClinicalYesNo;
  disseminationPlan?: DisseminationPlanDocument;
}

/** One complete PHS human-subject study record. */
@Question.meta(#{ id: "clinical-study/study-record", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
@UI.label("Human Subject Study")
model HumanSubjectStudyRecord {
  @Response.role(ResponseRole.systemValue)
  @UI.readOnly
  @maxLength(40)
  @minLength(1)
  studyId?: string;
  @maxLength(600)
  @minLength(1)
  studyTitle: string;
  exemptFromFederalRegulations: ClinicalYesNo;
  @minItems(1)
  @maxItems(8)
  exemptionNumbers?: QuestionBank.ResearchProject.HumanSubjectExemptionCode[];
  clinicalTrialQuestionnaire: ClinicalTrialQuestionnaire;
  @maxLength(11)
  @minLength(1)
  clinicalTrialsGovIdentifier?: string;
  populationCharacteristics?: StudyPopulationCharacteristics;
  protectionMonitoringPlans?: ProtectionMonitoringPlans;
  protocolSynopsis?: ProtocolSynopsis;
  @maxItems(100)
  @UI.widget(WidgetName.AttachmentArray)
  otherClinicalTrialAttachments?: OtherClinicalTrialDocument[];
}
