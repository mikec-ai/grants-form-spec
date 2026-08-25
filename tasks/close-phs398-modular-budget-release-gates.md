---
type: Task
title: Close PHS 398 Modular Budget release gates
priority: P1
assignee: human-review
description: >-
  Technical gates are merged in producer PR 31 (7585c622) and consumer PR 29
  (5ba62bca). Exact-XSD XML, shared-container merging, eight calculations,
  modular choices, date validation, attachment mappings, and automated canaries
  pass; human semantic, visual/accessibility, instruction, and registration
  gates remain.
superbee_progress_status: blocked
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-25T01:31:29.079Z'
---
[depends on](harvest-phs398-modular-budget.md)

## Visible calculated outputs and browser closure — 2026-08-24

- Source review confirmed that all eight PHS 398 Modular Budget calculations already executed and
  were schema-read-only, but the generated UI suppressed every calculated output with `type: null`.
  This was a producer declaration gap, not a Simpler runtime defect.
- [grants-form-spec PR 97](https://github.com/mikec-ai/grants-form-spec/pull/97), merged at
  `4d3d969a398e1d6a19095bf5ec00eaa66a36a830`, adds form-scoped declarative visible-read-only
  overrides for the three period totals and five cumulative totals. No shared runtime or R&R code
  changed. Producer preflight passed 124 TypeScript tests, 346 Python tests with ten skips, all 30
  pinned XSD fixtures, 1,536 artifact validations, and zero unclassified fields.
- [simpler-grants-gov PR 99](https://github.com/mikec-ai/simpler-grants-gov/pull/99), merged at
  `209f31182a32639a3669061b6948745187cac62c`, consumes that immutable producer revision. The final
  consumer diff contains only the artifact manifest, generated PHS schema/UI, PHS/browser-plan tests,
  and one generic test-harness guard excluding file uploads from editable scalar fallback. It adds no
  form-specific runtime, adapter, registration, R&R, or subaward branch.
- During parallel integration, merged consumer PR 98 supplied a more general nested-repeater harness.
  PR 99 rebased onto and reused that implementation, deleting its independently developed duplicate
  repeater helper. This is direct evidence that parallel form work can converge on shared machinery
  rather than accumulate per-form code.
- Local consumer validation passed 42 focused API tests, Ruff, Black, isort, nine matrix-contract Jest
  tests, and targeted ESLint. Exact rebased-head browser run
  [32797218557](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32797218557) completed its
  PHS 398 Modular Budget E2E job successfully at
  `489a0fb0036a9c7e6011c17af16bb141578fa8c2`; final report packaging was still completing at merge.
  The prior exact-head run passed Chrome, Firefox, WebKit, and mobile Chrome with registration,
  adapter preflight, render, save/reload, automated accessibility, and print probes green; the
  rebased run was required because shared nested-repeater code changed underneath that first receipt.
- These are fork-level automated technical receipts. Human semantic, visual/accessibility,
  instruction, policy, privacy/security, operational, registration, and release approvals remain
  open, so the task remains blocked on human review rather than marked complete.
