---
type: Task
title: Correct R&R Personal Data source parity
priority: P0
assignee: implement_rr_personal_data
description: Correct verified source-parity and evidence defects in merged producer PR68.
superbee_progress_status: done
superbee_updated_by: promote_new_forms
generated:
  by: 'process:superbee'
  at: '2026-08-24T04:11:10.542Z'
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
- Producer PR #69 independently approved and merged as `14b08b8cbd6016778a8f0688ed924a7ede4c8d2d`, lifting the promotion hold for this exact revision only.
- Draft consumer correction PR: https://github.com/mikec-ai/simpler-grants-gov/pull/62, base `aa46719f794e114e31f9c503e1ed7bda9d2d54a0`, head `91be21d224d2294643d28695e6720c5f5bf94434`.
- Consumer bundle SHA-256: `055e85435d25c6301d4026a5230542e9723dfd5ee01a0b00fe49edb2e23cbf6d`; selection remains all 38 forms and 442 artifacts, including Cover Page Supplement.
- Consumer delta is the exact regenerated manifest plus five corrected Personal Data artifacts. Runtime identities and registrations remain byte-identical; Personal Data remains bank-only.
- Local consumer classifier reports `bankOnly=true`; focused integrity/provenance/registration/updater tests passed 29/29. Hosted lightweight CI is running; PR remains unmerged for independent review.

[depends on](author-integrate-rr-personal-data.md)
