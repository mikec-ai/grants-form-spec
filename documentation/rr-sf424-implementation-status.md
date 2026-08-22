# R&R SF-424 implementation status

This is a source-bound declarative baseline for `RR_SF424_5_0`, version 5.0, Grants.gov
FID 768. It is not a production approval and does not contribute to published semantic
coverage. The evidence sidecar accepts zero semantic mappings.

## Implemented in the portable declaration

- All 107 extracted source leaves are represented. The 106 applicant-facing leaves render in
  the source's 21 numbered sections; the second nested EIN is preserved but hidden because the
  reviewed XFA has no binding for it and the top-level Employer ID is the visible answer.
- Source requiredness, scalar limits, enum wire values, and the four funding ranges are
  represented where the current declarative contract supports them.
- Applicant organization, application contact, principal investigator, and authorized
  representative are role-specific blocks composed from shared address, person-name,
  organization, phone, email, and identifier questions.
- The applicant-type code list is reused without importing SF-424's different one-to-three
  cardinality. R&R asks for one code.
- Three attachment information requirements remain semantically distinct while sharing the
  generic attachment capture mechanism.
- Applicant-type Other, other-agency explanation, revision details, state-review date, and
  the previous Grants.gov tracking ID have source-backed conditional requiredness and SGG
  visibility projection.
- Federal ID uses a generic nested-path condition and becomes required for Renewal,
  Continuation, and Revision without form-specific compiler code.
- Opportunity and UEI prepopulation, attachment validation, read-only system fields, project
  title length, and congressional-district format are declarative.

## Remaining implementation gates

- Encoded revision checkboxes still need their code-to-checkbox combination table in the
  portable contract, plus clear-on-parent-change behavior.
- Source-reviewed defaults, copy-if-missing lifecycle population, submission-managed AOR
  signature/date population, and end-date-not-before-start-date validation need generic
  portable rule vocabulary.
- Exact XML element names, namespaces, sequence, and attachment envelopes remain in the
  previously generated source-backed oracle. XML mappings are not yet part of the portable
  artifact contract, so the public Simpler adapter must not register this form yet.
- Numbered help text, certification language, burden-statement access, browser accessibility,
  save/reload, print, and submission behavior require focused conformance and human review.

## Source conflicts retained for review

- Metadata expiration `11/30/2025` conflicts with the rendered PDF expiration `01/31/2029`.
- Instructions cite Executive Order `12732`; the rendered form cites `12372`.
- Applicant Province and ZIP prose conflict with extracted activation behavior.
- PD/PI Street 2 prose says required while the rendered form and XFA treat it as optional.
- Revision prose permits broad multiple selection while the DAT/XFA restrict valid pairs to
  AC, AD, BC, or BD and make E exclusive.

These conflicts are intentionally unresolved. Structural validity or a successful render is
not treated as proof that policy or behavior is correct.
