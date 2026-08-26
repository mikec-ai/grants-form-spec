---
type: Task
title: Add a generic portable matrix presentation contract
priority: P0
assignee: codex
description: >-
  Preserve visible and programmatic dimensional context without form-specific
  renderer code or inferred calculations.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-26T11:45:18.934Z'
---
# Goal

Generalize the proven SF-424C table path so dimensional fields inside repeatable entries retain visible row/column context, keyboard order, deterministic error routing, and screen-reader coordinate context without form-specific renderer code.

# Evidence boundary

- PHS Inclusion Enrollment exposes 115 unique coordinate-qualified runtime fields from one reused semantic question.
- Exact source evidence identifies 8 conditions and 28 calculation targets, but does not yet pin operands or blank-value semantics. This work must not infer those behaviors.
- SF-424C already proves that the producer can derive a regular table from model structure and the consumer can render it generically.

# Delivery sequence

1. Extend the producer contract and emitter for tables nested in repeatable entries and multi-level row dimensions.
2. Extend the consumer's existing FieldList/Table path for fully nested repeated-item definitions and accessible grouped headers.
3. Verify SF-424C remains identical, then verify standalone PHS Inclusion and its embedded occurrence in PHS Human Subjects.
4. Apply the capability to PHS 398 Modular Budget or PHS Additional Indirect Costs.
5. Evaluate incremental adoption by the R&R Budget family and SF-424A without forcing unsuitable simple repeaters into tables.

# Acceptance criteria

- No PHS-specific compiler, adapter, or React branch.
- Existing SF-424C generated output and behavior remain unchanged.
- Row and column headers are programmatically associated with every coordinate.
- Repeat-entry, save/reload, validation routing, locked state, print, and keyboard behavior are tested.
- Existing stable paths, XML projection, and source provenance remain unchanged.
