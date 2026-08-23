---
type: Task
title: Canonicalize SF-424 cover question clusters
priority: P1
description: >-
  Normalize 50 likely semantic occurrences across SF-424 and the two R&R cover
  variants using accepted evidence.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T20:50:17.919Z'
assignee: prepare_cover_clusters
---
---
type: Task
title: Canonicalize SF-424 cover question clusters
priority: P1
description: >-
  Normalize 50 likely semantic occurrences across SF-424 and the two R&R cover
  variants using accepted evidence.
superbee_progress_status: in_progress
superbee_updated_by: prepare_cover_clusters
generated:
  by: 'process:superbee'
  at: '2026-08-23T20:49:01.673Z'
assignee: prepare_cover_clusters
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

# Delivery receipt

- Pull request: `mikec-ai/grants-form-spec#47`
- Producer base: `e0b0fb24c421a7c70e395afedf5be3f37f366606`
- Verified head: `eb859b2f22feba23c35be8d0a690293019a482f2`
- Review state: independent functional review clean; GitHub CI passed; cleanly mergeable and
  frozen for merge
- Verification: full preflight and GitHub CI passed with zero TypeSpec warnings, 102 TypeScript
  tests, 125 Python tests (1 skipped), 161 blocks and 924 artifacts validated, 34 promotion
  records, and the honest `76/76/0` unclassified-field ratchet.
- Publication boundary: all 50 source-bound mappings remain proposed and unpublished.
- Merge: producer PR 47 merged to `main` as `262f7a27127aa44fa6f3cf31eb30bb5f415ff933` after the clean independent review and final green CI run.
