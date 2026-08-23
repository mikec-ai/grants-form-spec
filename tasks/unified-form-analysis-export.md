---
type: Task
title: Emit reviewed form-analysis and marginal-reuse datasets
priority: P0
assignee: codex
description: >-
  Create the spreadsheet-ready analytical read model for question mappings,
  similarity, provenance, and marginal capability reuse.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T15:54:25.050Z'
---
# Objective

Produce one machine-readable analytical projection from emitted form artifacts that supports Billy's question inventory, form-to-question association, pairwise similarity, and the marginal-capability reuse curve without treating unreviewed semantic proposals as published coverage.

# Scope

- Join form occurrences to canonical question metadata, occurrence constraints, review state, source provenance, and Grants.gov XML/XSD metadata where available.
- Emit explicit reviewed and exploratory projections so unreviewed mappings cannot inflate published metrics.
- Measure reused versus newly introduced semantic questions, capture mechanisms, and portable behaviors by a versioned form sequence.
- Keep deterministic facts separate from semantic acceptance and read only the emitted artifact graph plus portable evidence/target sidecars.
- Provide stable JSON and CSV outputs suitable for a spreadsheet, with deterministic ordering.

# Acceptance criteria

- The exporter produces question inventory, form-question associations, pairwise similarity, and marginal capability rows for every emitted form.
- Each association preserves stable IDs and paths plus available XML/XSD provenance and clearly marks unavailable fields.
- Published metrics include only reviewed mappings; exploratory metrics are unmistakably labeled and separately reported.
- Calculated outputs, technical fields, static content, attestations, and capture mechanisms are not silently counted as applicant questions.
- Tests cover review gating, directional similarity, provenance joining, classifications, and marginal reuse.
- Repository preflight and test suites pass, and documentation explains the spreadsheet contract and remaining evidence gaps.

# Boundaries

Do not infer semantic equivalence from wording or shape, do not mutate accepted mappings, and do not add form-specific compiler or adapter branches.
