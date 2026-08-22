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
  at: '2026-08-22T18:54:59.534Z'
---
# Objective

Move the portable R&R Budget 3.0 implementation from reference parity toward production readiness.

# Review dimensions

- Exact semantic meaning of every applicant input, calculated output, system value, attachment role, and structural group.
- Source XSD, instructions, existing implementation, UI behavior, calculation graph, XML transform, validation, save/reload, print, and accessibility behavior.
- Question-bank boundaries and evidence for reuse.
- Remaining unresolved, inferred, or weakly evidenced behavior.

# Agent validation findings

- The emitted UI contains nested repeating groups. The public Simpler frontend currently rejects nested `fieldList` definitions, so a schema-counting adapter test is insufficient evidence of renderability.
- Thirty of 56 DAT calculations currently execute. Eight required or read-only calculated targets are among the missing rules: budget-year direct costs, equipment total, indirect-cost total, key-person total, other-direct-cost total, other-personnel count, participant/trainee total, and cumulative total costs plus fee.
- One broad decimal profile currently covers currency, totals, months, rates, and counts. Production hardening needs source-faithful scalar profiles for money, larger totals, two- and three-digit months, indirect rates, and integer counts.
- Fifty-six non-empty DAT conditions remain unmodeled, including paired inputs, attachment dependencies, date ordering, and row-completeness behaviors.
- Evidence pins the XSD but must also pin the DAT hash `c85158ce7ddcc756d6e8a55a050e00b4a95cdfc8d9a2d91b7bd94c7f8bdb1035`.
- The current adapter tests prove bundle self-consistency, not browser rendering, XML or REST submission, save/reload, print, or accessibility behavior.

# Acceptance criteria

- A source-grounded semantic and behavioral review is recorded.
- High-confidence defects are fixed declaratively and covered by tests.
- Unresolved policy or source ambiguities are explicitly recorded without inventing behavior.
- Portable artifacts continue to load through the generic Simpler adapter.
- Production readiness is reported by dimension, without claiming approval or release completion.
