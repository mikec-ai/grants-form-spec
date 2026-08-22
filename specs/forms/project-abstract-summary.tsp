import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/opportunity/index.tsp";
import "../question-bank/primary-org/index.tsp";
import "../question-bank/project/index.tsp";

using SimplerForms;
using QuestionBank.Opportunity;
using QuestionBank.PrimaryOrg;
using QuestionBank.Project;

namespace Forms.ProjectAbstractSummary;

enum ProjectAbstractSummarySection {
  /** This Project Abstract Summary form must be submitted or the application will be considered incomplete. Ensure the Project Abstract field succinctly describes the project in plain language that the public can understand and use without the full proposal. Use 4,000 characters or less. Do not include personally identifiable, sensitive or proprietary information. Refer to Agency instructions for any additional Project Abstract field requirements. If the application is funded, your project abstract information (as submitted) will be made available to public websites and/or databases including USAspending.gov. */
  projectAbstractSummary: "1. Project Abstract Summary",
}

/** Project Abstract Summary, Grants.gov form version 2.0. */
@Form.meta(#{
  id: "project-abstract-summary",
  formId: "bf683068-23a4-43fa-ac7a-0f046b83cb14",
  legacyFormId: 591,
  formName: "Project Abstract Summary",
  shortFormName: "Project_AbstractSummary_2_0",
  formVersion: "2.0",
  agencyCode: "SGG",
  ombNumber: "4040-0019",
  formType: "ProjectAbstractSummary",
  sggVersion: "1.0",
})
@UI.sections(ProjectAbstractSummarySection)
@Sgg.prePopulate(#{
  `fundingOpportunityNumber`: SggPrePop.opportunityNumber,
  `assistanceListingNumber`: SggPrePop.assistanceListingNumber,
})
model ProjectAbstractSummary {
  @UI.label("Funding Opportunity Number")
  @UI.section(ProjectAbstractSummarySection.projectAbstractSummary)
  fundingOpportunityNumber: OpportunityNumber;

  @UI.label("Assistance Listing Number")
  @UI.section(ProjectAbstractSummarySection.projectAbstractSummary)
  assistanceListingNumber?: AssistanceListingNumber;

  @UI.label("Applicant Name")
  @UI.helpText("This should match the 'Legal Name' field from the SF-424 form")
  @UI.section(ProjectAbstractSummarySection.projectAbstractSummary)
  applicantName: LegalName;

  @UI.label("Descriptive Title of Applicant's Project")
  @UI.helpText("This should match the 'Project Title' field from the SF-424 form")
  @UI.section(ProjectAbstractSummarySection.projectAbstractSummary)
  @Validation.constraints(#{ maxLength: 250 })
  projectTitle: ProjectTitle;

  @UI.section(ProjectAbstractSummarySection.projectAbstractSummary)
  projectAbstract: ProjectAbstract;
}
