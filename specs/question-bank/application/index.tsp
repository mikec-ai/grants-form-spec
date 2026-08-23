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
