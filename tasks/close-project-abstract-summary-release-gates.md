---
type: Task
title: Close Project Abstract Summary release gates
priority: P1
assignee: codex-project-abstract-closure
description: >-
  Promote Project Abstract Summary's exact Grants.gov XML profile and gather
  bounded generic consumer/browser lifecycle evidence while preserving the
  existing implementation as oracle.
superbee_progress_status: in_progress
superbee_updated_by: codex-project-abstract-closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T08:29:08.799Z'
---
# Scope

Close the technical release gates for Project Abstract Summary FID 591 v2.0 through the portable producer and generic Simpler adapter. Preserve the current Simpler form as the parity oracle until the portable path proves schema, UI, rule, XML, and bounded browser lifecycle parity.

# Fixed boundaries

- Pin exact official XSD bytes, URI, version, hash, and deterministic extraction provenance.
- Do not infer or publish semantic equivalence; semantic review remains unreviewed.
- Add no form-specific compiler or adapter branches.
- Keep policy and human acceptance gates separate from technical closure.
- Do not touch narrative PR #103, PR #93 isolation files, or R&R Subaward variants.

# Acceptance criteria

- Portable Grants.gov XML profile renders exact root, namespace, version, field names, optionality, sequence, and values and validates against pinned XSD fixtures.
- Simpler consumes the emitted XML target through the generic adapter with differential parity against the existing implementation.
- Bounded browser evidence covers render, required validation, valid save/reload, print, and basic accessibility checks.
- Record exact PRs, commits, CI/browser run receipts, and remaining human-only gates.

# Progress receipts

- Producer PR [#105](https://github.com/mikec-ai/grants-form-spec/pull/105) merged as `b6a584df98570c9ee1c521eda75635e010fa1555`. It authors the Project Abstract Summary 2.0 XML profile without a compiler branch. Full producer preflight passed: 366 Python tests, 125 TypeSpec tests, exact-XSD fixture gate 34 profiles/34 fixtures, zero unclassified fields.
- The pinned official `Project_AbstractSummary_2_0-V2.0.xsd` is byte-identical to the existing Simpler oracle fixture at SHA-256 `3022f177a7f0ebb9a1888e9b8a4a644ed2ba7857a775d2d05642a9fbd1cc008f`.
- Consumer PR [#111](https://github.com/mikec-ai/simpler-grants-gov/pull/111), current head `108a6dd4759d2f939bc8bbed58528e325735ca80`, pins the merged producer revision and proves the generic adapter produces the same parsed root, namespaced version attribute, child order, field values, and optional CFDA omission as the existing implementation. The output validates against the exact official XSD.
- Fifty-seven bounded portable/adapter tests passed locally. A broader portable cohort produced 385 passes; four database-dependent tests were unavailable because the local `grants-db` service was not running. The only initial failure was the expected producer bundle revision pin, which this PR updates.
- Project Abstract Summary remains banked and unregistered. The existing production implementation remains the runtime oracle. Semantic review remains `unreviewed` with zero accepted mappings.

# Open gates and dependency

- Do not merge consumer PR #111 until its hosted checks are green and the active PR #93 test-isolation/scanner work is either merged and rebased or explicitly shown not to affect the bounded browser run.
- After that dependency resolves, run the exact one-form portable browser cohort for `project-abstract-summary` across render, required validation, valid save/reload, print, and bounded accessibility checks. Record exact workflow/run/artifact receipts before closing this task.
- Human semantic review, policy/content acceptance, and production registration remain separate approvals and are not implied by technical closure.
