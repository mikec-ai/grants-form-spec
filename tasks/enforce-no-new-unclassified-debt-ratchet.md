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
  at: '2026-08-23T18:12:15.615Z'
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

Implemented and merged in grants-form-spec PR #41 at commit `c0eaa1870`. `analysis/unclassified-fields-baseline.v1.json` records the exact 76 occurrence identities. The original sorted identity universe is pinned by a code-reviewed SHA-256 digest, so contributors may move identities to `resolved` but cannot silently expand the initial allowlist. CI and local preflight reject new identities, removals not explicitly moved to `resolved`, and any resolved identity that returns.

A field is classified through lineage to a declared semantic-question or capture-mechanism block, or through an explicit non-applicant response role. Semantic-question and capture-mechanism classifications remain orthogonal in analysis: capture controls do not become questions. Purpose-specific overflow uploads therefore remain correctly classified capture mechanisms, while later parsing of attachment content remains a separate phase. The checker reports each added, silently removed, returned, or baseline-rewrite identity. Full preflight passed with 118 blocks, 660 validated artifacts, 91 TypeScript tests, 76 Python tests, and a verified 440-artifact package.

[depends on](classify-portable-response-roles.md)
