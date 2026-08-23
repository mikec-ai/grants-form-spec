---
type: Task
title: Migrate the remaining four SGG legacy forms
superbee_progress_status: todo
priority: P1
description: >-
  Add the four legacy-only SGG forms to the portable architecture after the
  uniform proof machinery is ready.
actor: Codex
timestamp: '2026-08-23T22:26:31.600Z'
---
# Goal

Migrate the four SGG legacy forms that remain outside the portable catalog after the current expansion tranche:

- EPA Form 4700-4;
- EPA Key Contacts;
- Project Abstract, distinct from Project Abstract Summary;
- Supplementary NEH Cover Sheet.

# Delivery approach

Treat each form as a source-evidenced portable definition, use the legacy implementation as a compatibility oracle, and route all differences through the intentional-delta gate. Reuse canonical questions and compositions where semantics genuinely match; preserve form-local concepts where they do not.

# Acceptance criteria

- Each form has authoritative source evidence, generated artifacts, and producer contract gates.
- Each form passes SGG artifact-bank, schema/rules/XML, browser/lifecycle, locked/print, and applicable XSD gates.
- Portable-versus-legacy parity receipts and any intentional deltas are complete.
- No form is production-registered without a separate human release decision.

[depends on](build-uniform-legacy-differential-parity.md)

[depends on](enforce-evidence-backed-parity-deltas.md)
