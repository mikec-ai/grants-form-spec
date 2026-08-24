---
type: Task
title: Bank PHS Inclusion Enrollment Report through lightweight CI
priority: P0
assignee: codex
description: >-
  Use the completed derivative form as the first timed hosted proof that
  additive artifact/XSD banking skips full API and E2E CI without weakening
  integrity gates.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T02:26:31.334Z'
---
# Goal

Bank the already-complete PHS Inclusion Enrollment Report into the SGG consumer through the supervised additive promotion workflow and use it as the first hosted measurement of the risk-tiered bank-only CI lane.

# Fixed inputs

- Portable form id: `phs-inclusion-enrollment-report`.
- Producer baseline containing the form: `a237bc9bdbc34784652840946faf46d53e10e3a4` (producer PR #64).
- Select the final immutable producer revision only after exact-XSD preflight PR #66 lands.
- Start from the SGG consumer `origin/main` that contains tiered-CI PR #55.

# Measurement protocol

- Do not start the timed promotion until both enabling PRs are merged and the consumer/producer base SHAs are recorded.
- Record dispatch/start time, promotion completion, PR-open time, lightweight-CI completion, merge time, and elapsed duration for each phase.
- Record added and removed forms, selected artifact count, producer SHA, bundle SHA-256, changed paths, and CI classification.
- Treat any full API, database, or E2E execution as a classifier defect unless the generated PR contains a fail-closed escalation path.

# Acceptance criteria

- Promotion is additive and removes no previously selected form or artifact closure.
- The consumer diff contains only vendored portable artifacts and exact XSD fixtures; no adapter code, tests, projections, runtime identities, registrations, or workflow files change.
- Artifact digests, exact XSD pins, and consumer selection integrity pass.
- Hosted CI selects `bank_only=true`, runs `Portable Form Bank Checks`, and skips full API and browser jobs.
- The form remains intentionally unregistered and runtime-disabled.
- The PR merges and the measured receipt is added to the roadmap and tiered-CI task.

[depends on](encode-tiered-portable-form-ci.md)

[depends on](enforce-exact-producer-xsd-fixture-digests.md)
