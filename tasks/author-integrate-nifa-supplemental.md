---
type: Task
title: Author and integrate NIFA Supplemental
priority: P1
description: >-
  Add a bounded, high-use supplemental form that should compose mostly from
  existing application, organization, attachment, and form-shell foundations.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T00:52:58.679Z'
assignee: codex
---
# Goal

Author NIFA Supplemental as a source-bound declarative form and use it as a near-term test of falling marginal form cost.

# Evidence starting point

- Two-year usage evidence records 18,405 form instances.
- The research factory records 32 question/structure records, 31 behavior records, and four conditions.
- Its bounded shape should exercise existing application, organization, attachment, and layout foundations without requiring a NIFA-specific runtime subsystem.

# Acceptance criteria

- Pin and promote exact official XSD, DAT, PDF/XFA, instructions, versions, and hashes.
- Reuse existing questions, blocks, conditions, attachment behavior, XML fragments, and form-shell composition only where role-qualified semantic evidence supports equivalence.
- Keep NIFA-specific program and policy content declarative and local to the form package.
- Express all source-backed conditions and mappings declaratively.
- Validate representative minimal, populated, conditional, invalid, and XML/XSD cases.
- Add no form-specific compiler, adapter, loader, renderer, or conformance branch.
- Record elapsed effort, reused versus new artifacts, unresolved review gates, and marginal effort relative to the preceding forms.
- Bank through the generic consumer promotion path; leave runtime registration and release behind explicit human semantic, policy, instruction, accessibility, lifecycle, and operational approval.

# Scope boundary

Do not generalize a NIFA policy framework from one form. Promote only reusable capabilities demonstrated by at least one concrete second consumer.

# Measured run receipt — 2026-08-23

- Explicit start: 20:52 ET.
- Producer package merged at 21:19 ET in PR #63 as `c1c2150f54fff4131119857ae46950cf2fd6ed22`.
- Byte-exact XSD correction merged at 21:25 ET in PR #65 as `3a6e51127e66d5555f3ef677cb21c4b9f7751e9a`.
- Consumer banking PR #54 opened at approximately 21:34 ET and remains intentionally unregistered.
- Research import: about 0.4 seconds for 32 source records, 31 source behaviors, 22 applicant fields, eight presentation groups, four runtime effects from two source conditions, 32 semantic proposals, zero accepted mappings, and 39 open gates.
- Portable result: nine canonical questions, two reused and seven new; one reused attachment capture mechanism; three reused behavior capabilities; zero unclassified fields; zero classification exceptions; no form-specific compiler, adapter, loader, renderer, or conformance branch.
- Producer verification: 109 TypeScript tests and 226 Python tests passed after rebase.
- Consumer verification: 38 focused tests and 225 non-DB form-spec tests passed; the DB-backed local suite requires the unavailable `grants-db` environment.
- Remaining source gate: DAT-specific H-option narrowing remains explicit and unclaimed for release.

The full cost analysis and next-run procedure are recorded in [the NIFA banking retrospective](../context-notes/nifa-supplemental-banking-retrospective.md).

[consumer delivery follows](automate-cross-repo-form-promotion.md)

[measured by](../context-notes/nifa-supplemental-banking-retrospective.md)
