---
type: Task
title: Extend Simpler for tables inside repeatable entries
priority: P0
description: >-
  Consume nested portable table definitions with correct paths, persistence,
  validation, accessibility, locked state, and print behavior.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-26T12:07:05.676Z'
assignee: codex
---
# Scope

Extend Simpler's existing generic `TableWidget` and `FieldList` composition path to consume a table nested inside a repeatable item. Resolve fully qualified item paths, preserve form state and validation routing, and support accessible grouped row headers.

# Acceptance

- No form-specific renderer or adapter branch.
- Existing SF-424C TableWidget tests remain green.
- Nested item paths bind, persist, validate, lock, and print correctly.
- Row/column associations and keyboard order are covered by focused tests.

[depends on](add-generic-portable-matrix-presentation.md)

# Implementation receipts

- Consumer commit: `254385a2a`
- Open consumer PR: https://github.com/mikec-ai/simpler-grants-gov/pull/139
- The generic FieldList configuration now accepts a one-root Table multiField.
- TableWidget resolves full portable paths against the current repeat-entry table value, writes back to the correct nested object, and scopes HTML identity to the actual repeat entry.
- Accessible names include all visible row dimensions plus the column header.
- Local checks passed: TypeScript, 89 targeted frontend tests (1 skipped), targeted formatting, and targeted lint with only three pre-existing TableWidget hook warnings.
- Browser persistence, locked-state, print, and end-to-end validation routing remain closure gates after the producer artifact is selected by the consumer.
- Consumer PR #139 merged as `88c7fc6c88058f3a2336218b128352c815e824af` after the frontend build, lint/type/format/test suite, Storybook, artifact classification, and API setup checks passed. Broad E2E and Pa11y jobs were still running at merge and are not claimed as receipts here.
