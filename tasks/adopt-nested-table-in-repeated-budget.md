---
type: Task
title: Adopt the nested-table contract in a repeated budget form
priority: P1
description: Prove reuse beyond PHS using Modular Budget or Additional Indirect Costs.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-26T13:00:18.099Z'
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
