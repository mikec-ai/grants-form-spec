---
type: Task
title: Enforce the classified form-field gate
priority: P1
description: >-
  Prevent unknown field classifications from returning after the baseline
  normalization work is complete.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:44:22.030Z'
assignee: gate_assessment_agent
---
# Objective

Make complete field classification a durable producer invariant after the baseline backlog is
resolved.

# Acceptance criteria

- The 30-form baseline emits zero unknown rows in `unclassified-form-fields.csv`; explicitly
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
- Head: `bd4bb2ae37f4c17cd64636e6d2480e52cecc5c4c`
- Base: producer main `c508ec23e478ffe8892a00fb3c0862218fc0d2d9`, which includes the completed cover normalization, SF-424D evidence reconciliation, and 30th portable form.
- The permanent gate consumes the deterministic `unclassifiedFormFields` analysis projection and starts at zero unknowns with an empty exception ledger.
- An emitted applicant-input field still requires canonical semantic lineage. Calculated outputs, system values, technical fields, attestations, and static content may remain form-local only when their explicit response role is authored.
- Temporary exceptions are exact `formId:fieldPath` records and fail closed unless they include evidence references that resolve through canonical repository `evidence/**/*.json` paths and valid JSON Pointers, an owner, a reason, and a removal criterion plus a recognized Superbee task or GitHub issue/PR tracking reference. Bogus, duplicate, unsorted, incomplete, and stale exceptions fail.
- No analyzer, pairwise-similarity, reviewed-mapping, or marginal-capability-reuse calculation changed. Semantic questions and capture mechanisms remain separate classifications.
- Author documentation explains how to reuse an existing question, add a genuinely new source-evidenced question, or classify a non-question field without inventing a duplicate.

## Validation

- Full producer preflight passed.
- TypeScript: 102 tests passed.
- Python: 146 tests passed, 1 environment/source-checkout skip.
- Artifact validation: 180 blocks and 1,010 artifacts.
- Bundle verification: 699 artifacts.
- Permanent gate: 0 unclassified occurrences and 0 exceptions.
- Every TypeSpec file compiled independently.

## Historical review boundary

PR 55 was reviewed in the private producer repository and later merged as `825ee6b1`. No HHS/upstream repository was involved.

## Independent-review correction

The first review correctly found that merely non-empty evidence and tracking strings could degrade into a silent allowlist. Head `c77f55f14` now resolves every evidence reference to existing repository JSON content through RFC 6901-style pointers and restricts removal tracking to canonical Superbee task identifiers or complete GitHub issue/PR URLs. Positive tests use real SF-424 evidence; negative tests cover missing files, missing pointers, invalid pointer escapes, paths outside `evidence/`, and unrecognized tracking strings. Full preflight passed again after the current-main rebase.

## Final 30-form integration

The reviewed patch was mechanically rebased without semantic changes onto producer main `c508ec23e`. `git range-diff` reported the patch as identical. The regenerated analysis covers 30 forms and 603 exploratory semantic associations with zero unclassified occurrences and an empty exception ledger. Full preflight passed at head `bd4bb2ae3`. GitHub CI completed successfully at 2026-08-23T21:15:18Z. Producer PR 55 merged to main as `825ee6b1dc3c038e4dbacbb38ffab52e4b4f6100`.
