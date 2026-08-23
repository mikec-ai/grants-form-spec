import "@simpler-grants/form-spec";
import "./rr-sf424.tsp";
import "../question-bank/aor/index.tsp";
import "../question-bank/application/index.tsp";
import "../question-bank/generics/index.tsp";
import "../question-bank/opportunity/index.tsp";
import "../question-bank/primary-org/index.tsp";
import "../question-bank/project/index.tsp";
import "../question-bank/research-application/index.tsp";

using SimplerForms;
using Forms.RRSF424;
using QuestionBank.Aor;
using QuestionBank.Application;
using QuestionBank.Generics;
using QuestionBank.Opportunity;
using QuestionBank.PrimaryOrg;
using QuestionBank.Project;
using QuestionBank.ResearchApplication;

namespace Forms.RRSF424MultiProjectCover;

// The official multi-project DAT treats signature and signed date as applicant-entered, and the
// read-only PDF omits the standalone form's "Completed on submission" text. They remain local
// because their lifecycle differs from Simpler's submission-populated standalone fields.
scalar MultiProjectSignature extends string;

// Version 4.0 has the same 139-node XSD inventory as the standalone R&R cover except
// for its root and Grants.gov tracking field names. Its material form delta is that the
// application, person, organization, and address values are optional. The shared semantic
// blocks carry that least-restrictive cardinality; the standalone form narrows its own
// occurrences with `@Validation.requiredPaths`.
model MultiProjectCountryControlledAddress extends QuestionAddress {
  @UI.label("State")
  @UI.enabledWhen(MultiProjectCountryControlledAddress.country, CountryCode.USA)
  state?: StateCode;

  @UI.label("Province")
  @minLength(1)
  @maxLength(30)
  @UI.readOnlyWhen(MultiProjectCountryControlledAddress.country, CountryCode.USA)
  province?: string;
}

model MultiProjectProvinceControlledAddress extends QuestionAddress {
  @UI.label("Province")
  @minLength(1)
  @maxLength(30)
  @UI.readOnlyWhen(MultiProjectProvinceControlledAddress.country, CountryCode.USA)
  province?: string;
}

model MultiProjectApplicantOrganization extends ResearchApplicantOrganization {
  address?: MultiProjectCountryControlledAddress;
}

model MultiProjectApplicationContact extends ResearchApplicationContact {
  address?: MultiProjectCountryControlledAddress;
}

model MultiProjectApplicant extends QuestionResearchApplicant {
  organizationInfo?: MultiProjectApplicantOrganization;
  contactPersonInfo?: MultiProjectApplicationContact;
}

model MultiProjectPrincipalInvestigator extends QuestionPrincipalInvestigator {
  address?: MultiProjectProvinceControlledAddress;
}

model MultiProjectAuthorizedRepresentative extends QuestionResearchAuthorizedRepresentative {
  address?: MultiProjectCountryControlledAddress;
}

model MultiProjectApplicationType extends QuestionResearchApplicationType {}

model MultiProjectApplicantType extends QuestionResearchApplicantType {}

model MultiProjectPeriod {
  @UI.label("Proposed Start Date")
  proposedStartDate?: ProjectStartDate;

  @UI.label("Proposed End Date")
  proposedEndDate?: ProjectEndDate;
}

model MultiProjectEstimatedFunding extends QuestionResearchEstimatedFunding {}

model MultiProjectStateReview extends QuestionResearchStateReview {}

/** Research & Related Multi-Project Cover, Grants.gov form version 4.0. */
@Form.meta(#{
  id: "rr-sf424-multi-project-cover",
  legacyFormId: 769,
  formName: "[Draft] Research & Related Multi-Project Cover",
  shortFormName: "RR_SF424_Multi_Project_Cover_4_0",
  formVersion: "4.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0001",
})
@UI.sections(RRSF424Section)
@UI.overrides(#{
  `applicationType.otherAgencySubmissionExplanation`: #{
    enabledWhen: #{ path: "applicationType.isOtherAgencySubmission", equals: YesNoCode.yes }
  },
  `applicationType.revisionCode`: #{
    enabledWhen: #{ path: "applicationType.applicationTypeCode", equals: ResearchApplicationTypeCode.revision }
  },
  `applicationType.revisionCodeOtherExplanation`: #{
    enabledWhen: #{ path: "applicationType.revisionCode", equals: ResearchRevisionCode.E }
  },
  `applicantType.applicantTypeCodeOtherExplanation`: #{
    enabledWhen: #{ path: "applicantType.applicantTypeCode", equals: ApplicantTypeCode.X }
  },
  `applicantType.smallBusinessOrganizationType`: #{
    enabledWhen: #{ path: "applicantType.applicantTypeCode", equals: ApplicantTypeCode.R }
  },
  `stateReview.stateReviewDate`: #{
    enabledWhen: #{ path: "stateReview.stateReviewCodeType", equals: ResearchStateReviewCode.yes }
  },
})
model RRSF424MultiProjectCover {
  ...QuestionResearchSubmissionType;

  @UI.label("Date Submitted")
  @UI.section(RRSF424Section.submittedDate)
  submittedDate?: ApplicantEnteredSubmissionDate;

  @UI.label("Applicant Identifier")
  @UI.section(RRSF424Section.applicantIdentifier)
  applicantId?: ResearchApplicantControlIdentifier;

  // The applicant enters the values assigned through the State review process.
  @UI.label("State Received Date")
  @UI.section(RRSF424Section.stateUse)
  @Response.role(ResponseRole.applicantInput)
  stateReceivedDate?: StateReceivedDate;

  @UI.label("State Application Identifier")
  @UI.section(RRSF424Section.stateUse)
  @minLength(1)
  @maxLength(30)
  @Response.role(ResponseRole.applicantInput)
  stateId?: StateApplicationIdentifier;

  @UI.label("Federal Identifier")
  @UI.section(RRSF424Section.stateUse)
  federalId?: ResearchFederalAwardIdentifier;

  @UI.label("Agency Routing Number")
  @UI.section(RRSF424Section.stateUse)
  // Assigned by the Federal agency and entered according to agency-specific instructions.
  @minLength(1)
  @maxLength(75)
  agencyRoutingNumber?: FederalAgencyRoutingNumber;

  @UI.label("Grants.gov Identifier")
  @UI.section(RRSF424Section.stateUse)
  // Assigned by Grants.gov for the prior submission and entered by the applicant here.
  @minLength(13)
  @maxLength(15)
  grantsTrackingNumber?: PreviousGrantsGovTrackingNumber;

  @UI.label("Applicant Information")
  @UI.section(RRSF424Section.applicantInformation)
  applicantInfo?: MultiProjectApplicant;

  @UI.label("Employer Identification Number")
  @UI.section(RRSF424Section.employerId)
  employerId?: EmployerIdentificationNumber;

  @UI.label("Type of Applicant")
  @UI.section(RRSF424Section.applicantType)
  applicantType?: MultiProjectApplicantType;

  @UI.label("Type of Application")
  @UI.section(RRSF424Section.applicationType)
  applicationType?: MultiProjectApplicationType;

  @UI.label("Federal Agency Name")
  @UI.section(RRSF424Section.federalAgency)
  federalAgencyName?: AgencyName;

  @UI.label("Assistance Listing Number")
  @UI.section(RRSF424Section.assistanceListing)
  assistanceListingNumber?: AssistanceListingNumber;

  @UI.label("Assistance Listing Title")
  @UI.section(RRSF424Section.assistanceListing)
  activityTitle?: AssistanceListingTitle;

  @UI.label("Project Title")
  @UI.section(RRSF424Section.projectTitle)
  @Validation.constraints(#{ maxLength: 200 })
  projectTitle?: ProjectTitle;

  @UI.label("Proposed Project Period")
  @UI.section(RRSF424Section.projectPeriod)
  proposedProjectPeriod?: MultiProjectPeriod;

  @UI.label("Applicant Congressional District")
  @UI.section(RRSF424Section.congressionalDistrict)
  @Validation.constraints(#{ pattern: "^(?:[A-Z]{2}|00)-[0-9]{3}$" })
  applicantCongressionalDistrict?: CongressionalDistrict;

  @UI.label("Project Director / Principal Investigator")
  @UI.section(RRSF424Section.principalInvestigator)
  principalInvestigator?: MultiProjectPrincipalInvestigator;

  @UI.label("Estimated Project Funding")
  @UI.section(RRSF424Section.estimatedFunding)
  estimatedProjectFunding?: MultiProjectEstimatedFunding;

  @UI.label("State Review")
  @UI.section(RRSF424Section.stateReview)
  stateReview?: MultiProjectStateReview;

  @UI.label("I agree")
  @UI.section(RRSF424Section.certification)
  @Response.role(ResponseRole.attestation)
  trustAgree?: AffirmativeCertification;

  @UI.label("SF-LLL or Other Explanatory Documentation")
  @UI.section(RRSF424Section.lobbyingDisclosure)
  @UI.widget(WidgetName.Attachment)
  sflllAttachment?: ResearchLobbyingDisclosure;

  @UI.label("Authorized Representative")
  @UI.section(RRSF424Section.authorizedRepresentative)
  authorizedRepresentative?: MultiProjectAuthorizedRepresentative;

  @UI.label("Signature of Authorized Representative")
  @UI.section(RRSF424Section.authorizedRepresentative)
  @Response.role(ResponseRole.attestation)
  @minLength(1)
  @maxLength(144)
  aorSignature?: MultiProjectSignature;

  @UI.label("Date Signed")
  @UI.section(RRSF424Section.authorizedRepresentative)
  @Response.role(ResponseRole.attestation)
  aorSignedDate?: plainDate;

  @UI.label("Pre-application")
  @UI.section(RRSF424Section.preApplication)
  @UI.widget(WidgetName.Attachment)
  preApplicationAttachment?: ResearchPreApplication;

  @UI.label("Cover Letter")
  @UI.section(RRSF424Section.coverLetter)
  @UI.widget(WidgetName.Attachment)
  coverLetterAttachment?: ResearchCoverLetter;
}

@@UI.section(RRSF424MultiProjectCover.submissionTypeCode, RRSF424Section.submissionType);
