import "@simpler-grants/form-spec";
import "../index.tsp";

using SimplerForms;

/** Questions used to communicate optional application assignment and review preferences. */
namespace QuestionBank.ReviewRouting;

/** Suggest one awarding component by its short abbreviation. */
@Question.meta(#{ id: "review-routing/suggested-awarding-component" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
@maxLength(7)
scalar SuggestedAwardingComponent extends string;

/** Suggest one scientific review group or special-emphasis-panel code. */
@Question.meta(#{ id: "review-routing/suggested-study-section" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
@maxLength(20)
scalar SuggestedStudySection extends string;

/** Explain why the awarding-component or study-section suggestions are appropriate. */
@Question.meta(#{ id: "review-routing/assignment-suggestion-rationale" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.narrative)
@maxLength(1000)
scalar AssignmentSuggestionRationale extends string;

/** Identify one scientific area of expertise needed to review the application. */
@Question.meta(#{ id: "review-routing/reviewer-expertise" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.details)
@maxLength(40)
scalar ReviewerExpertise extends string;

/** Identify individuals who should not review the application and explain why. */
@Question.meta(#{ id: "review-routing/excluded-reviewer-request" })
@Catalog.entity(EntityName.application)
@Catalog.tag(TagName.narrative)
@maxLength(1000)
scalar ExcludedReviewerRequest extends string;
