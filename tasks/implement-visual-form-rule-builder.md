---
type: Task
title: Add visual conditions and validation rule authoring
priority: P0
description: >-
  Extend the shared authoring workspace and composer with a bounded,
  evidence-aware rule builder. Humans and agents must produce the same neutral
  behavior declarations; GUI state and renderer-specific rules remain outside
  the canonical draft.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T20:29:55.684Z'
assignee: Codex
---
# Acceptance criteria

- [x] Author conditions by choosing a trigger question, supported operator, value, target question, and effect.
- [x] Support the existing portable visible, enabled, and required effects before calculations.
- [x] Display agent rationale and exact evidence separately from the canonical rule declaration.
- [x] Preview rules through the existing generic behavior runtime.
- [x] Keep every rule proposed until review and preserve exact evidence receipts.
- [x] Add framework-neutral command tests, architecture-boundary tests, and composer interaction tests.

# Delivery receipts

- Merged workbench PR: https://github.com/mikec-ai/grants-form-workbench/pull/38
- Merge commit: `b22d7752cabe2b5b32e23c33cb9df79da8d9e079`
- Focused validation: 32 authoring-workspace, architecture-boundary, and portal interaction tests passed.
- Broader validation: 360 non-agent-tool tests passed; the deterministic producer reimport passed when supplied the pinned local producer checkout.
- TypeScript workspace typecheck passed.
- Production build passed for the demo portal and every reusable package.
- Browser interaction test proved an agent-proposed visibility rule and a human-authored required rule compile through the same draft and execute in the generic runtime.

# Boundary receipts

- `@grants-form-workbench/authoring-workspace` remains framework-neutral and imports only contracts.
- Agent rationale stays in `portable-form-agent-proposal/v1`; exact rule evidence is content-addressed separately from the canonical proposed rule.
- Rules compile to `form-behaviors/v1`; no renderer-specific behavior is stored in the draft.
- Removing a selected question also removes dependent proposed rules and evidence receipts.
- Calculations, compound predicates, and rule acceptance/reviewer authority remain explicitly deferred.

# Environmental notes

- GitHub created no checks because of the known account Actions/billing constraint; mergeability was clean and local validation was green.
- The in-app browser blocked direct access to the new localhost port. The equivalent end-to-end component interaction passed; no alternate browser automation was substituted.
- The separate agent-tools suite currently has pre-existing checked-in fixture/hash drift. This PR changes no agent-tools files.

[depends on](implement-human-agent-form-composer.md)
