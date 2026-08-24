---
type: Task
title: Prove SF-424A browser compatibility
description: >-
  Teach the generic capability planner to recognize declarative multiField table
  widgets, then run a bounded SF-424A receipt through the real Simpler frontend
  without form-specific runtime behavior.
superbee_updated_by: sf424a_multifield
generated:
  by: 'process:superbee'
  at: '2026-08-24T14:37:58.522Z'
superbee_progress_status: in_progress
priority: P0
assignee: codex-root
---
# Goal

Produce the next bounded SF-424A compatibility increment and make its table interaction surface visible to the generic browser plan.

# Acceptance criteria

- Generic capability discovery recognizes `multiField` table widgets and their editable fields without a form-id branch.
- Existing ordinary-field planning remains unchanged.
- The bounded plan reports SF-424A table/editable capabilities accurately.
- Focused contract tests pass.
- The follow-on browser receipt covers navigation, calculations, persistence, accessibility, locked state, and print only to the extent observed.
- The receipt preserves the distinction between runtime parity and unresolved source-semantic acceptance.

# Capability-discovery increment, 2026-08-24

Implemented and pushed as consumer commit `d30141473` in fork-only stacked PR [#74](https://github.com/mikec-ai/simpler-grants-gov/pull/74), based on `codex/sf424-compatibility-receipt`.

The generic planner now normalizes single-pointer `field`/`fieldList` declarations and array-pointer `multiField` declarations through one capability boundary. It contains no form-ID or widget-name branch. Every declared pointer is resolved against the projected schema before publication.

Observed bounded SF-424A plan result:

- `uiFields`: 0 to 6
- `editableScalar`: `not_applicable` to `applicable`
- Stable projected UI definition paths: 10
- Editable pointer bindings: 13

Ordinary SF-424 behavior remains 66 UI fields and 66 editable declarations. Focused evidence: 11 browser-plan tests passed; focused Ruff formatting/lint and mypy passed. No Docker, API, or browser environment was run or mutated.

This completes capability discovery only. The task remains in progress for the browser receipt and does not yet claim SF-424A runtime parity or source-semantic acceptance.
