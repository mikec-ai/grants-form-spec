---
type: Task
title: Reconcile SF-424D burden-statement policy evidence
description: >-
  Preserve the active burden-statement interaction and make three-profile policy
  equivalence reproducible before consumer or release work.
superbee_updated_by: sf424d_policy_followup
generated:
  by: 'process:superbee'
  at: '2026-08-23T20:50:11.313Z'
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
