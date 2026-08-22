---
type: Task
title: Harvest R&R SF-424 Multi-Project Cover
priority: P1
assignee: codex
description: >-
  Use the reviewed R&R SF-424 foundation and generic crosswalk promotion
  importer to stage and declaratively author the Multi-Project Cover derivative.
  Preserve exact source/version provenance, keep semantic mappings proposed
  until reviewed, and quantify the real delta without form-specific compiler or
  adapter code.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T22:31:12.377Z'
---
# Objective

Demonstrate falling marginal form cost by adding the R&R SF-424 Multi-Project Cover as a thin declarative derivative of the merged R&R SF-424 foundation.

# Acceptance criteria

- The importer stages deterministic source records, behaviors, provenance, and review gates reproducibly.
- Shared questions are composed only where semantic identity is supported; similar labels remain proposals.
- Form-specific differences are visible as declarative deltas.
- Emitted artifacts validate and the public adapter can load the form as a canary without form-specific runtime code.
- Remaining XML, human review, accessibility, and release gates are explicit.
