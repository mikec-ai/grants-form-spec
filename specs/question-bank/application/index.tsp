import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

namespace QuestionBank.Application;

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
@Response.role(ResponseRole.systemValue)
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
@Response.role(ResponseRole.systemValue)
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.identifier)
@UI.label("Grants.gov Identifier")
scalar PreviousGrantsGovTrackingNumber extends string;
