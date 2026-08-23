namespace SimplerForms;

/** How a reusable block participates in semantic analysis. */
enum BlockClassification {
  /** A stable information requirement that forms may ask or produce. */
  semanticQuestion,
  /** Reusable machinery used to capture an answer, rather than the answer's meaning. */
  captureMechanism,
}

/** Identity, lifecycle, and analytical classification for a bank block. */
model QuestionMeta {
  /** Semantic id, `entity/attribute` — e.g. "poc/details". */
  id: string;
  version?: string;
  status?: "draft" | "stable" | "deprecated";
  classification?: BlockClassification;
}

/** Portable identity, lifecycle, and source metadata for a form. */
model FormMeta {
  /** Semantic id — e.g. "key-contacts". */
  id: string;
  legacyFormId?: int32;
  formName: string;
  shortFormName: string;
  formVersion: string;
  agencyCode?: string;
  ombNumber?: string;
}

/** Source-specific constraints applied where a reusable question is composed into a form. */
model ValidationConstraints {
  minLength?: int32;
  maxLength?: int32;
  minItems?: int32;
  maxItems?: int32;
  pattern?: string;
}

enum TagName {
  address, phone, email, identifier, name, title, person, organization,
  details, generic, money, count, attachment, narrative, date, role,
}

enum EntityName {
  primaryOrg, fiscalSponsor, poc, principalInvestigator,
  authorizedRepresentative, project, opportunity, application, generic,
}

/** Mirrors the SGG frontend's WidgetTypes union. */
enum WidgetName {
  Attachment, AttachmentArray, Checkbox, EncodedCheckboxGroup, Text, TextArea,
  Radio, Select, MultiSelect, Print, PrintAttachment, FieldList, Table,
  Budget424aSectionA, Budget424aSectionB, Budget424aSectionC,
  Budget424aSectionD, Budget424aSectionE, Budget424aSectionF,
}

enum Op {
  Sum, Subtract, PercentOf,
}

/**
 * SGG's `gg_pre_population` rule names for external lookups.
 * Each member documents the canonical mapping that will replace it.
 */
enum SggPrePop {
  /** successor: @Map.from(Sources.Opportunity.agencyName) */
  agencyName: "agency_name",
  /** successor: @Map.from(Sources.Opportunity.number) */
  opportunityNumber: "opportunity_number",
  /** successor: @Map.from(Sources.Opportunity.title) */
  opportunityTitle: "opportunity_title",
  /** successor: @Map.from(Sources.Opportunity.assistanceListingNumber) */
  assistanceListingNumber: "assistance_listing_number",
  /** successor: @Map.from(Sources.Opportunity.assistanceListingProgramTitle) */
  assistanceListingProgramTitle: "assistance_listing_program_title",
  /** successor: @Map.from(Sources.Competition.publicId) */
  publicCompetitionId: "public_competition_id",
  /** successor: @Map.from(Sources.Competition.title) */
  competitionTitle: "competition_title",
  /** successor: @Map.from(Sources.OrgProfile.samUei) */
  uei: "uei",
}
