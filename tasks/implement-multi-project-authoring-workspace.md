---
type: Task
title: Add multi-project form authoring workspace
priority: P0
assignee: Codex
description: >-
  Turn the single saved authoring review into multiple named, resumable consumer
  projects while preserving the portable-package boundary and exact review
  provenance.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-28T03:23:42.773Z'
---
# Outcome

The standalone consumer can create, name, switch between, and resume multiple form-authoring projects without changing the portable form-package boundary.

# Scope and acceptance

- Introduce a versioned, consumer-neutral project collection around reviewable authoring sessions.
- Keep persistence behind an injected store interface; local browser storage is only the prototype adapter.
- Preserve each session's exact request, recommendation, decision history, revisions, and content digests.
- Migrate the prior single-session browser record into a named project without deleting the legacy record.
- Add UI for creating, naming, selecting, and resuming projects; do not add destructive deletion in this slice.
- Prove two projects remain isolated and resumable through automated tests.
- Preserve renderer, producer, CommonGrants, Grants Standard, and SGG boundaries.

# Evidence required

Record the merged workbench commit, tests, architecture checks, migration behavior, and any intentional limitations. This task depends on the completed reviewable form lifecycle.

[depends on](implement-reviewable-form-lifecycle.md)

# Completion receipt

- Merged workbench PR: https://github.com/mikec-ai/grants-form-workbench/pull/48
- Merge commit: `d3051684faabc1caca9c5b6dc6c85a3aa885479d`
- Portable lifecycle contract: `portable-form-authoring-projects/v1`
- Persistence boundary: injected `AuthoringProjectStore`; browser local storage remains a consumer adapter.
- Migration: an exact legacy `portable-form-authoring-review-session/v1` record is imported once under a stable project ID; the legacy record is not deleted.
- Isolation proof: lifecycle tests preserve different decisions in two named projects, verify collection/session digests, reject tampering, and preserve session provenance across rename.
- Browser proof: the PHS source-authoring flow shows multiple saved projects, resumes the selected accepted preview with oracle parity, and renames the project without changing its session digest.
- Focused verification: 37 lifecycle, workspace-architecture, and browser tests passed; production build passed; visual desktop inspection passed.
- Broader verification: 409 non-agent-tools tests passed with two expected skips when the pinned producer reimport was explicitly skipped. The current external producer checkout is newer than the configured historical revision, and the separate legacy agent-tools receipt suite has existing artifact drift; neither is changed by this slice.
- Boundary result: no renderer, producer, CommonGrants, Grants Standard, SGG adapter, or form-ID-specific branch was added.

# Intentional limitation

Projects currently persist reviewable agent recommendation sessions. Persistence for arbitrary human-only drafts remains a later consumer capability rather than being inferred into this evidence-bound contract.
