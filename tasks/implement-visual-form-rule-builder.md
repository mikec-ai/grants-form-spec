---
type: Task
title: Add visual conditions and validation rule authoring
priority: P0
description: >-
  Extend the shared authoring workspace and composer with a bounded,
  evidence-aware rule builder. Humans and agents must produce the same neutral
  behavior declarations; GUI state and renderer-specific rules remain outside
  the canonical draft.
superbee_progress_status: todo
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T20:16:45.508Z'
---
# Acceptance criteria

- Author conditions by choosing a trigger question, supported operator, value, target question, and effect.
- Support the existing portable visible, enabled, and required effects before calculations.
- Display agent rationale and exact evidence separately from the canonical rule declaration.
- Preview rules through the existing generic behavior runtime.
- Keep every rule proposed until review and preserve exact evidence receipts.
- Add framework-neutral command tests, architecture-boundary tests, and composer interaction tests.

[depends on](implement-human-agent-form-composer.md)
