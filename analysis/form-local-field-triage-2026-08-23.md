---
type: Analysis Note
title: Triage of unclassified form-local fields
description: >-
  Evidence-backed disposition of the 90 unclassified occurrences emitted at
  grants-form-spec commit 46e71d5.
superbee_updated_by: codex
---
# Baseline

This triage is based on the successful `grants-form-spec` CI artifact for commit
`46e71d58516f3c5250702b1de30d8fc27e9ed95a` (GitHub Actions run `32652087969`). The emitted
`unclassified-form-fields.csv` contains 90 form/field occurrences representing 60 distinct field
names across 19 forms.

An unclassified row is not automatically a missing question. It means the emitted form leaf is not
currently attributable to a classified question-bank block. The 90 rows divide into four different
problems that require different remedies.

# Triage result

| Disposition | Occurrences | Distinct names | Required remedy |
| --- | ---: | ---: | --- |
| Canonical lineage/accounting artifact | 14 | 8 | Preserve or recover existing question-bank identity; do not create new questions |
| Likely semantic question | 58 | 39 | Review semantics, map to an existing question or promote a canonical question |
| Lifecycle ownership unresolved | 12 | 9 | Determine applicant/system/state/Grants.gov ownership before classification |
| Attestation or UI/workflow control | 6 | 5 | Classify explicitly; keep technical controls out of semantic reuse |

# 1. Canonical lineage/accounting artifacts

These are already inherited, spread, or overridden from question-bank models. Their appearance in
the unclassified ledger is primarily an emitter/analyzer lineage limitation.

- `budgetType`: `rr-budget`, `rr-budget-10yr`
- `state`, `province`, `zipCode`: address overrides in `performance-site` and
  `rr-key-person-expanded`; `state` and `province` also occur in
  `rr-sf424-multi-project-cover`
- `projectRole`: the principal-investigator default override in `rr-key-person-expanded` only
- `department`, `division`, `employerId`: inherited applicant-organization members surfaced through
  the multi-project cover's local subtype graph

Resolution must preserve the existing canonical block identity through spreads and occurrence-level
overrides. Creating duplicate questions to make the report green would corrupt the question bank.

# 2. Likely semantic-question backlog

Fifty occurrences (31 names) are in the SF-424 cover family:

- `applicantId`, `federalEntityIdentifier`, `federalAwardIdentifier`, `federalId`,
  `grantsGovTrackingId`
- `submissionType`, `submissionTypeCode`, `applicationType`, `applicationTypeCode`
- `revisionType`, `revisionCode`, `revisionOtherSpecify`, `revisionCodeOtherExplanation`
- `isOtherAgencySubmission`, `otherAgencySubmissionExplanation`
- `applicantTypeCode`, `applicantTypeCodeOtherExplanation`,
  `sociallyEconomicallyDisadvantaged`, `womenOwned`
- `departmentName`, `divisionName`, `organizationAffiliation`
- `totalEstimatedAmount`, `totalNonFederalRequested`,
  `totalFederalNonFederalRequested`, `estimatedProgramIncome`
- `stateReview`, `stateReviewCodeType`, `stateReviewAvailableDate`, `stateReviewDate`
- `delinquentFederalDebt`

Eight occurrences remain in smaller reference forms:

- `key-contacts`: `projectRole`
- `sf424-short`: `applicantWebAddress`, `projectDescription`
- `sf424a`: `activityTitle`, `assistanceListingNumber`, `directChargesExplanation`,
  `indirectChargesExplanation`, `remarks`

These are candidates, not accepted equivalences. Similar names across SF-424 and R&R forms must not
be merged without source evidence and accepted semantic mappings. Source-specific cardinality,
enumerations, wording, and constraints should remain occurrence-level deltas where possible.

# 3. Lifecycle ownership unresolved

These 12 occurrences require an ownership decision before they can be classified honestly:

- `agencyRoutingNumber`: both R&R covers
- `aorSignature`, `aorSignedDate`, `submittedDate`, `grantsTrackingNumber`: multi-project cover
- `stateApplicationId`, `stateReceiveDate`: SF-424
- `stateId`, `stateReceivedDate`: both R&R covers

The multi-project source explicitly differs from the standalone R&R cover for signature/date
ownership, so portability must not be achieved by assuming the standalone SGG lifecycle applies.

# 4. Attestations and UI/workflow controls

- Attestation candidates: `applicationCertification`, `certificationAgree`, and `trustAgree` in
  both R&R covers
- Workflow/control candidates: `confirmation`, `sameAsProjectDirector`

`sameAsProjectDirector` is likely a UI copy mechanism rather than a submitted semantic answer;
`confirmation` may be an SGG completion control. Those are hypotheses to verify against emitted XML,
the legacy oracle, and source evidence.

# Guardrails

- Do not infer semantic equivalence from names, labels, JSON types, widgets, or shared XML controls.
- Keep response role orthogonal to semantic identity and capture mechanism.
- Keep unresolved roles explicitly `unclassified` until evidence supports a decision.
- Keep all form knowledge in the portable form/question artifacts; the SGG adapter remains generic.
- Re-run the emitted analysis after every batch and preserve this commit as the historical baseline.

[planned by](../roadmap-items/form-field-normalization.md)

[creates work](../tasks/classify-portable-response-roles.md)

[creates work](../tasks/repair-form-local-lineage-analysis.md)

[creates work](../tasks/canonicalize-sf424-cover-question-clusters.md)

[creates work](../tasks/promote-residual-reference-form-questions.md)

[creates work](../tasks/resolve-lifecycle-attestation-control-fields.md)

[creates work](../tasks/enforce-classified-form-field-gate.md)

[creates work](../tasks/enforce-no-new-unclassified-debt-ratchet.md)
