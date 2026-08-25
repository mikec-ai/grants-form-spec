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
  at: '2026-08-25T07:54:35.070Z'
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
