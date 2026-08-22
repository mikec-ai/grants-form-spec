---
type: Task
title: 'Harden SF-424A instructions, navigation, and budget behavior'
priority: P0
assignee: codex-team
description: >-
  Implement source-grounded SF-424A improvements in our portable producer and
  public Simpler fork, using upstream issues only as read-only guidance.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T18:43:39.134Z'
---
# Objective

Harden the portable SF-424A Budget form and implement the applicant-experience improvements identified by the three upstream issues as guidance, without modifying those issues or HHS code.

# Guidance sources

- https://github.com/HHS/simpler-grants-gov/issues/11223
- https://github.com/HHS/simpler-grants-gov/issues/11239
- https://github.com/HHS/simpler-grants-gov/issues/11359

# Confirmed issue nuance

Column G rows 1 through 4 are not a simple sum in every business case. Legacy behavior can auto-populate a common-case sum while permitting override, but the current HHS implementation intentionally uses manual entry until richer client-side behavior exists. Issue 11359 requests removal of misleading summation descriptions without functional changes. Issue 11239 describes future end-to-end coverage for row and grand totals.

# Scope

- Verify exact SF-424A instructions and current portable/runtime behavior before selecting functionality.
- Add clear tooltips and in-form instructions grounded in source instructions.
- Improve section and keyboard navigation within the existing renderer architecture.
- Correct misleading Section A labels in our portable declaration.
- Decide and test calculated, manually entered, or calculated-but-overridable behavior based on authoritative source evidence and explicit product semantics.
- Add focused save/reload, submission/print, calculation, validation, navigation, and accessibility-oriented tests.

# Acceptance criteria

- No HHS issue or upstream repository is modified.
- Guidance text and labels do not misrepresent Column G business rules.
- Navigation and instructional improvements are portable declarations or generic capabilities.
- Calculation behavior is evidence-backed and distinguishes rows 1 through 4 from the grand total.
- Producer preflight and focused Simpler adapter tests pass.
- Remaining approval, UAT, and policy decisions are explicit.
