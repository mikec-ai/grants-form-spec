---
type: Task
title: Harvest R&R SF-424 Multi-Project Cover
priority: P1
assignee: codex
description: >-
  Producer PR #22 is open and green locally: 139 deterministic source records,
  143 source behaviors, 138 of 139 relative XSD paths shared with standalone R&R
  SF-424, 28 top-level properties, 106 rendered leaves, zero unconditional
  required fields, exact encoded revision values, and 14 generic nested
  enabled/read-only conditions. Crosswalk proof PR #18 is merged. Zero semantic
  mappings are accepted. Remaining work is CI/merge, public adapter canary,
  exact XML, and human/accessibility/release review.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T22:49:27.384Z'
---
# Objective

Demonstrate falling marginal form cost by adding the R&R SF-424 Multi-Project Cover as a thin declarative derivative of the merged R&R SF-424 foundation.

# Acceptance criteria

- The importer stages deterministic source records, behaviors, provenance, and review gates reproducibly.
- Shared questions are composed only where semantic identity is supported; similar labels remain proposals.
- Form-specific differences are visible as declarative deltas.
- Emitted artifacts validate and the public adapter can load the form as a canary without form-specific runtime code.
- Remaining XML, human review, accessibility, and release gates are explicit.
