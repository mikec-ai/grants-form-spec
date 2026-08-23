---
type: Task
title: Enforce a no-new-unclassified-debt ratchet
priority: P0
assignee: codex
description: >-
  Block new unexplained form-local fields immediately while the historical
  baseline is normalized.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T17:14:42.952Z'
---
# Objective

Prevent the current unclassified-field backlog from growing while historical normalization proceeds.

# Baseline

Use the emitted field identities from producer commit `46e71d5` as the initial ceiling. The baseline
contains 90 form/field occurrences, including known lineage false positives that will be removed by
the canonical-lineage task.

# Acceptance criteria

- CI compares the newly emitted unclassified occurrence identities with a committed, reviewable
  baseline and fails on every addition, not merely on an increased aggregate count.
- Removing a baseline occurrence is allowed and updates the generated report; removed debt cannot
  silently return.
- A new form passes only when each field either composes canonical lineage or carries an explicit
  portable classification.
- The check reports added and removed identities clearly enough for PR review.
- The baseline is deterministic, source-controlled, documented, and shrinks monotonically.
- The later zero-unclassified gate can delete the baseline without changing the authoring contract.

[depends on](classify-portable-response-roles.md)
