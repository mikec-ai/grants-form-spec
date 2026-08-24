---
type: Task
title: Correct R&R Personal Data source parity
priority: P0
assignee: implement_rr_personal_data
description: Correct verified source-parity and evidence defects in merged producer PR68.
superbee_progress_status: done
superbee_updated_by: implement_rr_personal_data
generated:
  by: 'process:superbee'
  at: '2026-08-24T04:06:20.904Z'
---
# Goal

Correct the merged R&R Personal Data producer artifacts so portable validation, semantic reuse, behavior evidence, display labels, and provenance match the binding source audit without adding form-specific runtime behavior.

# Verified defects

- `research-person/name` narrows official `HumanNameDataType` prefix and suffix strings to enums. Source-valid values such as suffix `III` pass the exact XSD but fail the portable schema. Reuse `generics/person-name` and apply first/last requiredness at the profile occurrence.
- The four DAT exclusivity rules are present only in the research audit. Add them to `evidence.json` as `source-bound-uncompiled`; do not infer runtime behavior.
- Canonical ethnicity choices use wire spellings instead of the current XFA display labels. Use declarative `valueMap` for `Non-Hispanic or Latino` to `Not Hispanic or Latino` and `Do Not Wish to Provide` to `Do Not Wish To Provide`.
- The evidence closure omits the official transitive `UniversalCodes-V2.0` source.
- Five source-specific demographic questions need stable declarative identities reused across PD/PI and Co-PD/PI occurrences while role context remains in the wrappers and clinical enrollment demographics stay distinct.
- The five PD/PI name fields' exact DAT forward-population and XFA protected-after-initialize behavior need a bounded per-field source audit, without misclassifying operational behavior as calculations or conditions.
- A mapping-node `valueMap` must remain legal only on `kind: value`; local object, group, array, and attachment nodes must be rejected.

# Acceptance criteria

- Exact portable JSON Schema and XML/XSD tests cover arbitrary valid prefix/suffix values, including `III`.
- One shared source-specific personal-data profile is composed under distinct PD/PI and Co-PD/PI occurrence roles without reusing clinical enrollment demographics.
- Exactly four DAT exclusivity records are source-bound and uncompiled in form evidence, with no emitted calculation or condition behavior.
- Exact official source/version/hash closure includes UniversalCodes.
- Privacy, policy, accessibility, lifecycle, and runtime registration gates remain closed.
- Full producer preflight passes and a focused draft PR is opened without merging.
- Generic non-rule operational behavior evidence is tracked separately in `tasks/generic-operational-behavior-evidence`.

# Delivery receipt

- Producer branch: `codex/fix-rr-personal-data-source-parity`
- Exact head: `63400f47d0c91b5818eb83ee5c11a0a588b4ccd6`
- Draft PR: https://github.com/mikec-ai/grants-form-spec/pull/69
- Local verification: full `npm run preflight` passed with 114 TypeScript tests, 272 Python tests (2 skipped), 29 exact-XSD fixture/profile checks, 258 blocks / 1,412 artifacts, and zero unclassified fields or exceptions.
- CI status: passed at https://github.com/mikec-ai/grants-form-spec/actions/runs/32688654215 (job `97318232245`, 1m37s).
- Merge status: intentionally unmerged.

[depends on](author-integrate-rr-personal-data.md)
