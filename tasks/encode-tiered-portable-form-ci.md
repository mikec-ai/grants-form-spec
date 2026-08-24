---
type: Task
title: Encode risk-tiered CI for portable form banking
priority: P1
assignee: codex
description: >-
  Make additive artifact/XSD banking fast by default while automatically
  escalating executable, destructive, release, and upstream-bound changes to
  full CI.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T02:52:56.475Z'
---
# Goal

Encode the tiered portable-form CI decision in the SGG fork without weakening full validation for executable or upstream-bound changes.

# Acceptance criteria

- One shared, tested classifier recognizes only additive or modified artifact/XSD changes as bank-only.
- Deletions, tests, adapters, runtime identities, registrations, projections, workflows, and unexpected paths fail closed to full CI.
- The bank-only lane verifies artifact digests, exact XSD digests, and no loss of selected forms or artifact closure.
- Existing API and E2E workflows retain their names and run fully for non-bank changes and non-PR invocations.
- The promotion workflow stages exact XSD fixtures as well as artifacts.
- Repository documentation explains the policy and the upstream/production release boundary.
- A hosted PR proves both workflow syntax and classification behavior before merge.

# Progress

- SGG PR #55 merged as `32f09a1ee3cec163095adfe8425ce4204b8f5aba`; it implements the classifier, bank-only integrity lane, full-CI escalation, XSD staging, wildcard byte preservation, tests, and repository documentation.
- Local gates: 230 form-spec tests passed with the one database-dependent lifecycle test deselected; repository-wide Black/isort and Ruff passed; classifier MyPy passed.
- Hosted workflow parsing and the fail-closed full-CI classification both passed on PR #55. The task remains in progress until the next artifact/XSD-only promotion proves the hosted lightweight lane.
- The full API run reproduced the preceding NIFA PR's exact 22 baseline failures while increasing passes from 4,509 to 4,514; E2E reproduced the unrelated 800-second API-readiness timeout. Neither failure was introduced by the tiering change.
- NIFA Supplemental consumer PR #54 merged as `91a01b0c5`; its unrelated E2E run failed after the API readiness wait exhausted 800 seconds, providing direct evidence for separating inert banking from runtime/browser validation.
- Hosted proof completed with PHS Inclusion Enrollment Report consumer PR #56. Both classifiers selected the bank-only tier; `Portable Form Bank Checks` passed in five seconds; full API, API build, Playwright, E2E infrastructure/tests, and report generation all skipped; the PR merged as `9fa568e1e6eb04e7218a9685cdf255215080cafb`.
- The first proof exposed an empty-report edge case. The report job had retained an always-run condition even when E2E was intentionally skipped. PR #57 added the classifier dependency and bank-only guard, passed GitHub workflow lint, and merged as `3974f60a540b7fb80e5452b27387bda174f2e0c0` before the successful proof rerun.
