---
type: Task
title: Make portable-form CI bounded and attributable
priority: P0
assignee: codex-root
description: >-
  Stop narrow portable-form PRs from repeatedly waiting on unrelated broad
  regressions while preserving exact form evidence and full post-merge safety.
superbee_progress_status: in_progress
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-25T13:20:04.180Z'
---
# Goal

Make CI scale with the risk and changed surface of a portable-form PR. Exact affected-form receipts should decide form-change readiness; unrelated legacy failures must remain visible without repeatedly blocking narrow work.

# Acceptance criteria

- Shared change classification selects exact portable forms and affected shared runtime capabilities.
- Required PR checks run focused compile, XML/XSD, unit, and bounded browser evidence for the selected surface.
- Full API and broad E2E remain required for shared executable/runtime/workflow changes, and run post-merge or scheduled for isolated form evidence changes.
- Known SF-424A and attachment baselines are explicitly tracked rather than silently ignored.
- Classification fails closed when the change cannot be proven isolated.
- Workflow and classifier behavior have deterministic tests.
- Exact hosted receipts demonstrate both the fast isolated path and the full-risk path.

[depends on](encode-tiered-portable-form-ci.md)
