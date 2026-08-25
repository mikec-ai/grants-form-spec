import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";
import "../research-application/index.tsp";
import "../research-budget/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.ResearchApplication;
using QuestionBank.ResearchBudget;

/** Portable, source-bound questions introduced by PHS Fellowship Supplemental 8.0. */
namespace QuestionBank.PHSFellowship;

/** Report whether the proposed fellowship work uses vertebrate animals. */
@Question.meta(#{ id: "fellowship/vertebrate-animals-used", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
@pattern("^(Y: Yes|N: No)$")
scalar FellowshipVertebrateAnimalsUsed extends string;

/** Attach the fellowship candidate's goals, preparation, and potential narrative. */
@Question.meta(#{ id: "fellowship/candidate-goals", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar FellowshipCandidateGoals extends AttachmentRef;

/** Attach the planned research training activities. */
@Question.meta(#{ id: "fellowship/training-activities", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar FellowshipTrainingActivities extends AttachmentRef;

/** Attach the plan for training in the responsible conduct of research. */
@Question.meta(#{ id: "fellowship/responsible-conduct-training", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar FellowshipResponsibleConductTraining extends AttachmentRef;

/** Attach the sponsor's commitment to the candidate's research training. */
@Question.meta(#{ id: "fellowship/sponsor-commitment", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar FellowshipSponsorCommitment extends AttachmentRef;

/** Attach the candidate's contribution to the goals of the fellowship training plan. */
@Question.meta(#{ id: "fellowship/candidate-contribution", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar FellowshipCandidateContribution extends AttachmentRef;

/** Attach a description of an application for concurrent support. */
@Question.meta(#{ id: "fellowship/concurrent-support-description", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar FellowshipConcurrentSupportDescription extends AttachmentRef;

/** Select the graduate degree sought by the fellowship candidate. */
enum FellowshipDegreeType {
  ma: "MA: Master of Arts",
  mba: "MBA: Master of Business Administration",
  mls: "MLS: Master of Library Science",
  mpa: "MPA: Master of Public Administration",
  mph: "MPH: Master of Public Health",
  ms: "MS: Master of Science",
  msn: "MSN: Master of Science In Nursing",
  dc: "DC: Doctor of Chiropractic",
  dnsc: "DNSC: Doctor of Nursing Science",
  dph: "DPH: Doctor of Public Health",
  drph: "DRPH: Doctor of Public Health",
  dsc: "DSC: Doctor of Science",
  edd: "EDD: Doctor of Education",
  egnd: "EGND: Foreign Doctor Engineering",
  jd: "JD: Doctor of Juris Prudence",
  phd: "PHD: Doctor of Philosophy",
  scd: "SCD: Doctor of Science",
  dds: "DDS: Doctor of Dental Surgery",
  dmd: "DMD: Doctor of Medical Dentistry",
  do: "DO: Doctor of Osteopathy",
  dpm: "DPM: Doctor of Podiatric Medicine",
  dsw: "DSW: Doctor of Social Work",
  dvm: "DVM: Doctor of Veterinary Medicine",
  mb: "MB: Foreign - Bachelor of Medicine",
  mbbs: "MBBS: Foreign - Bachelor of Medicine and Surgery",
  md: "MD: Doctor of Medicine",
  nd: "ND: Doctor of Naturopathy",
  od: "OD: Doctor of Optometry",
  phmd: "PHMD: Doctor of Pharmacy",
  psyd: "PSYD: Doctor of Psychology",
  vmd: "VMD: Doctor of Veterinary Medicine",
  otherMasters: "MOTH: Other Masters Degree",
  otherDoctorate: "DOTH: Other Doctorate",
  otherDental: "DDOT: Other Doctor of Medical Dentistry",
  otherMedicine: "MDOT: Other Doctor of Medicine",
  otherVeterinary: "VDOT: Other Doctor of Veterinary Medicine",
  other: "OTH: Other",
}

/** A month and year in the source-defined MM/YYYY format. */
@pattern("^(0[1-9]|1[0-2])/[0-9]{4}$")
@minLength(7)
@maxLength(7)
scalar FellowshipMonthYear extends string;

/** The graduate degree sought and expected completion month for the candidate. */
@Question.meta(#{ id: "fellowship/graduate-degree-sought", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.details)
model QuestionFellowshipGraduateDegreeSought {
  @UI.label("Degree Sought")
  degreeType: FellowshipDegreeType;

  // The DAT enables and requires this only for its six Other degree codes. The current
  // portable validation contract cannot express required-when-any without weakening that
  // predicate to mere presence, so the exact source behavior remains an explicit open gate.
  @UI.label("Other Degree Type")
  @minLength(1)
  @maxLength(10)
  otherDegreeTypeText?: string;

  @UI.label("Expected Completion Date (MM/YYYY)")
  degreeDate: FellowshipMonthYear;
}

/** Select the candidate's field of training from the source-defined PHS vocabulary. */
enum FellowshipFieldOfTraining {
  f100: "100 Biochemistry",
  f102: "102 Bioinformatics",
  f103: "103 Biomedical Sciences (see also Statistics in MATHEMATICS and SOCIAL SCIENCES)",
  f104: "104 Computational Biology",
  f105: "105 Biophysics (also in Physics)",
  f107: "107 Biotechnology",
  f110: "110 Bacteriology",
  f115: "115 Plant Genetics",
  f120: "120 Plant Pathology/Phytopathology",
  f125: "125 Plant Physiology",
  f129: "129 Botany/Plant Biology",
  f130: "130 Anatomy",
  f133: "133 Biometrics & Biostatistics",
  f136: "136 Cell/Cellular Biology & Histology",
  f137: "137 Evolutionary Biology",
  f139: "139 Ecology",
  f142: "142 Developmental Biology/Embryology",
  f145: "145 Endocrinology",
  f148: "148 Entomology",
  f151: "151 Immunology",
  f152: "152 Marine Biology & Biological Oceanography",
  f154: "154 Molecular Biology",
  f155: "155 Structural Biology",
  f157: "157 Microbiology",
  f158: "158 Cancer Biology",
  f160: "160 Neurosciences & Neurobiology",
  f163: "163 Nutrition Sciences",
  f166: "166 Parasitology",
  f167: "167 Environmental Toxicology",
  f168: "168 Virology",
  f169: "169 Toxicology",
  f170: "170 Genetics/Genomics, Human & Animal",
  f175: "175 Pathology, Human & Animal",
  f180: "180 Pharmacology, Human & Animal",
  f185: "185 Physiology, Human & Animal",
  f189: "189 Zoology",
  f198: "198 Biology/Biomedical Sciences, General",
  f199: "199 Biology/Biomedical Sciences, Other",
  f200: "200 Speech-Language Pathology & Audiology",
  f207: "207 Oral Biology/Oral Pathology",
  f210: "210 Environmental Health",
  f212: "212 Health Systems/Service Administration",
  f215: "215 Public Health",
  f217: "217 Health Policy Analysis",
  f220: "220 Epidemiology",
  f222: "222 Kinesiology/Exercise Physiology",
  f227: "227 Gerontology (Also in Social Sciences)",
  f230: "230 Nursing Science",
  f240: "240 Medicinal/Pharmaceutical Sciences",
  f245: "245 Rehabilitation/Therapeutic Services",
  f250: "250 Veterinary Sciences",
  f290: "290 Clinical and Translational Sciences",
  f298: "298 Health Sciences, General",
  f299: "299 Health Sciences, Other",
  f526: "526 Organic Chemistry",
  f539: "539 Chemistry, Other",
  f565: "565 Biophysics (also in BIOLOGICAL SCIENCES)",
  f577: "577 Medical Physics/Radiological Science",
  f579: "579 Physics, Other",
  f410: "410 Information Sciences & Systems (see also Bioinformatics in BIOLOGICAL SCIENCES)",
  f419: "419 Computer & Information Science, Other",
  f450: "450 Statistics (also in SOCIAL SCIENCES; see also Biometrics and Statistics in BIOLOGICAL SCIENCES)",
  f306: "306 Bioengineering & Biomedical Engineering",
  f399: "399 Engineering, Other",
  f600: "600 Clinical Psychology",
  f603: "603 Cognitive Psychology & Psycholinguistics",
  f612: "612 Developmental & Child Psychology",
  f615: "615 Experimental Psychology",
  f614: "614 Health & Medical Psychology",
  f627: "627 Neuropsychology/Physiological Psychology",
  f624: "624 Personality Psychology",
  f633: "633 Psychometrics & Quantitative Psychology",
  f639: "639 Social Psychology",
  f649: "649 Psychology, Other",
  f662: "662 Demography/Population Studies",
  f684: "684 Gerontology (also in HEALTH SCIENCES)",
  f690: "690 Statistics (also in MATHEMATICS; see also Biometrics and Statistics in BIOLOGICAL SCIENCES)",
  f980: "980 Social Work",
  f989: "989 Other",
}

/** Enter the fellowship candidate's primary field of training. */
@Question.meta(#{ id: "fellowship/field-of-training", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.details)
model QuestionFellowshipFieldOfTraining {
  @UI.label("Field of Training")
  fieldOfTraining: FellowshipFieldOfTraining;
}

enum FellowshipNrsaLevel {
  predoctoral: "Predoctoral",
  postdoctoral: "Postdoctoral",
}

enum FellowshipNrsaType {
  individual: "Individual",
  institutional: "Institutional",
}

/** One current or prior NRSA support record. */
model FellowshipNrsaSupportRecord {
  @UI.label("Level")
  level: FellowshipNrsaLevel;

  @UI.label("Type")
  type: FellowshipNrsaType;

  @UI.label("Start Date")
  startDate?: plainDate;

  @UI.label("End Date")
  @Validation.notBefore(FellowshipNrsaSupportRecord.startDate)
  endDate?: plainDate;

  @UI.label("Grant Number")
  @minLength(1)
  @maxLength(19)
  grantNumber?: string;
}

/** Report current or prior NRSA support and up to four support records. */
@Question.meta(#{ id: "fellowship/current-prior-nrsa-support", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.details)
model QuestionFellowshipCurrentPriorNrsaSupport {
  @UI.label("Have you received current or prior NRSA support?")
  hasSupport: YesNoCode;

  @UI.label("Current or Prior NRSA Support")
  @UI.enabledWhen(QuestionFellowshipCurrentPriorNrsaSupport.hasSupport, YesNoCode.yes)
  @Validation.constraintsWhen(
    QuestionFellowshipCurrentPriorNrsaSupport.hasSupport,
    YesNoCode.yes,
    #{ minItems: 1 },
  )
  @maxItems(4)
  records?: FellowshipNrsaSupportRecord[];
}

/** Report whether another application requests support concurrently. */
@Question.meta(#{ id: "fellowship/concurrent-support", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.details)
model QuestionFellowshipConcurrentSupport {
  @UI.label("Applications for Concurrent Support")
  hasConcurrentSupport: YesNoCode;

  @UI.label("Concurrent Support Description")
  @UI.widget(WidgetName.Attachment)
  @UI.enabledWhen(QuestionFellowshipConcurrentSupport.hasConcurrentSupport, YesNoCode.yes)
  @Validation.requiredWhen(QuestionFellowshipConcurrentSupport.hasConcurrentSupport, YesNoCode.yes)
  description?: FellowshipConcurrentSupportDescription;
}

enum FellowshipNonUsCitizenStatus {
  permanentVisa: "With a Permanent U.S. Resident Visa",
  temporaryVisa: "With a Temporary U.S. Visa",
}

/** Report the fellowship candidate's source-defined citizenship and residency status. */
@Question.meta(#{ id: "fellowship/candidate-citizenship", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.details)
model QuestionFellowshipCandidateCitizenship {
  @UI.label("U.S. Citizen")
  usCitizen: YesNoCode;

  @UI.label("Non-U.S. Citizen Status")
  @UI.enabledWhen(QuestionFellowshipCandidateCitizenship.usCitizen, YesNoCode.no)
  @Validation.requiredWhen(QuestionFellowshipCandidateCitizenship.usCitizen, YesNoCode.no)
  nonUsCitizenStatus?: FellowshipNonUsCitizenStatus;

  @UI.label("Permanent Resident by Award")
  @UI.enabledWhen(
    QuestionFellowshipCandidateCitizenship.nonUsCitizenStatus,
    FellowshipNonUsCitizenStatus.temporaryVisa,
  )
  permanentResidentByAward?: YesNoCode;
}

/** Report a change of sponsoring institution and name the former institution. */
@Question.meta(#{ id: "fellowship/institution-change", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.organization, TagName.details)
model QuestionFellowshipInstitutionChange {
  @UI.label("Change of Sponsoring Institution")
  changesInstitution?: YesNoCode;

  @UI.label("Name of Former Institution")
  @UI.enabledWhen(QuestionFellowshipInstitutionChange.changesInstitution, YesNoCode.yes)
  formerInstitution?: OrganizationName;
}

/** Additional identity, education, support, and citizenship information for the candidate. */
@Question.meta(#{ id: "fellowship/candidate-additional-information", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.details)
model QuestionFellowshipCandidateInformation {
  @UI.label("Alternate Phone Number")
  alternatePhone?: PhoneNumber;

  @UI.label("Graduate Degree Sought")
  graduateDegreeSought?: QuestionFellowshipGraduateDegreeSought;

  ...QuestionFellowshipFieldOfTraining;

  currentPriorNrsaSupport: QuestionFellowshipCurrentPriorNrsaSupport;
  concurrentSupport: QuestionFellowshipConcurrentSupport;
  citizenship: QuestionFellowshipCandidateCitizenship;
  institutionChange?: QuestionFellowshipInstitutionChange;
}

enum FellowshipAcademicPeriod {
  sixMonth: "6-month",
  nineMonth: "9-month",
  tenMonth: "10-month",
  twelveMonth: "12-month",
}

@pattern("^(?:[0-9]|1[0-9]|2[0-4])(?:[.][0-9]{1,2})?$")
scalar FellowshipMonthsUpTo24 extends string;

@pattern("^(?:[0-9]|1[0-2])(?:[.][0-9]{1,2})?$")
scalar FellowshipMonthsUpTo12 extends string;

/** Six source-defined annual amount slots and their calculated total. */
model FellowshipSixYearAmounts {
  @UI.label("Year 1")
  year1?: ResearchBudgetAmount14;
  @UI.label("Year 2")
  year2?: ResearchBudgetAmount14;
  @UI.label("Year 3")
  year3?: ResearchBudgetAmount14;
  @UI.label("Year 4")
  year4?: ResearchBudgetAmount14;
  @UI.label("Year 5")
  year5?: ResearchBudgetAmount14;
  @UI.label("Year 6")
  year6?: ResearchBudgetAmount14;
}

/** Request tuition and fees for up to six fellowship years. */
@Question.meta(#{ id: "fellowship-budget/tuition", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
model QuestionFellowshipTuition {
  @UI.label("Tuition and Fees Requested")
  fundsRequested: YesNoCode;

  // Spread the shared source shape into this question. Inheritance leaves these
  // occurrence fields behind an allOf reference, where question emission cannot
  // apply the declarative UI overrides or bind the total calculation inputs.
  ...FellowshipSixYearAmounts;

  @UI.label("Total Tuition and Fees Requested")
  @Validation.computed(
    Op.Sum,
    QuestionFellowshipTuition.year1,
    QuestionFellowshipTuition.year2,
    QuestionFellowshipTuition.year3,
    QuestionFellowshipTuition.year4,
    QuestionFellowshipTuition.year5,
    QuestionFellowshipTuition.year6,
  )
  @Validation.materializeWhenAnySourcePresent
  @UI.readOnly
  total?: ResearchBudgetTotalAmount15;
}

/** Request childcare costs for up to six fellowship years. */
@Question.meta(#{ id: "fellowship-budget/childcare", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
model QuestionFellowshipChildcare {
  @UI.label("Childcare Costs Requested")
  fundsRequested: YesNoCode;

  // Keep the six source-defined periods visible to the generic emitter while
  // retaining one declarative definition of their shape.
  ...FellowshipSixYearAmounts;

  @UI.label("Total Childcare Costs Requested")
  @Validation.computed(
    Op.Sum,
    QuestionFellowshipChildcare.year1,
    QuestionFellowshipChildcare.year2,
    QuestionFellowshipChildcare.year3,
    QuestionFellowshipChildcare.year4,
    QuestionFellowshipChildcare.year5,
    QuestionFellowshipChildcare.year6,
  )
  @Validation.materializeWhenAnySourcePresent
  @UI.readOnly
  total?: ResearchBudgetTotalAmount15;
}

/** Enter the candidate's institutional base salary. */
@Question.meta(#{ id: "fellowship-budget/institutional-base-salary", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.money)
model QuestionFellowshipInstitutionalBaseSalary {
  amount: ResearchBudgetAmount14;
  academicPeriod: FellowshipAcademicPeriod;
  numberOfMonths: FellowshipMonthsUpTo24;
}

/** Enter the federal stipend requested for the candidate. */
@Question.meta(#{ id: "fellowship-budget/federal-stipend", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.money)
model QuestionFellowshipFederalStipend {
  amount: ResearchBudgetAmount14;
  numberOfMonths: FellowshipMonthsUpTo12;
}

/** Enter stipend supplementation supplied from other sources. */
@Question.meta(#{ id: "fellowship-budget/supplementation", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.money)
model QuestionFellowshipSupplementation {
  amount: ResearchBudgetAmount14;
  numberOfMonths: FellowshipMonthsUpTo12;

  @minLength(1)
  @maxLength(30)
  type: string;

  @minLength(1)
  @maxLength(60)
  source: string;
}

/** Fellowship-specific budget requests and compensation information. */
@Question.meta(#{ id: "fellowship-budget/request", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.money)
model QuestionFellowshipBudget {
  tuition: QuestionFellowshipTuition;
  childcare: QuestionFellowshipChildcare;

  // Each optional source group has internally required fields. That preserves the DAT's
  // any-entered-means-all-required behavior without a form-specific runtime rule.
  institutionalBaseSalary?: QuestionFellowshipInstitutionalBaseSalary;
  federalStipend?: QuestionFellowshipFederalStipend;
  supplementation?: QuestionFellowshipSupplementation;
}
