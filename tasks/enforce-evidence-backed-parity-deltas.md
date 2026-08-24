---
type: Task
title: Require evidence-backed intentional parity deltas
superbee_progress_status: in_progress
priority: P0
description: >-
  Govern every accepted portable-versus-legacy difference as narrow, reviewed,
  evidence-backed data.
actor: Codex
timestamp: '2026-08-23T22:26:31.285Z'
assignee: codex-root
superbee_updated_by: codex-root
---
# Goal

Create a machine-readable, evidence-backed ledger and enforcement gate for intentional differences between portable forms and SGG legacy implementations.

# Required record

Each delta must identify:

- the form, semantic target, and compared behavior;
- classification such as legacy bug fix, authoritative-source correction, or approved intentional incompatibility;
- supporting official evidence or explicit product/engineering decision;
- review state and accountable reviewer;
- the differential fixture or assertion that exercises the difference.

# Acceptance criteria

- Differential tests fail on undocumented differences.
- Blanket form-level allowlists are rejected; exceptions are narrow and semantic.
- Missing evidence, missing review, stale targets, and unused delta entries fail validation.
- The ledger is portable domain evidence, not adapter control flow.
- Reports distinguish accepted deltas from unresolved mismatches.

[depends on](add-source-evidence-sidecars.md)

[depends on](enforce-rule-evidence-target-coverage.md)

[depends on](design-parity-delta-ledger-contract.md)

[depends on](audit-seven-form-parity-deltas.md)
