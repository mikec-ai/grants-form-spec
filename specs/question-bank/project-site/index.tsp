import "@simpler-grants/form-spec";
import "../index.tsp";
import "../generics/index.tsp";
import "../primary-org/index.tsp";
import "../project/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.PrimaryOrg;
using QuestionBank.Project;

namespace QuestionBank.ProjectSite;

enum SiteIndividualIndicator {
  yes: "Y: Yes",
  no: "N: No",
}

/** Organization, address, and congressional district for a project performance site. */
@Question.meta(#{ id: "project-site/details" })
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.organization, TagName.address, TagName.details)
model QuestionProjectSiteDetails {
  @UI.label("Submitting as an Individual")
  individual?: SiteIndividualIndicator;

  @UI.label("Organization Name")
  organizationName?: OrganizationName;

  @UI.label("UEI")
  samUei?: SamUei;

  @UI.label("Address")
  address: QuestionAddress;

  @UI.label("Project / Performance Site Congressional District")
  @Validation.constraints(#{ minLength: 6, maxLength: 6, pattern: "^..-...$" })
  @Validation.requiredWhenPath("address.country", CountryCode.USA)
  congressionalDistrict?: CongressionalDistrict;
}

/** Overflow file for project sites beyond the structured-entry capacity. */
@Question.meta(#{
  id: "project-site/additional-locations-upload",
  classification: BlockClassification.captureMechanism,
})
@Catalog.entity(EntityName.project)
@Catalog.tag(TagName.organization, TagName.address, TagName.attachment)
scalar AdditionalProjectSites extends AttachmentRef;
