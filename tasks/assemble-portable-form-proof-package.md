---
type: Task
title: Assemble the portable form proof package
priority: P0
assignee: proof_package
description: >-
  Package reproducible parity, source-validation, reuse, and demonstration
  evidence for the initial proof.
superbee_progress_status: in_progress
superbee_updated_by: rr_budget_condition_contract
generated:
  by: 'process:superbee'
  at: '2026-08-24T16:55:37.449Z'
---
# Goal

Assemble a concise, reproducible evidence package showing what the portable form architecture has proven and what remains open.

# Contents

- Side-by-side visual and behavioral evidence for SF-424, SF-424 Short, and SF-424A.
- Uniform automated compatibility receipts for at least seven overlap forms, targeting ten when supported without form-specific harness logic.
- An end-to-end source-validation receipt for R&R SF-424.
- Current catalog, question, capability, reuse, and data-quality metrics generated from implementation evidence.
- Pinned producer and consumer revisions plus brief instructions or a short recording showing how to reproduce the comparison.
- A clear separation between technical proof, unresolved compatibility gaps, human semantic review, accessibility review, policy decisions, and production registration.

# Acceptance criteria

- Every headline claim links to a reproducible receipt or is labeled as a limitation.
- The package communicates the value of reusable declarative authoring without requiring readers to understand the implementation repository.
- No internal organizational, procurement, or competitive commentary appears in the package.

[depends on](prove-sf424-family-visual-and-behavioral-parity.md)

[depends on](build-uniform-legacy-differential-parity.md)

[depends on](close-rr-sf424-release-gates.md)

# First increment

PR [mikec-ai/grants-form-spec#76](https://github.com/mikec-ai/grants-form-spec/pull/76) at exact head
`e26107c0a32bfc4555aa1a778fedeb76d057b996` adds a generated proof-package contract and index for
the evidence already available:

- SF-424 comparison and runtime receipts;
- SF-424 Short runtime receipt;
- SF-424A runtime receipt;
- R&R SF-424 lifecycle, exact-XSD, and six-probe browser evidence;
- the five-profile R&R Budget family proof;
- the reviewed-similarity boundary established by the corrected analysis export.

Each claim records pinned revisions, reproducibility steps, and explicit limitations. Producer files
are read from their exact Git revisions and hashed. Generated outputs remain ignored and are
published as a lightweight CI artifact. The four browser receipts use stable fork merge commits for
consumer PRs 71, 73, 74, and 75. The corrected analysis now records that reviewed pairwise
similarity is unavailable because there are zero accepted occurrence mappings. Reviewed values are
blank rather than zero, and implementation-derived exploratory similarity remains separate.

Local verification at the PR head: full `npm run preflight` passed (118 TypeScript tests and 314
Python tests with 2 skips), all pinned producer paths resolve at exact revision
`4229eca2e5902ea99c917271963be6bd0edf3027`, the focused builder tests passed, deterministic output
was verified, a worktree-only evidence regression passed, unknown flags return exit 2 with stderr
diagnostics, and `git diff --check` passed. Hosted form-spec CI and the dedicated proof-package
artifact job both passed at the exact head. This increment does not complete the broader
seven-to-ten-form or catalog-metrics scope, so the task remains in progress.

# R&R Budget condition-evidence follow-through

[grants-form-spec PR 78](https://github.com/mikec-ai/grants-form-spec/pull/78) pins every
producer-path claim to merged producer main revision
`2bd979045f3dabfd1f77655c92f36fd496b08f65` and adds the exact machine-readable R&R Budget DAT
condition inventory to the family claim. The claim now distinguishes 56 DAT-defined calculations
from the condition boundary: 64 conditioned occurrences, 50 represented by existing declarations,
and 14 explicitly source-bound and uncompiled. The inventory and family evidence remain
`unreviewed` for semantic acceptance.

The builder now rejects producer-path evidence whose revision differs from the package producer
revision. All declared producer paths resolve and are hashed from the pinned Git tree. Generated
`index.md` and `proof-manifest.json` remain ignored build artifacts. At PR head `4f28d50d1`, four
focused proof-package tests pass, deterministic generation reports six claims, and full preflight
passes with 118 TypeScript tests and 323 Python tests (two skipped). This is an evidence-hardening
increment; the broader proof-package task remains in progress.

# R&R Budget cross-section proof refresh

[grants-form-spec PR 80](https://github.com/mikec-ai/grants-form-spec/pull/80), merged at
`a667b9fa6904f9b12bdf424ac354c66935462631`, refreshes every producer-path claim to producer revision
`563e7d8b5a38c7b5d66723bfbc1607caeeff4aad` after the generic F-8-1 condition contract landed.
The family claim now states the exact 64-occurrence boundary as 50 represented by existing
declarations, 10 compiled through one generic cross-section contract, and four source-bound and
uncompiled pending source-exact numeric-string comparison semantics. It continues to state that
semantic acceptance and the broader human/release gates remain open.

The focused four-test proof suite and full producer preflight pass at PR head `4cc63b49d` (121
TypeScript tests and 325 Python tests, two skipped). Generated proof index and manifest remain
ignored build artifacts.
