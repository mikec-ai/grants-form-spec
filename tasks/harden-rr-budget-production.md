---
type: Task
title: Harden R&R Budget toward production readiness
priority: P0
assignee: codex-team
description: >-
  Source-grounded semantic and behavioral hardening of the existing portable R&R
  Budget form.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T18:06:43.127Z'
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

# Delivered hardening

- `mikec-ai/grants-form-spec` PR 12 is merged at `f82c772fd`.
- All 56 DAT-defined calculations are now declaratively authored and emitted for R&R Budget and its R&R Subaward Budget sibling.
- Calculation order is deterministic and contiguous from 1 through 56.
- Three count-valued totals compile to a generic integer-sum rule; monetary totals remain monetary strings.
- Source-wire profiles now distinguish signed 14- and 15-digit decimals, nonnegative budget amounts and totals, month profiles, indirect rates, and bounded three- and four-digit counts.
- The exact DAT SHA-256 is pinned alongside the XSD.
- Public Simpler fork PR 8 executes the complete graph and validates key-person totals, direct costs, cumulative totals, and integer personnel counts.
- Agent semantic findings remain proposals. The evidence sidecar stays `unreviewed` until human semantic acceptance.

# Completion

This source-grounded hardening slice is complete. Producer PRs #12 and #21 and Simpler PRs #8 and
#15 subsequently completed the shared 56-calculation graph, nested rendering support, and portable
XSD-valid XML delivery for the R&R Budget family. Remaining policy, DAT-condition, lifecycle,
browser, accessibility, review, and production-registration work is tracked separately in
`tasks/close-rr-budget-family-release-gates`.

# Acceptance criteria

- A source-grounded semantic and behavioral review is recorded.
- High-confidence defects are fixed declaratively and covered by tests.
- Unresolved policy or source ambiguities are explicitly recorded without inventing behavior.
- Portable artifacts continue to load through the generic Simpler adapter.
- Production readiness is reported by dimension, without claiming approval or release completion.
