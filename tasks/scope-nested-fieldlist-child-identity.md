---
type: Task
title: Scope nested FieldList child identity to full paths
priority: P0
assignee: codex
description: >-
  Eliminate React identity collisions when nested reusable groups share leaf
  field names.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-26T06:01:43.054Z'
---
Use fully qualified generated field paths as React identity for children inside nested FieldLists. Leaf-only identity collides when unrelated budget groups share names such as `requested_salary`.

Implemented in private-fork PR #138 with a regression test. Merged consumer commit: `00d9f61cd13032b4cdbae9089439c9cac5c5b290`.
