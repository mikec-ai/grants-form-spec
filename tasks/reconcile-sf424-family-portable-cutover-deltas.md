---
type: Task
title: Reconcile SF-424 family portable cutover deltas
priority: P0
description: >-
  Resolve the producer, declaration, and reviewed compatibility differences
  exposed by PR63 while production remains fail-closed on legacy definitions.
superbee_progress_status: in_progress
superbee_updated_by: review-operational-evidence
generated:
  by: 'process:superbee'
  at: '2026-08-24T05:15:03.259Z'
assignee: codex-cardinality-emitter
---
# Goal

Resolve the portable-versus-legacy schema and validation deltas exposed when consumer PR #63 temporarily made SF-424, SF-424 Short, and SF-424A production-active. Keep the three portable candidates banked and previewable while production stays on the legacy definitions until each delta is mechanically fixed or explicitly reviewed as intentional.

# Incident evidence

- Consumer PR #63 head `44a217345868ed15192431ee755c9f41febcc8b7` consumed producer revision `14b08b8cbd6016778a8f0688ed924a7ede4c8d2d` and produced 12 relevant API test failures across the three forms. The failures collapse to three root causes; repeated fixtures amplify the same field-level differences.
- Consumer PR #65 began by restoring the three legacy definitions for production while preserving the portable bank, adapter, and preview seam. Its current head `1f2f47f164674e91904d7392978ae58c63c5936d` also closes a CI-classifier gap: the lightweight additive lane had allowed modifications to existing portable a

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

