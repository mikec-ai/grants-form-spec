---
type: Task
title: Prove R&R Key Person Expanded through the full SGG lifecycle
priority: P0
assignee: codex-team
description: >-
  Use the existing Key Person form as the post-leverage vertical canary before
  authoring a twentieth form; validate registration, lifecycle, repeated
  structures, projection, XML/XSD, and explicit human gates.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T17:58:01.860Z'
---
---
type: Task
title: Prove R&R Key Person Expanded through the full SGG lifecycle
priority: P0
assignee: codex-team
description: >-
  Use the existing Key Person form as the post-leverage vertical canary before
  authoring a twentieth form; validate registration, lifecycle, repeated
  structures, projection, XML/XSD, and explicit human gates.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T17:22:12.125Z'
---
# Goal

Take the already-authored R&R Senior/Key Person Profile (Expanded) through the complete Simpler lifecycle before authoring a twentieth portable form. Use it to validate that the leverage pass actually reduces marginal delivery cost.

# Acceptance criteria

- Consume the existing portable form through the post-leverage artifact contract; do not rewrite it as a new architecture.
- Exercise generic SGG registration metadata, irregular path projection, repeated-person cardinality, person/name/address/organization/contact blocks, conditional UI, attachments, validation, save/reload, locked/print, and submission behavior.
- Add or complete the portable Grants.gov XML target by composing reviewed reusable XML fragments; validate representative output against the exact official XSD when the pinned source set is available.
- Record any semantic, source, accessibility, instruction, or release blockers explicitly; do not represent them as accepted.
- Record before-and-after authoring size, new reusable blocks or fragments required, form-specific adapter/compiler branch count, and end-to-end conformance results.
- Register for production only after the applicable human and operational gates are accepted.

# Scope boundary

This is a vertical canary for an existing form, not permission to add a general override language, cross-form orchestration engine, new intermediate representation, independent reference consumer, or wholesale `@Sgg.*` migration.

# Exit

After this canary proves the bounded architecture and records its exceptions, resume new foundation authoring with PHS Human Subjects and Clinical Trials.

[depends on](simplify-multi-project-cardinality-reuse.md)

[depends on](factor-grants-gov-xml-fragments.md)

[depends on](unify-simpler-path-projection.md)

[depends on](separate-sgg-runtime-identity-metadata.md)

[depends on](fix-repeated-attachment-audit.md)

[depends on](complete-key-person-declaration-xml.md)

[depends on](add-composable-presence-conditions.md)

[depends on](prove-key-person-sgg-lifecycle.md)

[depends on](project-key-person-xml-in-sgg.md)

[depends on](distinguish-xml-array-wrapper-cardinality.md)

[depends on](integrate-key-person-overflow-gating.md)

# Result

The post-leverage vertical canary is technically complete without production opt-in.

## Reuse and marginal authoring

- The existing 104-line form declaration grew by only 16 source-backed lines to add ZIP/default corrections and three overflow annotations.
- The new portable wire target is 134 declarative lines: a 75-line form profile plus a 59-line reusable research-person mapping. It composes existing name, address, and attachment fragments.
- Reusable capabilities added for future forms: count-or-own-value conditions, array-aware attachment auditing, leaf XML containers, explicit array wrapper cardinality, and a research-person XML profile.
- Form-specific compiler or adapter branch count: zero.

## Technical conformance

- 57 rendered fields, up to 99 repeated people, nine conditional UI behaviors, and seven declared attachment fields compile and load generically.
- Real database save/reload, attachment add/remove auditing, repeated-row interaction/max, nested validation, locked/print rendering, and submit service transition are covered.
- Exact XML includes PI, multiple senior/key people, ordinary person data, nested attachments, and overflow attachments with exact QName/order/data assertions.
- The complete five-file official XSD closure is byte-pinned and hash-verified; exact validation is mandatory. All 33 vendored XSDs compile.
- The final consumer suite passed 140 API form-spec tests and 35 artifact-backed frontend tests; producer preflight passed 90 TypeScript tests, 68 Python tests, and 660 artifacts.

## Remaining gates

The declaration and mappings remain proposed/source-bound-unreviewed. Production identifiers/instructions, semantic acceptance, accessibility and visual review, one-row deletion UX, State/Province stale-value policy, content/instruction approval, and operational release remain open. The form is not production-registered and this result does not claim production approval.
