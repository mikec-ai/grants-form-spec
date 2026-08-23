---
type: Task
title: Unify canonical path projection in the Simpler adapter
priority: P1
description: >-
  Replace parallel UI and rule path-renaming traversal with one
  conformance-tested adapter primitive.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T14:27:32.599Z'
---
# Goal

Consolidate canonical-to-Simpler path projection so UI JSON Pointers and rule references use one segment-aware renaming implementation.

# Acceptance criteria

- One tested primitive handles JSON Pointer paths, root-relative dotted references, `@THIS` references, and repeated-item markers without changing their external syntax.
- UI schema, rule schema, and any XML source-path projection call the shared primitive rather than maintaining independent field-segment traversal.
- Golden tests cover irregular per-form renames, arrays, nested blocks, escaped pointer segments, and unchanged non-field identifiers.
- Existing adapter parity payloads and validation behavior remain unchanged.
- The change introduces no producer dependency and no form-specific adapter branch.

# Design constraint

Keep consumer projection in the Simpler adapter. This task simplifies that boundary; it does not push legacy naming into canonical artifacts.
