---
type: Task
title: Bank PHS Inclusion Enrollment Report through lightweight CI
priority: P0
assignee: codex
description: >-
  Use the completed derivative form as the first timed hosted proof that
  additive artifact/XSD banking skips full API and E2E CI without weakening
  integrity gates.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T02:52:56.277Z'
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

# Timed result

- Timer start: `2026-08-24T02:42:46Z` (`22:42:46 ET`). Consumer base was `32f09a1ee3cec163095adfe8425ce4204b8f5aba`; immutable producer revision was `70fa65f82f66901f8a6a330aa8ef70479ded9b5e`.
- Hosted promotion run `32683964276` started at `02:42:53Z`. Producer build, exact-XSD verification, bundle ingestion, consumer integrity/release checks, commit, and branch push all succeeded by `02:44:35Z`: 1 minute 49 seconds after the timer start.
- The workflow could not open the PR because the fork disabled Actions PR creation. The preserved branch was opened manually as consumer PR #56 at `02:46:34Z`; the repository setting is now durably enabled.
- The first bank-only pass correctly ran the classifiers and five-second integrity lane and skipped full API and E2E execution. It exposed one orchestration defect: the E2E report aggregator still ran despite there being no test artifacts. The two-line condition fix merged separately in PR #57 as `3974f60a540b7fb80e5452b27387bda174f2e0c0` at `02:50:03Z`.
- After refreshing PR #56, both classifiers passed, `Portable Form Bank Checks` passed in 5 seconds, and API tests, API build, Playwright caching, E2E infrastructure/tests, and the empty report aggregator all skipped. The corrected hosted lane was green at `02:51:04Z` and PR #56 merged at `02:51:13Z` as `9fa568e1e6eb04e7218a9685cdf255215080cafb`.
- Total first-run elapsed time, including discovery and repair of both repository-permission and aggregator configuration defects: 8 minutes 27 seconds. The steady-state path demonstrated by the successful phases is approximately 2-3 minutes from dispatch through merge, excluding human review latency.

# Promotion receipt

- Added form: `phs-inclusion-enrollment-report`; removed forms: none.
- Selected forms: 34; selected artifacts: 370.
- Bundle SHA-256: `4b147e74598d4abd8fe9e00926ec66c7eb35809119e5c0579b737e73ea376289`.
- Consumer diff: 11 paths, limited to the artifact manifest, portable form/question artifacts, two producer-refresh artifact changes, and the exact `PHSInclusionEnrollmentReport-V1.0.xsd` fixture.
- No adapter code, tests, runtime identities, registrations, projections, or workflow files were included in the promotion PR. The form remains intentionally unregistered.

[depends on](encode-tiered-portable-form-ci.md)

[depends on](enforce-exact-producer-xsd-fixture-digests.md)
