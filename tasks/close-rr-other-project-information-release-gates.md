---
type: Task
title: Close R&R Other Project Information release gates
priority: P1
assignee: human-review
description: >-
  Technical gates are merged in producer PR 31 (7585c622) and consumer PR 29
  (5ba62bca). Exact-XSD XML, all condition and conditional-required paths,
  scalar attachment arrays, and generic projections pass; human semantic,
  product-policy, visual/instruction, and registration gates remain.
superbee_progress_status: blocked
superbee_updated_by: root_form_lane_status
generated:
  by: 'process:superbee'
  at: '2026-08-25T19:59:08.329Z'
---
[depends on](harvest-rr-other-project-information.md)

## Source-behavior reconciliation checkpoint — 2026-08-25

- Producer PR [#116](https://github.com/mikec-ai/grants-form-spec/pull/116), final head `60b9a398eb1e40e65d577c183f2909b6e2744d47`, pins all 24 exact F619 DAT records that contain a condition or business rule. A deterministic source-to-ledger comparison found 24/24 records in order with no missing or extra entries.
- The source is the exact pinned artifact `source-1-54234acd9882`, SHA-256 `54234acd9882a129120c0a5dd44c5cde2998b66ffdfe91a4bb4a745e0d39c2ff`, at `https://apply07.grants.gov/apply/forms/formversions/RR_OtherProjectInfo_1_4-V1.4_F619.xls`. Independent review caught and rejected a same-bytes alternative URL, preserving exact URI provenance as well as the digest.
- The 24 official records remain `source-bound-uncompiled`. They are separated from 13 current emitted UI dispositions, which remain `compiled` with unresolved authority. No source-parity or semantic-equivalence acceptance is implied.
- Open technical/semantic decisions are explicit: visible/hidden versus enabled/disabled and value retention; aggregation of the presentation row plus eight exemption checkboxes into one array and its missing conditional property requiredness; extra conditional requiredness on environmental question 4.c; the vertebrate assurance two-part condition; two cross-form project-summary/narrative requiredness rules; and the derived non-XML attachment indicator.
- Semantic review remains `unreviewed` with zero accepted mappings. No form declaration, shared question-bank, compiler, adapter, XML, runtime, or registration files changed.
- Focused R&R Other Project Information and rule-evidence validation passed six tests with one skip. Full producer preflight passed 125 TypeScript tests, 394 Python tests with 10 skips, 8 XML projection tests, 36 exact-XSD fixtures, 1,721 artifact validations, zero unclassified fields, and zero exceptions.

## Technical evidence closure — 2026-08-25

- PR #116 merged as `e20238dd55efe484dcdace8c3fd7513b3b79e455` after two independent clean reviews.
- Hosted producer CI run `32892383230` passed, including the full form-spec job in 2m22s. Hosted proof-package run `32892384411` also passed.
- Automated source/evidence reconciliation is closed. The 13 runtime dispositions and the source rules remain deliberately separated until the listed semantic and product decisions are reviewed.
- Human semantic review, instruction and policy acceptance, visual/accessibility review, registration, and release acceptance remain open.
