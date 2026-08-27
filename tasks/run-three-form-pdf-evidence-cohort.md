---
type: Task
title: Run three-form PDF visual evidence cohort
priority: P0
assignee: Codex
description: >-
  Completed the three-form PDF visual evidence cohort through a generic
  producer-artifact target, exact pinned sources, page-complete proposed
  reviews, and human decision packets. Merged as grants-form-workbench PR #33.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T18:12:06.493Z'
---
[depends on](implement-pdf-visual-evidence-pipeline.md)

# Outcome

Implemented and merged a generic PDF evidence loop for forms that already have resolved producer artifacts. The loop derives stable review targets from exact manifest, schema, UI, and evidence artifacts; binds every proposed observation to those targets; and generates a human packet that cannot accept semantic mappings or modify runtime artifacts.

# Cohort receipts

- Attachment Form 1.2: 3/3 pages reviewed; 4 proposed observations; 0 conflicts; 2 explicit gaps. Review SHA-256: 1c6f610ec85e8d7f865c7ecab215cbd31965ec60574fe35c80f5dac8513be948.
- R&R SF-424 5.0: 15/16 pages reviewed; one XFA sample explicitly unavailable; 9 proposed observations; 1 conflict; 3 explicit gaps. Review SHA-256: c093706cad63cae51dcb83818711353cffbdf4e96ff33a8026287207ac15344a.
- R&R Budget 3.0: 5/6 pages reviewed; one XFA sample explicitly unavailable; 6 proposed observations; 0 conflicts; 4 explicit gaps. Review SHA-256: 11833424028a6dc9732fe02e92042cdcaf86af9dc21fb635b24c793f269cab1b.

# Material findings

- R&R SF-424 has a source conflict that requires human authority: the instructions visibly state Executive Order 12732 while the read-only form visibly states 12372. No automatic reconciliation was made.
- The R&R Budget official instructions URL tested for this cohort returned HTTP 404; no substitute source was inferred.
- XFA-only sample pages remain explicitly unavailable rather than counted as reviewed.

# Shared implementation

- Added portable-form-pdf-review-target/v1 and portable-form-pdf-target-review/v1.
- Added target, check-target, and packet-target CLI operations with structured TOON stdout and usage failures at exit 2.
- Fixed deterministic page rendering for longer PDFs by rendering one requested page at a time with stable filenames.
- Added attachment as a genuine PDF observation category.
- Added tests for strict producer receipts, stable field and behavior refs, proposed-only review, CLI output, packets, and human acceptance guardrails.

# Verification

Merged PR: https://github.com/mikec-ai/grants-form-workbench/pull/33
Merge commit: b38afad6e33fe1afd1afa67a048a0137e77768b1

- 66/66 agent-tool tests passed.
- Typecheck passed.
- Question catalog check passed at 126 questions.
- Workspace build passed.
- All three exact cohort checks passed.
- Browser QA confirmed embedded source images and that accepting an observation requires reviewer, role, and review-record link.
- The broad Vitest suite exposed existing concurrency/timing flakes; the initially timed-out catalog-selector test passed in isolation.
- GitHub Actions did not start because of the account billing/spending-limit restriction; the annotation was external to the code.
