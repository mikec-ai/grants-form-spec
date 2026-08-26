---
type: Task
title: Add a generic portable matrix presentation contract
priority: P0
assignee: codex
description: >-
  Preserve visible and programmatic dimensional context without form-specific
  renderer code or inferred calculations.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-26T05:56:56.534Z'
---
---
type: Task
title: Add a generic portable matrix presentation contract
priority: P0
assignee: codex
description: >-
  Preserve visible and programmatic dimensional context without form-specific
  renderer code or inferred calculations.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-26T05:54:24.096Z'
---
# Goal

Design and implement a generic portable matrix-presentation contract so dimensional fields retain visible row/column context, keyboard order, deterministic error routing, and screen-reader coordinate context without a PHS-specific renderer branch.

# Evidence boundary

- The PHS Inclusion Enrollment Report exposes 115 unique coordinate-qualified runtime fields from one reused semantic question.
- Source audit preserves exact XSD, DAT, read-only PDF, and XFA PDF hashes.
- The existing producer intentionally compiles zero of 8 source-bound conditions and 28 calculation targets because exact operands and blank-value semantics are not pinned.
- This task must not infer those missing rules. Matrix presentation is separable from calculation execution.

# Acceptance criteria

- A portable, output-neutral matrix presentation shape represents row and column dimensions generically.
- Simpler renders the shape without form-specific compiler, adapter, or renderer branches.
- Row and column headers are programmatically associated with every editable and protected coordinate.
- Keyboard order, focus/error routing, repeat-entry behavior, save/reload, locked state, and print are tested.
- At least PHS Inclusion Enrollment and one second dimensional form exercise the contract before it is called shared.
- Existing stable paths, XML projection, and source provenance remain unchanged.

# Architecture reconnaissance

- Simpler already has a generic `TableWidget` with column headers, captions, editable/read-only cells, numeric formatting, nested value paths, validation routing, locked-state behavior, and print support. Reusing it is preferable to adding a PHS renderer.
- The current portable SGG emitter can only emit `SggMultiField` at section level. `SggFieldList.children` accepts fields and nested field lists, but not multi-fields, so a matrix inside a repeated report cannot currently reach the existing table widget declaratively.
- The likely smallest slice is therefore producer-first: add a target-neutral matrix/table presentation decorator and shape, allow emitted multi-fields inside field-list children, then make the existing Table widget accept the fully nested repeated-item definitions.
- PHS coordinates require grouped row semantics across ethnicity and sex, not merely a flat label column. The contract design must support programmatic row headers (including grouped headers where needed) before implementation begins.
