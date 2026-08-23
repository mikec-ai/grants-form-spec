---
type: Task
title: Enforce a no-new-unclassified-debt ratchet
priority: P0
assignee: codex
description: >-
  Block new unexplained form-local fields immediately while the historical
  baseline is normalized.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T17:35:28.270Z'
---
# Objective

Prevent the current unclassified-field backlog from growing while historical normalization proceeds.

# Baseline

The original producer report at commit `46e71d5` contained 90 form/field occurrences. Canonical-lineage repair removed 14 false positives, so the committed ratchet begins with 76 path-qualified unresolved occurrences.

# Acceptance criteria

- CI compares newly emitted unclassified occurrence identities with a committed, reviewable baseline and fails on every addition, not merely on an increased aggregate count.
- Removing a baseline occurrence is allowed and updates the generated report; removed debt cannot silently return.
- A new form passes only when each field either composes canonical lineage or carries an explicit portable classification.
- The check reports added and removed identities clearly enough for PR review.
- The baseline is deterministic, source-controlled, documented, and shrinks monotonically.
- The later zero-unclassified gate can delete the baseline without changing the authoring contract.

# Result

Implemented in grants-form-spec PR #41 at commit `6515f80`. `analysis/unclassified-fields-baseline.v1.json` records the exact 76 occurrence identities. CI and local preflight reject new identities, removals not explicitly moved to `resolved`, and any resolved identity that returns. A new field passes only with canonical question lineage or an explicit non-applicant response role; applicant input still requires semantic identity. The checker reports each added, silently removed, or returned identity. Full preflight passed with 118 blocks, 660 validated artifacts, 91 TypeScript tests, 75 Python tests, and a verified 440-artifact package.

[depends on](classify-portable-response-roles.md)
