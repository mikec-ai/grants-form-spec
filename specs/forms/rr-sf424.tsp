import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/aor/index.tsp";
import "../question-bank/application/index.tsp";
import "../question-bank/generics/index.tsp";
import "../question-bank/opportunity/index.tsp";
import "../question-bank/primary-org/index.tsp";
import "../question-bank/project/index.tsp";
import "../question-bank/research-application/index.tsp";

using SimplerForms;
using QuestionBank.Aor;
using QuestionBank.Application;
using QuestionBank.Generics;
using QuestionBank.Opportunity;
using QuestionBank.PrimaryOrg;
using QuestionBank.Project;
using QuestionBank.ResearchApplication;

namespace Forms.RRSF424;

enum RRSF424Section {
  submissionType: "1. Type of Submission",
  submittedDate: "2. Date Submitted",
  applicantIdentifier: "3. Applicant Identifier",
  stateUse: "4. Federal and State Identifiers",
  applicantInformation: "5. Applicant Information",
  employerId: "6. Employer Identification Number",
  applicantType: "7. Type of Applicant",
  applicationType: "8. Type of Application",
  federalAgency: "9. Name of Federal Agency",
  assistanceListing: "10. Assistance Listing Number and Title",
  projectTitle: "11. Descriptive Title of Applicant's Project",
  projectPeriod: "12. Proposed Project Period",
  congressionalDistrict: "13. Congressional District of Applicant",
  principalInvestigator: "14. Project Director / Principal Investigator",
  estimatedFunding: "15. Estimated Project Funding",
  stateReview: "16. State Review",
  certification: "17. Certification",
  lobbyingDisclosure: "18. Lobbying Disclosure",
  authorizedRepresentative: "19. Authorized Representative",
  preApplication: "20. Pre-application",
  coverLetter: "21. Cover Letter",
}

enum ResearchSubmissionType {
  preapplication: "Preapplication",
  application: "Application",
  changedCorrected: "Change/Corrected Application",
}

enum ResearchApplicationTypeCode {
  new: "New",
  resubmission: "Resubmission",
  renewal: "Renewal",
  continuation: "Continuation",
  revision: "Revision",
}

enum ResearchRevisionCode {
  A: "A",
  B: "B",
  C: "C",
  D: "D",
  E: "E",
  AC: "AC",
  AD: "AD",
  BC: "BC",
  BD: "BD",
}

enum YesNoCode {
  yes: "Y: Yes",
  no: "N: No",
}

enum AffirmativeCertification {
  yes: "Y: Yes",
}

enum ResearchStateReviewCode {
  yes: "Y: Yes",
  notCovered: "Program is not covered by E.O. 12372",
  notSelected: "Program has not been selected by state for review",
}

model ResearchApplicationType {
  @UI.label("Application Type")
  applicationTypeCode: ResearchApplicationTypeCode;

  @UI.label("Is this application being submitted to another agency?")
  isOtherAgencySubmission: YesNoCode;

  @UI.label("Other Agency Submission Explanation")
  @minLength(1)
  @maxLength(20)
  @Validation.requiredWhen(ResearchApplicationType.isOtherAgencySubmission, YesNoCode.yes)
  @UI.visibleWhen(ResearchApplicationType.isOtherAgencySubmission, YesNoCode.yes)
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
  @Validation.requiredWhen(ResearchApplicationType.applicationTypeCode, ResearchApplicationTypeCode.revision)
  @UI.visibleWhen(ResearchApplicationType.applicationTypeCode, ResearchApplicationTypeCode.revision)
  revisionCode?: ResearchRevisionCode;

  @UI.label("Other Revision Explanation")
  @minLength(1)
  @maxLength(45)
  @Validation.requiredWhen(ResearchApplicationType.revisionCode, ResearchRevisionCode.E)
  @UI.visibleWhen(ResearchApplicationType.revisionCode, ResearchRevisionCode.E)
  revisionCodeOtherExplanation?: string;
}

model ResearchSmallBusinessType {
  @UI.label("Socially and Economically Disadvantaged")
  sociallyEconomicallyDisadvantaged?: string;

  @UI.label("Women Owned")
  womenOwned?: string;
}

model ResearchApplicantType {
  @UI.label("Applicant Type")
  applicantTypeCode: ApplicantTypeCode;

  @UI.label("Other Applicant Type Explanation")
  @minLength(1)
  @maxLength(50)
  @Validation.requiredWhen(ResearchApplicantType.applicantTypeCode, ApplicantTypeCode.X)
  @UI.visibleWhen(ResearchApplicantType.applicantTypeCode, ApplicantTypeCode.X)
  applicantTypeCodeOtherExplanation?: string;

  @UI.label("Small Business Organization Type")
  @UI.visibleWhen(ResearchApplicantType.applicantTypeCode, ApplicantTypeCode.R)
  smallBusinessOrganizationType?: ResearchSmallBusinessType;
}

model ResearchProjectPeriod {
  @UI.label("Proposed Start Date")
  proposedStartDate: ProjectStartDate;

  @UI.label("Proposed End Date")
  @Validation.notBefore(ResearchProjectPeriod.proposedStartDate)
  proposedEndDate: ProjectEndDate;
}

model ResearchEstimatedFunding {
  @UI.label("Total Federal Funds Requested")
  @minValue(0)
  @maxValue(9999999999999.99)
  totalEstimatedAmount: float64;

  @UI.label("Total Non-Federal Funds")
  @minValue(0)
  @maxValue(9999999999999.99)
  totalNonFederalRequested: float64;

  @UI.label("Total Federal and Non-Federal Funds")
  @minValue(0)
  @maxValue(9999999999999.99)
  totalFederalNonFederalRequested: float64;

  @UI.label("Estimated Program Income")
  @minValue(0)
  @maxValue(9999999999999.99)
  estimatedProgramIncome: float64;
}

model ResearchStateReview {
  @UI.label("State Review")
  stateReviewCodeType: ResearchStateReviewCode;

  @UI.label("State Review Date")
  @Validation.requiredWhen(ResearchStateReview.stateReviewCodeType, ResearchStateReviewCode.yes)
  @UI.visibleWhen(ResearchStateReview.stateReviewCodeType, ResearchStateReviewCode.yes)
  stateReviewDate?: plainDate;
}

/** Research & Related Application for Federal Assistance, Grants.gov form version 5.0. */
@Form.meta(#{
  id: "rr-sf424",
  formId: "98f03cc4-5cd8-455b-a318-ba5abd0cf572",
  legacyFormId: 768,
  formName: "[Draft] Research & Related Application for Federal Assistance (SF424 R&R)",
  shortFormName: "RR_SF424_5_0",
  formVersion: "5.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0001",
  formType: "RRSF424",
  sggVersion: "1.0",
})
@UI.sections(RRSF424Section)
@Sgg.prePopulate(#{
  `federalAgencyName`: SggPrePop.agencyName,
  `assistanceListingNumber`: SggPrePop.assistanceListingNumber,
  `activityTitle`: SggPrePop.assistanceListingProgramTitle,
  `applicantInfo.organizationInfo.samUei`: SggPrePop.uei,
})
model RRSF424 {
  @UI.label("Type of Submission")
  @UI.section(RRSF424Section.submissionType)
  submissionTypeCode: ResearchSubmissionType;

  @UI.label("Date Submitted")
  @UI.section(RRSF424Section.submittedDate)
  @UI.readOnly
  submittedDate?: SubmittedDate;

  @UI.label("Applicant Identifier")
  @UI.section(RRSF424Section.applicantIdentifier)
  @minLength(1)
  @maxLength(30)
  applicantId?: string;

  @UI.label("State Received Date")
  @UI.section(RRSF424Section.stateUse)
  @UI.readOnly
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
  @Validation.requiredWhenPath("applicationType.applicationTypeCode", ResearchApplicationTypeCode.renewal)
  @Validation.requiredWhenPath("applicationType.applicationTypeCode", ResearchApplicationTypeCode.continuation)
  @Validation.requiredWhenPath("applicationType.applicationTypeCode", ResearchApplicationTypeCode.revision)
  federalId?: string;

  @UI.label("Agency Routing Number")
  @UI.section(RRSF424Section.stateUse)
  @minLength(1)
  @maxLength(75)
  agencyRoutingNumber?: string;

  @UI.label("Previous Grants.gov Tracking ID")
  @UI.section(RRSF424Section.stateUse)
  @minLength(13)
  @maxLength(15)
  @Validation.requiredWhen(RRSF424.submissionTypeCode, ResearchSubmissionType.changedCorrected)
  @UI.visibleWhen(RRSF424.submissionTypeCode, ResearchSubmissionType.changedCorrected)
  grantsGovTrackingId?: string;

  @UI.label("Applicant Information")
  @UI.section(RRSF424Section.applicantInformation)
  @Validation.requiredPaths(
    "organizationInfo.organizationName",
    "organizationInfo.address.street1",
    "organizationInfo.address.city",
    "organizationInfo.address.country",
    "organizationInfo.samUei",
    "contactPersonInfo.name.firstName",
    "contactPersonInfo.name.lastName",
    "contactPersonInfo.address.street1",
    "contactPersonInfo.address.city",
    "contactPersonInfo.address.country",
    "contactPersonInfo.phone",
    "contactPersonInfo.email"
  )
  @Validation.requiredPathWhen(
    "organizationInfo.address.state",
    "organizationInfo.address.country",
    CountryCode.USA
  )
  @Validation.requiredPathWhen(
    "organizationInfo.address.zipCode",
    "organizationInfo.address.country",
    CountryCode.USA
  )
  @Validation.requiredPathWhen(
    "contactPersonInfo.address.state",
    "contactPersonInfo.address.country",
    CountryCode.USA
  )
  @Validation.requiredPathWhen(
    "contactPersonInfo.address.zipCode",
    "contactPersonInfo.address.country",
    CountryCode.USA
  )
  applicantInfo: QuestionResearchApplicant;

  @UI.label("Employer Identification Number")
  @UI.section(RRSF424Section.employerId)
  employerId: EmployerIdentificationNumber;

  @UI.label("Type of Applicant")
  @UI.section(RRSF424Section.applicantType)
  applicantType: ResearchApplicantType;

  @UI.label("Type of Application")
  @UI.section(RRSF424Section.applicationType)
  applicationType: ResearchApplicationType;

  @UI.label("Federal Agency Name")
  @UI.section(RRSF424Section.federalAgency)
  @UI.readOnly
  federalAgencyName: AgencyName;

  @UI.label("Assistance Listing Number")
  @UI.section(RRSF424Section.assistanceListing)
  @UI.readOnly
  assistanceListingNumber?: AssistanceListingNumber;

  @UI.label("Assistance Listing Title")
  @UI.section(RRSF424Section.assistanceListing)
  @UI.readOnly
  activityTitle?: AssistanceListingTitle;

  @UI.label("Project Title")
  @UI.section(RRSF424Section.projectTitle)
  @Validation.constraints(#{ maxLength: 200 })
  projectTitle: ProjectTitle;

  @UI.label("Proposed Project Period")
  @UI.section(RRSF424Section.projectPeriod)
  proposedProjectPeriod: ResearchProjectPeriod;

  @UI.label("Applicant Congressional District")
  @UI.section(RRSF424Section.congressionalDistrict)
  @Validation.constraints(#{ pattern: "^(?:[A-Z]{2}|00)-[0-9]{3}$" })
  applicantCongressionalDistrict: CongressionalDistrict;

  @UI.label("Project Director / Principal Investigator")
  @UI.section(RRSF424Section.principalInvestigator)
  @Validation.requiredPaths(
    "name.firstName",
    "name.lastName",
    "organizationName",
    "address.street1",
    "address.city",
    "address.country",
    "phone",
    "email"
  )
  @Validation.requiredPathWhen("address.state", "address.country", CountryCode.USA)
  @Validation.requiredPathWhen("address.zipCode", "address.country", CountryCode.USA)
  principalInvestigator: QuestionPrincipalInvestigator;

  @UI.label("Estimated Project Funding")
  @UI.section(RRSF424Section.estimatedFunding)
  estimatedProjectFunding: ResearchEstimatedFunding;

  @UI.label("State Review")
  @UI.section(RRSF424Section.stateReview)
  stateReview: ResearchStateReview;

  @UI.label("I agree")
  @UI.section(RRSF424Section.certification)
  trustAgree: AffirmativeCertification;

  @UI.label("SF-LLL or Other Explanatory Documentation")
  @UI.section(RRSF424Section.lobbyingDisclosure)
  @UI.widget(WidgetName.Attachment)
  sflllAttachment?: ResearchLobbyingDisclosure;

  @UI.label("Authorized Representative")
  @UI.section(RRSF424Section.authorizedRepresentative)
  @Validation.requiredPaths(
    "name.firstName",
    "name.lastName",
    "title",
    "organizationName",
    "address.street1",
    "address.city",
    "address.country",
    "phone",
    "email"
  )
  @Validation.requiredPathWhen("address.state", "address.country", CountryCode.USA)
  @Validation.requiredPathWhen("address.zipCode", "address.country", CountryCode.USA)
  authorizedRepresentative: QuestionResearchAuthorizedRepresentative;

  @UI.label("Signature of Authorized Representative")
  @UI.section(RRSF424Section.authorizedRepresentative)
  @UI.readOnly
  aorSignature?: AorSignature;

  @UI.label("Date Signed")
  @UI.section(RRSF424Section.authorizedRepresentative)
  @UI.readOnly
  aorSignedDate?: AorDateSigned;

  @UI.label("Pre-application")
  @UI.section(RRSF424Section.preApplication)
  @UI.widget(WidgetName.Attachment)
  preApplicationAttachment?: ResearchPreApplication;

  @UI.label("Cover Letter")
  @UI.section(RRSF424Section.coverLetter)
  @UI.widget(WidgetName.Attachment)
  coverLetterAttachment?: ResearchCoverLetter;
}
