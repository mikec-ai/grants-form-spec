---
type: Task
title: Author and integrate R&R Subaward Budget
priority: P0
assignee: codex-team
description: >-
  Next R&R sibling proving declarative reuse from R&R Budget through the generic
  Simpler adapter.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T18:54:59.397Z'
---
# Objective

Author R&R Subaward Budget as the next sibling of R&R Budget, using the existing portable research-budget questions and structures wherever semantic meaning and behavior are actually equivalent.

# Scope

- Establish exact source identity and version provenance before authoring.
- Compare the sibling with R&R Budget at question, rule, calculation, UI, XML, and evidence levels.
- Reuse declarative blocks for confirmed shared meaning.
- Preserve subaward-specific identity, cardinality, nesting, and wire mappings.
- Emit portable artifacts and integrate them through the generic adapter in the public Simpler fork.
- Add parity, validation, calculation, artifact-contract, and browser-facing tests in proportion to the form's behavior.

# Acceptance criteria

- No form-specific compiler or adapter branch is introduced.
- Every reused question has an evidence-backed semantic basis rather than a label-only match.
- Source-bound differences remain explicit.
- Producer preflight and focused Simpler adapter tests pass.
- Work is merged only in `mikec-ai` repositories.

# Delivery status

- Producer implementation merged in `mikec-ai/grants-form-spec` PR 11 at merge commit `1ebbd4077`.
- Form identity: `RR_SubawardBudget_3_0`, version 3.0, legacy FID 776.
- Exact XSD and DAT hashes are recorded in the form evidence sidecar.
- The form composes the shared R&R Budget detail block and adds the subaward attachment collection.
- Analysis reports 14 of 15 semantic blocks reused, one new composition block, and 93.3 percent pairwise similarity.
- The generic compiler now supports parent-scoped calculation paths, emitted as `@PARENT` references when a reused block is nested.

# Remaining production work

- Integrate the emitted bundle through the public Simpler fork's generic adapter.
- Add generic frontend support for nested repeating groups; the current frontend rejects nested `fieldList` definitions.
- Reconcile the remaining source calculations and conditions rather than inferring them.
- Validate save/reload, read-only, print, accessibility, and submission behavior.

# Coordination

This task builds on the completed portable R&R Budget implementation and should expose reusable improvements that strengthen both forms.

[depends on](author-integrate-rr-budget.md)
