---
type: Task
title: Build uniform portable-versus-legacy differential parity
superbee_progress_status: in_progress
priority: P0
description: >-
  Prove one generic compatibility harness across an initial 7-10 form cohort,
  then extend it across every overlap form.
actor: Codex
timestamp: '2026-08-23T22:26:31.443Z'
superbee_updated_by: legacy_diff_cohort
assignee: legacy_diff_cohort
---
# Goal

Build one portable-versus-existing differential harness, prove it first across an initial cohort of at least seven forms and preferably ten, then extend it to every form with an existing counterpart.

# Comparisons

- applicant-visible schema paths, types, requiredness, constraints, and defaults;
- UI ordering, grouping, labels, help text, and conditional presentation;
- validation verdicts across the same generated and curated payload cases;
- rule and calculation outcomes;
- persistence, locked, and print behavior where the runtime supports it;
- XML mappings and representative serialized output.

# Delivery sequence

1. Use SF-424, SF-424 Short, and SF-424A as manually inspected canaries.
2. Extend the same automated mechanism to at least four additional overlap forms, targeting a ten-form initial cohort.
3. Emit a comparable receipt for every run and quantify gaps instead of translating them into qualitative confidence.
4. After the initial proof package is complete, extend the harness across the remaining overlap catalog.

# Oracle policy

Existing behavior is a compatibility oracle, not semantic authority. A difference may be accepted when official source evidence or an approved product decision shows the portable behavior is more correct, but it must pass through the intentional-delta mechanism.

# Acceptance criteria

- The initial cohort contains at least seven forms and targets ten without form-specific comparison logic.
- All overlap forms can ultimately run through the same differential harness and emit comparable receipts.
- Fixtures and comparison logic are generic and capability-driven, with form-specific data remaining declarative.
- Undocumented differences fail the gate.
- Results clearly separate parity, intentional evidence-backed deltas, unresolved review items, and defects requiring correction.

[depends on](add-portable-form-preview-registration.md)

[depends on](enforce-evidence-backed-parity-deltas.md)

## Implementation checkpoint: initial seven-form cohort

Draft consumer PR [mikec-ai/simpler-grants-gov#76](https://github.com/mikec-ai/simpler-grants-gov/pull/76), exact head `05f67f9ee469c24f01734bea462eed7c1cbcbcb1`, implements the first uniform cohort from fork `main` after merged PR 75.

The cohort is SF-424, SF-424 Short, SF-424A, Key Contacts, Project Abstract Summary, Project Narrative Attachments, and SF-424B. The same generic comparator runs every form; form-specific declarations are limited to existing-oracle identity and exact intentional-delta keys with a reason and durable evidence path. It has no form-ID branches.

Current reproducible result:

- 7 comparison-gated receipts passed and 0 failed;
- schema: 1 parity and 6 evidence-linked intentional deltas;
- UI: 3 parity and 4 evidence-linked intentional deltas;
- validation: 5 parity and 2 evidence-linked intentional deltas;
- rules: 6 declaration parity and 1 not applicable;
- 46 focused and related tests passed;
- direct isort, Black, Ruff, and full API mypy passed.

The static mechanism deliberately reports XML, rule outcomes, and runtime lifecycle as `unavailable`. It does not convert an unsupported comparison into zero differences or parity. Project Narrative Attachments is exact parity across all four supported dimensions. Generated receipts remain ignored and are published as a CI build artifact.

Receipt provenance does not depend on Git being installed in the runtime container. CI injects and strictly validates the full GitHub commit SHA; local runs may use the same option or fall back to the local Git HEAD. Tests reject invalid revisions and assert the injected revision is preserved in every receipt.

The next extension should add further overlap forms only when their existing implementation is a stable compatibility oracle. Diagnostic runs against SF-LLL and Performance Site Locations exposed broad source or structural divergence, so they were not normalized into large intentional-delta allowlists merely to increase the cohort count. They remain candidates for source reconciliation before cohort admission.
