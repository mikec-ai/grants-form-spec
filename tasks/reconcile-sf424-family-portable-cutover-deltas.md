---
type: Task
title: Reconcile SF-424 family portable cutover deltas
priority: P0
description: >-
  Resolve the producer, declaration, and reviewed compatibility differences
  exposed by PR63 while production remains fail-closed on legacy definitions.
superbee_progress_status: in_progress
superbee_updated_by: codex-operational-evidence
generated:
  by: 'process:superbee'
  at: '2026-08-24T05:18:53.017Z'
assignee: codex-cardinality-emitter
---
# Goal

Resolve the portable-versus-legacy schema and validation deltas exposed when consumer PR #63 temporarily made SF-424, SF-424 Short, and SF-424A production-active. Keep the three portable candidates banked and previewable while production stays on the legacy definitions until each delta is mechanically fixed or explicitly reviewed as intentional.

# Incident evidence

- Consumer PR #63 head `44a217345868ed15192431ee755c9f41febcc8b7` consumed producer revision `14b08b8cbd6016778a8f0688ed924a7ede4c8d2d` and produced 12 relevant API test failures across the three forms. The failures collapse to three root causes; repeated fixtures amplify the same field-level differences.
- Consumer PR #65 began by restoring the three legacy definitions for production while preserving the portable bank, adapter, and preview seam. Its current head `1f2f47f164674e91904d7392978ae58c63c5936d` also closes a CI-classifier gap: the lightweight additive lane had allowed modifications to existing portable artifacts and XSDs, while those changes can alter already-banked behavior. Existing artifact or XSD modifications now require full CI; only strictly additive files qualify for the lightweight lane. Both changes are the correct fail-closed disposition.
- The legacy implementation is a compatibility oracle, not semantic authority. The SF-424A evidence records cited below are still `proposed`, so they cannot yet authorize an intentional production delta.

# Root-cause classification

## A. Duplicate applicant-address validation: producer generic emitter defect

SF-424 and SF-424 Short each compose `primary-org/address`. The published question block already owns three unconditional required paths and two USA-conditional required paths. `cardinalityAnnotations()` in `typespec-form-spec/src/emitters/overlay.ts` recursively copies those same model-level decorators beside the form occurrence `$ref`, so SGG receives two identical validators and reports each missing address field twice.

Correct this in the producer's generic emitter. A reference to a separately published question must retain the question's intrinsic cardinality only in the referenced block. The form occurrence may add only decorators declared on that occurrence. Do not deduplicate validation errors in SGG and do not add form-id branches.

## B. SF-424 Short pre-population versus JSON Schema `readOnly`: producer declarative decision

The producer declaration applies both `@Sgg.prePopulate` and `@UI.readOnly` to six fields: agency name, Assistance Listing number/title, opportunity number/title, and SAM UEI. The legacy SGG oracle hides all six through pre-population UI rules but reserves JSON Schema `readOnly` for the three submission-populated outputs.

This is not an adapter transformation defect. Review the intended portable meaning of `readOnly` separately from the SGG capture mechanism. If legacy behavior is intended, remove the six `@UI.readOnly` declarations in `specs/forms/sf424-short.tsp` while preserving `@Sgg.prePopulate`. If the portable distinction is intentional, record it as a narrow reviewed delta with evidence before cutover. Do not teach the adapter that pre-population implies or removes `readOnly`.

## C. SF-424A optional blank narratives: unresolved semantic delta, then a generic adapter choice only if required

The portable bank defines direct-charge explanation, indirect-charge explanation, and remarks as optional properties whose present values have minimum length 1. The legacy SGG payload convention persists absent values as empty strings and its schemas allow minimum length 0. The producer evidence sidecar ties the 1-character minima to the pinned XSD, but all three mappings remain `proposed` rather than reviewed.

Do not weaken the shared bank questions solely to satisfy legacy fixtures. First review the exact XSD mappings and choose between: (1) retain canonical `minLength: 1`, normalize absent SGG optional text to omission through one generic, declaratively governed adapter policy, and record an accepted legacy delta; or (2) preserve empty-string compatibility through a narrow declarative projection override implemented by a generic adapter capability. Adding `minLength: 0` beside a `$ref` cannot weaken the referenced constraint and is not a valid fix. Any override must target exact paths, carry a reason and review reference, fail on stale paths, and contain no SF-424A branch in Python.

# Minimal correction sequence

1. Land PR #65 independently after its full CI is green. Production remains legacy; portable candidates remain banked and previewable; modifications to existing artifact or XSD files continue through full CI.
2. Fix producer cardinality emission generically, rebuild artifacts, promote the immutable producer revision, and prove one validation issue per missing address path in both forms.
3. Resolve and encode the SF-424 Short read-only decision in producer declarations or the governed intentional-delta ledger; keep pre-population behavior unchanged.
4. Complete semantic review of the three SF-424A XSD mappings. Only then implement the selected generic SGG compatibility behavior or accept the canonical delta.
5. Rerun the same legacy differential suite plus preview/browser receipts. Production cutover is a separate reviewed change after all applicable deltas are resolved or accepted.

# Acceptance criteria

- Producer tests prove that a published question retains intrinsic required/conditional rules while a composing form does not duplicate them, and that explicit occurrence-level narrowing still emits beside the reference.
- SF-424 and SF-424 Short validation receipts contain one error per missing applicant address path, not duplicates.
- SF-424 Short tests independently assert the six pre-population bindings, null UI fields, and the reviewed JSON Schema `readOnly` set.
- SF-424A tests exercise omitted, empty, and nonempty values for all three narrative fields at the canonical producer boundary and the SGG boundary; the chosen difference is represented as reviewed data, not form-specific adapter control flow.
- Differential receipts identify producer revision, consumer revision, form, path, expected/actual behavior, disposition, evidence status, and review state.
- CI classifier tests prove that new additive artifacts may use the lightweight bank lane, while any modification or deletion of an existing artifact or XSD selects full CI. This classification is an architectural parity gate, not merely an optimization.
- No production registration changes accompany the producer or adapter corrections; a later cutover remains fail-closed and separately approved.

# Boundary

No HHS upstream writes. Do not edit or merge PR #63 or PR #65 from this task. Similar behavior is not semantic equivalence, and proposed evidence does not count as reviewed acceptance.

# SF-424 Short six-field semantic audit

## Disposition

The official sources support prepopulation for all six fields. They do not support an unconditional portable `readOnly` assertion. Five read-only assertions appear to have been inferred from prepopulation. SAM UEI has context-dependent and conflicting evidence, so its editability remains unresolved, but the current unconditional `readOnly` assertion is still too strong.

Recommended producer action: remove `@UI.readOnly` from all six fields while preserving the six declarative `@Sgg.prePopulate` bindings. Do not add an adapter rule that equates prepopulation with read-only. Preserve the SAM UEI conflict and the Assistance Listing requiredness conflict in a source audit. Keep the three true submission-populated outputs - Date Received, AOR Signature, and Date Signed - separately read-only.

## Exact source set

- Root XSD: `https://apply07.grants.gov/apply/forms/schemas/SF424_Short_3_0-V3.0.xsd`, native version 3.0, SHA-256 `82b0f2a0ddbbcfae4ec7e083188287fb05700e201ade3b2f69684241bf8baabd`. The pinned schema declares value types and cardinality for the six elements but no UI editability semantics.
- F711 DAT: `https://apply07.grants.gov/apply/forms/sample/SF424_Short_3_0-V3.0_F711.xls`, native version 3.0, SHA-256 `a905f905928a730b10d48d0b77cbb59397edb3ad3c99770391e1e160c3fb06df`. Exact cell review used the workbook's `Form DAT` sheet without OCR.
- Active read-only reference PDF: `https://apply07.grants.gov/apply/forms/readonly/SF424_Short_3_0-V3.0.pdf`, native version 3.0, retrieved 2026-08-24, SHA-256 `0c0b2405ce06adf4b0bd7fcf456ec4a42eab540246c6c04842dece8d3c082ffc`. It labels Date Received and the signature/date outputs as completed upon submission, but provides no read-only statement for these six fields.
- Active sample XFA PDF: `https://apply07.grants.gov/apply/forms/sample/SF424_Short_3_0-V3.0.pdf`, native version 3.0, retrieved 2026-08-24, SHA-256 `efd781d0f799d65e2ea90e219070c62a3c00fdee06ecd118bde418cfb7f68298`. Review used deterministic XFA template packet inspection, not OCR.
- Active instructions: `https://apply07.grants.gov/apply/forms/instructions/SF424_Short_3_0-V3.0-Instructions.pdf`, form version 3.0, OMB expiration 2028-07-31, retrieved 2026-08-24, SHA-256 `5c0a58a5bedb4040baf8a2166b9e7b0b47d4bfcad2fb859a414de3edd03c3dd0`. The PDF title retains the historical text `V1.1 Instructions`, but its form-identifiers table says V3.0; preserve that metadata inconsistency rather than normalizing it away.
- Current FID 711 data-element page: `https://www.grants.gov/forms/form-items-description/fid/711`, observed 2026-08-24. It repeats the prepopulation help text and contains no non-editable business rule for these six records. Other Grants.gov records use explicit `Non-editable when forward populating` wording when that behavior is intended, so prepopulation wording alone must not be upgraded to read-only.

## Field-by-field findings

| Canonical field | Exact DAT coordinate and source | PDF/instruction evidence | Read-only classification | Declarative recommendation |
| --- | --- | --- | --- | --- |
| `/agencyName` | F711 `Form DAT` row `1`; Field Type `Pre-populated`; Field Type Source `SubmissionDef.AgencyName` | Instructions field 1 says pre-populated. XFA calculates from `SubmissionDef.AgencyName` or `PDFDef.AgencyName` and contains no protected-access assignment. | Inferred from prepopulation; not source-supported as unconditional read-only. | Remove `@UI.readOnly`; retain `@Sgg.prePopulate` agency-name binding. |
| `/assistanceListingNumber` | Row `2-1`; `Pre-populated`; `SubmissionDef.CFDANumber` | Instructions say pre-populated. XFA calculates from `SubmissionDef.CFDANumber` or `PDFDef.CFDANumber`; its initialize packet literally comments out `//this.access = "protected";`. Instructions call the field required while the DAT and XSD make it optional, a separate unresolved cardinality conflict. | Inferred from prepopulation and directly contradicted by the inactive protection statement. | Remove `@UI.readOnly`; retain the assistance-listing-number prepopulation binding; record the requiredness conflict separately. |
| `/assistanceListingProgramTitle` | Row `2-2`; `Pre-populated`; `SubmissionDef.CFDATitle` | Instructions say pre-populated. XFA calculates from `SubmissionDef.CFDATitle` or `PDFDef.CFDATitle`; its initialize packet also comments out `//this.access = "protected";`. Instructions call the field required while DAT/XSD make it optional. | Inferred from prepopulation and directly contradicted by the inactive protection statement. | Remove `@UI.readOnly`; retain the assistance-listing-title prepopulation binding; record the requiredness conflict separately. |
| `/fundingOpportunityNumber` | Row `4-1`; `Pre-populated`; `SubmissionDef.OpportunityID` | Instructions say pre-populated. The XFA field has no protected-access assignment and remains a normal text-edit field. | Inferred from prepopulation; not source-supported as unconditional read-only. | Remove `@UI.readOnly`; retain the opportunity-number prepopulation binding. |
| `/fundingOpportunityTitle` | Row `4-2`; `Pre-populated`; `SubmissionDef.OpportunityIDTitle` | Instructions say pre-populated. XFA calculates from `SubmissionDef.OpportunityTitle` or `PDFDef.OpportunityTitle` and contains no protected-access assignment. | Inferred from prepopulation; not source-supported as unconditional read-only. | Remove `@UI.readOnly`; retain the opportunity-title prepopulation binding. Preserve the DAT/XFA source-path naming difference rather than silently equating it. |
| `/samUei` | Row `5f-1`; `Pre-populated`; `SubmissionDef.SAMUEI`; business rule only says 12 characters | The current instructions say `Enter the organization's UEI`, not pre-populated. The XFA calculate event first sets access to `open`, protects it only when `PDFDef` exists or for an individual-applicant sentinel branch, and otherwise leaves it editable. | Context-dependent and source-conflicted; unconditional read-only is not supported. | Remove `@UI.readOnly`; retain the current SGG UEI prepopulation binding as a target capture mechanism; preserve the instruction/DAT/XFA conflict and defer any canonical editability claim until application context is modeled. |

## Operational-evidence boundary

Do not automatically create `operationalBehaviorEvidence` from the six `@Sgg.prePopulate` declarations. The DAT proves prepopulation, while XFA supplies much of the editability evidence, and the current operational record has one evidence coordinate. Any later records must name evidence that supports every asserted facet or evolve the generic contract to preserve multiple exact evidence coordinates. In particular, do not force SAM UEI into a static `editable` or `protected` record while its application-context predicate is unresolved.

## Review state

This is an agent-reviewed source audit and implementation recommendation, not accepted semantic evidence and not authorization for production cutover. The existing task remains in progress until the declaration change, source-audit sidecar, focused tests, regenerated artifacts, consumer promotion, and differential receipts are independently reviewed.

## SF-424A optional blank-string semantic audit

### Result

All three affected Section F fields have the same reviewed disposition: an empty string is not a source-valid XML value. The source model is omission-only. Simpler's current empty strings are a legacy UI/persistence normalization for an absent optional response.

| Canonical path | Source field | XSD disposition | DAT / applicant UI | XFA submission behavior | Classification |
| --- | --- | --- | --- | --- | --- |
| `/directChargesExplanation` | `BudgetInformation.OtherInformation.OtherDirectChargesExplanation` | `minOccurs=0`; if present, `glob:StringMin1Max50Type` requires 1-50 characters | F-0-1, optional AN, reported minimum 0 and maximum 50 | The bound node carries `dd:minOccur="0" dd:nullType="exclude"`; pre-submit removes `OtherInformation` when all three Section F controls are null or empty | omission-only source value; legacy empty-string normalization |
| `/indirectChargesExplanation` | `BudgetInformation.OtherInformation.OtherIndirectChargesExplanation` | `minOccurs=0`; if present, `glob:StringMin1Max50Type` requires 1-50 characters | F-0-2, optional AN, reported minimum 0 and maximum 50 | Same null-exclusion and wrapper-removal behavior | omission-only source value; legacy empty-string normalization |
| `/remarks` | `BudgetInformation.OtherInformation.Remarks` | `minOccurs=0`; if present, `glob:StringMin1Max250Type` requires 1-250 characters | F-0-3, optional AN, reported minimum 0 and maximum 250 | Same null-exclusion and wrapper-removal behavior | omission-only source value; legacy empty-string normalization |

### Exact evidence

- XSD: `https://apply07.grants.gov/apply/forms/schemas/SF424A-V1.0.xsd`, SHA-256 `d5a636733d72c1e4cc9087ffc59b3d10000ee51f80da0dde3150ff91bcad0b5c`. Lines 240-264 declare all three global elements with `StringMin1...` types and make each reference under `OtherInformation` optional.
- Global XSD dependency: `Global-V1.0.xsd`. `StringMin1Max50Type` and `StringMin1Max250Type` each have `minLength value="1"`.
- DAT: `https://apply07.grants.gov/apply/forms/sample/SF424A-V1.0_F241.xls`, SHA-256 `5228e637f00b1946f10df473376d9f6dd50956b929cbf823b5dd8313e0bbd7a4`. Rows F-0-1 through F-0-3 are optional applicant-entered fields and record UI minima of zero.
- Sample XFA PDF: `https://apply07.grants.gov/apply/forms/sample/SF424A-V1.0.pdf`, SHA-256 `74f89e6c250d900ada5f7e6f7bc5546c24a88885c9c07f458cb408b91bc95095`. Deterministic stream inspection, without OCR, shows each XML node as optional with `dd:nullType="exclude"`. The `OtherInformation` pre-submit event removes its instance when Direct Charges, Indirect Charges, and Remarks are all null or empty.
- Instructions: `https://apply07.grants.gov/apply/forms/instructions/SF424A-V1.0-Instructions.pdf`, SHA-256 `6176bbf30c6288876dff8b95e7f150ca8c9f0ce474a2286be6410d2c28fd255b`. Embedded text on the Section F table labels fields 21, 22, and 23 optional. It does not authorize empty XML elements.
- Legacy SGG oracle: all three fields have `minLength: 0`, and the minimal-valid fixture stores `""`. That proves current JSON compatibility behavior only; it is not source semantic authority. The legacy `compose_object` transform excludes `None` but does not itself exclude `""`, so the current empty-string acceptance must not be treated as XML parity evidence.

### Recommendation

Keep the shared bank questions optional with `minLength: 1` when present. This is the exact XSD meaning and matches the XFA's null-exclusion behavior. Do not lower a shared question to `minLength: 0` and do not attempt to weaken it with a sibling schema constraint beside `$ref`.

Add one generic, declaratively governed adapter normalization operator, such as `empty-string-to-absent`, applied before canonical validation and XML projection. Author the policy at the exact form-occurrence paths above, with the pinned evidence and a reviewed compatibility disposition. The generic adapter must validate that every configured path exists, is optional, resolves to a string schema whose present-value minimum is at least one, and becomes absent after normalization. It should transform only the exact empty string; whitespace-only values remain governed by the source string type and must not be trimmed by inference. The same operator can later support other forms when independently evidenced, with no SF-424A branch.

Required differential tests should cover each path independently and together: omitted values pass; `""` is normalized to omission at the SGG compatibility boundary; nonempty values pass unchanged; over-limit values fail; direct canonical validation still rejects present `""`; XML contains no empty child; and the `OtherInformation` wrapper is absent when all three values are absent after normalization.

### Review boundary

This audit resolves the blank-value mechanics from exact sources. It does not accept the three semantic question mappings for published reuse metrics, change production registration, or authorize a production cutover. The existing mapping status remains proposed until the separate semantic-review workflow accepts those identities.

## PR #72 review follow-up

- Review found R&R Personal Data as the third emitted form affected by the same generic correction. The regression now proves both its direct `projectDirector` reference and repeated `coProjectDirectors.items` reference do not copy nested name cardinality, while both shared question artifacts retain required first and last names.
- Full preflight passed again at exact amended head `f4cf21eb8326d92872efe5e4d7f3a58786217172`: 116 TypeScript tests and 291 Python tests with 2 skipped, plus every producer artifact and conformance gate. Draft PR #72 remains unmerged; hosted CI is running on the amended head.

[depends on](implement-exact-empty-string-to-absent-normalization.md)
