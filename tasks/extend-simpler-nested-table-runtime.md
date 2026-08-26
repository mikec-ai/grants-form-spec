---
type: Task
title: Extend Simpler for tables inside repeatable entries
priority: P0
description: >-
  Consume nested portable table definitions with correct paths, persistence,
  validation, accessibility, locked state, and print behavior.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-26T11:45:19.096Z'
---
# Scope

Extend Simpler's existing generic `TableWidget` and `FieldList` composition path to consume a table nested inside a repeatable item. Resolve fully qualified item paths, preserve form state and validation routing, and support accessible grouped row headers.

# Acceptance

- No form-specific renderer or adapter branch.
- Existing SF-424C TableWidget tests remain green.
- Nested item paths bind, persist, validate, lock, and print correctly.
- Row/column associations and keyboard order are covered by focused tests.

[depends on](add-generic-portable-matrix-presentation.md)
