---
type: Task
title: Research attachment semantics versus capture mechanisms
priority: P1
assignee: mikec-ai
description: >-
  Explore and recommend how the portable architecture should distinguish
  reusable attachment controls from the semantic information requested by
  role-specific narrative attachments, and how analysis outputs should treat
  each.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T18:02:29.711Z'
---
# Research question

How should the portable form model distinguish a reusable attachment control from the semantic information a particular attachment is intended to collect?

# Evidence prompting the work

- `grants-form-spec` PR #5 correctly reuses `AttachmentRef` for Project Narrative, Budget Narrative, and Other Narrative forms without adding emitter branches.
- The current analysis counts `generics/attachment` as a question, reports one question for each narrative form, and scores the three forms as 100% semantically similar.
- That analytical result conflicts with the intended distinction: an attachment is a content-capture mechanism, while the narrative role identifies different information requirements.
- The public Simpler adapter PR #5 preserves runtime parity but does not resolve this analysis-model distinction.

# Exploration scope

- Define whether classification belongs on the reusable block, the form occurrence, or both.
- Evaluate a minimal vocabulary covering semantic question, content-capture mechanism, calculated output, technical field, and static content.
- Determine how a role-specific attachment occurrence records the content requested without incorrectly creating or collapsing semantic questions.
- Specify how inventory, form-question association, pairwise similarity, coverage, deprecation analysis, and prefill analysis should treat each classification.
- Check compatibility with TypeSpec authoring, emitted artifacts, evidence sidecars, CommonGrants mappings, and the generic Simpler adapter.
- Identify migration implications for existing SF-424 and R&R Budget attachment occurrences.

# Acceptance criteria

- A short design recommendation compares at least two viable modeling options and identifies the preferred boundary.
- The recommended model preserves reusable attachment runtime machinery and distinct narrative roles.
- Semantic similarity no longer treats the three narrative forms as 100% equivalent merely because each accepts attachments.
- Capture mechanisms remain available in machine-readable field/form exports without being counted as applicant questions.
- Reviewed semantic mappings remain separate from deterministic structural classification, and only reviewed mappings can affect published coverage.
- Follow-up implementation and migration tasks are identified, but this task does not silently choose or implement a model before the design is reviewed.

# References

- https://github.com/mikec-ai/grants-form-spec/pull/5
- https://github.com/mikec-ai/simpler-grants-gov/pull/5

[depends on](integrate-standalone-attachment-forms.md)
