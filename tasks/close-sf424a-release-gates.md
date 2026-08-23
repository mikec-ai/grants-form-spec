---
type: Task
title: Close SF-424A release gates
priority: P1
description: >-
  Prove SF-424A lifecycle, browser accessibility, human acceptance, and
  production readiness after the completed portable implementation.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T19:09:19.908Z'
assignee: codex
---
# Goal

Close the remaining release gates for the already-delivered portable SF-424A implementation without
moving form-specific behavior into the Simpler adapter.

# Delivered baseline

- Producer PR #13 owns source-grounded Section A guidance and field help declaratively.
- Simpler PR #9 consumes that guidance, preserves manual Column G rows 1–4 and the row-5 vertical
  total, adds semantic headers and accessible input names, honors locked state, and improves generic
  section navigation.
- Focused producer, adapter, and frontend tests pass; this task does not reopen that implementation
  work.

# Acceptance criteria

- Exercise DB-backed save/reload, validation, and submission with the exception case where columns
  C–F total 10 but entered Column G is 100.
- Prove locked and print rendering preserve the same values and guidance.
- Run browser-level keyboard navigation and automated accessibility checks, then record the required
  human accessibility and guidance acceptance separately from technical results.
- Record semantic, policy, instruction-asset, identifier, and production-registration decisions;
  unknown or unaccepted decisions remain explicit gates.
- Reuse the generic lifecycle and browser harnesses. Add no SF-424A-specific compiler or adapter
  branch merely to satisfy a release check.
- Enable production registration only after the applicable human and operational gates are accepted.

# Boundary

Technical conformance is not semantic acceptance, accessibility approval, or authorization to
modify HHS upstream.

[depends on](improve-sf424a-budget-experience.md)

[depends on](integrate-sf424a-reference-form.md)

# Progress receipt

- Fork PR [mikec-ai/simpler-grants-gov#39](https://github.com/mikec-ai/simpler-grants-gov/pull/39)
  adds DB-backed save/reload and validation coverage for C-F = 10 with applicant-entered G = 100.
- The same PR adds an automated Section A accessibility scan and verifies the entered G value is
  preserved in the locked rendering path. Existing generic print coverage proves print always uses
  the locked path.
- Focused frontend tests, ESLint, Prettier, API Ruff checks, and the DB-backed lifecycle test pass
  locally against the PostgreSQL test service.
- Submission, browser-level keyboard testing, human accessibility/guidance acceptance, policy
  decisions, and production registration remain open gates.
