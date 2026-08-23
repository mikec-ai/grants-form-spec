---
type: Task
title: Reuse R&R SF-424 blocks in Multi-Project Cover
priority: P0
description: >-
  Bounded schema-composition canary that removes optional-cardinality clones
  without weakening semantic identity.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T14:36:36.321Z'
assignee: rr_sf424_semantic_review
---
# Goal

Replace the form-local optional clones in R&R SF-424 Multi-Project Cover with the smallest generic, declarative JSON Schema composition mechanism that preserves the source-specific cardinality difference from standalone R&R SF-424.

# Acceptance criteria

- Shared semantic blocks remain referenced through ordinary JSON Schema `$ref` or `allOf`; the compiler does not gain a branch keyed to this form.
- Optionality is expressed as reviewable declarative data and validated against real paths at build time.
- The form retains its source-bound field inventory, conditions, presentation, mappings, and consumer parity.
- The 14 local `MultiProject*` model clones are materially reduced, with before-and-after declaration size and reusable-reference counts recorded.
- Existing producer, independent-consumer, XML, and Simpler adapter conformance tests remain green.

# Design constraint

Do not create a general override language. Prove only the cardinality capability required by this sibling pair, then stop and reassess.
