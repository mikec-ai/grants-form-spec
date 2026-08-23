---
type: Task
title: Canonicalize SF-424 cover question clusters
priority: P1
description: >-
  Normalize 50 likely semantic occurrences across SF-424 and the two R&R cover
  variants using accepted evidence.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T16:58:42.768Z'
---
# Objective

Normalize the 50 likely semantic-question occurrences in SF-424, R&R SF-424, and R&R SF-424
Multi-Project Cover into evidence-backed canonical question composition.

# Field clusters

- Submission/application/revision: `submissionType`, `submissionTypeCode`, `applicationType`,
  `applicationTypeCode`, `revisionType`, `revisionCode`, `revisionOtherSpecify`,
  `revisionCodeOtherExplanation`, `isOtherAgencySubmission`, `otherAgencySubmissionExplanation`
- Identifiers: `applicantId`, `federalEntityIdentifier`, `federalAwardIdentifier`, `federalId`,
  `grantsGovTrackingId`
- Applicant organization/type: `applicantTypeCode`, `applicantTypeCodeOtherExplanation`,
  `sociallyEconomicallyDisadvantaged`, `womenOwned`, `departmentName`, `divisionName`,
  `organizationAffiliation`
- Funding: `totalEstimatedAmount`, `totalNonFederalRequested`,
  `totalFederalNonFederalRequested`, `estimatedProgramIncome`
- State review/debt: `stateReview`, `stateReviewCodeType`, `stateReviewAvailableDate`,
  `stateReviewDate`, `delinquentFederalDebt`

# Acceptance criteria

- Each occurrence is mapped to an existing canonical question, promoted as a new canonical question,
  or explicitly reclassified as non-semantic based on source evidence.
- Same-looking standard and R&R fields are merged only after accepted semantic review; differing
  enumerations or lifecycle semantics remain distinct or share only a justified base vocabulary.
- Form-specific labels, requiredness, constraints, and XML mappings remain occurrence/profile data.
- Both R&R covers compose shared definitions for genuinely shared clusters instead of maintaining
  parallel local models.
- Producer tests, XML goldens, and SGG oracle parity remain green.
