---
type: Task
title: Author and integrate R&R SF-424
priority: P0
assignee: codex-team
description: >-
  Production-oriented declarative implementation and generic Simpler integration
  for R&R SF-424.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T18:43:38.981Z'
---
# Objective

Author and integrate the R&R SF-424 form as a production-oriented portable form, using shared questions only where source evidence supports the same semantic identity.

# Review dimensions

- Exact form/version identity and authoritative XSD, instruction, PDF, and existing implementation sources.
- Applicant questions, calculated or supplied values, conditions, attachments, repeating groups, validation, XML mappings, save/reload, print, and accessibility behavior.
- Reuse with SF-424, R&R Budget, and existing question-bank blocks.

# Acceptance criteria

- The form is declaratively authored without a form-specific compiler or adapter branch.
- Semantic review distinguishes shared meaning from merely similar labels.
- Source and version provenance accompanies emitted evidence.
- The generic Simpler adapter loads the form and focused parity/behavior tests pass.
- Remaining human review, policy, accessibility, and release work is explicit.
