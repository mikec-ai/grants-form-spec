---
type: Task
title: Enable single-package agent preflight
priority: P0
assignee: Codex
description: >-
  Let an agent validate one portable package directly, without fabricating a
  cohort catalog. Preserve exact package/source receipts and semantic review
  states; report capability support for one or more consumer profiles as
  structured TOON; keep authoring separate from runtime and semantic acceptance.
  Acceptance: mutually exclusive --package/--cohort inputs, actionable exit
  codes/help, deterministic tests for ready, unsupported, invalid, and usage
  paths, and updated agent-facing documentation.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T13:35:44.260Z'
---
## Delivered

Merged [grants-form-workbench PR #19](https://github.com/mikec-ai/grants-form-workbench/pull/19) at merge commit `570ed4f5a21045e6e1340f0ad32ab98faf4fb030`.

Agents can now run `grants-form-preflight --package <package.json>` against one authored or revised form. The command preserves the cohort default, rejects ambiguous package/cohort input, checks one or more consumer profiles, keeps review-state counts unchanged, and emits structured TOON with exact repository, revision, source, artifact, and package SHA-256 receipts. Unsupported capabilities retain their exact UI or behavior location and data path.

## Verification receipts

- full repository suite: 23 test files and 322 tests passed
- agent-tools: 14/14 tests passed, covering ready, unsupported, invalid, usage, help, and version paths
- `npm run build`: passed
- `git diff --check`: passed
- implementation commit: `ad0fffb`

GitHub Actions run `33077555868` failed before execution with zero job steps and no log. No repository check ran; the complete local gate above is the merge evidence.

## Boundary

This is capability and provenance preflight, not semantic acceptance, accessibility approval, XML parity, policy approval, or human acceptance.
