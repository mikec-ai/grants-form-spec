---
type: Task
title: Close R&R SF-424 release gates
priority: P0
assignee: codex
description: >-
  Build generic lifecycle conformance evidence for R&R SF-424; close
  high-confidence conditional validation, save/reload, locked/print, XML/XSD,
  and accessibility gates; register only after the relevant gates pass.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T13:43:59.073Z'
---
# Scope

- Keep the portable producer authoritative and the Simpler integration generic.
- Add reusable lifecycle validation rather than form-specific test-only shortcuts.
- Preserve unresolved source conflicts and human approval gates explicitly.
- Work only in mikec-ai public repositories; do not modify HHS upstream.

## Completed

- Added the missing RRSF424 Simpler runtime type.
- Added a reusable lifecycle conformance helper that executes the production registry, validator, and rule processor.
- Proved JSON save/reload preservation, corrected-application and renewal requirements, and submit-time signature/date population.
- Merged adapter PR 25 to main; 103 portable-form tests pass.

## Remaining

- Exact Grants.gov XML and XSD conformance.
- Form-specific rendered and locked/print evidence.
- Accessibility and human semantic/policy review.

## Discovery

The provisional crosswalk XML mapping exposes an architectural gap: some Grants.gov output wrappers do not align one-to-one with canonical response nesting. The next reusable slice is an output mapping capable of declaring source paths independently from XML grouping.

[depends on](author-integrate-rr-sf424.md)
