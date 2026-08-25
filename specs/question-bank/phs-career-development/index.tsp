import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";
import "../research-application/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.ResearchApplication;

/** Portable, source-bound questions introduced by PHS 398 Career Development Award Supplemental 6.0. */
namespace QuestionBank.PHSCareerDevelopment;

/** Attach the candidate's information and goals for career development. */
@Question.meta(#{ id: "candidate/career-development-information-and-goals", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar CareerCandidateInformationAndGoals extends AttachmentRef;

/** Attach the candidate's training in the responsible conduct of research. */
@Question.meta(#{ id: "research-policy/responsible-conduct-training-plan", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar CareerResponsibleConductOfResearch extends AttachmentRef;

/** Attach the candidate's plan for providing mentoring. */
@Question.meta(#{ id: "candidate/plan-to-provide-mentoring", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar CareerCandidateMentoringPlan extends AttachmentRef;

/** Attach the mentor and co-mentor plans and statements. */
@Question.meta(#{ id: "mentoring/mentor-and-co-mentor-statements", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar CareerMentorStatements extends AttachmentRef;

/** Attach a description of the institutional environment supporting the candidate. */
@Question.meta(#{ id: "research-environment/institutional-environment-description", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar CareerInstitutionalEnvironment extends AttachmentRef;

/** Attach the institution's commitment to the candidate's research career development. */
@Question.meta(#{ id: "research-environment/institutional-career-development-commitment", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.primaryOrg)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar CareerInstitutionalCommitment extends AttachmentRef;

/** Attach the candidate's contribution to program goals. */
@Question.meta(#{ id: "candidate/contribution-to-program-goals", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar CareerCandidateContribution extends AttachmentRef;

enum CareerNonUsCitizenStatus {
  permanentVisa: "Permanent U.S. Resident Visa",
  temporaryVisa: "Temporary U.S. Visa",
  notResidingInUs: "Not Residing in the U.S.",
}

/** Report the candidate's source-defined citizenship and residency status. */
@Question.meta(#{ id: "candidate/citizenship-and-residency-status", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.principalInvestigator)
@Catalog.tag(TagName.person, TagName.details)
model QuestionCareerCandidateCitizenship {
  @UI.label("U.S. Citizen or Non-Citizen National?")
  usCitizenOrNational: YesNoCode;

  @UI.label("Non-U.S. Citizen Status")
  @UI.enabledWhen(QuestionCareerCandidateCitizenship.usCitizenOrNational, YesNoCode.no)
  @Validation.requiredWhen(QuestionCareerCandidateCitizenship.usCitizenOrNational, YesNoCode.no)
  nonUsCitizenStatus?: CareerNonUsCitizenStatus;

  @UI.label("Permanent Resident by Award")
  @UI.enabledWhen(
    QuestionCareerCandidateCitizenship.nonUsCitizenStatus,
    CareerNonUsCitizenStatus.temporaryVisa,
  )
  permanentResidentByAward?: YesNoCode;
}
