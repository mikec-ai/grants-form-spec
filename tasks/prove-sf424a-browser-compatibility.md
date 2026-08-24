---
type: Task
title: Prove SF-424A browser compatibility
description: >-
  Teach the generic capability planner to recognize declarative multiField table
  widgets, then run a bounded SF-424A receipt through the real Simpler frontend
  without form-specific runtime behavior.
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-24T15:37:55.075Z'
superbee_progress_status: done
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

Implemented and pushed through consumer commit `5814ffdf5` in fork-only stacked PR [#74](https://github.com/mikec-ai/simpler-grants-gov/pull/74), now based on the completed SF-424 Short receipt branch.

The generic planner now normalizes single-pointer `field`/`fieldList` declarations and array-pointer `multiField` declarations through one capability boundary. It contains no form-ID or widget-name branch. Every declared pointer is resolved against the projected schema before publication.

Observed bounded SF-424A plan result:

- `uiFields`: 0 to 6
- `editableScalar`: `not_applicable` to `applicable`
- Stable projected UI definition paths: 10
- Editable pointer bindings: 13

Ordinary SF-424 discovery remains intact while calculated/prepopulated outputs are correctly excluded from applicant-editable controls. Focused API evidence: 31 browser-plan, preview, and bounded-seed tests passed, plus Ruff.

# Browser receipt, 2026-08-24

The bounded plan exposed six specialized budget interaction surfaces, 13 editable schema bindings, and all 35 calculation declarations. The real Simpler application route passed all six Stage A probes:

- preview registration;
- adapter API preflight;
- live application render;
- deterministic edit, save, and reload with 116 editable controls preserved;
- WCAG 2 A/AA and 2.1 A/AA Axe scan with zero violations and keyboard focus reaching the first budget field; and
- locked print render.

The receipt also produced three generic improvements rather than form-ID exceptions: composite interaction surfaces fall back to a rendered editable child, persistence compares applicant-editable state rather than normalized calculated output, and shared budget inputs/tooltips now expose valid accessible names and roles. Focused frontend evidence: 44 component/matrix tests passed, plus ESLint, Prettier, TypeScript, a production build, and the bounded Chrome receipt.

Generated plans and receipts remain local build evidence and are not checked into the runtime repository. This completes browser compatibility for the portable SF-424A projection. It does not claim that unresolved source semantics or human accessibility review are complete.

Roadmap: [[roadmaps/portable-form-spec]]
