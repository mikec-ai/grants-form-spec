---
type: Task
title: Import a pinned producer-backed form cohort into the workbench
priority: P0
assignee: Codex
description: >-
  Completed and independently approved. Workbench commits 71b3642, a538d93, and
  4c3c60c import SF-424, SF-424 Short, Attachment Form, and PHS Assignment
  Request from pinned grants-form-spec revision 273d1ba8. The importer
  regenerates producer output, preserves exact artifacts and conservative
  semantic-review status, compiles nested JSON Schema resources safely, rejects
  unresolved active references, constrains cleanup to a dedicated cohort
  directory, and provides an AXI-compliant command interface. Combined
  integration verification: 166 tests passed, 1 skipped; typecheck, all builds,
  dependency tree, and diff checks green. Independent review found no remaining
  P0/P1/P2 issues.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T01:51:32.496Z'
---
[depends on](implement-portable-form-catalog.md)
