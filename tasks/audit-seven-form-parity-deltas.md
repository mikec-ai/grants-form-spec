---
type: Task
title: Audit the twelve seven-form parity deltas
priority: P0
assignee: parity_delta_audit
description: >-
  Trace all twelve current intentional differences to exact evidence, classify
  them without assuming acceptance, and prepare contract-ready records that
  distinguish reviewed, proposed, and unresolved states.
superbee_progress_status: in_progress
superbee_updated_by: parity_delta_audit
generated:
  by: 'process:superbee'
  at: '2026-08-24T18:36:17.049Z'
---
## Audit scope and boundary

Audited consumer revision `1e4cdb8b6481a0e34946df7b380e8cf306d552cd` and producer revision `42070f20c1a755e624eebbfe284050976b050088`.

The cohort contains **12 form/dimension results**, **17 rationale groups**, and **50 exact difference keys**. All 50 keys are mechanically bounded by the uniform comparator. That proves the observed differences are complete and stable for this revision; it does **not** prove that their semantic reasons have been accepted.

All 17 cohort declarations currently cite only consumer test files. Independent tracing found exact authoritative producer evidence for **5 groups / 16 keys**. The other **12 groups / 34 keys** have partial, non-granular, implementation-only, or missing source support and must remain proposed or unresolved.

There are **11 positional UI keys**. They are index-brittle but not conceptually targetless: each can be migrated to a stable field, section, or policy identifier. The future ledger should store that stable target and retain the observed JSON pointer only as differential evidence.

No semantic mapping or intentional delta is marked accepted by this audit.

## Machine-usable audit

```json
{
  "contract": "parity-delta-evidence-audit/v1",
  "auditStatus": "agent-reviewed-proposal",
  "acceptanceAuthorityExercised": false,
  "consumer": {
    "repository": "https://github.com/mikec-ai/simpler-grants-gov",
    "revision": "1e4cdb8b6481a0e34946df7b380e8cf306d552cd",
    "cohortPath": "api/src/form_schema/form_spec/differential-cohort.json",
    "cohortSha256": "e73c947088a6b33b20ed368bca233bcab8544ae1f36972c33367a149264031d1"
  },
  "producer": {
    "repository": "https://github.com/mikec-ai/grants-form-spec",
    "revision": "42070f20c1a755e624eebbfe284050976b050088"
  },
  "inventory": {
    "formDimensionResults": 12,
    "rationaleGroups": 17,
    "exactKeys": 50,
    "mechanicallyBoundedKeys": 50,
    "groupsWithExactAuthoritativeProducerEvidence": 5,
    "keysWithExactAuthoritativeProducerEvidence": 16,
    "groupsWithoutExactAuthoritativeProducerEvidence": 12,
    "keysWithoutExactAuthoritativeProducerEvidence": 34,
    "positionalUiKeys": 11
  },
  "records": [
    {
      "id": "sf424.schema.system-ownership",
      "formId": "sf424",
      "dimension": "schema",
      "keys": [
        "/properties/date_received#readOnly",
        "/properties/total_estimated_funding#readOnly",
        "/properties/aor_signature#readOnly",
        "/properties/date_signed#readOnly"
      ],
      "classification": "proposed-system-ownership-correction",
      "observed": "portable adds readOnly=true; existing has no readOnly keyword",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424_parity.py",
      "producerEvidence": ["evidence/forms/sf424/evidence.json", "specs/forms/sf424.tsp"],
      "sourceSupport": "unverified",
      "sourceEvidence": ["grantsgov-sf424-xsd-4.0 sha256:21670776cc2751c806b1ec43a59d6296628e219733bc654cf518ede5b9ae0364"],
      "gap": "The pinned XSD establishes fields and types but not editability, lifecycle ownership, or the total calculation. No exact DAT, XFA, PDF, instruction, or runtime-ownership locator is attached to these four claims.",
      "reviewStatus": "proposed",
      "recommendedDisposition": "Keep fail-closed as proposed; split calculated total from submission-managed fields and add exact operational evidence before approval."
    },
    {
      "id": "sf424.schema.guidance",
      "formId": "sf424",
      "dimension": "schema",
      "keys": [
        "/properties/project_start_date#description",
        "/properties/project_end_date#description",
        "/properties/debt_explanation#description"
      ],
      "classification": "mixed-presentation-normalization-and-guidance-addition",
      "observed": "date descriptions remove one trailing space; debt explanation changes empty text to applicant guidance",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424_parity.py",
      "producerEvidence": ["specs/forms/sf424.tsp", "specs/question-bank/project/index.tsp", "evidence/forms/sf424/evidence.json"],
      "sourceSupport": "partial",
      "gap": "The date text is semantically identical whitespace normalization. The debt guidance has no exact official-source locator in the evidence record.",
      "reviewStatus": "proposed",
      "recommendedDisposition": "Split into a reviewed-technical whitespace record and a separately proposed debt-guidance record requiring a source locator."
    },
    {
      "id": "sf424.schema.aor-email-max-length",
      "formId": "sf424",
      "dimension": "schema",
      "keys": ["/properties/authorized_representative_email#maxLength"],
      "classification": "proposed-shared-canonical-constraint",
      "observed": "portable adds maxLength=60; existing has no maxLength",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424_parity.py",
      "producerEvidence": ["specs/question-bank/generics/index.tsp", "evidence/forms/sf424/evidence.json"],
      "sourceSupport": "unverified",
      "gap": "The form evidence pins only the root SF-424 XSD. It does not pin the imported type definition or an exact source path proving 60 for this occurrence.",
      "reviewStatus": "proposed",
      "recommendedDisposition": "Retain as proposed; pin the transitive XSD/type source and exact path before calling it a source correction."
    },
    {
      "id": "sf424.validation.aor-email-max-length",
      "formId": "sf424",
      "dimension": "validation",
      "keys": ["authorized_representative_email#maxLength"],
      "classification": "proposed-shared-canonical-constraint",
      "observed": "portable rejects the over-60-character corpus value; existing accepts it",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424_parity.py",
      "producerEvidence": ["specs/question-bank/generics/index.tsp", "evidence/forms/sf424/evidence.json"],
      "sourceSupport": "unverified",
      "gap": "Same missing transitive type/path evidence as the schema record.",
      "reviewStatus": "proposed",
      "recommendedDisposition": "Link to the schema constraint record; do not count the behavioral manifestation as a second semantic decision."
    },
    {
      "id": "sf424-short.schema.website-uri",
      "formId": "sf424-short",
      "dimension": "schema",
      "keys": ["/properties/applicant_web_address#format"],
      "classification": "source-correct-schema-constraint",
      "observed": "portable adds format=uri-reference; existing has no format",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424_short_parity.py",
      "producerEvidence": ["research/sf424-short/source-audit.json", "evidence/forms/sf424-short/evidence.json"],
      "sourceSupport": "verified",
      "sourceEvidence": ["SF424_Short_3_0.ApplicantWebAddress in grantsgov-sf424-short-xsd-3.0 sha256:82b0f2a0ddbbcfae4ec7e083188287fb05700e201ade3b2f69684241bf8baabd; xs:anyURI"],
      "reviewStatus": "proposed",
      "recommendedDisposition": "Eligible for explicit review as a source-correct delta; source verification alone does not constitute product acceptance."
    },
    {
      "id": "sf424-short.ui.operational-field-visibility",
      "formId": "sf424-short",
      "dimension": "ui",
      "keys": [
        "/0/children/0/type",
        "/1/children/0/type",
        "/1/children/1/type",
        "/3/children/0/type",
        "/3/children/1/type",
        "/4/children/13/type"
      ],
      "stableTargets": [
        "/agencyName",
        "/assistanceListingNumber",
        "/assistanceListingProgramTitle",
        "/fundingOpportunityNumber",
        "/fundingOpportunityTitle",
        "/samUei"
      ],
      "classification": "source-audited-editability-correction",
      "observed": "portable renders fields; existing uses null presentation nodes",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424_short_parity.py",
      "producerEvidence": ["research/sf424-short/source-audit.json", "specs/forms/sf424-short.tsp"],
      "sourceSupport": "verified",
      "sourceEvidence": ["Form DAT rows 1, 2-1, 2-2, 4-1, 4-2, and 5f-1; exact XFA field-event findings and source digests are recorded in the source audit; OCR was not used"],
      "gap": "SAM UEI remains context-dependent and the audit deliberately does not claim universal editability. The portable disposition is to remove unsupported unconditional readOnly while retaining prepopulation.",
      "reviewStatus": "proposed",
      "recommendedDisposition": "Replace six positional pointers with stable field targets; preserve the source-audit conflict note, especially for SAM UEI."
    },
    {
      "id": "sf424a.schema.block-headings-guidance",
      "formId": "sf424a",
      "dimension": "schema",
      "keys": [
        "/properties/total_budget_summary#title",
        "/properties/total_budget_summary#description",
        "/properties/total_budget_categories#title",
        "/properties/total_budget_categories#description",
        "/properties/total_non_federal_resources#title",
        "/properties/total_non_federal_resources#description",
        "/properties/total_federal_fund_estimates#title",
        "/properties/total_federal_fund_estimates#description"
      ],
      "classification": "mixed-canonical-heading-and-guidance-addition",
      "observed": "portable adds four titles and four descriptions; existing omits them",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424a_parity.py",
      "producerEvidence": ["specs/question-bank/budget/index.tsp", "evidence/forms/sf424a/evidence.json"],
      "sourceSupport": "partial",
      "gap": "The form evidence maps other SF-424A fields but has no exact source paths or instruction locators for these eight strings. Titles resemble official table headings, while descriptions are normalized summaries; the current group hides that distinction.",
      "reviewStatus": "proposed",
      "recommendedDisposition": "Split titles from descriptions and add exact source locators or classify descriptions honestly as authored guidance."
    },
    {
      "id": "sf424a.schema.optional-nonempty-explanations",
      "formId": "sf424a",
      "dimension": "schema",
      "keys": [
        "/properties/direct_charges_explanation#minLength",
        "/properties/indirect_charges_explanation#minLength",
        "/properties/remarks#minLength"
      ],
      "classification": "source-correct-schema-constraint",
      "observed": "portable minLength=1; existing minLength=0; properties remain optional",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424a_parity.py",
      "producerEvidence": ["evidence/forms/sf424a/evidence.json", "specs/question-bank/budget/index.tsp"],
      "sourceSupport": "verified",
      "sourceEvidence": ["BudgetInformation.OtherInformation.OtherDirectChargesExplanation length 1-50; OtherIndirectChargesExplanation length 1-50; Remarks length 1-250 in SF424A-V1.0.xsd sha256:d5a636733d72c1e4cc9087ffc59b3d10000ee51f80da0dde3150ff91bcad0b5c"],
      "reviewStatus": "proposed",
      "recommendedDisposition": "Eligible for explicit review as source-correct constraints; retain optionality and exact-empty normalization boundary."
    },
    {
      "id": "sf424a.ui.section-a-guidance",
      "formId": "sf424a",
      "dimension": "ui",
      "keys": ["/0/description"],
      "stableTargets": ["section:SectionA"],
      "classification": "proposed-in-form-guidance-addition",
      "observed": "portable adds multi-sentence Section A guidance; existing has no section description",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424a_parity.py",
      "producerEvidence": ["specs/forms/sf424a.tsp", "evidence/forms/sf424a/evidence.json"],
      "sourceSupport": "partial",
      "gap": "The wording is presented as source-derived, but the current producer evidence has no exact PDF/instruction page locator for the full text or the manual Column G claim.",
      "reviewStatus": "proposed",
      "recommendedDisposition": "Replace the positional key with SectionA and add exact instruction/PDF locator before calling the full guidance source-verified."
    },
    {
      "id": "sf424a.validation.nonempty-source-fields",
      "formId": "sf424a",
      "dimension": "validation",
      "keys": [
        "activity_line_items[0].activity_title#minLength",
        "activity_line_items[0].assistance_listing_number#minLength",
        "direct_charges_explanation#minLength",
        "indirect_charges_explanation#minLength",
        "remarks#minLength"
      ],
      "classification": "source-correct-validation-constraint",
      "observed": "portable rejects supplied empty strings; existing accepts them; exact-empty normalization preserves legacy omission behavior for three root explanations",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424a_parity.py",
      "producerEvidence": ["evidence/forms/sf424a/evidence.json", "specs/forms/sf424a.tsp", "specs/question-bank/budget/index.tsp"],
      "sourceSupport": "verified",
      "sourceEvidence": ["SummaryLineItem.@activityTitle length 1-120; SummaryLineItem.CFDANumber length 1-15; three OtherInformation fields as recorded in sf424a evidence; SF424A-V1.0.xsd sha256:d5a636733d72c1e4cc9087ffc59b3d10000ee51f80da0dde3150ff91bcad0b5c"],
      "reviewStatus": "proposed",
      "recommendedDisposition": "Link manifestations to their schema constraints rather than treating five corpus observations as independent semantic decisions."
    },
    {
      "id": "key-contacts.schema.guidance",
      "formId": "key-contacts",
      "dimension": "schema",
      "keys": [
        "/properties/key_contacts#description",
        "/properties/key_contacts/items/properties/phone#description",
        "/properties/key_contacts/items/properties/fax#description",
        "/properties/key_contacts/items/properties/email#description"
      ],
      "classification": "proposed-guidance-addition",
      "observed": "portable replaces the repeater description and adds three contact help strings",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_key_contacts_parity.py",
      "producerEvidence": ["specs/forms/key-contacts.tsp", "specs/question-bank/generics/index.tsp", "evidence/forms/key-contacts/evidence.json"],
      "sourceSupport": "unverified",
      "sourceEvidence": ["grantsgov-key-contacts-xsd-2.0 sha256:d361843ac5acaf39aa58a10d87cb36647e2f834052ef5d7cf9370442908296e6"],
      "gap": "The pinned XSD establishes cardinality and types, not the four guidance strings. No DAT, PDF, or instruction source/locator is recorded for them.",
      "reviewStatus": "proposed",
      "recommendedDisposition": "Do not label these source guidance. Pin exact text sources or classify them as authored usability guidance."
    },
    {
      "id": "key-contacts.ui.field-list-definition",
      "formId": "key-contacts",
      "dimension": "ui",
      "keys": ["/0/children/1/definition"],
      "stableTargets": ["fieldList:key_contacts"],
      "classification": "generic-adapter-contract-difference",
      "observed": "portable adds definition=/properties/key_contacts; existing omits definition",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_key_contacts_parity.py",
      "producerEvidence": ["specs/forms/key-contacts.tsp"],
      "sourceSupport": "not-applicable",
      "gap": "This is a renderer/adapter contract, not an official-form semantic claim. The current positional pointer is brittle.",
      "reviewStatus": "technically-verified-not-semantically-accepted",
      "recommendedDisposition": "Govern as a technical compatibility delta keyed to fieldList:key_contacts, outside semantic source-correction metrics."
    },
    {
      "id": "project-abstract-summary.schema.guidance",
      "formId": "project-abstract-summary",
      "dimension": "schema",
      "keys": [
        "/properties/funding_opportunity_number#description",
        "/properties/assistance_listing_number#description",
        "/properties/project_abstract#description"
      ],
      "classification": "proposed-guidance-addition",
      "observed": "portable adds three descriptions; existing omits them",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_project_abstract_summary_portable.py",
      "producerEvidence": ["specs/forms/project-abstract-summary.tsp", "specs/question-bank/opportunity/index.tsp", "specs/question-bank/project/index.tsp", "evidence/forms/project-abstract-summary/evidence.json"],
      "sourceSupport": "unverified",
      "sourceEvidence": ["DAT sha256:75114a512cf3a768a7a20e837d17adaf18a1a5a3ec57523388120e39ee40413c", "root XSD sha256:3022f177a7f0ebb9a1888e9b8a4a644ed2ba7857a775d2d05642a9fbd1cc008f"],
      "gap": "The evidence status is unreviewed with no mappings, and no exact source locators support these strings. Similar form wording is not enough.",
      "reviewStatus": "unreviewed",
      "recommendedDisposition": "Keep unresolved/proposed and add field-level DAT/PDF/instruction provenance before treating the descriptions as source-derived."
    },
    {
      "id": "sf424b.schema.response-ownership",
      "formId": "sf424b",
      "dimension": "schema",
      "keys": [
        "/properties/signature#readOnly",
        "/properties/title#readOnly",
        "/properties/applicant_organization#readOnly",
        "/properties/date_signed#readOnly"
      ],
      "classification": "proposed-response-ownership-correction",
      "observed": "portable adds readOnly=true; existing has no readOnly keyword",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424b_portable.py",
      "producerEvidence": ["specs/forms/sf424b.tsp", "policy-bindings/forms/sf424b.json", "evidence/forms/sf424b/evidence.json"],
      "sourceSupport": "partial",
      "sourceEvidence": ["SF424B-V1.1 DAT sha256:15944ea4df287b94e27e2f7e459c05a88e3fad74d39f2abd0bcad170c475665d", "policy binding declares systemValue sources"],
      "gap": "The policy binding states ownership, but its source strings are not exact sourceRefs and the evidence file provides no DAT row/XFA/PDF locator for editability. Individual SF-424B intentionally differs, confirming ownership is profile-specific.",
      "reviewStatus": "proposed",
      "recommendedDisposition": "Keep profile-scoped and proposed; add exact operational source locators before acceptance."
    },
    {
      "id": "sf424b.schema.cover-relationship-guidance",
      "formId": "sf424b",
      "dimension": "schema",
      "keys": [
        "/properties/title#description",
        "/properties/applicant_organization#description"
      ],
      "classification": "legacy-wording-normalization",
      "observed": "portable rewrites existing 'should match' guidance as 'must match' guidance",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424b_portable.py",
      "producerEvidence": ["specs/forms/sf424b.tsp", "policy-bindings/forms/sf424b.json", "evidence/forms/sf424b/evidence.json"],
      "sourceSupport": "partial",
      "gap": "The relationship to the SF-424 cover is represented declaratively, but no exact source locator supports changing normative force from 'should' to 'must'.",
      "reviewStatus": "proposed",
      "recommendedDisposition": "Do not call this merely normalized wording; obtain an exact instruction/DAT source or retain the legacy normative wording."
    },
    {
      "id": "sf424b.ui.policy-text",
      "formId": "sf424b",
      "dimension": "ui",
      "keys": ["/1/description"],
      "stableTargets": ["policy:grants-gov/nonconstruction-assurances@1.1#assurances"],
      "classification": "source-correct-policy-text-and-presentation-normalization",
      "observed": "portable uses a page-reconciled 19-item policy bundle; existing differs in NOTE prefix, punctuation, quotation style, capitalization, and assurance 19 wording",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424b_portable.py",
      "producerEvidence": ["policies/nonconstruction-assurances-1.1.json", "policy-bindings/forms/sf424b.json", "evidence/forms/sf424b/evidence.json"],
      "sourceSupport": "verified",
      "sourceEvidence": ["Mandatory_SF424B-V1.1.pdf sha256:fb1fc7bb8cb2825dd400f951f2875876a36d78acb46506bc3993ce56f1ee80d1 with item-level page 1/page 2 locators for all 19 assurances", "SF424B-V1.1 DAT sha256:15944ea4df287b94e27e2f7e459c05a88e3fad74d39f2abd0bcad170c475665d for burden text"],
      "gap": "Policy-owner, accessibility, instructions, and production-registration gates remain pending in the binding. Source reconciliation is not release approval.",
      "reviewStatus": "proposed",
      "recommendedDisposition": "Eligible for policy/content review; key the delta to the policy section rather than UI index 1."
    },
    {
      "id": "sf424b.ui.hide-cover-identity",
      "formId": "sf424b",
      "dimension": "ui",
      "keys": ["/2/children/1/type", "/2/children/2/type"],
      "stableTargets": ["/title", "/applicantOrganization"],
      "classification": "proposed-response-ownership-presentation",
      "observed": "portable hides title and applicant organization; existing renders editable fields",
      "differentialAssertionEvidence": "api/tests/src/form_schema/form_spec/test_sf424b_portable.py",
      "producerEvidence": ["specs/forms/sf424b.tsp", "policy-bindings/forms/sf424b.json"],
      "sourceSupport": "partial",
      "gap": "This is the UI manifestation of the unresolved profile-specific ownership claim and lacks exact editability locators.",
      "reviewStatus": "proposed",
      "recommendedDisposition": "Link to the ownership record and replace positional keys with stable field targets; do not count it as a separate semantic decision."
    }
  ]
}
```

## Integration guidance

- Preserve differential assertion evidence separately from official/source evidence.
- Migrate one exact key per ledger record if the contract requires atomic targets; retain `groupId` links so one rationale is not counted repeatedly.
- A source-verified record remains `proposed` until the appropriate review accepts it.
- Treat validation manifestations as links to schema constraints, not duplicate semantic decisions.
- Replace all 11 positional UI pointers with the stable targets listed above.
- Split the three mixed groups before enforcement: SF-424 guidance, SF-424A block headings/guidance, and SF-424B policy text/presentation if the contract distinguishes content from formatting.
