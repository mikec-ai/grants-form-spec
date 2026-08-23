import "@simpler-grants/form-spec";
import "./index.tsp";
import "../question-bank/generics/index.tsp";
import "../question-bank/project-site/index.tsp";

using SimplerForms;
using QuestionBank.Generics;
using QuestionBank.ProjectSite;

namespace Forms.PerformanceSite;

enum PerformanceSiteSection {
  primary: "Primary Project / Performance Site",
  additional: "Additional Project / Performance Sites",
  overflow: "Additional Locations Attachment",
}

model PerformanceSiteAddress extends QuestionAddress {
  @UI.label("State")
  @UI.enabledWhen(PerformanceSiteAddress.country, CountryCode.USA)
  state?: StateCode;

  @UI.label("Province")
  @minLength(1)
  @maxLength(30)
  @UI.readOnlyWhen(PerformanceSiteAddress.country, CountryCode.USA)
  province?: string;

  @UI.label("Zip / Postal Code")
  @minLength(1)
  @maxLength(30)
  @Validation.constraintsWhen(
    PerformanceSiteAddress.country,
    CountryCode.USA,
    #{ minLength: 9 },
  )
  zipCode?: string;
}

model PerformanceSiteDetails extends QuestionProjectSiteDetails {
  @UI.label("Address")
  address: PerformanceSiteAddress;
}

/** The primary location alone requires an organization when it is not an individual filing. */
model PrimaryPerformanceSiteDetails extends PerformanceSiteDetails {
  @UI.label("Organization Name")
  @Validation.requiredWhen(PrimaryPerformanceSiteDetails.individual, SiteIndividualIndicator.no)
  organizationName?: OrganizationName;
}

/** Project/Performance Site Location(s), Grants.gov version 4.0. */
@Form.meta(#{
  id: "performance-site",
  formId: "3dac12c6-ef6f-573e-8958-fedd16b3a8d2",
  legacyFormId: 723,
  formName: "Project/Performance Site Location(s)",
  shortFormName: "PerformanceSite_4_0",
  formVersion: "4.0",
  agencyCode: "GRANTS_GOV",
  ombNumber: "4040-0010",
  formType: "PerformanceSite",
  sggVersion: "1.0",
})
@UI.sections(PerformanceSiteSection)
model PerformanceSite {
  @UI.label("Primary Project / Performance Site")
  @UI.section(PerformanceSiteSection.primary)
  primarySite: PrimaryPerformanceSiteDetails;

  @UI.label("Additional Project / Performance Site")
  @UI.section(PerformanceSiteSection.additional)
  @Sgg.fieldList(#{ validateBeforeAdd: true })
  @maxItems(299)
  additionalSites?: PerformanceSiteDetails[];

  @UI.label("Additional Locations")
  @UI.section(PerformanceSiteSection.overflow)
  @UI.widget(WidgetName.Attachment)
  @UI.enabledWhenCount(PerformanceSite.additionalSites, 299)
  additionalLocations?: AdditionalProjectSites;
}
