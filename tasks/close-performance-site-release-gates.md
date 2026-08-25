---
type: Task
title: Close Project/Performance Site release gates
priority: P1
assignee: root_form_lane_status
description: >-
  Technical gates are merged in producer PR 31 (7585c622) and consumer PR 29
  (5ba62bca). Exact-XSD XML, conditional/repeating behavior, site limits,
  overflow activation, validation overlays, and automated canaries pass; human
  semantic, visual/accessibility, instruction, and registration gates remain.
superbee_progress_status: in_progress
superbee_updated_by: root_form_lane_status
generated:
  by: 'process:superbee'
  at: '2026-08-25T19:39:49.612Z'
---
[depends on](harvest-performance-site.md)

## Source-behavior reconciliation checkpoint — 2026-08-25

- The five emitted country/overflow condition targets were reconciled against the exact F723 DAT source (`source-1-c0747c333fb8`, SHA-256 `c0747c333fb89f0be2403e1b4b2beb6ab971391fd85c6aa0cf0a678519e26615`).
- The overflow attachment rule at DAT path `3-3` is exact and compiled: it becomes enabled at the 299-site maximum.
- Four country-dependent source rules at `1-07`, `1-08`, `2-08`, and `2-08a` remain source-bound and uncompiled as complete parity claims. The current UI executes corresponding interactions, but State requiredness is absent and Province uses read-only where the source says inactive. Those current interactions are separately recorded as compiled with unresolved authority; none counts as accepted semantic equivalence.
- Semantic review remains `unreviewed` with zero accepted mappings. Registration and all human semantic, instruction, visual/accessibility, policy, and release decisions remain open.
- Producer branch: `codex/performance-site-evidence-closure` from producer main `90d30ce208f77c184b7a67cc40564b701303aed7`.
- Focused evidence projection and seven Performance Site/rule-evidence tests passed. Full producer preflight passed: 125 TypeScript tests, 393 Python tests with 10 skips, 8 XML projection tests, 36 exact-XSD fixtures, 1,721 artifact validations, zero unclassified fields, and zero exceptions.

## Technical evidence closure — 2026-08-25

- Producer PR [#115](https://github.com/mikec-ai/grants-form-spec/pull/115) merged as `2d8380cdbf3de146aa1f7615ec3f128e2df1228f`.
- The final reviewed head was `0e94779e8875bf2d02b7296981375e882f09c518`. Its regression pins exact conditional equality for all four emitted paths: primary State, primary Province, repeating State, and repeating Province, including root/item country references, the exact USA value, and the current enabled/disabled or read-only/enabled interactions.
- Focused validation passed seven tests with one skip. Full producer preflight passed 125 TypeScript tests, 393 Python tests with 10 skips, 8 XML projection tests, 36 exact-XSD fixtures, 1,721 artifact validations, zero unclassified fields, and zero exceptions.
- The initial hosted checks were green before the test-only assertion strengthening. The final test-only delta received an independent clean review and the full producer preflight remained green; it changed no evidence or emitted form output.
- Automated source/evidence reconciliation is closed. The four country-dependent rules remain explicitly unresolved rather than semantically accepted. Human semantic review, instruction and policy acceptance, visual/accessibility review, registration, and release acceptance remain open.
