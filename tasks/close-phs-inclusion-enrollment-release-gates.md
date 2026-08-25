---
type: Task
title: Close PHS Inclusion Enrollment release gates
priority: P0
assignee: codex-phs-inclusion
description: >-
  Protect exact DAT-calculated targets and gather bounded generic
  consumer/browser evidence without inferring arithmetic.
superbee_progress_status: done
superbee_updated_by: codex-phs-inclusion
generated:
  by: 'process:superbee'
  at: '2026-08-25T05:04:14.202Z'
---
# Goal

Close the bounded consumer and browser evidence gates for the already-banked PHS Inclusion Enrollment Report without inventing calculation semantics.

# Fixed evidence boundary

- Exact Grants.gov FID 791 v1.0 XSD, DAT, read-only PDF, XFA PDF, and NIH Forms I guide remain pinned by physical SHA-256.
- The exact DAT identifies 28 calculated row/column targets, but does not establish operands or blank-value semantics.
- Those exact targets are visible read-only outputs; the producer compiles zero calculations.
- Semantic review remains proposed and does not contribute to published reviewed coverage.

# Completed technical closure

- Producer PR [#98](https://github.com/mikec-ai/grants-form-spec/pull/98), merge `b5853f403e00074f0b23d138e9c989985c2f8b08`, promoted the exact 28 DAT targets as protected outputs without inventing arithmetic.
- Producer PR [#100](https://github.com/mikec-ai/grants-form-spec/pull/100), merge `c484de1862b44bc93bebf2af1af51bedd4a22a6c`, added generic array-item presentation overrides. Full producer preflight passed: 125 TypeScript tests, 346 Python tests with 10 skips, 30 XSD checks, 1,536 artifacts, and zero unclassified records.
- Consumer PR [#102](https://github.com/mikec-ai/simpler-grants-gov/pull/102), merge `d02fdee6e1f2d2346352e18b3b6f9cb4b82a7f45`, added the generic browser plan and FieldList label/protection behavior. It contains no form-specific compiler, adapter, or renderer branch.
- The consumer exposes one report repeater, 94 editable controls, and 28 visible read-only targets. The 28 targets are excluded from edit/persistence probes and no calculation is compiled.

# Browser and test receipts

- Exact bounded run [#32807068440](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32807068440) passed in Chrome, Firefox, WebKit, and Mobile Chrome. Every browser passed preview registration, adapter preflight, Apply render, initial save/reload, automated accessibility, and print; `validationWarningCount=0`, `accessibility.violations=0`, and print had zero interactive controls.
- The exact run was produced on pre-final-rebase head `b7855efddb72bf538994bb3e3cd16c13e6cba31e`. A three-commit `git range-diff` against merged head `6e328b09573769e6f50622bfab5114173950a31b` was patch-identical. The intervening base changes touched only the manifest, Fellowship question-bank artifacts, and the promoted-form count test, so the exact runtime/form-content evidence remained applicable.
- Post-final-rebase focused API evidence passed 39 tests across the browser plan, Inclusion portable contract, and promotion integrity/count suites. Focused frontend evidence passed 64 tests with one skip; targeted ESLint, full TypeScript checking, formatting, and diff checks passed.
- Full API on the preceding patch-identical head passed 4,730 tests and exposed one stale baseline assertion (`39` forms versus the newly promoted `40`). Baseline repair PR [#107](https://github.com/mikec-ai/simpler-grants-gov/pull/107), merge `0e0c898376a3921a1bc9ca8d4992bce765d8d74b`, updated only that assertion; its focused suite passed 11 tests.
- Broad Apply smoke failures were confirmed as pre-existing: merged-base run `32800919858`, job `97661761791`, and final-head run `32807058708`, job `97679443883`, both reported the same legacy attachment/SF-424/SF-424A failure cohort, including the `Total, row 1` locator. No Inclusion production code was changed for that baseline red signal.

# Explicitly open

- The source evidence does not establish formulas, operands, rounding, or blank-value semantics for the 28 calculated targets; those behaviors remain unclosed.
- Human accessibility, policy, and acceptance review remain required. The automated evidence is not a production approval.
- R&R Subaward Budget 10YR/30 files remained outside this lane.

[depends on](author-integrate-phs-inclusion-enrollment-report.md)
