---
type: Task
title: Harvest R&R SF-424 Multi-Project Cover
priority: P1
assignee: codex
description: >-
  Completed and merged end to end. Crosswalk PR #18 added the deterministic
  proof records. Producer PR #22 added the fifteenth portable form plus generic
  nested enabled/read-only projection. Public adapter PR #19 loads the exact
  package with no form-specific adapter code. The implementation proves 138 of
  139 relative XSD paths align with standalone R&R SF-424 while preserving zero
  unconditional required fields, 14 typed conditions, the tracking-field rename,
  and unresolved lifecycle ownership. Zero semantic mappings are accepted. Exact
  XML, human semantic acceptance, accessibility, and release remain separate
  portfolio gates.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T22:55:40.807Z'
---
# Objective

Demonstrate falling marginal form cost by adding the R&R SF-424 Multi-Project Cover as a thin declarative derivative of the merged R&R SF-424 foundation.

# Acceptance criteria

- The importer stages deterministic source records, behaviors, provenance, and review gates reproducibly.
- Shared questions are composed only where semantic identity is supported; similar labels remain proposals.
- Form-specific differences are visible as declarative deltas.
- Emitted artifacts validate and the public adapter can load the form as a canary without form-specific runtime code.
- Remaining XML, human review, accessibility, and release gates are explicit.
