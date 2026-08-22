---
type: Task
title: Harden R&R Budget toward production readiness
priority: P0
assignee: codex-team
description: >-
  Source-grounded semantic and behavioral hardening of the existing portable R&R
  Budget form.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T18:43:38.847Z'
---
# Objective

Move the portable R&R Budget 3.0 implementation from reference parity toward production readiness.

# Review dimensions

- Exact semantic meaning of every applicant input, calculated output, system value, attachment role, and structural group.
- Source XSD, instructions, existing implementation, UI behavior, calculation graph, XML transform, validation, save/reload, print, and accessibility behavior.
- Question-bank boundaries and evidence for reuse.
- Remaining unresolved, inferred, or weakly evidenced behavior.

# Acceptance criteria

- A source-grounded semantic and behavioral review is recorded.
- High-confidence defects are fixed declaratively and covered by tests.
- Unresolved policy or source ambiguities are explicitly recorded without inventing behavior.
- Portable artifacts continue to load through the generic Simpler adapter.
- Production readiness is reported by dimension, without claiming approval or release completion.
