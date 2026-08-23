---
type: Task
title: Promote residual reference-form questions
priority: P1
description: >-
  Normalize eight likely semantic fields in Key Contacts, SF-424 Short, and
  SF-424A.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T17:58:29.167Z'
assignee: residual_questions_agent
---
# Objective

Classify and promote the eight likely semantic fields remaining in smaller reference forms.

# Baseline fields

- Key Contacts: `projectRole`
- SF-424 Short: `applicantWebAddress`, `projectDescription`
- SF-424A: `activityTitle`, `assistanceListingNumber`, `directChargesExplanation`,
  `indirectChargesExplanation`, `remarks`

# Acceptance criteria

- Every field has source evidence and either composes an existing canonical question or gains a
  portable canonical definition with entity/tag metadata.
- Key Contacts' free-text project role is not conflated with the R&R Key Person controlled role
  vocabulary without accepted semantic evidence.
- SF-424A per-row occurrence semantics and constraints are preserved.
- Analysis counts and occurrence paths update deterministically, and form/target tests remain green.
