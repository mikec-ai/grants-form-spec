---
type: Task
title: Build uniform portable-versus-legacy differential parity
superbee_progress_status: in_progress
priority: P0
description: >-
  Prove one generic compatibility harness across an initial 7-10 form cohort,
  then extend it across every overlap form.
actor: Codex
timestamp: '2026-08-23T22:26:31.443Z'
superbee_updated_by: codex-root
assignee: legacy_diff_cohort
---
# Goal

Build one portable-versus-existing differential harness, prove it first across an initial cohort of at least seven forms and preferably ten, then extend it to every form with an existing counterpart.

# Comparisons

- applicant-visible schema paths, types, requiredness, constraints, and defaults;
- UI ordering, grouping, labels, help text, and conditional presentation;
- validation verdicts across the same generated and curated payload cases;
- rule and calculation outcomes;
- persistence, locked, and print behavior where the runtime supports it;
- XML mappings and representative serialized output.

# Delivery sequence

1. Use SF-424, SF-424 Short, and SF-424A as manually inspected canaries.
2. Extend the same automated mechanism to at least four additional overlap forms, targeting a ten-form initial cohort.
3. Emit a comparable receipt for every run and quantify gaps instead of translating them into qualitative confidence.
4. After the initial proof package is complete, extend the harness across the remaining overlap catalog.

# Oracle policy

Existing behavior is a compatibility oracle, not semantic authority. A difference may be accepted when official source evidence or an approved product decision shows the portable behavior is more correct, but it must pass through the intentional-delta mechanism.

# Acceptance criteria

- The initial cohort contains at least seven forms and targets ten without form-specific comparison logic.
- All overlap forms can ultimately run through the same differential harness and emit comparable receipts.
- Fixtures and comparison logic are generic and capability-driven, with form-specific data remaining declarative.
- Undocumented differences fail the gate.
- Results clearly separate parity, intentional evidence-backed deltas, unresolved review items, and defects requiring correction.

[depends on](add-portable-form-preview-registration.md)

[depends on](enforce-evidence-backed-parity-deltas.md)
