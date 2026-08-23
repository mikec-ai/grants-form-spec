---
type: Task
title: Enforce the classified form-field gate
priority: P1
description: >-
  Prevent unknown field classifications from returning after the baseline
  normalization work is complete.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T17:14:43.135Z'
---
# Objective

Make complete field classification a durable producer invariant after the baseline backlog is
resolved.

# Acceptance criteria

- The 19-form baseline emits zero unknown rows in `unclassified-form-fields.csv`; explicitly
  classified form-local technical/system/attestation fields remain visible in the full occurrence
  dataset but are not counted as semantic questions.
- CI fails when a new emitted field lacks both canonical lineage and an explicit response role.
- Any temporary exception requires a source/evidence reference, owner, reason, and bounded removal
  condition; silent allowlists are not accepted.
- Marginal capability reuse and pairwise similarity continue to count only the intended semantic and
  capture-mechanism classifications.
- Documentation explains how a form author resolves the gate without inventing a duplicate question.

[depends on](classify-portable-response-roles.md)

[depends on](repair-form-local-lineage-analysis.md)

[depends on](canonicalize-sf424-cover-question-clusters.md)

[depends on](promote-residual-reference-form-questions.md)

[depends on](resolve-lifecycle-attestation-control-fields.md)

[depends on](enforce-no-new-unclassified-debt-ratchet.md)
