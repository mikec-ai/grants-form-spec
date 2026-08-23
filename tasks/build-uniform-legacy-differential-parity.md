---
type: Task
title: Build uniform portable-versus-legacy differential parity
superbee_progress_status: todo
priority: P0
description: >-
  Apply one differential harness to the expected 21 portable forms with SGG
  legacy counterparts.
actor: Codex
timestamp: '2026-08-23T22:26:31.443Z'
---
# Goal

Build a uniform portable-versus-legacy differential harness for the expected 21 forms that have both a banked portable implementation and a hand-written SGG legacy implementation.

# Comparisons

- applicant-visible schema paths, types, requiredness, constraints, and defaults;
- UI ordering, grouping, labels, help text, and conditional presentation;
- validation verdicts across shared fixture cases;
- rule and calculation outcomes;
- XML mappings and representative serialized output.

# Oracle policy

Legacy behavior is a compatibility oracle, not the semantic authority. A difference may be accepted when official source evidence or an approved product decision shows that the portable behavior is more correct, but it must pass through the intentional-delta mechanism.

# Acceptance criteria

- All overlap forms run through the same differential harness and emit comparable receipts.
- Fixtures and comparison logic are generic and capability-driven, with form-specific data remaining declarative.
- Undocumented differences fail the gate.
- The result clearly separates parity, intentional evidence-backed deltas, and defects requiring correction.

[depends on](add-portable-form-preview-registration.md)

[depends on](enforce-evidence-backed-parity-deltas.md)
