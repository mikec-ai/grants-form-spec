---
type: Task
title: Research attachment semantics versus capture mechanisms
priority: P1
assignee: mikec-ai
description: >-
  Implemented and validated the distinction between semantic attachment
  questions and reusable capture mechanisms across the portable producer,
  analysis projection, and generic Simpler adapter.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T18:42:01.381Z'
---
# Research question

How should the portable form model distinguish a reusable attachment control from the semantic information a particular attachment is intended to collect?

# Evidence prompting the work

- `grants-form-spec` PR #5 correctly reused `AttachmentRef` for Project Narrative, Budget Narrative, and Other Narrative forms without adding emitter branches.
- The earlier analysis counted `generics/attachment` as a question, reported one question for each narrative form, and scored the three forms as 100% semantically similar.
- That analytical result conflicted with the intended distinction: an attachment is a content-capture mechanism, while the narrative role identifies a specific information requirement.
- The public Simpler adapter preserved runtime parity but could not resolve an analysis-model distinction that belonged in the portable source.

# Decision

The architecture uses three orthogonal facets:

1. Semantic identity records the information requirement.
2. Response role records whether a form occurrence is applicant-entered, calculated, system-supplied, technical, or static.
3. Capture mechanism records how an answer is supplied.

Portable blocks are classified as `semanticQuestion` or `captureMechanism`. A role-specific semantic attachment question extends `generics/attachment`. Its block index publishes that composition relationship, including for scalar inheritance that stock JSON Schema flattens. Response role belongs on a form occurrence and will be added when the first non-applicant role is exported.

This keeps semantic mapping decisions in reviewable declarations. Deterministic structural classification remains separate from proposed or reviewed cross-form semantic mappings. Only reviewed mappings may affect published coverage.

# Implemented outcome

- Project Narrative, Budget Narrative, and Other Narrative are distinct semantic questions.
- Existing attachment occurrences in SF-424 and R&R Budget now use role-specific semantic questions.
- `generics/attachment` remains the shared capture mechanism.
- The analysis exports semantic form-question associations and capture-mechanism associations separately, with occurrence paths and direct or transitive composition.
- Pairwise similarity uses semantic questions only. The three standalone narrative forms now have 0% semantic overlap while retaining complete attachment-mechanism reuse.
- The portable artifact contract requires question classification and machine-readable composition ancestry.
- The artifact validator rejects unknown composition targets.
- The generic Simpler adapter consumed the refreshed artifacts without new adapter or form-specific runtime logic.

# Verification and delivery

- Producer PR: https://github.com/mikec-ai/grants-form-spec/pull/10
- Simpler fork PR: https://github.com/mikec-ai/simpler-grants-gov/pull/7
- Producer preflight passed with 48 TypeScript and TypeSpec tests, 12 Python tests, 69 emitted blocks, and 349 validated JSON artifacts.
- Simpler adapter verification passed with 43 focused tests.
- Both PRs are merged to their public repositories. No upstream HHS repository was modified.

# Follow-up boundary

Add response-role vocabulary to form occurrences when a concrete calculated, system-supplied, technical, or static occurrence is introduced into the exported association table. Do not infer those roles from labels or control types.

[depends on](integrate-standalone-attachment-forms.md)
