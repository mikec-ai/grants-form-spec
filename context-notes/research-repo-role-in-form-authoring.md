---
type: Context Note
title: How the research repository informs portable form authoring
timestamp: '2026-08-22T18:55:44.000Z'
description: >-
  Current handoff, evidence boundaries, and recommended agent workflow between
  grants-question-crosswalk and grants-form-spec.
tags:
  - research
  - provenance
  - architecture
  - migration
superbee_updated_by: codex
---
# Summary

The `grants-question-crosswalk` research repository is already informing this build, but as a source-pinned evidence and migration input rather than a runtime or canonical authoring dependency. Agents should use it to avoid repeating extraction and form review while preserving the authority boundary of `grants-form-spec`.

## Current use

- Nine form evidence sidecars in `grants-form-spec` identify `https://github.com/mikec-ai/grants-question-crosswalk` as their extraction repository.
- Each sidecar pins extraction revision `dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef`, the originating proof-manifest path, and a form-specific source-set SHA-256.
- The imported evidence currently covers Key Contacts, SF-424, SF-424A, SF-424 Short, R&R Budget, R&R Subaward Budget, and the three standalone narrative attachment forms.
- The research repository supplied deterministic XSD structure, source/version identity, DAT behavior records, PDF/XFA findings, XML-plan evidence, question candidates, and portfolio overlap hypotheses used during TypeSpec authoring and parity review.
- All nine current semantic-review sidecars remain `unreviewed`; this is intentional and prevents extraction evidence or agent proposals from being mistaken for accepted semantic equivalence.

## Appropriate responsibility

Use `grants-question-crosswalk` as the evidence, extraction, reconciliation, and migration system:

1. Locate the exact form/version and its pinned XSD, DAT, PDF/XFA, instructions, and existing implementation evidence.
2. Separate deterministic source facts from agent-proposed semantic mappings and unresolved policy conflicts.
3. Reuse reviewed form findings to identify candidate question-bank blocks, behavior declarations, XML requirements, and parity fixtures.
4. Promote only the needed facts into a versioned `grants-form-spec` evidence sidecar and declarative TypeSpec form/question definitions.
5. Preserve the originating repository revision, artifact path, source-set hash, and review status so later agents can reproduce or challenge the promotion.
6. Use portfolio analysis to select high-leverage next forms, but verify semantic equivalence just in time against the forms being authored.

## Boundaries

- `grants-form-spec` remains the canonical portable authoring repository. Do not import the research repository as a production runtime dependency.
- Do not copy expanded research schemas or generated runtime snapshots and call them reusable questions. Author reviewed semantic blocks declaratively and preserve form-specific deltas.
- Similar labels, paths, validation shapes, or question-candidate IDs are not proof of semantic equivalence.
- Deterministic extraction may establish structure, type, cardinality, source identity, and provenance. Semantic reuse requires an explicit review state.
- Only reviewed mappings may contribute to published reuse, coverage, deprecation, or prefill claims.
- When research evidence and official sources conflict, record the conflict and fail closed rather than silently choosing a value.

## Immediate value

The active R&R SF-424 task should start from the existing research corpus rather than re-extracting the form. That corpus already records 139 XSD records, 145 DAT behavior records, a source-pinned XML plan, PDF/XFA behavior findings, likely reuse candidates, and unresolved source conflicts. Agents still need to reconcile those findings into the current TypeSpec question bank and generic adapter; the old generated form package is evidence, not the new source of truth.

## Improvement opportunity

The current handoff is source-pinned but mostly manual. A future research/design slice should define a generic, review-gated promotion report from `grants-question-crosswalk` into `grants-form-spec` evidence sidecars. It should compare source identities and hashes, enumerate deterministic facts, proposals, reviewed mappings, and unresolved gates, and never generate canonical semantic identities without review.

## References

- Research repository: https://github.com/mikec-ai/grants-question-crosswalk
- Canonical architecture decision: `decisions/canonical-form-architecture`
- Active R&R SF-424 task: `tasks/author-integrate-rr-sf424`
- Evidence contract: `contract/v1/evidence.schema.json`
- Current evidence sidecars: `evidence/forms/*/evidence.json`

[informs](../tasks/author-integrate-rr-sf424.md)

[supports](../decisions/canonical-form-architecture.md)

[informs](../tasks/harden-rr-budget-production.md)

[informs](../tasks/author-integrate-rr-subaward-budget.md)

[informs](../tasks/spike-crosswalk-promotion-importer.md)
