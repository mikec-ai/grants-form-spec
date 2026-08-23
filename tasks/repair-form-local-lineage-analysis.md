---
type: Task
title: Repair canonical lineage accounting for form-local fields
priority: P0
description: >-
  Remove 14 false-positive unclassified occurrences caused by spreads,
  inheritance, and occurrence overrides.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T17:35:28.079Z'
assignee: codex
---
# Objective

Stop the unclassified-field ledger from treating inherited, spread, or occurrence-overridden members as new form-local questions.

# Baseline cases

Fourteen known occurrences at producer commit `46e71d5` already have canonical lineage:

- `budgetType` in both R&R budget durations
- `state`, `province`, and `zipCode` address overrides in Performance Site and R&R Key Person; `state` and `province` in Multi-Project Cover
- the `projectRole` default override in R&R Key Person
- `department`, `division`, and `employerId` inherited through the Multi-Project Cover applicant subtype graph

# Acceptance criteria

- The emitted contract carries enough canonical lineage to distinguish a genuinely local field from a spread/inherited question and an occurrence-level override.
- The analyzer removes all 14 baseline false positives without adding duplicate question-bank definitions.
- Tests cover model spread, inheritance, nested subtype override, and default/constraint override.
- Question occurrence paths, source constraints, and marginal-reuse counts remain correct.

# Result

Implemented in grants-form-spec PR #41 at commit `6515f80`. Each form index now emits path-qualified `fieldOccurrences` while the TypeSpec graph still exists, preserving canonical block lineage through spreads, inheritance, arrays, nested subtype overrides, and occurrence overrides. Artifact validation proves that this inventory exactly covers the emitted JSON Schema field graph. All 14 known false positives disappeared without new question definitions, reducing the ledger from 90 to 76 real occurrences. Existing association and reuse counts remain covered by regression tests.
