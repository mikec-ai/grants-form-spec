---
type: Task
title: Reconcile SF-424D burden-statement policy evidence
description: >-
  Preserve the active burden-statement interaction and make three-profile policy
  equivalence reproducible before consumer or release work.
superbee_updated_by: sf424d_policy_followup
generated:
  by: 'process:superbee'
  at: '2026-08-23T20:58:16.281Z'
priority: P1
superbee_progress_status: in_progress
assignee: sf424d_policy_followup
---
# Goal

Resolve the active SF-424D v1.1 burden-statement evidence gap before any consumer or release work, and make cross-profile policy equivalence reproducible.

# Review finding

- The canonical policy bundle currently projects the printed DAT fields 00-3/00-4 statement (15 minutes; OMB project 0348-0042).
- Each of the three pinned active v1.1 DAT workbooks also contains field 00-0, a `View Burden Statement` interaction whose current content states 30 minutes, OMB 4040-0009, and the HHS PRA address.
- The interaction is currently omitted without an explicit unresolved or excluded disposition.
- The existing audit hashes one staged assurance array and trusts `identicalAcrossProfiles`; it does not deterministically derive and compare the three pinned profiles.

# Acceptance criteria

- Deterministically extract and preserve the active field 00-0 burden-statement content from every pinned profile, with exact source/version/hash provenance.
- Represent both the printed statement and current interactive statement declaratively, or record an explicit evidence-backed unresolved/excluded disposition pending policy-owner review. Do not silently choose one.
- Keep all semantic and policy conclusions proposed/unpublished; no production registration or consumer release claim.
- Recompute and compare normalized per-profile assurance arrays from pinned evidence, recording reproducible hashes rather than trusting a boolean assertion.
- Add tests for the burden-statement disposition and cross-profile equivalence derivation.
- Add no form-specific compiler or adapter branch.

[follows up](migrate-sf424d-assurance-family.md)

# Progress receipts

## Producer correction ready for review (2026-08-23)

- Producer branch: `codex/sf424d-policy-evidence` from main `262f7a27127aa44fa6f3cf31eb30bb5f415ff933`.
- Producer commit: `342afde9b` (`Reconcile SF-424D burden policy evidence`).
- Draft boundary: PR `mikec-ai/grants-form-spec#54` is open and intentionally unmerged.
- Added `profile-policy-extract-v1.1.json`, a source-bound/unreviewed extraction artifact that pins each profile's exact DAT URI, v1.1 identity, and SHA-256; preserves the active burden interaction; and records all twenty normalized assurance rows independently for each profile.
- Tests now recompute every per-profile assurance-array hash and compare the derived arrays. All three equal `89c82c4e717dab69a9a751259e9148b97d6b092e88d1a57e8537953c5ee1c4be`.
- Tests also recompute the identical normalized burden-interaction hash `afa221267ca5e165754d2001e5ab90e6974064772c16984d6813dadd674d1506` for every profile.
- The 15-minute printed statement versus 30-minute active interaction is explicitly `unresolved-pending-policy-owner-review`; a dedicated pending release gate was added to all three bindings.
- Semantic and policy status remains source-bound/unreviewed; forms remain draft and unregistered. No compiler, adapter, consumer, or HHS code changed.
- Full producer preflight passes: 102 TypeScript tests; 127 Python tests with 8 existing skips; artifact validation; 20 XML profiles; packaging; analysis; and the zero-unclassified gate.
- GitHub CI run `32665902765` passed at exact head `342afde9bebbdaedb7c542537b77bb7085af72d3`.

# Remaining gate

- Review and merge producer PR `#54`; policy-owner resolution of which burden presentation is authoritative remains intentionally outside this correction.
