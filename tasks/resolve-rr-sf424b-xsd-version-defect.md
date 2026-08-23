---
type: Task
title: Resolve and bank the R&R SF-424B XSD version defect
priority: P0
assignee: Codex
description: >-
  Classify the official schema-level version mismatch as a tested upstream
  metadata defect, then bank the exact XSD and form in SGG without runtime
  enablement.
superbee_progress_status: in_progress
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T23:25:02.216Z'
---
# Goal

Resolve the R&R SF-424B official-XSD version discrepancy as a narrow, evidence-backed upstream metadata defect and bank the form in SGG without enabling or registering it.

# Evidence and disposition

- Preserve the exact official `RRSF424_SF424B-V1.1.xsd` bytes and SHA-256.
- Record that the V1.1 filename, source URL, target namespace, fixed instance `FormVersion`, and emitted `FormVersionIdentifier` agree on 1.1.
- Record that only `xsd:schema/@version` says 1.0; W3C defines that attribute for user convenience with no instance-validation semantics.
- Continue validating minimal and representative XML against the exact official schema and dependency closure.

# Acceptance criteria

- The producer records the disposition as an accepted upstream metadata defect rather than a blocked wire-contract ambiguity.
- Regression tests fail if the official mismatch disappears or any authoritative V1.1 signal changes without review.
- The official XSD is not patched, normalized, or replaced.
- SGG banks `rr-sf424b` from an immutable producer revision using the generic banked-only path.
- Runtime loading, preview, FormType/UUID projection, registration, and production routing remain unavailable until separately approved.
- Existing policy-owner, accessibility, instructions, semantic, and production-registration gates remain explicit.

# Delivery sequence

1. Land the producer evidence/disposition and tests.
2. Repin the consumer artifact bank after the producer merge.
3. Verify digest, XSD, selection, and fail-closed runtime tests in SGG.

[depends on](separate-banked-from-runtime-enabled-forms.md)
