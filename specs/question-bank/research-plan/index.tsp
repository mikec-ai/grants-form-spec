import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";

using SimplerForms;
using QuestionBank.Generics;

/** Source-defined research-content attachments used by PHS research applications. */
namespace QuestionBank.ResearchPlan;

/** Provide the introduction required for an eligible resubmission or revision application. */
@Question.meta(#{ id: "research-plan/introduction", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanIntroduction extends AttachmentRef;

/** State the specific aims of the proposed research. */
@Question.meta(#{ id: "research-plan/specific-aims", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanSpecificAims extends AttachmentRef;

/** Describe the significance, innovation, and approach of the proposed research. */
@Question.meta(#{ id: "research-plan/research-strategy", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanStrategy extends AttachmentRef;

/** Provide the publication list required for an eligible renewal application. */
@Question.meta(#{ id: "research-plan/progress-report-publication-list", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanProgressReportPublicationList extends AttachmentRef;

/** Address the vertebrate-animal information requested for the proposed research. */
@Question.meta(#{ id: "research-plan/vertebrate-animals-document", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanVertebrateAnimalsDocument extends AttachmentRef;

/** Address the select-agent information requested for the proposed research. */
@Question.meta(#{ id: "research-plan/select-agent-research", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanSelectAgentResearch extends AttachmentRef;

/** Describe governance and responsibilities for a multiple-PD/PI application. */
@Question.meta(#{ id: "research-plan/multiple-pdpi-leadership-plan", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanMultiplePdPiLeadershipPlan extends AttachmentRef;

/** Describe consortium or contractual arrangements for the proposed research. */
@Question.meta(#{ id: "research-plan/consortium-contractual-arrangements", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanConsortiumContractualArrangements extends AttachmentRef;

/** Provide the letters of support requested for the proposed research. */
@Question.meta(#{ id: "research-plan/letters-of-support", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanLettersOfSupport extends AttachmentRef;

/** Describe applicable plans for sharing research resources. */
@Question.meta(#{ id: "research-plan/resource-sharing-plans", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanResourceSharingPlans extends AttachmentRef;

/** Provide another applicable research plan, including a data management and sharing plan. */
@Question.meta(#{ id: "research-plan/other-plans", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanOtherPlans extends AttachmentRef;

/** Describe authentication of key biological or chemical resources used by the research. */
@Question.meta(#{ id: "research-plan/key-resource-authentication", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanKeyResourceAuthentication extends AttachmentRef;

/** Provide one policy-allowed appendix document for the research application. */
@Question.meta(#{ id: "research-plan/appendix-document", status: "draft" })
@Response.role(ResponseRole.applicantInput)
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.narrative, TagName.attachment)
scalar ResearchPlanAppendixDocument extends AttachmentRef;
