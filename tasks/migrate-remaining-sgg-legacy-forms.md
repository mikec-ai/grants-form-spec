---
type: Task
title: Migrate the remaining four SGG legacy forms
superbee_progress_status: in_progress
priority: P1
description: >-
  Migrate four legacy-only Simpler forms after uniform parity machinery is
  ready; EPA Key Contacts is not yet portable or banked and is the named
  later-candidate oracle migration.
actor: Codex
timestamp: '2026-08-23T22:26:31.600Z'
superbee_updated_by: codex
assignee: personal_data_closure
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

## Active isolated slice — EPA Key Contacts

The `personal_data_closure` lane claimed the smallest non-overlapping slice on 2026-08-25: EPA Key Contacts only. Project Abstract remains independently owned; EPA 4700-4 and the Supplementary NEH Cover Sheet remain outside this slice.

Verified starting evidence exists without asserting producer completion: 81 deterministic XSD records with pinned source URL/version and no extraction warnings; a preserved versioned XLS behavior source; a legacy Simpler form, XML profile, exact-XSD tests, and browser fixtures that can serve as a compatibility oracle; and prior agent-proposed role-qualified mappings that remain proposals. No open producer or consumer PR/remote branch currently claims EPA Key Contacts. The first deliverable is producer-owned source/provenance reconciliation and a declarative authoring plan; no consumer registration or release claim is authorized.
