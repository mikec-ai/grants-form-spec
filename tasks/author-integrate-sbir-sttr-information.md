---
type: Task
title: Author and integrate SBIR/STTR Information
priority: P1
description: >-
  Add a moderately sized, high-value small-business supplemental form after the
  immediate PHS tranche, reusing shared application and organization concepts.
superbee_progress_status: in_progress
superbee_updated_by: audit_sbir_sttr
generated:
  by: 'process:superbee'
  at: '2026-08-24T03:49:21.468Z'
assignee: audit_sbir_sttr
---
# Goal

Author SBIR/STTR Information as a source-bound declarative supplemental form and measure how much of its structure composes from the established portable library.

# Evidence starting point

- Two-year usage evidence records 22,853 form instances.
- The research factory records 40 question/structure records, 78 behavior records, and nineteen working conditions.
- The form should reuse application, organization, person, attachment, condition, and XML foundations while retaining SBIR/STTR-specific program semantics.

# Acceptance criteria

- Pin and promote exact official XSD, DAT, PDF/XFA, instructions, versions, and hashes.
- Reuse shared questions, blocks, conditions, XML fragments, and organization or person concepts only where role-qualified semantic evidence supports equivalence.
- Keep SBIR/STTR-specific eligibility, ownership, affiliation, certification, and program policy declarative and versioned.
- Express all source-backed conditions and mappings declaratively; retain unresolved policy decisions explicitly.
- Validate representative minimal, populated, conditional, invalid, save/reload, locked/print, and XML/XSD cases.
- Add no form-specific compiler, adapter, loader, renderer, or conformance branch.
- Bank through the generic consumer promotion path, with registration and release gated by human semantic, policy, instruction, accessibility, lifecycle, and operational review.
- Record marginal effort and the exact reusable versus new artifacts.

# Scope boundary

Do not introduce a general eligibility or policy DSL solely for this form. Any new generic capability must be justified by concrete reuse.

[consumer delivery follows](automate-cross-repo-form-promotion.md)
