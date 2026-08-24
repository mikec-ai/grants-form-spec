---
type: Task
title: Require evidence-backed intentional parity deltas
superbee_progress_status: done
priority: P0
description: >-
  Govern every accepted portable-versus-legacy difference as narrow, reviewed,
  evidence-backed data.
actor: Codex
timestamp: '2026-08-23T22:26:31.285Z'
assignee: codex-root
superbee_updated_by: parity_delta_contract
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

# Delivered result

Producer PRs 82 through 85 established the portable ledger contract and fail-closed validator through merge `2a316a832a343f3830c4b6a8948fd746c3dd8c56`. Consumer PR 79 merged at `29fafef5c1f1032b559b519d73387475932297fd` and consumes the exact producer pin without form-specific adapter decisions. Producer PR 86 merged at `884936fe89f95757ce9435eabf73757144252709` and corrected the proof package.

The validator rejects blanket targets, missing or unstable semantic targets, undocumented differences, stale and unused entries, missing evidence, broken receipt joins, unsupported rule paths, and every accepted record until an independent decision-artifact receipt exists. Reports separate exact parity, proposed deltas, unresolved mismatches, reviewed deltas, and actual failures. The current ledger contains 50 exact targets: 16 source-verified, 34 unverified, all 50 proposed, and 0 accepted.

Consumer PR 80 merged at `eb15d0fa87b8f5ee2764e51f9bf4b8a2d8b08bf9` after the post-merge API formatter gate exposed import ordering and Black-only mechanical differences in PR 79 files. The correction contains no behavioral change; the exact full-repository isort and Black checks plus 26 focused tests, Ruff, mypy, and diff check pass locally.
