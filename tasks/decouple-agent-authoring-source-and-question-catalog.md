---
type: Task
title: Decouple form source evidence from reusable question catalog
superbee_progress_status: done
priority: P0
assignee: Codex
description: >-
  Delivered in grants-form-workbench PR #24. Agent-authored forms can now
  combine independently pinned producer source evidence with a deterministic,
  self-contained catalog of 126 exact question records. CD-511 proves exact
  package parity without using its existing portable form package as an
  authoring input; legacy package-backed resolution remains compatible.
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T15:19:32.396Z'
---
# Delivery receipts

- Pull request: https://github.com/mikec-ai/grants-form-workbench/pull/24
- Merge commit: 04ca49140772609b3054b2370a16b91eb48e8b7d
- Question catalog: 126 exact records; canonical SHA-256 `2c36323cb279a8fc3ec917e259aec97b85cf0f2dcd046904f8c4d8380babf774`
- CD-511 exact compiled package SHA-256: `ca442c0071ac10dfe311611cfa8644b405165a20f2a357ae82306b8850736a4b`
- R&R Personal Data regression SHA-256: `7820b1f758c1579e0e0dc3a4625cc745a79eee73d9db940ed4bee0b6cad1584e`
- Verification: 42/42 agent-tool tests; 57/57 architecture/contract/catalog tests; typecheck, deterministic catalog check, build, and diff check passed locally.
- Hosted CI did not start because GitHub rejected the job for the account billing/spending limit; it executed zero steps.

# Architectural result

Source provenance and reusable question selection are now independent inputs joined through exact hashes. Duplicate question identifiers must have identical full records; semantic review state is preserved and similar wording is never promoted to equivalence.
