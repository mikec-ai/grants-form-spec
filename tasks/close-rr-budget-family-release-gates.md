---
type: Task
title: Close R&R Budget family release gates
priority: P0
description: >-
  Close shared DAT-condition, lifecycle, browser, accessibility,
  semantic-review, and production gates across R&R Budget and Subaward Budget
  profiles.
superbee_progress_status: in_progress
superbee_updated_by: gate_assessment_agent
generated:
  by: 'process:superbee'
  at: '2026-08-23T18:47:16.856Z'
assignee: gate_assessment_agent
---
# Goal

Close the remaining shared and form-specific release gates for R&R Budget, R&R Subaward Budget, and
their published duration/cardinality profiles while preserving one portable budget architecture.

# Delivered baseline

- The family composes shared research-budget question blocks with no form-specific compiler branch.
- All 56 DAT-defined calculations execute for root and nested subaward contexts with source-faithful
  numeric profiles.
- The generic Simpler adapter renders nested repeaters and parent-scoped rules.
- Five portable XML profiles reuse one declarative mapping and emit maximal payloads valid against
  their pinned official XSDs; the adapter contains no budget-family or duration branch.

# Acceptance criteria

- Decide and source the materialization policy for calculated outputs when every operand is absent
  versus explicitly zero; implement it generically and test both root and nested contexts.
- Classify, author, and exhaustively test the 56 non-empty DAT conditions without treating similar
  wording as accepted semantic equivalence or introducing a form-specific expression engine.
- Exercise calculations, validation, nested attachment auditing, save/reload, locked/print,
  submission, and official-XSD XML for representative minimal, maximal, invalid, and nested
  subaward payloads across every published family profile.
- Run browser-level editing, keyboard, and automated accessibility checks for nested repeaters and
  record human accessibility review separately.
- Record semantic-review, policy, instruction-asset, identifier, and production-registration gates;
  proposed mappings remain unpublished until accepted.
- Preserve zero form-specific compiler/adapter branches. Any genuinely reusable runtime extension
  must be bounded, portable, and exercised by more than one family member.

# Boundary

This task closes release evidence and policy gaps; it does not rewrite the already-delivered form
architecture or silently claim human approval.

# Implementation progress

## 2026-08-23: calculated-output materialization slice

- Source review found 20 of the 56 R&R Budget DAT calculations with non-empty conditions stating
  that the calculated output is required only when corresponding data is entered. The official
  XSD and DAT hashes remain pinned in the form evidence sidecar.
- Chosen portable policy: all declared sources absent or null leaves/removes the output; an
  explicitly entered zero is present and materializes zero. The policy is opt-in and changes
  neither formulas nor requiredness.
- Producer implementation is ready in [grants-form-spec PR 44](https://github.com/mikec-ai/grants-form-spec/pull/44):
  one declarative decorator, generic SGG projection, exactly 20 source-bound annotations,
  diagnostic coverage, and a source-bound decision record. Producer preflight passes (93 TypeSpec
  tests, 76 Python tests, 660 artifact validations, and the unclassified-field ratchet). GitHub CI
  passed in 1m17s.
- Adapter implementation is ready in [simpler-grants-gov PR 38](https://github.com/mikec-ai/simpler-grants-gov/pull/38):
  generic server-side monetary-sum, integer-sum, and subtraction handling plus the exact producer
  commit pinned across all five family profiles. The focused 105-test rule-processing, root-budget,
  nested-subaward, and artifact-integrity suite passes against the local test database; lint,
  formatting, and targeted mypy pass. This fork currently reports no GitHub checks for the branch.
- SGG executes this portable calculation contract in its server-side rule processor. This slice does
  not add or claim a client-side calculation implementation.
- This slice has no lifecycle/residual-normalization overlap and adds no budget-family branch.

[depends on](harden-rr-budget-production.md)

[depends on](author-integrate-rr-subaward-budget.md)

[depends on](author-integrate-rr-budget.md)
