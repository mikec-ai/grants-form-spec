---
type: Task
title: Define the independent parity decision-artifact receipt
priority: P1
description: >-
  Add the separately verified decision-evidence contract required before any
  parity delta can be accepted or reported as reviewed_delta.
superbee_progress_status: done
superbee_updated_by: codex-parity-decision-receipt
generated:
  by: 'process:superbee'
  at: '2026-08-25T16:14:47.287Z'
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

This is a governance capability. It does not mark any current parity delta accepted.

# Implementation receipts

Producer [PR 114](https://github.com/mikec-ai/grants-form-spec/pull/114) merged at
`90d30ce208f77c184b7a67cc40564b701303aed7`. It adds separate decision-artifact and receipt
schemas, requires a previously committed exact decision artifact, packages the artifact bytes for
offline verification, and rejects missing, stale, tampered, reused, unverified, and unused decision
evidence. The receipt remains empty and all 50 current records remain proposed. Full producer
preflight passed with 125 TypeScript tests, 391 Python tests (10 skipped), eight XML projection
tests, and a verified 1,199-artifact bundle.

Consumer [PR 119](https://github.com/mikec-ai/simpler-grants-gov/pull/119) merged from exact head
`3aec12b3f86bbe911abe7980421ad13f650bf184` as
`5306be67eaf230c6c509b75516be3aa8db380a74`. It implements the same generic fail-closed joins,
carries referenced decision artifacts through synchronization only when a ledger opts into the
decision contract, and preserves valid pre-decision bundles. It rejects any decision artifact path
outside `^parity/decisions/[a-z0-9][a-z0-9.-]+\.json$` and verifies resolved-path containment before
writing a selection. Regression tests cover receipt traversal, direct write escape, and a complete
legacy-bundle selection/write.

Local consumer verification passed 43 focused differential, synchronization, and provenance tests;
the wider form-spec collection passed 422 tests, with only two environment-only setup errors because
the local `grants-db` host was unavailable. Ruff, Black, and MyPy passed. Independent fixed-head
re-review found both security and backward-compatibility blockers closed and passed 35 focused tests.

Hosted API run [32867496119](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32867496119)
passed 4,806 tests (two skipped) in 23:34; the complete API job passed in 27:05. Its differential
receipt covered seven forms with one comparison gate passed, six blocked, and zero failures. Artifact
`9571879766` contains eight files (13,484 bytes), SHA-256
`2a4f9fe949fa80aad00dd3ad071f3062d0e71c198fa9a38873a633f6fdd66eab`.

The parallel E2E run's attachment/upload saturation failures were classified as unrelated: this
server-side parity verifier cannot exercise that frontend path, so no non-attributable rerun or code
change was made.

The newest producer bundle was deliberately not promoted in PR 119 because doing so would also
import EPA/shared personal-data changes owned by another lane.

[depends on](enforce-evidence-backed-parity-deltas.md)
