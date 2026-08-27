---
type: Task
title: Extend agent authoring for nested and repeatable composition
superbee_progress_status: done
priority: P0
assignee: Codex
description: >-
  Extend portable-form-authoring/v1 in grants-form-workbench with strict generic
  object and array containers, nested UI scope shorthand, and repeatable
  question occurrences without renderer or form-ID branches. Preserve exact
  question/source receipts and semantic-review boundaries. Prove the extension
  by regenerating the structurally rich R&R Personal Data package with canonical
  parity and both consumer profiles green.
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T15:00:43.727Z'
---
## Result

Implemented and merged nested and repeatable schema-only authoring in `mikec-ai/grants-form-workbench` PR #23.

- Pull request: https://github.com/mikec-ai/grants-form-workbench/pull/23
- Merge commit: `2d2199f8b1ed6fa2ffb5f4e5ed5aa07ddf04a450`
- Contract remains backward-compatible `portable-form-authoring/v1`.

## Architecture

Authoring definitions can now declare generic object and array containers. Wildcard JSON Pointer segments represent array items, so `/people/*/name` compiles deterministically into an array of objects with a source-pinned reusable question at `name`. The compiler requires explicit parent containers, prevents authored overrides of `type`, `properties`, `items`, and question `$ref`, enforces `many` cardinality on wildcard paths, and validates nested UI paths through exact pinned question schemas.

No renderer branches, producer imports, form-ID conditions, inferred semantic equivalence, or semantic-review promotion were added.

## Exact proof

- CD-511 remains canonically identical: `ca442c0071ac10dfe311611cfa8644b405165a20f2a357ae82306b8850736a4b`.
- R&R Personal Data—including repeatable co-project-directors and deeply nested person fields—is canonically identical: `7820b1f758c1579e0e0dc3a4625cc745a79eee73d9db940ed4bee0b6cad1584e`.
- Both packages pass `generic/v1` and `simpler-compatible/v1` preflight.

## Verification

- Agent-tools: 36/36 tests passed.
- Targeted architecture, contracts, and catalog: 57/57 tests passed.
- Typecheck and production build passed.
- GitHub Actions executed zero steps because of the account billing/spending limit; this was infrastructure-only.
