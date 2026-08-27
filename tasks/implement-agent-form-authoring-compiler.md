---
type: Task
title: Implement agent form authoring compiler
priority: P0
assignee: Codex
description: >-
  Create the first schema-only agent authoring vertical slice in
  grants-form-workbench. Define a strict portable-form-authoring/v1 contract
  that references exact portable question records and declares form fields,
  layout, review state, and optional behavior without application code. Add an
  AXI-compliant compile/check CLI with structured TOON, exact provenance and
  hashes, strict unknown-flag handling, and no semantic inference. Prove the
  compiler by regenerating CD-511 with canonical package parity, then run
  single-package preflight and both presentation profiles.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T14:47:13.556Z'
---
## Result

Implemented and merged the first schema-only agent authoring vertical slice in `mikec-ai/grants-form-workbench` PR #22.

- Authoring contract: `portable-form-authoring/v1`
- Result contract: `portable-form-authoring-result/v1`
- CLI: `grants-form-author check|compile`
- Merge commit: `a4dc9ee0fb08c5234f2d3619e725ce30fc4665af`
- Pull request: https://github.com/mikec-ai/grants-form-workbench/pull/22

## Exact proof

The concise CD-511 authoring definition regenerates the trusted resolved package with canonical SHA-256 `ca442c0071ac10dfe311611cfa8644b405165a20f2a357ae82306b8850736a4b`. Both `generic/v1` and `simpler-compatible/v1` capability preflight profiles report ready. No semantic mappings were promoted: all seven occurrences remain proposed.

## Verification

- Agent-tools: 30/30 tests passed.
- Targeted architecture, contracts, and catalog: 57/57 tests passed.
- Typecheck and production build passed.
- The broad local suite reached 324 passing tests; four unrelated failures were a sibling producer checkout revision mismatch and three timing/state-sensitive UI tests.
- GitHub Actions did not start a runner because of the account billing/spending limit; no CI steps executed.

## Boundary

The compiler references exact question records from canonical-hash-pinned portable packages, corroborates the form source receipt, verifies transitive question dependencies, emits manifests and artifact hashes, and refuses silent schema-reference overrides or accepted mappings without review receipts. The v1 scope is intentionally top-level question occurrences; nested/repeatable composition is the next authoring-language extension.
