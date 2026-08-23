---
type: Task
title: Promote residual reference-form questions
priority: P1
description: >-
  Normalize eight likely semantic fields in Key Contacts, SF-424 Short, and
  SF-424A.
superbee_progress_status: in_progress
superbee_updated_by: residual_questions_agent
generated:
  by: 'process:superbee'
  at: '2026-08-23T18:17:09.933Z'
assignee: residual_questions_agent
---
# Objective

Classify and promote the eight likely semantic fields remaining in smaller reference forms.

# Baseline fields

- Key Contacts: `projectRole`
- SF-424 Short: `applicantWebAddress`, `projectDescription`
- SF-424A: `activityTitle`, `assistanceListingNumber`, `directChargesExplanation`,
  `indirectChargesExplanation`, `remarks`

# Acceptance criteria

- Every field has source evidence and either composes an existing canonical question or gains a
  portable canonical definition with entity/tag metadata.
- Key Contacts' free-text project role is not conflated with the R&R Key Person controlled role
  vocabulary without accepted semantic evidence.
- SF-424A per-row occurrence semantics and constraints are preserved.
- Analysis counts and occurrence paths update deterministically, and form/target tests remain green.

# Delivery receipt

Draft PR: [grants-form-spec #42](https://github.com/mikec-ai/grants-form-spec/pull/42)

Eight applicant-input occurrences now have canonical lineage:

- Key Contacts `projectRole` composes `poc/project-role`, a free-text 1-45 character question that
  remains distinct from the R&R controlled role vocabulary.
- SF-424 Short composes `primary-org/website` and `project/description`; the existing website
  length override remains local to this form occurrence.
- SF-424A composes a row-scoped `budget/activity-title`, the existing
  `opportunity/assistance-listing-number`, and three new Section F budget questions. The activity
  title remains required within each repeated row, the Assistance Listing number remains optional
  within each row, and all pinned XSD length constraints are preserved.

All eight source mappings are `proposed`, have no reviewer attribution, and remain excluded from
published similarity. The deterministic ledger moves exactly those eight identities to `resolved`.

Verification on commit `5347be1a8`:

- full `npm run preflight` passed;
- 91 TypeScript tests and 81 Python tests passed;
- 125 blocks and 688 emitted artifacts validated;
- question inventory: 101; form/question associations: 426;
- unclassified-field ratchet: 8 resolved, 68 remaining.
