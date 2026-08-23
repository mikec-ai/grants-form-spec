import "@simpler-grants/form-spec";

using SimplerForms;

namespace PromotionDraft.PerformanceSite;

// Generated staging scaffold. Source facts are transcribed; semantic reuse is not accepted here.
// Promotion packet source set: sha256:ba3348472c48a2fac951308c9a8f44fc078c5b014771d7e9d1a4b0521a00d879

model PrimarySiteAddressDraft {
  // Source: PerformanceSite_4_0.PrimarySite.Address.Street1 (unresolved/unreviewed)
  @UI.label("Street1")
  @minLength(1)
  @maxLength(55)
  street1: string;

  // Source: PerformanceSite_4_0.PrimarySite.Address.Street2 (unresolved/unreviewed)
  @UI.label("Street2")
  @minLength(1)
  @maxLength(55)
  street2?: string;

  // Source: PerformanceSite_4_0.PrimarySite.Address.City (unresolved/unreviewed)
  @UI.label("City")
  @minLength(1)
  @maxLength(35)
  city: string;

  // Source: PerformanceSite_4_0.PrimarySite.Address.County (unresolved/unreviewed)
  @UI.label("County")
  @minLength(1)
  @maxLength(30)
  county?: string;

  // Source: PerformanceSite_4_0.PrimarySite.Address.State (unresolved/unreviewed)
  // REVIEW: 71 extracted enum values remain in the promotion packet.
  @UI.label("State")
  state?: string;

  // Source: PerformanceSite_4_0.PrimarySite.Address.Province (unresolved/unreviewed)
  @UI.label("Province")
  @minLength(1)
  @maxLength(30)
  province?: string;

  // Source: PerformanceSite_4_0.PrimarySite.Address.ZipPostalCode (unresolved/unreviewed)
  @UI.label("ZipPostalCode")
  @minLength(1)
  @maxLength(30)
  zipPostalCode?: string;

  // Source: PerformanceSite_4_0.PrimarySite.Address.Country (unresolved/unreviewed)
  // REVIEW: 261 extracted enum values remain in the promotion packet.
  @UI.label("Country")
  country: string;
}

model OtherSiteAddressDraft {
  // Source: PerformanceSite_4_0.OtherSite.Address.Street1 (unresolved/unreviewed)
  @UI.label("Street1")
  @minLength(1)
  @maxLength(55)
  street1: string;

  // Source: PerformanceSite_4_0.OtherSite.Address.Street2 (unresolved/unreviewed)
  @UI.label("Street2")
  @minLength(1)
  @maxLength(55)
  street2?: string;

  // Source: PerformanceSite_4_0.OtherSite.Address.City (unresolved/unreviewed)
  @UI.label("City")
  @minLength(1)
  @maxLength(35)
  city: string;

  // Source: PerformanceSite_4_0.OtherSite.Address.County (unresolved/unreviewed)
  @UI.label("County")
  @minLength(1)
  @maxLength(30)
  county?: string;

  // Source: PerformanceSite_4_0.OtherSite.Address.State (unresolved/unreviewed)
  // REVIEW: 71 extracted enum values remain in the promotion packet.
  @UI.label("State")
  state?: string;

  // Source: PerformanceSite_4_0.OtherSite.Address.Province (unresolved/unreviewed)
  @UI.label("Province")
  @minLength(1)
  @maxLength(30)
  province?: string;

  // Source: PerformanceSite_4_0.OtherSite.Address.ZipPostalCode (unresolved/unreviewed)
  @UI.label("ZipPostalCode")
  @minLength(1)
  @maxLength(30)
  zipPostalCode?: string;

  // Source: PerformanceSite_4_0.OtherSite.Address.Country (unresolved/unreviewed)
  // REVIEW: 261 extracted enum values remain in the promotion packet.
  @UI.label("Country")
  country: string;
}

model PrimarySiteDraft {
  // Source: PerformanceSite_4_0.PrimarySite.Individual (unresolved/unreviewed)
  // REVIEW: 2 extracted enum values remain in the promotion packet.
  @UI.label("Individual")
  individual?: string;

  // Source: PerformanceSite_4_0.PrimarySite.OrganizationName (unresolved/unreviewed)
  @UI.label("OrganizationName")
  @minLength(1)
  @maxLength(60)
  organizationName?: string;

  // Source: PerformanceSite_4_0.PrimarySite.SAMUEI (unresolved/unreviewed)
  @UI.label("SAMUEI")
  @minLength(12)
  @maxLength(12)
  samuei?: string;

  // Source: PerformanceSite_4_0.PrimarySite.Address (container/deterministic)
  @UI.label("Address")
  address: PrimarySiteAddressDraft;

  // Source: PerformanceSite_4_0.PrimarySite.CongressionalDistrictProgramProject (unresolved/unreviewed)
  @UI.label("CongressionalDistrictProgramProject")
  @minLength(6)
  @maxLength(6)
  congressionalDistrictProgramProject?: string;
}

model OtherSiteDraft {
  // Source: PerformanceSite_4_0.OtherSite.Individual (unresolved/unreviewed)
  // REVIEW: 2 extracted enum values remain in the promotion packet.
  @UI.label("Individual")
  individual?: string;

  // Source: PerformanceSite_4_0.OtherSite.OrganizationName (unresolved/unreviewed)
  @UI.label("OrganizationName")
  @minLength(1)
  @maxLength(60)
  organizationName?: string;

  // Source: PerformanceSite_4_0.OtherSite.SAMUEI (unresolved/unreviewed)
  @UI.label("SAMUEI")
  @minLength(12)
  @maxLength(12)
  samuei?: string;

  // Source: PerformanceSite_4_0.OtherSite.Address (container/deterministic)
  @UI.label("Address")
  address: OtherSiteAddressDraft;

  // Source: PerformanceSite_4_0.OtherSite.CongressionalDistrictProgramProject (unresolved/unreviewed)
  @UI.label("CongressionalDistrictProgramProject")
  @minLength(6)
  @maxLength(6)
  congressionalDistrictProgramProject?: string;
}

model AttachedFileDraft {
  // Source: PerformanceSite_4_0.AttachedFile.FileName (technical_field/deterministic)
  @UI.label("FileName")
  @minLength(1)
  @maxLength(255)
  fileName: string;

  // Source: PerformanceSite_4_0.AttachedFile.MimeType (technical_field/deterministic)
  @UI.label("MimeType")
  @minLength(1)
  @maxLength(255)
  mimeType: string;

  // Source: PerformanceSite_4_0.AttachedFile.FileLocation (technical_field/deterministic)
  @UI.label("FileLocation")
  fileLocation: string;

  // Source: PerformanceSite_4_0.AttachedFile.HashValue (technical_field/deterministic)
  @UI.label("HashValue")
  hashValue: string;
}

/** Review-gated source scaffold; not a canonical form declaration. */
@Form.meta(#{
  id: "draft/performanceSite",
  legacyFormId: 723,
  formName: "[Promotion draft] Project/Performance Site Location(s)",
  shortFormName: "PerformanceSite_4_0",
  formVersion: "4.0",
  agencyCode: "GRANTS_GOV",
})
model PerformanceSiteDraft {
  // Source: PerformanceSite_4_0.PrimarySite (container/deterministic)
  @UI.label("PrimarySite")
  primarySite: PrimarySiteDraft;

  // Source: PerformanceSite_4_0.OtherSite (container/deterministic)
  @UI.label("OtherSite")
  @minItems(0)
  @maxItems(299)
  otherSite?: OtherSiteDraft[];

  // Source: PerformanceSite_4_0.AttachedFile (attachment/deterministic)
  @UI.label("AttachedFile")
  attachedFile?: AttachedFileDraft;
}
