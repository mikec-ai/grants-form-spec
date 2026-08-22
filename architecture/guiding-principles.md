---
type: Architecture Principles
title: Portable grants form guiding principles
description: >-
  Public-safe principles and review questions governing implementation of the
  portable form architecture.
tags:
  - architecture
  - public
superbee_updated_by: mikec-ai
---
# Purpose

These principles govern architecture, implementation, analysis, and review for the portable grants form specification. They operationalize the canonical architecture decision and public repository documentation. They remain governing until an explicit decision supersedes them.

# Guiding principles

## 1. The canonical source is portable and declarative

Questions, form composition, presentation, behavior, mappings, and source metadata are reviewable data. The canonical model stays independent of Simpler.Grants.gov, Python, and any single authoring language.

## 2. Build artifacts are the contract

TypeSpec is the first typed producer, not a permanent consumer dependency. TypeSpec, JSON authoring, or a future builder may produce the same versioned artifact contract. Consumers depend on emitted artifacts and conformance rules, not on a producer's AST, runtime, or repository.

## 3. Reuse is visible in the artifact graph

Shared questions and blocks retain stable identities and compose through standard references. Recursive composition is supported. Expanded per-form snapshots may be useful build outputs, but they do not establish reusable architecture by themselves.

## 4. Question identity is semantic and each occurrence is role-qualified

A reusable question has a stable meaning. Each use records the form-specific role, cardinality, repetition context, source path, mapping evidence, and review state. Similar wording, labels, or validation shapes do not prove semantic equivalence.

## 5. Prefer standards and ordinary mechanisms

Use JSON Schema for structure, constraints, and composition, and use JSON Forms-compatible presentation artifacts where practical. Extensions must address demonstrated gaps, remain generic and versioned, and avoid embedding delivery-target behavior in the canonical model.

## 6. Keep concerns separate and interfaces explicit

Schema, presentation, conditions, calculations, mappings, provenance, semantic review, and target adapters remain independently inspectable and jointly validated. A form's meaning must not be hidden inside compiler or adapter branches.

## 7. The portable kernel does not bend to a delivery target

Simpler identifiers, legacy projections, runtime rule names, and XML integration belong in a named, generic adapter. Adding another consumer should require another adapter, not a change to the canonical question model.

## 8. Modernize incrementally while preserving evidence

Migrate one abstraction or representative form at a time. Preserve parity oracles, source provenance, XML behavior, validation behavior, accessibility findings, known exceptions, and useful runtime capabilities. Runtime parity demonstrates compatibility; it does not establish source completeness, semantic acceptance, accessibility approval, or release readiness.

## 9. Prove portability with more than one consumer

At least one independent reference consumer must be able to load, resolve, validate, and traverse the artifacts without importing Simpler code or the authoring toolchain.

## 10. Derive analysis from implementation evidence

Question inventories, form-question associations, pairwise similarity, frequency counts, and reuse curves derive from canonical identities and role-qualified occurrences. Deterministic extraction remains separate from agent-proposed semantic mappings. Proposed, reviewed, accepted, and publishable states remain distinct. Only reviewed and accepted mappings contribute to published coverage metrics.

## 11. Correctness fails early

Unknown fields, dangling references, invalid paths, cycles, stale hashes, unbound occurrences, and projection gaps fail during authoring or build with actionable diagnostics. The compiler must not silently infer form semantics.

## 12. Central claims remain falsifiable

Track newly required reusable blocks, resolved and blocked behavior, target-specific surface area, parity exceptions, and source coverage as forms are added. Preserve an explicit open question when the evidence does not justify a conclusion.

# Architecture review checklist

Use these questions for plans, pull requests, and implementation reviews:

1. Does each semantic decision live in declarative, language-neutral data?
2. Is reuse visible through standard references rather than executable form-specific generator logic?
3. Are stable question identity and role-qualified occurrences both preserved?
4. Are presentation, behavior, mappings, provenance, and review state separately inspectable?
5. Could a second producer emit the same contract without changing consumers?
6. Can an independent consumer use the artifacts without Simpler or the producer runtime?
7. Are delivery-target details confined to a generic, named adapter?
8. Does the change preserve source evidence, parity checks, and known exceptions?
9. Are proposed semantic mappings excluded from accepted and published metrics?
10. Can the next form be added without a new form-specific compiler or adapter branch?

A negative answer requires a bounded, documented exception with an explicit retirement condition. It must not silently become precedent.

# Interpretation boundaries

- TypeSpec is useful but is not mandatory for every future producer.
- The completeness of an external question bank is not a dependency.
- The existing Simpler runtime can be adapted incrementally.
- Similar labels are candidates for review, not proof of reuse.
- The direction is a portable declarative semantic source, standard composition, generic adapters, incremental migration, multi-consumer proof, and analysis projected from accepted implementation evidence.

[applies](form-architecture.md)

[applies](authoring-model.md)

[applies](deferred-designs.md)
