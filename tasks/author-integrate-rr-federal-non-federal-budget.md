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
  at: '2026-08-25T13:02:04.611Z'
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

[depends on](close-rr-budget-family-release-gates.md)
