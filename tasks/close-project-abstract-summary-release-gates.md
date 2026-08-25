---
type: Task
title: Close Project Abstract Summary release gates
priority: P1
assignee: codex-project-abstract-closure
description: >-
  Promote Project Abstract Summary's exact Grants.gov XML profile and gather
  bounded generic consumer/browser lifecycle evidence while preserving the
  existing implementation as oracle.
superbee_progress_status: done
superbee_updated_by: codex-project-abstract-closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T12:51:19.740Z'
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
- Consumer PR [#111](https://github.com/mikec-ai/simpler-grants-gov/pull/111) merged as `d1f657ae77f24422b07820e5bf01e795f6f520bf` from final head `2d5745bcca41dc4c574f4a7cce8318cf61085cea`. It pins producer revision `b6a584df98570c9ee1c521eda75635e010fa1555` and proves the generic adapter produces the same parsed root, namespaced version attribute, child order, field values, and optional CFDA omission as the existing implementation. The output validates against the exact official XSD.
- Fifty-seven focused portable/adapter/provenance tests passed locally after rebasing onto merged PR #93. Isort, Ruff, Bandit, and the hardened XML parser gate passed.
- Full hosted API run [#32847134194](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32847134194) passed on exact head `2d5745bcca41dc4c574f4a7cce8318cf61085cea`: readiness, formatting, lint, migrations, security, complete tests, and portable-versus-existing differential receipts were green. The API job completed in 28m44s.
- Exact bounded browser run [#32847137957](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32847137957) passed on the same head with `PORTABLE_BROWSER_FORM_IDS=project-abstract-summary`: 4/4 lifecycle checks passed, the merged report passed, and portable catalog receipt artifact `9563055459` was published (65,721,308 bytes).
- The broad PR E2E run's red signal was inspected and was unrelated baseline: two application-submission tests failed while 35 passed. Failures involved organization/individual submission inputs and attachment-upload persistence; the exact Project Abstract cohort was green.
- Project Abstract Summary remains banked and unregistered. The existing production implementation remains the runtime oracle. Semantic review remains `unreviewed` with zero accepted mappings.

# Remaining non-technical gates

- Technical portable release closure is complete. The producer and private-fork consumer are merged with exact XML/XSD, parity, API, and bounded browser evidence.
- Human semantic review, policy/content acceptance, and production registration remain separate approvals and are not implied by this technical closure.
