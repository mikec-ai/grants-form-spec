---
type: Task
title: Generalize source-backed agent authoring across forms
priority: P0
assignee: Codex
description: >-
  Replace the one-form demo adapter with a neutral source-authoring dossier and
  prove it on PHS Assignment Request and Attachment Form.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-28T00:51:01.789Z'
---
# Scope

Replace the PHS Assignment Request demo-specific dossier and prompt assembly with a form-neutral design-time source-authoring contract. Prove that the same agent exchange, human acceptance, compiler, parity comparison, and renderer work for both PHS Assignment Request and the structurally different Attachment Form.

# Result

Completed and merged in [grants-form-workbench PR #45](https://github.com/mikec-ai/grants-form-workbench/pull/45), merge commit `4bad9d0fc4bc641ac1c0b822c3e17e98530b1195`.

- Added strict `portable-form-source-authoring-dossier/v1` validation for form identity, pinned evidence, normalized source text, exact field occurrences, ordered content, presentation metadata, and layout completeness.
- Added generic dossier-to-agent-request, dossier-to-evidence, and dossier-to-empty-draft functions. The compiled oracle package is not part of the dossier or request.
- Added neutral `add-content` authoring operations and typed `Attachment` presentation support through the runner, exchange, workspace, compiler, and review UI.
- Preserved deterministic source facts, agent recommendations, human operational decisions, and semantic review state as separate records. Accepted operational recommendations remain semantically proposed and do not change published coverage.
- Prevented ambiguous rule editing when a draft contains repeated occurrences of only one semantic concept.

# Proof receipts

- Live Codex / PHS Assignment Request 4.0: 13 `add-field` recommendations; 13 compiled fields; exact supported parity for field mappings, schema, presentation, behaviors, and review-state safeguards.
- Live Codex / Attachment Form 1.2: 17 recommendations (2 `add-content`, 15 `add-field`); 15 compiled fields and 17 ordered layout elements; exact supported parity for the same five checks.
- Browser-integrated Attachment proof: live agent proposal accepted into the shared draft and rendered as a 15-control Simpler-style applicant preview; withheld-oracle comparison reported every supported check green.
- Focused dossier, exchange, runner, workspace, parity, and portal tests pass. Typecheck, build, the 152-question catalog check, and diff validation pass.
- GitHub Actions run `33130944386` failed before executing any steps because of the account-level hosted Actions limitation. Local verification supplied the merge gate.
- The broad repository suite still exposes one unrelated USWDS numeric-control failure reproduced unchanged on `origin/main`; deterministic producer reimport also requires the historical pinned producer revision rather than the current producer checkout. Neither condition was changed in this task.

# Acceptance criteria

- [x] Define one strict, machine-readable source-authoring dossier without a compiled oracle package.
- [x] Build agent requests and digest-bound evidence references generically from the dossier.
- [x] Keep deterministic source facts separate from agent recommendations and human decisions.
- [x] Add reusable typed attachment controls and source-backed instructional content.
- [x] Let a human select either proof, invoke Codex, accept recommendations, render the compiled candidate, and compare it with a withheld oracle.
- [x] Preserve semantic and response-role mappings as proposed or unreviewed.
- [x] Add contract, exchange, compilation, parity, and end-to-end tests for both forms.

[depends on](compile-accepted-agent-form.md)

[depends on](decouple-agent-authoring-source-and-question-catalog.md)
