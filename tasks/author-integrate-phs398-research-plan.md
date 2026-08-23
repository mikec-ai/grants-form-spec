---
type: Task
title: Author and integrate PHS 398 Research Plan
priority: P1
description: >-
  Compose thirteen source-bound research attachment roles from the portable
  Attachment Form foundation.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T23:04:22.525Z'
assignee: research_plan_agent
---
# Goal

Author PHS 398 Research Plan as a declarative composition of typed attachment roles built on the portable Attachment Form foundation.

# Evidence starting point

- The research factory records 80 source question/structure records and thirteen behavior records.
- The runtime package models thirteen working attachment roles and one condition.
- Two-year usage evidence records 213,859 form instances.

# Acceptance criteria

- Pin and promote exact official XSD, DAT, PDF/XFA, instructions, versions, and hashes.
- Reuse one attachment primitive while preserving thirteen role-specific semantic identities, labels, applicability, instructions, cardinality, ordering, and XML paths.
- Model the source-backed conditional behavior declaratively.
- Do not collapse inline narrative concepts and uploaded document roles into one question identity.
- Validate minimal, conditionally applicable, and fully populated attachment sets, including XML/XSD, save/reload, locked/print, submission, and accessibility.
- Add no form-specific compiler or adapter branch.
- Record marginal effort and the exact reusable attachment artifacts consumed.

# Scope boundary

The Attachment Form runtime mechanism is reusable; each Research Plan attachment role remains independently reviewable policy content.

[builds on producer output from](migrate-attachment-form-parity-oracle.md)

# Implementation receipt

Draft producer PR [#60](https://github.com/mikec-ai/grants-form-spec/pull/60) at commit `6ec72f8a4` implements the source-conformance slice and remains unmerged for independent review.

- Authored thirteen role-qualified, draft semantic questions over the one shared `generics/attachment` capture mechanism.
- Composed PHS 398 Research Plan FID 797 v5.0 with exact source order, identity, labels, sections, required Research Strategy, and ten-file applicant Appendix limit.
- Pinned the official XSD, DAT, read-only PDF, XFA PDF, NIH Forms I instructions, and full transitive XSD closure with exact versions and hashes. No OCR was used.
- Preserved the XSD prefix/target-namespace defect, the Specific Aims requiredness conflict, and the Appendix 10-applicant-versus-100-XSD boundary explicitly.
- Preserved Introduction, renewal-publication-list, and vertebrate-animal requirements as structured `source-bound-unresolved-cross-form` evidence. The producer emits no fake local paths or unsupported rules.
- Added one generic XML operation for flattening a shared attachment payload into an already-declared collection item. No form-specific compiler, adapter, renderer, or conformance branch was added.
- Generated analysis reports thirteen semantic questions and one capture mechanism; all semantic associations remain proposed and unpublished.

# Verification

`npm run preflight` passes: 104 TypeSpec/Vitest tests, 197 Python tests with one existing skip, 202 blocks and 1,116 artifacts validated, plus promotion, provenance, packaging, exact-XSD, analysis, and zero-unclassified gates.

# Independent review response

The first independent review found that `flatten: true` attachment nodes could declare properties the reference runtime silently ignored. Commit `6ec72f8a4` resolves that merge blocker generically:

- The JSON contract permits a flattened attachment only as an array `items.node` with a declared `itemElement`.
- Its exact declarative shape is only `{ "kind": "attachment", "flatten": true }`; element, namespace, attributes, source, container, and other ignored declarations are rejected.
- The reference runtime independently enforces exact keys and legal array-item context, including misspelled properties.
- Negative contract and runtime tests mutate element, namespace, attributes, source, `flatten` spelling, top-level placement, and missing `itemElement`.
- The positive Research Plan XML/XSD projection remains green.

# Remaining review and consumer gates

- Independent architecture, source, and semantic review of PR #60.
- Human acceptance before any mapping contributes to published coverage.
- An application-level condition contract and consumer support for the three cross-form requirements.
- NOFO-aware policy composition for Specific Aims requiredness.
- Consumer validation of save/reload, locked/print views, attachment ownership and audit behavior, submission, accessibility, registration, and release approval.
- No legacy Simpler implementation exists, so this slice proves official-source conformance rather than runtime parity.
