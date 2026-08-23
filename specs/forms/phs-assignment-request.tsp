import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/review-routing/index.tsp";

using SimplerForms;
using QuestionBank.ReviewRouting;

namespace Forms.PHSAssignmentRequest;

enum PHSAssignmentRequestSection {
  awardingComponents: "Awarding Component Assignment Suggestions",
  studySections: "Study Section Assignment Suggestions",
  rationale: "Rationale for Assignment Suggestions",
  expertise: "Scientific Areas of Expertise",
  excludedReviewers: "Individuals Who Should Not Review the Application",
}

/** PHS Assignment Request Form, Grants.gov form version 4.0. */
@Form.meta(#{
  id: "phs-assignment-request",
  legacyFormId: 833,
  formName: "PHS Assignment Request Form",
  shortFormName: "PHS_AssignmentRequestForm_4_0",
  formVersion: "4.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "0925-0001",
})
@UI.sections(PHSAssignmentRequestSection)
model PHSAssignmentRequest {
  /** Enter an awarding-component abbreviation, such as NCI. */
  @UI.label("Suggested Awarding Component 1")
  @UI.helpText("Enter a short awarding-component abbreviation. Confirm that the component participates in the funding opportunity or is supported by an appropriate Notice of Special Interest in R&R Cover Form box 4B.")
  @UI.section(PHSAssignmentRequestSection.awardingComponents)
  suggestedAwardingComponent1?: SuggestedAwardingComponent;

  /** Enter a second awarding-component abbreviation. */
  @UI.label("Suggested Awarding Component 2")
  @UI.section(PHSAssignmentRequestSection.awardingComponents)
  suggestedAwardingComponent2?: SuggestedAwardingComponent;

  /** Enter a third awarding-component abbreviation. */
  @UI.label("Suggested Awarding Component 3")
  @UI.section(PHSAssignmentRequestSection.awardingComponents)
  suggestedAwardingComponent3?: SuggestedAwardingComponent;

  /** Enter a study-section code without hyphens, parentheses, or spaces. */
  @UI.label("Suggested Study Section 1")
  @UI.helpText("Enter the short study-section code without hyphens, parentheses, or spaces. Assignment suggestions are considered but cannot always be honored.")
  @UI.section(PHSAssignmentRequestSection.studySections)
  suggestedStudySection1?: SuggestedStudySection;

  /** Enter a second study-section code. */
  @UI.label("Suggested Study Section 2")
  @UI.section(PHSAssignmentRequestSection.studySections)
  suggestedStudySection2?: SuggestedStudySection;

  /** Enter a third study-section code. */
  @UI.label("Suggested Study Section 3")
  @UI.section(PHSAssignmentRequestSection.studySections)
  suggestedStudySection3?: SuggestedStudySection;

  /** Explain why the assignment suggestions are appropriate. */
  @UI.label("Rationale for Assignment Suggestions")
  @UI.helpText("Explain why you think the awarding-component or study-section suggestions are appropriate. If you contacted NIH staff, include their names.")
  @UI.section(PHSAssignmentRequestSection.rationale)
  @UI.widget(WidgetName.TextArea)
  rationaleSuggestions?: AssignmentSuggestionRationale;

  /** Enter one scientific area of expertise needed to review the application. */
  @UI.label("Expertise 1")
  @UI.helpText("Enter an area of scientific expertise, not the name of an individual.")
  @UI.section(PHSAssignmentRequestSection.expertise)
  expertise1?: ReviewerExpertise;

  /** Enter a second scientific area of expertise. */
  @UI.label("Expertise 2")
  @UI.section(PHSAssignmentRequestSection.expertise)
  expertise2?: ReviewerExpertise;

  /** Enter a third scientific area of expertise. */
  @UI.label("Expertise 3")
  @UI.section(PHSAssignmentRequestSection.expertise)
  expertise3?: ReviewerExpertise;

  /** Enter a fourth scientific area of expertise. */
  @UI.label("Expertise 4")
  @UI.section(PHSAssignmentRequestSection.expertise)
  expertise4?: ReviewerExpertise;

  /** Enter a fifth scientific area of expertise. */
  @UI.label("Expertise 5")
  @UI.section(PHSAssignmentRequestSection.expertise)
  expertise5?: ReviewerExpertise;

  /** Identify individuals who should not review the application and explain why. */
  @UI.label("Individuals Who Should Not Review the Application and Why")
  @UI.helpText("Provide enough information, such as name and organizational affiliation, for review staff to identify each individual and explain why the individual should not review the application.")
  @UI.section(PHSAssignmentRequestSection.excludedReviewers)
  @UI.widget(WidgetName.TextArea)
  notReview?: ExcludedReviewerRequest;
}
