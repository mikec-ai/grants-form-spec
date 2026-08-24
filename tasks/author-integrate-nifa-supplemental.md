---
type: Task
title: Author and integrate NIFA Supplemental
priority: P1
description: >-
  Add a bounded, high-use supplemental form that should compose mostly from
  existing application, organization, attachment, and form-shell foundations.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T00:38:09.000Z'
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

[consumer delivery follows](automate-cross-repo-form-promotion.md)
