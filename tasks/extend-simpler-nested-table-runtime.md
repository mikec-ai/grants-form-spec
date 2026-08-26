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
  at: '2026-08-26T12:42:07.145Z'
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

# Closure update — 2026-08-26

- Consumer artifact-selection and validator PR #140 merged as `c886be7101c93a8308182d8491aa0308080708f5`: https://github.com/mikec-ai/simpler-grants-gov/pull/140
- Artifact-selection commit: `7c8d7bb09`; producer pinned at `c700c8bd1edb4e7537325e26a141776826f643b8`.
- Browser testing exposed a generic server-side UI-schema validator exclusion that rejected a `Table` child inside `FieldList`, even though the renderer supported it. Commit `732da5e48` removes that exclusion and adds the regression expectation.
- Focused frontend verification after the validator fix: 4 suites passed, 108 tests passed, 1 skipped; targeted ESLint passed.
- Standalone PHS Inclusion rendered both matrices, preserved repeat-entry-qualified names, exposed coordinate-qualified accessible names, added a second report occurrence, and persisted title plus matrix values through save and reload.
- Embedded PHS Human Subjects rendered the same two matrices inside `studies[0].populationCharacteristics.inclusionEnrollmentReports[0]`, preserved the full study/report-qualified names and coordinate-qualified accessible names, and persisted study title, report title, and a matrix value through save and reload.
- No form-specific adapter or renderer branch was added.

# Remaining closure gates

- Locked-state, print, and keyboard-order browser receipts remain open.
- Delete was not exercised in the browser because it is a destructive local-data action; unit coverage is not represented as a browser receipt.
- The embedded occurrence intentionally leaves 28 total-like coordinates editable: its pinned parent XSD and F705 DAT contain zero calculation records. Similar structure to standalone F791 is not evidence of equivalent calculations. Exact version-matched embedded-study behavior evidence is required before protecting or calculating them.
