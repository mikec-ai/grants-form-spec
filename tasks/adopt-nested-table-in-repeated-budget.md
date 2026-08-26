---
type: Task
title: Adopt the nested-table contract in a repeated budget form
priority: P1
description: Prove reuse beyond PHS using Modular Budget or Additional Indirect Costs.
superbee_progress_status: in_progress
generated:
  by: 'process:superbee'
  at: '2026-08-26T13:36:36.806Z'
assignee: codex
---
# Scope

Prove the generalized matrix/table capability on one additional repeated budget structure. Compare PHS 398 Modular Budget and PHS Additional Indirect Costs, choose the cheaper evidence-backed candidate, and implement it without altering XML or behavior semantics.

# Acceptance

- Candidate selection is based on exact authored structure and existing runtime output.
- At least one repeated budget/indirect-cost grid adopts the generic contract.
- PHS and SF-424C regression suites remain green.

[depends on](verify-phs-inclusion-matrix-occurrences.md)

# Candidate decision — 2026-08-26

Selected the PHS 398 Modular Budget `periods[].directCosts` group for the bounded proof.

- It is a fixed, source-authored three-column comparison inside each repeatable budget period: two applicant inputs plus one exact read-only calculated total.
- PHS Additional Indirect Costs is not the cheaper fit for the current contract: its apparent grid is a variable-length `indirectCost[]` collection. That is an ordinary dynamic repeater and would require a separate dynamic-table-row capability; it should not be forced into the fixed-dimensional Table contract.
- The modular-budget change preserves the existing XML profile and eight calculation rules. Only portable presentation changes.

# Implementation receipts

- Producer PR #121: https://github.com/mikec-ai/grants-form-spec/pull/121
- Clean producer commit: `85ad91d4a13481b02f94cc5c0c61360750f3ce47` (61 additions, 7 deletions across four files).
- The reusable period question now declares its `directCosts` object as a generic Table.
- Generic flat tables with no row dimensions now allocate 100% width instead of the 60% dimensional-grid allocation.
- Money-tagged scalar columns preserve dollar formatting without form-specific logic.
- Full producer preflight passed: 126 TypeScript tests, 399 Python tests (2 skipped), 1,721 artifacts, 36 XML fixtures, 0 unclassified fields.
- Producer PR #121 merged as `72b2ff69129f56f0146ae601e047d20bb8e3fb6f`.

# Empirical compatibility finding — 2026-08-26

The first exact consumer promotion correctly exposed a generic contract gap before release. `directCostLessConsortiumFandA` is not a free numeric input: its authoritative question-bank schema constrains the applicant to 11 exact modular-budget wire values. The original Table projection emitted every editable scalar as `input`, which would have weakened that enum into free text.

This is being fixed centrally rather than patched for PHS 398 Modular Budget:

- Producer PR #122: https://github.com/mikec-ai/grants-form-spec/pull/122 at `f7315ee8c5c78ff7781c7dfbdad3f997a3308549` projects any editable enum-valued table column as a portable `select` cell with its exact declared values. Full producer preflight passed again: 126 TypeScript tests, 399 Python tests (2 skipped), 1,721 artifacts, 36 XML fixtures, and zero unclassified fields.
- Consumer PR #143: https://github.com/mikec-ai/simpler-grants-gov/pull/143 at `912136634f9f4a185365e5866f0f8431bf5bed7b` renders and locks select cells generically, preserves exact values, updates nested values through the existing path seam, and makes the UI-schema validator fail closed when options are absent. Local TypeScript checking and 68 targeted Table/UI-schema tests passed.
- Consumer artifact PR #142: https://github.com/mikec-ai/simpler-grants-gov/pull/142 at `36befa45e` remains intentionally unmerged. Its focused check failed because the pre-#143 validator rejected the new `select` contract; that is a useful expected gate, not an artifact or form-specific defect.

The next release gate is to merge #122 and #143 when green, regenerate #142 from the merged producer revision, then browser-test the exact choice, calculation, repeated-period scoping, save, and refresh behavior before closing this task.

# Release receipts — 2026-08-26

- Producer PR #122 merged as `77fcbe1d63fdb5d5e247f0a9e3bb3b7a1939b46d` after both producer checks passed.
- Atomic consumer regeneration from that exact revision synchronized all 43 selected forms and 541 artifacts. Only the artifact manifest and modular-budget UI projection changed before the bounded consumer test update.
- Updated consumer PR #142 head: `c235352185fb7920c2a4a75a85bdc323f532c405`. Its branch temporarily includes the generic consumer #143 commit so the new contract can be validated and browser-tested before #143 merges; the shared runtime commit will fall out of #142's diff once it is on main.
- Focused consumer verification passed: 3 modular-budget API tests, TypeScript checking, and 68 targeted Table/UI-schema tests.
- Browser application: `32b4bdae-7d92-4d75-a668-313009598684`; form occurrence: `7a248692-7eef-42ce-b18c-b5618a577ba5`.
- Browser structure: adding two budget periods rendered two generic `directCosts` tables. Each table exposed the exact 11 producer-declared choices, one money input, and one read-only total. HTML names were correctly entry-scoped under `periods[0]` and `periods[1]`.
- Browser persistence and calculations after save plus hard refresh: choices `25000.00` and `50000.00`; consortium inputs `5000.00` and `10000.00`; calculated period totals `$30,000.00` and `$60,000.00`; cumulative direct costs `90000.00`.
- The initially blank second calculated total immediately after the save action was a client timing observation, not persisted data loss: the hard refresh returned both source values, both totals, and the correct cumulative value from the server.

Remaining gate: merge generic consumer PR #143 when its running broad shards finish, let #142 reconcile against main, then merge #142 when its release checks are acceptably resolved.
