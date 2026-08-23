---
type: Task
title: Unify canonical path projection in the Simpler adapter
priority: P1
description: >-
  Replace parallel UI and rule path-renaming traversal with one
  conformance-tested adapter primitive.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T15:34:46.790Z'
assignee: sf424a_semantic_review
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

# Result

Merged as `mikec-ai/simpler-grants-gov` PR #30 at commit `31139a235ee5962d36cd7628bae035cd86b1ce0c` after independent review and correction of item ancestry, numeric pointer segments, regex keys, and unsupported selectors. UI pointers, rule references, and XML source pointers now share one ancestry-aware field-segment projector. The final branch passed 117 form-spec tests, 34 focused API tests, 82 frontend tests with one skip, Ruff, mypy, isort, Black, and diff checks. A prerequisite baseline repair was separately merged as PR #31 so main remained green.
