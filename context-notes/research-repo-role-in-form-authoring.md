---
type: Context Note
title: How the research repository informs portable form authoring
description: >-
  Current handoff, evidence boundaries, and agent workflow between
  grants-question-crosswalk and grants-form-spec.
tags:
  - research
  - provenance
  - architecture
  - migration
timestamp: '2026-08-23T21:29:18Z'
superbee_updated_by: codex
---
# Summary

The `grants-question-crosswalk` research repository is already informing this build, but as a source-pinned evidence and migration input rather than a runtime or canonical authoring dependency. Agents should use it to avoid repeating extraction and form review while preserving the authority boundary of `grants-form-spec`.

## Current use

- The 30-form producer contains 30 exact evidence sidecars; 29 identify `https://github.com/mikec-ai/grants-question-crosswalk` as an extraction or reconciliation source.
- Each sidecar pins its own extraction revision, originating artifact or manifest, exact official-source identities and hashes, and a form-specific source-set digest where available.
- The imported evidence now spans the application, identity, budget, subaward, attachment, policy/attestation, assurance, and construction-budget foundations.
- The research repository supplied deterministic XSD structure, source/version identity, DAT behavior records, PDF/XFA findings, XML-plan evidence, question candidates, and portfolio overlap hypotheses used during TypeSpec authoring and parity review.
- Semantic mappings remain proposed or unreviewed unless an explicit reviewer and publishing authority accepts them; this prevents extraction evidence or agent proposals from becoming published equivalence claims.

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

Every new form should start from the existing research corpus rather than re-extracting sources unnecessarily. Agents must still reconcile those findings into the current declarative question bank and target profiles; generated research packages remain evidence, not the portable source of truth.

## Current promotion path

The review-gated crosswalk promotion importer is implemented. It compares source identity and hashes, preserves deterministic facts, proposals, review state, and unresolved gates, and never creates accepted canonical semantic identities automatically. The research repository remains an optional authoring input rather than a runtime dependency.

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

[informs](../tasks/migrate-sflll-parity-oracle.md)

[informs](../tasks/author-integrate-phs-human-subjects.md)

[informs](../tasks/migrate-attachment-form-parity-oracle.md)

[informs](../tasks/author-integrate-phs-inclusion-enrollment-report.md)

[informs](../tasks/migrate-sf424b-parity-oracle.md)

[informs](../tasks/author-integrate-phs398-research-plan.md)

[informs](../tasks/migrate-gg-lobbying-parity-oracle.md)

[informs](../tasks/author-integrate-phs-assignment-request.md)

[informs](../tasks/migrate-sf424c-parity-oracle.md)

[informs](../tasks/author-integrate-phs398-cover-page-supplement.md)
