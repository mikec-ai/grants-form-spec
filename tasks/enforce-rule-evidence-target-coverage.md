---
type: Task
title: Enforce exact rule-to-evidence target coverage
description: >-
  Require every calculation and condition target to have an exact-path evidence
  disposition with explicit authority class.
superbee_updated_by: rule_evidence_agent
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:50:06.592Z'
superbee_progress_status: in_progress
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

# Delivery receipt

- Draft implementation: [grants-form-spec PR #57](https://github.com/mikec-ai/grants-form-spec/pull/57)
- Head commit: `d7236c23c84cc144b1ffb8db0dbc7137c8983cdc`
- Full local preflight passed after review fixes: 102 TypeSpec tests, 158 Python tests with one skip, 1,010 artifact validations, artifact packaging verification, and zero unclassified occurrences or exceptions.
- Coverage proof: SF-424C has 24 official-source calculation dispositions; the R&R Budget family inherits 56 exact calculation dispositions (20 official, 36 unresolved); R&R Other Project Information has 13 exact unresolved condition dispositions.
- Negative regressions cover missing and duplicate dispositions, input-only/count substitution, ambiguous array normalization, and implementation evidence misclassified as official authority.
- Independent review response: duplicate emitted target identities now fail before map construction; calculation detection accepts only explicit `fields` or `amount` + `percentage` operand shapes, and unknown or mixed prepopulation shapes fail closed. Three negative regressions cover these cases.
- GitHub CI is rerunning for the review-fix head. Status remains in progress until independent re-review completes; the PR is intentionally unmerged.
