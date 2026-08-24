import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";
import "../research-application/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.ResearchApplication;

namespace QuestionBank.SbirSttr;

enum SbirSttrAgencyCode {
  doe: "DOE",
  hhs: "HHS",
  usda: "USDA",
  other: "Other",
}

enum SbirSttrProgramTypeCode {
  sbir: "SBIR",
  sttr: "STTR",
  both: "Both",
}

enum SbirSttrApplicationTypeCode {
  phaseI: "Phase I",
  phaseII: "Phase II",
  fastTrack: "Fast-Track",
  directPhaseII: "Direct Phase II",
  phaseIIA: "Phase IIA",
  phaseIIB: "Phase IIB",
  phaseIIC: "Phase IIC",
  commercializationReadinessProgram: "Commercialization Readiness Program",
}

/** Select the Federal agency to which this SBIR/STTR application is submitted. */
@Question.meta(#{ id: "sbir-sttr/agency" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrAgency {
  @UI.label("Agency to which you are applying (select only one)")
  @UI.widget(WidgetName.Radio)
  value: SbirSttrAgencyCode;
}

/** Name the agency when the Federal agency selection is Other. */
@Question.meta(#{ id: "sbir-sttr/other-agency" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
@maxLength(20)
scalar QuestionSbirSttrOtherAgency extends string;

/** Enter the nine-digit Small Business Concern control identifier. */
@Question.meta(#{ id: "sbir-sttr/sbc-control-id" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@pattern("^[0-9]{9}$")
@minLength(9)
@maxLength(9)
scalar QuestionSbcControlId extends string;

/** Select whether this application is for SBIR, STTR, or both programs. */
@Question.meta(#{ id: "sbir-sttr/program-type" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrProgramType {
  @UI.label("Program Type (select only one)")
  @UI.widget(WidgetName.Radio)
  value: SbirSttrProgramTypeCode;
}

/** Select the SBIR/STTR application phase or commercialization program. */
@Question.meta(#{ id: "sbir-sttr/application-type" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrApplicationType {
  @UI.label("Application Type (select only one)")
  @UI.widget(WidgetName.Radio)
  value: SbirSttrApplicationTypeCode;
}

/** Enter the Phase I letter-of-intent number, when applicable. */
@Question.meta(#{ id: "sbir-sttr/phase-i-letter-of-intent-number" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@maxLength(20)
scalar QuestionSbirSttrPhaseILetterOfIntentNumber extends string;

/** Enter the agency topic or subtopic for this application. */
@Question.meta(#{ id: "sbir-sttr/agency-topic-subtopic" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@maxLength(10)
scalar QuestionSbirSttrAgencyTopicSubtopic extends string;

/** Certify anticipated small-business eligibility at the time of award. */
@Question.meta(#{ id: "sbir-sttr/small-business-eligibility-certification" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrSmallBusinessEligibility {
  @UI.label("Do you certify that at the time of award your organization will meet the eligibility criteria for a small business as defined in the funding opportunity announcement?")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Enter the anticipated number of organization personnel at the time of award. */
@Question.meta(#{ id: "sbir-sttr/anticipated-employee-count" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
@minValue(1)
@maxValue(999)
scalar QuestionSbirSttrEmployeeCount extends int32;

/** Report whether the small business is majority owned by specified investment entities. */
@Question.meta(#{ id: "sbir-sttr/vcoc-majority-ownership" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrVcocOwnership {
  @UI.label("Is your small business majority owned by venture capital operating companies, hedge funds, or private equity firms?")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Report whether the small business is faculty- or student-owned. */
@Question.meta(#{ id: "sbir-sttr/faculty-student-ownership" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrFacultyStudentOwnership {
  @UI.label("Is your small business a Faculty or Student-Owned entity?")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Report whether the application includes subcontracts with Federal laboratories or agencies. */
@Question.meta(#{ id: "sbir-sttr/federal-subcontracts-included" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrFederalSubcontractsIncluded {
  @UI.label("Does this application include subcontracts with Federal laboratories or any other Federal Government agencies?")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Name the Federal laboratories or agencies included as subcontractors. */
@Question.meta(#{ id: "sbir-sttr/federal-subcontractor-names" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
@maxLength(250)
scalar QuestionSbirSttrFederalSubcontractorNames extends string;

/** Report whether the small business is located in a HUBZone. */
@Question.meta(#{ id: "sbir-sttr/hubzone-location" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrHubzoneLocation {
  @UI.label("Are you located in a HUBZone? To find out if your business is in a HUBZone, use the mapping utility provided by the Small Business Administration at its web site: http://www.sba.gov")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Report whether all project research and development will occur in the United States. */
@Question.meta(#{ id: "sbir-sttr/domestic-performance" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
model QuestionSbirSttrDomesticPerformance {
  @UI.label("Will all research and development on the project be performed in its entirety in the United States?")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Explain project research and development performed outside the United States. */
@Question.meta(#{ id: "sbir-sttr/non-domestic-performance-explanation" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.attachment)
scalar QuestionSbirSttrNonDomesticPerformanceExplanation extends AttachmentRef;

/** Report essentially equivalent proposals or awards under other Federal programs. */
@Question.meta(#{ id: "sbir-sttr/equivalent-federal-work" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrEquivalentFederalWork {
  @UI.label("Has the applicant and/or Program Director/Principal Investigator submitted proposals for essentially equivalent work under other Federal program solicitations or received other Federal awards for essentially equivalent work?")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Name other Federal agencies receiving or awarding essentially equivalent work. */
@Question.meta(#{ id: "sbir-sttr/equivalent-work-federal-agencies" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
@maxLength(250)
scalar QuestionSbirSttrEquivalentWorkFederalAgencies extends string;

/** Authorize the Government disclosure described by the form if no award results. */
@Question.meta(#{ id: "sbir-sttr/disclosure-permission" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrDisclosurePermission {
  @UI.label("Disclosure Permission Statement: If this application does not result in an award, is the Government permitted to disclose the title of your proposed project, and the name, address, telephone number and email address of the official signing for the applicant organization to state-level economic development organizations that may be interested in contacting you for further information (e.g., possible collaborations, investment)?")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Report whether the application requests SBIR or STTR funds for TABA. */
@Question.meta(#{ id: "sbir-sttr/taba-funding-request" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.money)
model QuestionSbirSttrTabaFundingRequest {
  @UI.label("Does the application include a request of SBIR or STTR funds for Technical and Business Assistance (TABA)? If yes, please follow the agency specific instructions to provide the budget request and justification. (Please answer no if you plan to use the agency TABA vendor, which does not require you to include a request for TABA funds in your application.)")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Attach the commercialization plan required by the applicable agency policy. */
@Question.meta(#{ id: "sbir-sttr/commercialization-plan" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.attachment)
scalar QuestionSbirSttrCommercializationPlan extends AttachmentRef;

/** Report whether the applicant has received SBIR Phase II awards from the Federal Government. */
@Question.meta(#{ id: "sbir-sttr/phase-ii-awards-received" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrPhaseIIAwardsReceived {
  @UI.label("Have you received SBIR Phase II awards from the Federal Government?")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Attach the company commercialization history requested after prior SBIR Phase II awards. */
@Question.meta(#{ id: "sbir-sttr/commercialization-history" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.attachment)
scalar QuestionSbirSttrCommercializationHistory extends AttachmentRef;

/** Report whether the PD/PI will be primarily employed by the small business at award. */
@Question.meta(#{ id: "sbir-sttr/pdpi-primary-employment" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrPdpiPrimaryEmployment {
  @UI.label("Will the Project Director/Principal Investigator have primary employment with the small business at the time of award?")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Report the STTR PD/PI appointment or commitment and minimum project effort. */
@Question.meta(#{ id: "sbir-sttr/pdpi-appointment-and-effort" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSbirSttrPdpiAppointmentAndEffort {
  @UI.label("Please indicate whether the answer to BOTH of the following questions is TRUE: (1) Does the Project Director/Principal Investigator have a formal appointment or commitment either with the small business directly (as an employee or a contractor) OR as an employee of the Research Institution, which in turn has made a commitment to the small business through the STTR application process; AND (2) Will the Project Director/Principal Investigator devote at least 10% effort to the proposed project?")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Report whether the proposed STTR work meets the 40/30 joint-performance thresholds. */
@Question.meta(#{ id: "sbir-sttr/joint-performance-percentage" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.details)
model QuestionSbirSttrJointPerformancePercentage {
  @UI.label("In the joint research and development proposed in this project, does the small business perform at least 40% of the work and the research institution named in the application perform at least 30% of the work?")
  @UI.widget(WidgetName.Radio)
  value: YesNoCode;
}

/** Enter the UEI of the non-profit research partner for an STTR application. */
@Question.meta(#{ id: "sbir-sttr/nonprofit-research-partner-uei" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier, TagName.role)
@minLength(12)
@maxLength(12)
scalar QuestionSbirSttrNonprofitResearchPartnerUei extends string;
