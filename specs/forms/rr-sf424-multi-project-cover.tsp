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

// These three values are source fields in the multi-project exchange form. The standalone
// R&R cover's same-looking fields are runtime-populated in Simpler. Keep them local until
// semantic review confirms whether the multi-project workflow has the same lifecycle owner.
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

model MultiProjectApplicationType {
  @UI.label("Application Type")
  applicationTypeCode?: ResearchApplicationTypeCode;

  @UI.label("Is this application being submitted to another agency?")
  isOtherAgencySubmission?: YesNoCode;

  @UI.label("Other Agency Submission Explanation")
  @minLength(1)
  @maxLength(20)
  @UI.enabledWhen(MultiProjectApplicationType.isOtherAgencySubmission, YesNoCode.yes)
  otherAgencySubmissionExplanation?: string;

  @UI.label("Revision Code")
  @UI.encodedCheckboxGroup(#{
    choices: #[
      #{ code: "A", label: "A. Increase Award" },
      #{ code: "B", label: "B. Decrease Award" },
      #{ code: "C", label: "C. Increase Duration" },
      #{ code: "D", label: "D. Decrease Duration" },
      #{ code: "E", label: "E. Other" },
    ],
    combinations: #[
      #{ value: "A", members: #["A"] },
      #{ value: "B", members: #["B"] },
      #{ value: "C", members: #["C"] },
      #{ value: "D", members: #["D"] },
      #{ value: "E", members: #["E"] },
      #{ value: "AC", members: #["A", "C"] },
      #{ value: "AD", members: #["A", "D"] },
      #{ value: "BC", members: #["B", "C"] },
      #{ value: "BD", members: #["B", "D"] },
    ],
  })
  @UI.enabledWhen(MultiProjectApplicationType.applicationTypeCode, ResearchApplicationTypeCode.revision)
  revisionCode?: ResearchRevisionCode;

  @UI.label("Other Revision Explanation")
  @minLength(1)
  @maxLength(45)
  @UI.enabledWhen(MultiProjectApplicationType.revisionCode, ResearchRevisionCode.E)
  revisionCodeOtherExplanation?: string;
}

model MultiProjectApplicantType {
  @UI.label("Applicant Type")
  applicantTypeCode?: ApplicantTypeCode;

  @UI.label("Other Applicant Type Explanation")
  @minLength(1)
  @maxLength(50)
  @UI.enabledWhen(MultiProjectApplicantType.applicantTypeCode, ApplicantTypeCode.X)
  applicantTypeCodeOtherExplanation?: string;

  @UI.label("Small Business Organization Type")
  @UI.enabledWhen(MultiProjectApplicantType.applicantTypeCode, ApplicantTypeCode.R)
  smallBusinessOrganizationType?: ResearchSmallBusinessType;
}

model MultiProjectPeriod {
  @UI.label("Proposed Start Date")
  proposedStartDate?: ProjectStartDate;

  @UI.label("Proposed End Date")
  proposedEndDate?: ProjectEndDate;
}

model MultiProjectEstimatedFunding {
  @UI.label("Total Federal Funds Requested")
  @minValue(0)
  @maxValue(9999999999999.99)
  totalEstimatedAmount?: float64;

  @UI.label("Total Non-Federal Funds")
  @minValue(0)
  @maxValue(9999999999999.99)
  totalNonFederalRequested?: float64;

  @UI.label("Total Federal and Non-Federal Funds")
  @minValue(0)
  @maxValue(9999999999999.99)
  totalFederalNonFederalRequested?: float64;

  @UI.label("Estimated Program Income")
  @minValue(0)
  @maxValue(9999999999999.99)
  estimatedProgramIncome?: float64;
}

model MultiProjectStateReview {
  @UI.label("State Review")
  stateReviewCodeType?: ResearchStateReviewCode;

  @UI.label("State Review Date")
  @UI.enabledWhen(MultiProjectStateReview.stateReviewCodeType, ResearchStateReviewCode.yes)
  stateReviewDate?: plainDate;
}

/** Research & Related Multi-Project Cover, Grants.gov form version 4.0. */
@Form.meta(#{
  id: "rr-sf424-multi-project-cover",
  formId: "6d1fcf04-63e9-5951-841f-8ff06071f40c",
  legacyFormId: 769,
  formName: "[Draft] Research & Related Multi-Project Cover",
  shortFormName: "RR_SF424_Multi_Project_Cover_4_0",
  formVersion: "4.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0001",
  formType: "RRSF424MPCover",
  sggVersion: "1.0",
})
@UI.sections(RRSF424Section)
model RRSF424MultiProjectCover {
  @UI.label("Type of Submission")
  @UI.section(RRSF424Section.submissionType)
  submissionTypeCode?: ResearchSubmissionType;

  @UI.label("Date Submitted")
  @UI.section(RRSF424Section.submittedDate)
  submittedDate?: plainDate;

  @UI.label("Applicant Identifier")
  @UI.section(RRSF424Section.applicantIdentifier)
  @minLength(1)
  @maxLength(30)
  applicantId?: string;

  @UI.label("State Received Date")
  @UI.section(RRSF424Section.stateUse)
  stateReceivedDate?: plainDate;

  @UI.label("State Application Identifier")
  @UI.section(RRSF424Section.stateUse)
  @minLength(1)
  @maxLength(30)
  stateId?: string;

  @UI.label("Federal Identifier")
  @UI.section(RRSF424Section.stateUse)
  @minLength(1)
  @maxLength(30)
  federalId?: string;

  @UI.label("Agency Routing Number")
  @UI.section(RRSF424Section.stateUse)
  @minLength(1)
  @maxLength(75)
  agencyRoutingNumber?: string;

  @UI.label("Grants.gov Identifier")
  @UI.section(RRSF424Section.stateUse)
  @minLength(13)
  @maxLength(15)
  grantsTrackingNumber?: string;

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
  @minLength(1)
  @maxLength(144)
  aorSignature?: MultiProjectSignature;

  @UI.label("Date Signed")
  @UI.section(RRSF424Section.authorizedRepresentative)
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
