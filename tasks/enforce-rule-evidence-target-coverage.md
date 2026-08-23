---
type: Task
title: Enforce exact rule-to-evidence target coverage
description: >-
  Require every calculation and condition target to have an exact-path evidence
  disposition with explicit authority class.
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:32:40.590Z'
superbee_progress_status: todo
priority: P0
assignee: rule_evidence_agent
---
# Goal

Make exact calculation and condition evidence coverage a generic artifact invariant so future forms do not need count-only, form-specific provenance tests.

# Evidence

SF-424C initially had 24 rule targets and 24 behavior records while still omitting one calculation target, counting an applicant input instead, and citing the SGG oracle for behavior directly supported by an official PDF. Exact target-set review found what equal counts missed.

# Acceptance criteria

- Deterministically enumerate every emitted calculation and condition target from portable artifacts.
- Match each target by exact canonical occurrence path to one behavior-evidence disposition: official source-bound evidence, explicitly typed implementation-parity evidence, or an explicit unresolved record with owner/reason/removal condition.
- Reject missing targets, duplicate target dispositions, input-only paths counted as rule evidence, ambiguous path normalization, and count-only substitutions.
- Prevent implementation oracles from masquerading as authoritative source evidence; preserve them as explicitly typed differential-parity evidence.
- Keep deterministic coverage separate from semantic mapping review and do not publish proposed mappings.
- Produce actionable diagnostics that identify form, rule kind, target path, and the missing or invalid disposition.
- Exercise the invariant across SF-424C plus at least one budget family and one condition-heavy form, with negative regression fixtures.
- Add no form-specific compiler or adapter branch.

# Boundary

The gate verifies evidence coverage and authority class. It does not infer behavior, approve semantic equivalence, or require an official-source resolution where the evidence is genuinely unresolved.
