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
  at: '2026-08-22T18:54:59.816Z'
---
# Objective

Harden the portable SF-424A Budget form and implement the applicant-experience improvements identified by the three upstream issues as guidance, without modifying those issues or HHS code.

# Guidance sources

- https://github.com/HHS/simpler-grants-gov/issues/11223
- https://github.com/HHS/simpler-grants-gov/issues/11239
- https://github.com/HHS/simpler-grants-gov/issues/11359

# Confirmed issue nuance

Column G rows 1 through 4 are manually entered for this delivery slice. Legacy behavior may calculate the common case while permitting override, but supplemental and change applications can require a different authorized total. Row 5 remains a vertical total for columns C through G, including the entered Column G values.

# Validated implementation findings

- Remove misleading descriptions that say Column G is always the sum of C through F or that row values are always summed horizontally.
- Preserve the existing declarative row-5 column totals, including Column G.
- Add source-grounded Section A guidance that explains the common case and the supplemental or change exception without presenting the common case as universal.
- The custom table must honor read-only state for Column G and supply accessible names for inputs.
- Table headers should use semantic header cells.
- Add save/reload, locked-state, print, XML, and navigation tests using an exception payload where C through F total 10 but G is 100.
- Improve generic multi-field help plumbing and section navigation rather than adding one-off behavior only for SF-424A.

# Scope

- Verify exact SF-424A instructions and current portable/runtime behavior before selecting functionality.
- Add clear tooltips and in-form instructions grounded in source instructions.
- Improve section and keyboard navigation within the existing renderer architecture.
- Correct misleading Section A labels in our portable declaration.
- Add focused save/reload, submission/print, calculation, validation, navigation, and accessibility-oriented tests.

# Acceptance criteria

- No HHS issue or upstream repository is modified.
- Guidance text and labels do not misrepresent Column G business rules.
- Navigation and instructional improvements are portable declarations or generic capabilities.
- Calculation behavior distinguishes rows 1 through 4 from the grand total.
- Producer preflight and focused Simpler adapter tests pass.
- Remaining approval, UAT, and policy decisions are explicit.
