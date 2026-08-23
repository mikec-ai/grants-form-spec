import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace QuestionBank.Application;

/** SF-424's exact submission vocabulary. */
enum Sf424SubmissionType {
  preapplication: "Preapplication",
  application: "Application",
  changedCorrected: "Changed/Corrected Application",
}

/** SF-424's application lifecycle vocabulary. */
enum Sf424ApplicationType {
  new: "New",
  continuation: "Continuation",
  revision: "Revision",
}

/** SF-424's encoded revision choices. */
enum Sf424RevisionType {
  A: "A: Increase Award",
  B: "B: Decrease Award",
  C: "C: Increase Duration",
  D: "D: Decrease Duration",
  E: "E: Other (specify)",
  AC: "AC: Increase Award, Increase Duration",
  AD: "AD: Increase Award, Decrease Duration",
  BC: "BC: Decrease Award, Increase Duration",
  BD: "BD: Decrease Award, Decrease Duration",
}

/** SF-424's exact Executive Order 12372 response vocabulary. */
enum Sf424StateReviewCode {
  madeAvailable: "a. This application was made available to the state under the Executive Order 12372 Process for review on",
  notSelected: "b. Program is subject to E.O. 12372 but has not been selected by the state for review.",
  notCovered: "c. Program is not covered by E.O. 12372.",
}

/** Select the kind of SF-424 submission being made. */
@Question.meta(#{ id: "application/standard-submission-type" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSf424SubmissionType {
  @UI.label("Submission Type")
  submissionType: Sf424SubmissionType;
}

/** Describe the SF-424 application lifecycle and any revision. */
@Question.meta(#{ id: "application/standard-application-type" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionSf424ApplicationType {
  @UI.label("Application Type")
  applicationType: Sf424ApplicationType;

  @UI.label("Revision Type")
  @Validation.requiredWhen(QuestionSf424ApplicationType.applicationType, Sf424ApplicationType.revision)
  revisionType?: Sf424RevisionType;

  @UI.label("Other Explanation")
  @minLength(0)
  @maxLength(21)
  @Validation.requiredWhen(QuestionSf424ApplicationType.revisionType, Sf424RevisionType.E)
  revisionOtherSpecify?: string;
}

/** Enter the applicant's control number, if applicable, on the SF-424. */
@Question.meta(#{ id: "application/standard-applicant-control-identifier" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@minLength(1)
@maxLength(30)
scalar Sf424ApplicantControlIdentifier extends string;

/** Enter the Federal entity identifier assigned to the applicant organization. */
@Question.meta(#{ id: "application/federal-entity-identifier" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@minLength(1)
@maxLength(30)
scalar FederalEntityIdentifier extends string;

/** Enter the previously assigned Federal award identifier on the SF-424. */
@Question.meta(#{ id: "application/federal-award-identifier" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@minLength(1)
@maxLength(25)
scalar Sf424FederalAwardIdentifier extends string;

/** Record whether and when the SF-424 was made available for State review. */
@Question.meta(#{ id: "application/standard-state-review" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details, TagName.date)
model QuestionSf424StateReview {
  @UI.label("Is Application Subject to Review By State Under Executive Order 12372 Process?")
  stateReview: Sf424StateReviewCode;

  @UI.label("State Review Date")
  @Validation.requiredWhen(QuestionSf424StateReview.stateReview, Sf424StateReviewCode.madeAvailable)
  stateReviewAvailableDate?: plainDate;
}

/** Report whether the SF-424 applicant is delinquent on Federal debt. */
@Question.meta(#{ id: "application/delinquent-federal-debt-status" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
model QuestionFederalDebtStatus {
  @UI.label("Applicant Delinquent on Federal Debt")
  @UI.widget(WidgetName.Radio)
  delinquentFederalDebt: boolean;
}

/** Provide other narrative information requested for the application. */
@Question.meta(#{ id: "application/other-narrative" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.narrative, TagName.attachment)
@UI.label("Other Narrative")
scalar OtherNarrative extends AttachmentRef;

/** Explain any delinquent federal debt reported by the applicant. */
@Question.meta(#{ id: "application/federal-debt-explanation" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.attachment)
scalar FederalDebtExplanation extends AttachmentRef;

/** Completed by Grants.gov upon submission. */
@Question.meta(#{ id: "application/date-received" })
@Response.role(ResponseRole.systemValue)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.date)
@UI.label("Date Received")
scalar DateReceived extends SubmittedDate;

/** Enter the date the application is submitted to the Federal agency or State. */
@Question.meta(#{ id: "application/submission-date-entered" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.date)
@UI.label("Date Submitted")
scalar ApplicantEnteredSubmissionDate extends plainDate;

/** The routing identifier assigned by the Federal agency for an R&R application. */
@Question.meta(#{ id: "application/federal-agency-routing-number" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@UI.label("Agency Routing Number")
scalar FederalAgencyRoutingNumber extends string;

/** The date on which a State received an application. */
@Question.meta(#{ id: "application/state-received-date" })
@Response.role(ResponseRole.systemValue)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.date)
@UI.label("State Received Date")
scalar StateReceivedDate extends plainDate;

/** The identifier assigned by a State to an application. */
@Question.meta(#{ id: "application/state-application-identifier" })
@Response.role(ResponseRole.systemValue)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@UI.label("State Application Identifier")
scalar StateApplicationIdentifier extends string;

/** The previous Grants.gov tracking number for a changed or corrected application. */
@Question.meta(#{ id: "application/previous-grants-gov-tracking-number" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@UI.label("Grants.gov Identifier")
scalar PreviousGrantsGovTrackingNumber extends string;
