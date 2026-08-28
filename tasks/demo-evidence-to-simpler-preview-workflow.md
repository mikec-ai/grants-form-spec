---
type: Task
title: Demo evidence-to-Simpler form authoring workflow
priority: P1
assignee: Codex
description: >-
  Build an evidence-backed agent authoring and human acceptance demo ending in
  an interactive Simpler-compatible applicant preview.
superbee_progress_status: done
generated:
  by: 'process:superbee'
  at: '2026-08-27T23:51:48.924Z'
superbee_updated_by: Codex
---
# Scope

Create one coherent, evidence-backed demonstration in the consumer workbench: load the exact PHS Assignment Request source dossier, ask an agent to propose the form, let a human accept all operational suggestions into a draft, and render an interactive Simpler-compatible applicant preview.

# Acceptance criteria

- The demo names and preserves the exact PDF, XSD, DAT, instructions, producer revision, and digests used as evidence.
- The agent request receives the source dossier and the exact question bank; deterministic source evidence remains separate from agent rationale.
- A single human action can add all ready question and rule suggestions to the draft without accepting semantic equivalence or changing published coverage.
- The applicant preview uses the generic portable runtime and Simpler presentation preset, supports data entry and validation, and clearly distinguishes demonstrated parity from unresolved production gates.
- The implementation introduces no form-specific compiler or renderer branch.
- Tests cover evidence receipts, accept-all behavior, review status, and the applicant preview.

# Authority boundary

Accepting suggestions changes only the working draft. It does not mark semantic mappings reviewed, approve a form for publication, or contribute to coverage metrics.

# Outcome

Completed and merged in [grants-form-workbench PR #43](https://github.com/mikec-ai/grants-form-workbench/pull/43), merge commit `8726f1b9623c97f1533712d52dbac4a3ccc29cba`.

- The reference workflow consumes six digest-bound evidence references: official XSD, DAT/XLS, official PDF, instructions, exact portable form package, and a normalized source dossier.
- A live Codex run using `gpt-5.6-luna` proposed five distinct semantic question concepts. The exact portable package preserved all 13 runtime occurrences, including repeated expertise and excluded-reviewer fields.
- One human action accepted the operational suggestions into a working draft and opened the exact form in a Simpler-style applicant workspace. All five semantic mappings remained proposed and therefore did not affect published coverage.
- Browser verification confirmed all 13 fields, successful data entry and retained values, and no console errors or warnings.
- The official PDF and XSD bytes were independently re-fetched and matched their pinned SHA-256 digests.

# Verification receipts

- Focused authoring and application flow: 24 tests passed.
- Workspace type check: passed.
- Question catalog check: current at 152 questions, digest `670428059f0d9a0391aeb07955be27e850709e73be7d641a32a3008a7249b115`.
- Production build: passed.
- Broader non-agent-tools suite: 390 tests passed and 1 skipped. The deterministic producer reimport requires an explicitly configured pinned producer checkout.
- GitHub Actions did not execute any steps because of the account-level Actions/minutes condition; the merge used the complete local verification above.

# Demonstrated boundary

This proves source-backed agent authoring, human operational acceptance, portable runtime behavior, and a close Simpler presentation for this form. It does not claim production backend, persistence, authentication, submission, or XML-delivery parity. The agent currently receives normalized PDF text plus an exact PDF provenance receipt; page-image inspection remains handled by the existing PDF visual-evidence pipeline.

[depends on](async-codex-authoring-job-interface.md)

[depends on](implement-pdf-visual-evidence-pipeline.md)
