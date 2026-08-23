---
type: Task
title: Enforce the classified form-field gate
priority: P1
description: >-
  Prevent unknown field classifications from returning after the baseline
  normalization work is complete.
superbee_progress_status: in_progress
superbee_updated_by: gate_assessment_agent
generated:
  by: 'process:superbee'
  at: '2026-08-23T20:58:32.126Z'
assignee: gate_assessment_agent
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

# Delivery receipt — 2026-08-23

- Producer PR: https://github.com/mikec-ai/grants-form-spec/pull/55
- Head: `76bc9c6943d6261676bd01063eb1675ffe3ef7bb`
- Base: producer main `262f7a27127aa44fa6f3cf31eb30bb5f415ff933`, where the historical 76-occurrence backlog is fully resolved.
- The permanent gate consumes the deterministic `unclassifiedFormFields` analysis projection and starts at zero unknowns with an empty exception ledger.
- An emitted applicant-input field still requires canonical semantic lineage. Calculated outputs, system values, technical fields, attestations, and static content may remain form-local only when their explicit response role is authored.
- Temporary exceptions are exact `formId:fieldPath` records and fail closed unless they include non-empty evidence references, an owner, a reason, and a removal criterion plus tracking reference. Duplicate, unsorted, incomplete, and stale exceptions fail.
- No analyzer, pairwise-similarity, reviewed-mapping, or marginal-capability-reuse calculation changed. Semantic questions and capture mechanisms remain separate classifications.
- Author documentation explains how to reuse an existing question, add a genuinely new source-evidenced question, or classify a non-question field without inventing a duplicate.

## Validation

- Full producer preflight passed.
- TypeScript: 102 tests passed.
- Python: 130 tests passed, 1 environment/source-checkout skip.
- Artifact validation: 161 blocks and 924 artifacts.
- Bundle verification: 637 artifacts.
- Permanent gate: 0 unclassified occurrences and 0 exceptions.
- Every TypeSpec file compiled independently.

## Review boundary

PR 55 is open and intentionally unmerged pending independent review. No HHS/upstream repository is involved.
