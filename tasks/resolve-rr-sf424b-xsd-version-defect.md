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
generated:
  by: 'process:superbee'
  at: '2026-08-23T23:42:44.531Z'
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

# Progress (2026-08-23)

- Producer PR [mikec-ai/grants-form-spec#61](https://github.com/mikec-ai/grants-form-spec/pull/61) merged as `7089fa6b0cca70e63e805a971c192a1849394d20`.
- Producer preflight passed: 198 Python tests, 104 TypeScript tests, artifact validation, promotion validation, bundle verification, and the classified-field gate.
- The official XSD remains byte-identical at SHA-256 `511de9a5594a739ce596a33a92d3dec1bac2a32f193a2fe6b4799b45f29ff296`.
- Consumer commit `930302c0` on `codex/bank-rr-sf424b-20260823` banks the form from the producer merge commit and leaves runtime identity and registration absent.
- The consumer promotion updater now provisions a missing XSD only from the immutable producer checkout and only when its bytes match the declared digest; it does not fetch live bytes or overwrite a conflicting consumer XSD.
- Focused consumer verification passed: Ruff plus 43 promotion/provenance/registration/SF-424B tests. The full portable-adapter directory produced 222 passes; its sole local error was the unrelated database lifecycle test because the non-container host `grants-db` was unavailable.
- Consumer delivery remains stacked on `tasks/separate-banked-from-runtime-enabled-forms` / SGG PR #51 and is not complete until that prerequisite lands and this branch is rebased, opened as a focused PR, and merged.

[depends on](separate-banked-from-runtime-enabled-forms.md)
