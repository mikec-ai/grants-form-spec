---
type: Task
title: Author and integrate R&R Federal/Non-Federal Budget
priority: P2
assignee: codex_rr_fed_nonfed_provenance
description: >-
  Extend the portable research-budget architecture to the distinct
  Federal/Non-Federal form after current budget-family gates.
superbee_progress_status: in_progress
superbee_updated_by: codex-scanner-defect-review
generated:
  by: 'process:superbee'
  at: '2026-08-25T13:10:26.819Z'
---
# Goal

Author R&R Federal/Non-Federal Budget as a distinct source-evidenced member of the portable research-budget architecture after the existing R&R Budget family gates are understood.

# Verified starting state

The form is absent from the current 39-form producer catalog and consumer bank. Existing budget questions and calculation primitives are reuse candidates, not proof that this form is a parameterized variant.

# Acceptance criteria

- Pin exact official XSD, DAT, PDF/XFA, and instruction sources with versions and digests.
- Compare every field, calculation, condition, period, and XML structure with the existing research-budget bank; classify similarity separately from reviewed semantic reuse.
- Express supported reuse through declarative questions, blocks, rules, and targets with no form-specific compiler or adapter branch.
- Prove representative minimal, maximal, invalid, calculation, conditional, and XML/XSD cases.
- Bank the immutable package without production registration and preserve human semantic, accessibility, instruction, and release gates.
- Record reused versus new capabilities and marginal effort.

# Claim — 2026-08-25

- Claimed by `codex_rr_fed_nonfed_provenance` after auditing the canonical board, producer worktrees, local/remote branches, and all private-fork pull requests. No existing R&R Federal/Non-Federal Budget producer branch, worktree, or PR was found.
- The first slice is deterministic provenance and source-accounting only. It pins crosswalk revision `4312f6504b060e2b9ffdbd2307fc41130c3123a0`, FID `738`, the official `RR_FedNonFedBudget_2_0-V2.0.xsd` receipt SHA-256 `2ae0445e5f0a7228c1b0cdecbedc8fb4bb064f6249644e20f3dc99164bd44a1f`, and DAT `RR_FedNonFedBudget_2_0-V2.0_F738.xls` receipt SHA-256 `cfa2cd8cb6003f44093c085fd3503c8b32d7cf6ac4a15c6362ca706fa5c8255e`.
- This bounded slice records the deterministic 364 question/structure records and 391 DAT behavior records, without touching the excluded 10-year or 30-year subaward wrapper lanes.
- No legacy Simpler runtime oracle exists for this form. The crosswalk's parameterized-variant architecture, semantic reuse, behavior bindings, calculations, conditions, runtime package, consumer readiness, banking, and registration remain agent-proposed or unreviewed and cannot contribute to published coverage.

# Producer receipt — 2026-08-25

- Opened private-fork producer PR `mikec-ai/grants-form-spec#111` at commit `4ba62c553`. Exact scope is two new files and 191 insertions: `research/rr-federal-non-federal-budget/source-audit.json` plus `tests/test_rr_federal_non_federal_budget_source_audit.py`.
- Fresh official downloads reproduced the pinned XSD and DAT hashes exactly. Deterministic XSD inspection records 143 declared element nodes and six root children: five required, one optional, with `BudgetYear` repeating `1..5`; it also distinguishes 8 named complex types and 5 named simple types from anonymous inline types.
- Focused source-audit tests passed 3/3. Full producer preflight passed 125 package tests, 377 Python tests with 10 skipped, 8 XML projection tests, and every compilation, projection, validation, packaging, analysis, and classified-field gate.
- No form declaration, semantic mapping, runtime/consumer projection, or 10-year/30-year subaward-wrapper file is present in the PR. All downstream architecture and behavior work remains gated.

# Deterministic provenance merge — 2026-08-25

- Private-fork PR `mikec-ai/grants-form-spec#111` merged at `2026-08-25T13:10:01Z` as squash commit `145ec347d7b03d2793190119ef1f995895511c26`; fetched and verified `origin/main` resolves to that exact commit.
- The exact pre-merge head was `4ba62c55391e61e227e554e7d66b6485ff5579a8`. GitHub reported `CLEAN` and `MERGEABLE`, with only the two provenance/test files and no 10-year or 30-year subaward-wrapper overlap.
- Hosted `form-spec` CI passed in run `32851446948`, job `97813086481`; hosted `proof-package` passed in run `32851446860`, job `97813085861`.
- The merge contains exactly 191 insertions: 110 in `research/rr-federal-non-federal-budget/source-audit.json` and 81 in `tests/test_rr_federal_non_federal_budget_source_audit.py`.
- This closes only the deterministic provenance/source-accounting slice. The task remains in progress; semantic reuse, parameterized-variant architecture, DAT behavior, portable authoring, runtime/consumer integration, PDF/instruction review, banking, and registration remain unstarted or explicitly gated.

[depends on](close-rr-budget-family-release-gates.md)
