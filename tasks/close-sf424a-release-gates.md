---
type: Task
title: Close SF-424A release gates
priority: P1
description: >-
  Portable SF-424A technical automation is merged; remaining work requires
  provisioned DB/browser execution, human semantic and accessibility review,
  instruction approval, and production registration.
superbee_progress_status: blocked
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T05:03:56.206Z'
assignee: human-review
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

- Merged fork PR [mikec-ai/simpler-grants-gov#39](https://github.com/mikec-ai/simpler-grants-gov/pull/39),
  commit `f2cd204e206edd9783d135bc633efc838cf4292a`, adds DB-backed save/reload and validation
  coverage for C-F = 10 with applicant-entered G = 100.
- The same PR adds an automated Section A accessibility scan and verifies the entered G value is
  preserved in the locked rendering path. Existing generic print coverage proves print always uses
  the locked path.
- Focused frontend tests, ESLint, Prettier, API Ruff checks, and the DB-backed lifecycle test pass
  locally against the PostgreSQL test service.
- Merged fork PR [mikec-ai/simpler-grants-gov#41](https://github.com/mikec-ai/simpler-grants-gov/pull/41),
  commit `777f854037465f46f4f884d56e3b3feaf63efbc7`, extends the existing Playwright
  submission/print harness with the same C-F = 10 / G = 100
  exception, browser A-to-G keyboard order, accessible-name assertions, the actual print route
  under print media, locked controls, and the persisted Column G total. It removes SF-424A's former
  exemption from the generic read-only print gate.
- Focused ESLint, Next type generation, TypeScript, the five-test Section A Jest suite, and
  Playwright discovery pass locally. The authenticated browser scenarios remain environment-run
  evidence because this workspace has no configured application session.
- Merged fork PR [mikec-ai/simpler-grants-gov#44](https://github.com/mikec-ai/simpler-grants-gov/pull/44),
  commit `f0a0aabd3308b4d0bddd1bae5ce881ea8e17309b`, corrects the DB lifecycle test fixture by
  supplying nonempty direct-charge explanation, indirect-charge explanation, and remarks values.
  The schema and validation remain strict, and the C-F = 10 / G = 100 intent is unchanged. The
  focused DB lifecycle and SF-424A parity suites pass all seven tests against localhost PostgreSQL;
  Ruff, isort, and Black pass.
- Human accessibility and guidance acceptance, semantic and policy decisions, instruction-asset
  and identifier acceptance, operational submission evidence, and production registration remain
  open gates. Technical automation does not resolve or approve them.

[depends on](reconcile-sf424-family-portable-cutover-deltas.md)
