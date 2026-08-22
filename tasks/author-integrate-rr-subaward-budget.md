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
  at: '2026-08-22T18:43:38.706Z'
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

# Coordination

This task builds on the completed portable R&R Budget implementation and should expose reusable improvements that strengthen both forms.

[depends on](author-integrate-rr-budget.md)
