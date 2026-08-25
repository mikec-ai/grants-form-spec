---
type: Task
title: Close PHS Inclusion Enrollment release gates
priority: P0
assignee: codex-phs-inclusion
description: >-
  Protect exact DAT-calculated targets and gather bounded generic
  consumer/browser evidence without inferring arithmetic.
superbee_progress_status: in_progress
superbee_updated_by: codex-phs-inclusion
generated:
  by: 'process:superbee'
  at: '2026-08-25T02:19:50.618Z'
---
# Goal

Close the bounded consumer and browser evidence gates for the already-banked PHS Inclusion Enrollment Report without inventing calculation semantics.

# Fixed evidence boundary

- Exact Grants.gov FID 791 v1.0 XSD, DAT, read-only PDF, XFA PDF, and NIH Forms I guide remain pinned by physical SHA-256.
- The exact DAT identifies 28 calculated row/column targets, but does not establish operands or blank-value semantics.
- Producer PR #98 may classify those exact targets as visible read-only outputs, but must compile zero calculations.
- Semantic review remains proposed and does not contribute to published reviewed coverage.

# Acceptance criteria

- Producer preflight verifies the exact 28 source targets are the exact 28 protected fields.
- The generic Simpler adapter exposes one report repeater with nested coordinate fields and no form-specific compiler, adapter, or renderer branch.
- Bounded browser evidence covers render, representative nested edit, save/reload, automated accessibility scan, and print in the private fork.
- Any unresolved dimensional-grid semantics or human accessibility judgments remain explicitly open.
- R&R Subaward Budget 10YR/30 files remain outside this lane.

[depends on](author-integrate-phs-inclusion-enrollment-report.md)
