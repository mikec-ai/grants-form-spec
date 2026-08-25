---
type: Task
title: Define the independent parity decision-artifact receipt
priority: P1
description: >-
  Add the separately verified decision-evidence contract required before any
  parity delta can be accepted or reported as reviewed_delta.
superbee_progress_status: in_progress
superbee_updated_by: codex-parity-decision-receipt
generated:
  by: 'process:superbee'
  at: '2026-08-25T15:19:34.668Z'
assignee: codex-parity-decision-receipt
---
# Goal

Define a portable, offline-verifiable contract for accountable parity acceptance decisions so an accepted ledger record can safely produce `reviewed_delta`.

# Acceptance criteria

- Decision evidence is distinct from comparator assertions and authoritative source evidence.
- Every accepted record names an accountable reviewer, immutable decision artifact, repository, revision, and exact path.
- A pinned receipt verifies the decision artifact offline without ambient network access.
- Producer and consumer reject missing, stale, tampered, reused, or unverified decision evidence.
- Positive and negative tests prove the accepted path without weakening the proposed and unresolved boundaries.

This is a deferred governance capability. It is not permission to mark any current delta accepted.

# Implementation receipts

Producer [PR 114](https://github.com/mikec-ai/grants-form-spec/pull/114) merged at
`90d30ce208f77c184b7a67cc40564b701303aed7`. It adds separate decision-artifact and receipt
schemas, requires a previously committed exact decision artifact, packages the artifact bytes for
offline verification, and rejects missing, stale, tampered, reused, unverified, and unused decision
evidence. The receipt remains empty and all 50 current records remain proposed. Full producer
preflight passed with 125 TypeScript tests, 391 Python tests (10 skipped), eight XML projection
tests, and a verified 1,199-artifact bundle.

Consumer [PR 119](https://github.com/mikec-ai/simpler-grants-gov/pull/119) is open at
`973d6c395`. It implements the same generic fail-closed joins, carries referenced decision artifacts
through artifact synchronization, and remains backward-compatible with the currently vendored
pre-receipt ledger. A clean-worktree run passes 40 focused differential, synchronization, and
artifact-provenance tests plus Ruff, Black, and MyPy. A wider form-spec run passed 419 tests; its
two errors were existing database-dependent SF-424A lifecycle tests because local `grants-db` was
unavailable. The latest producer bundle is deliberately not promoted in PR 119 because that would
also import EPA/shared personal-data changes owned by another lane.

[depends on](enforce-evidence-backed-parity-deltas.md)
