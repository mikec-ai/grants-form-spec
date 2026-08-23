---
type: Task
title: 'Resolve lifecycle, attestation, and control fields'
priority: P0
description: >-
  Determine evidence-backed ownership and roles for 18 lifecycle-sensitive or
  nonstandard form-local occurrences.
superbee_progress_status: done
superbee_updated_by: correct_tracking_role
generated:
  by: 'process:superbee'
  at: '2026-08-23T19:18:17.577Z'
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

# Delivery

Focused producer PR: [mikec-ai/grants-form-spec#43](https://github.com/mikec-ai/grants-form-spec/pull/43), commit `5af4b807d`.

The initial PR #43 disposition was:

- Nine `systemValue` occurrences: agency routing numbers in both R&R covers; the Multi-Project
  Grants.gov tracking number; SF-424 State received date/application identifier; and the equivalent
  State-owned date/identifier fields in both R&R covers.
- Six `attestation` occurrences: the four form-local certification controls and the Multi-Project
  AOR signature/date pair.
- Two `technicalField` occurrences: SF-424 Short `sameAsProjectDirector` and SF-424A
  `confirmation`.
- One `applicantInput`: Multi-Project `submittedDate`, represented by the new
  `application/submission-date-entered` canonical question.

Response role is orthogonal to semantic identity. In PR #43, the nine externally assigned occurrences
retain canonical lineage through four source-neutral blocks: Federal agency routing number, State
received date, State application identifier, and previous Grants.gov tracking number. Each emitted
occurrence has both its canonical block id and `systemValue` role. The nine evidence mappings are
proposal-only, have no reviewer attribution, and remain unpublished.

The analysis projection now preserves exact path-qualified proposal status. The 17 proposals from
PRs #42 and #43 report `mappingStatus: proposed` with their source id/path while remaining
`publishable: false`; only accepted mappings can enter reviewed or published metrics. An occurrence
without an exact mapping remains `unmapped` on a proposed form or `unreviewed` on an unreviewed form.

The Multi-Project signature/date pair was reviewed independently using its pinned 4.0 XSD, DAT,
and read-only PDF. It remains form-local because its applicant/AOR lifecycle differs from the
submission-populated standalone R&R fields. Certification controls also remain form-local: their
semantic identity and portable boolean-versus-source-code answer shape are not reviewed.

The official SF-424 Short 3.0 DAT is pinned at
`a905f905928a730b10d48d0b77cbb59397edb3ad3c99770391e1e160c3fb06df`. It requires
`sameAsProjectDirector` to disable Primary Contact rows 8-04 through 8-20. The control remains a
`technicalField`, while the portable runtime's missing disable behavior is recorded as an explicit
source-parity gap.

After rebasing on merged PR #42, full `npm run preflight` passed with 91 TypeSpec tests, 86 Python
tests, 131 validated blocks / 712 artifacts, 107 canonical questions, 436 exploratory associations,
zero reviewed associations, and the combined monotonic ratchet at 76 initial / 26 resolved / 50
remaining. XML profiles and current runtime presentation/validation behavior are unchanged. No
HHS/upstream repository or issue was modified.

# Superseding correction

PR #43's actor-versus-authority interpretation was corrected after independently re-reading the
pinned population instructions. Merged producer PR
[mikec-ai/grants-form-spec#46](https://github.com/mikec-ai/grants-form-spec/pull/46), main commit
`c4a7fa5e722bca4dd92eb66a887bc2f7f6e0a865`, is authoritative:

- Eight R&R occurrences are `applicantInput`: State-received date, State application identifier,
  agency routing identifier, and prior Grants.gov tracking number in both R&R covers.
- Classic SF-424's two State fields remain read-only `systemValue`s.
- The other attestations, technical controls, and Multi-Project submitted date retain their PR #43
  roles.
- The standalone tracking occurrence now shares the proposal-only canonical identity, moving the
  ratchet to 27 resolved / 49 remaining and exploratory associations to 437.

The standalone instructions (`666647f...`) and independent Multi-Project DAT (`361e00d...`) both
direct the applicant to enter the four R&R values. External authority remains in descriptions and
provenance; it no longer overrides the documented response-population actor. All ten mappings remain
proposed and unpublished.
