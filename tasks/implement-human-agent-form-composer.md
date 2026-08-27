---
type: Task
title: Implement shared human-agent form composer foundation
priority: P0
assignee: Codex
description: >-
  Create a renderer-independent authoring workspace where agents and humans edit
  the same portable-form-authoring draft. First slice: browse the exact question
  catalog, inspect provenance and review status, select/remove/reorder
  questions, preserve stable IDs, and render a live example without introducing
  a GUI-only form format.
superbee_progress_status: in_progress
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T20:05:58.693Z'
---
# Architectural boundary

The GUI and agent are peer clients of the same neutral authoring contract. The composer may not store React components, HTML, renderer names, or WYSIWYG-only state in the canonical draft. Question selection and edits must preserve exact question-catalog identities, source receipts, and semantic-review status.

# Acceptance evidence

- A framework-neutral package owns authoring workspace state and commands.
- A human-facing composer uses that package to browse and select catalog questions.
- The selected questions are visible alongside their exact IDs and review status.
- The same neutral draft can be serialized for agent or CLI continuation.
- A live form example updates from the selected questions through a generic renderer path.
- Tests enforce dependency boundaries and deterministic draft edits.
