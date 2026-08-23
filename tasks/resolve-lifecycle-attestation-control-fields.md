---
type: Task
title: 'Resolve lifecycle, attestation, and control fields'
priority: P0
description: >-
  Determine evidence-backed ownership and roles for 18 lifecycle-sensitive or
  nonstandard form-local occurrences.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T17:58:29.007Z'
assignee: lifecycle_fields_agent
---
# Objective

Resolve value ownership and response roles for 18 fields that should not be normalized by name alone.

# Lifecycle-owned candidates (12 occurrences)

- `agencyRoutingNumber` in both R&R covers
- `aorSignature`, `aorSignedDate`, `submittedDate`, and `grantsTrackingNumber` in Multi-Project Cover
- `stateApplicationId` and `stateReceiveDate` in SF-424
- `stateId` and `stateReceivedDate` in both R&R covers

# Attestation and workflow candidates (6 occurrences)

- `applicationCertification`, `certificationAgree`, and `trustAgree` in both R&R covers
- `confirmation`, `sameAsProjectDirector`

# Acceptance criteria

- Each field has an evidence-backed role and lifecycle owner; unknowns remain explicitly unresolved
  rather than being guessed.
- Multi-Project Cover signature/date behavior is reviewed independently of standalone R&R SF-424,
  as required by the source-model comment and XML contract.
- Attestations may receive canonical semantic identities when justified, while technical copy or
  completion controls remain excluded from semantic similarity.
- System/calculated/technical behavior is represented portably and the SGG adapter contains no
  five-year/ten-year or form-id-specific classification table.
- XML projection and legacy-oracle behavior remain unchanged unless an evidence-backed correction is
  intentionally approved.

[depends on](classify-portable-response-roles.md)
