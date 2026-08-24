import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/nifa/index.tsp";
import "../question-bank/opportunity/index.tsp";
import "../question-bank/primary-org/index.tsp";

using SimplerForms;
using QuestionBank.Nifa;
using QuestionBank.Opportunity;
using QuestionBank.PrimaryOrg;

namespace Forms.NifaSupplemental;

enum NifaSupplementalSection {
  /** Complete this form together with the SF-424 Application for Federal Financial Assistance. */
  fundingOpportunity: "1. Funding Opportunity",
  program: "2. Program to Which You Are Applying",
  applicantType: "3. Type of Applicant",
  additionalApplicantType: "4. Additional Applicant Types",
  supplementalApplicantTypes: "5. Supplemental Applicant Types (Check all that apply)",
  asapRecipientInformation: "6. ASAP Recipient Information",
  keywords: "7. Key Words",
  conflictOfInterestList: "8. Conflict of Interest List",
}

/** Funding-opportunity identity reused from the portable opportunity question bank. */
model NifaFundingOpportunity {
  @UI.label("Funding Opportunity Name")
  title: OpportunityTitle;

  @UI.label("Funding Opportunity Number")
  number: OpportunityNumber;
}

/** NIFA Supplemental Information, Grants.gov FID 483, version 1.2. */
@Form.meta(#{
  id: "nifa-supplemental",
  legacyFormId: 483,
  formName: "NIFA Supplemental Information",
  shortFormName: "NIFA_Supplemental_Info_1_2",
  formVersion: "1.2",
  agencyCode: "GRANTS_GOV",
  ombNumber: "0524-0039",
})
@UI.sections(NifaSupplementalSection)
@Sgg.prePopulate(#{
  `fundingOpportunity.title`: SggPrePop.opportunityTitle,
  `fundingOpportunity.number`: SggPrePop.opportunityNumber,
})
@UI.overrides(#{
  `additionalApplicantType.additionalApplicantType`: #{
    enabledWhen: #{
      path: "applicantType.applicantTypeCode",
      in: #[ApplicantTypeCode.H, ApplicantTypeCode.X]
    }
  },
})
model NifaSupplemental {
  @UI.section(NifaSupplementalSection.fundingOpportunity)
  @UI.readOnly
  fundingOpportunity: NifaFundingOpportunity;

  @UI.section(NifaSupplementalSection.program)
  program: QuestionNifaProgram;

  @UI.section(NifaSupplementalSection.applicantType)
  applicantType: QuestionApplicantTypeCode;

  @UI.label("Additional Applicant Types")
  @UI.section(NifaSupplementalSection.additionalApplicantType)
  @UI.widget(WidgetName.Select)
  @Validation.requiredWhenPath("applicantType.applicantTypeCode", ApplicantTypeCode.H)
  @Validation.requiredWhenPath("applicantType.applicantTypeCode", ApplicantTypeCode.X)
  additionalApplicantType?: QuestionNifaAdditionalApplicantType;

  @UI.section(NifaSupplementalSection.supplementalApplicantTypes)
  supplementalApplicantTypes?: QuestionNifaSupplementalApplicantTypes;

  @UI.section(NifaSupplementalSection.asapRecipientInformation)
  asapRecipientInformation: QuestionNifaAsapRecipientInformation;

  @UI.label("Key Words")
  @UI.section(NifaSupplementalSection.keywords)
  keywords: NifaApplicationKeywords;

  @UI.label("Conflict of Interest List")
  @UI.section(NifaSupplementalSection.conflictOfInterestList)
  @UI.widget(WidgetName.Attachment)
  conflictOfInterestList?: NifaConflictOfInterestList;
}
