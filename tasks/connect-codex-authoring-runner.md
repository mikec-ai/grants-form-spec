---
type: Task
title: Connect Codex through the portable authoring exchange
priority: P1
assignee: Codex
description: >-
  Implement the smallest end-to-end Codex authoring path: stage an immutable
  exchange request in an isolated workspace, invoke subscription-authenticated
  codex exec through a replaceable edge runner, construct and validate an atomic
  recommendation package, and return it for human review without granting
  repository or publication authority.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T21:56:47.418Z'
---
# Scope

Reuse the proven Builder runner shape while keeping form authoring contracts provider-neutral.

# Acceptance criteria

- Codex receives only a staged authoring request and explicit output schema.
- The process adapter uses an ephemeral isolated workspace and no shell interpolation.
- Contributor runtime/model provenance is recorded by the trusted runner.
- The runner constructs canonical digests and validates the returned recommendation package before publishing it.
- Runtime tests use a fake Codex executable; no live model call is required in automated tests.
- Unknown CLI flags fail with exit code 2 and actionable TOON output.
- The browser authoring experience can request and review Codex recommendations without direct Codex or filesystem coupling in browser code.

# Outcome

Merged `mikec-ai/grants-form-workbench` PR #41. Source commit `794f829d0b876da6120605c0c8c019f1bb7a99fe`; merge commit `c5bac8d4116712d00914bd557189efca2ac3c85a`.

- Added the optional `@grants-form-workbench/agent-runner` integration edge.
- Added a bounded local development-server endpoint and a human-reviewable Codex action in the form composer. Browser code receives only the portable recommendation contract.
- Codex runs in an ephemeral read-only workspace containing only the immutable exchange request and output schema. User/project instructions are disabled and the runner invokes argv without a shell.
- Trusted code records runtime/model provenance and canonical evidence/package digests, then validates exact exchange identity, baseline, question IDs, operations, evidence references, and content before returning results.
- UI capabilities are explicitly restricted to the additive operations it can display; unsupported edits fail closed.
- Applied questions and rules remain proposed and cannot contribute to accepted semantic coverage.
- The default interactive profile is `gpt-5.6-luna` at medium reasoning with a three-minute timeout; model choice remains adapter configuration.

# Verification receipts

- Live isolated smoke over three exact bank records completed in about 12 seconds and returned the two requested question IDs.
- Live browser run over the full 185-record question bank returned four questions and one conditional rule; the package validated, the human review actions applied it, and the generic preview rendered it.
- 27 focused runner, exchange, UI, and architecture tests passed.
- 377 broader non-agent-tool tests passed; one unrelated environment-gated producer reimport was then run and passed against exact pinned checkout `a97da3714733566847349efcc013c6a79045b21b`.
- TypeScript project references and production build passed.
- Unknown CLI flags return exit code 2 with actionable TOON output.
- GitHub Actions created no check runs; local verification is the authoritative merge signal.

[depends on](portable-authoring-exchange.md)
