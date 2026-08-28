---
type: Task
title: Persist human-authored form projects
priority: P0
assignee: Codex
description: >-
  Extend named projects so human-only drafts autosave and resume before agent
  recommendations exist, with explicit contract migration and unchanged consumer
  boundaries.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-28T11:21:46.570Z'
---
# Outcome

Named projects preserve ordinary human-authored form drafts before any agent recommendation exists, while retaining the same portable-package and target-adapter boundaries.

# Scope and acceptance

- Evolve the project collection through an explicit new contract version; do not silently redefine version 1.
- Preserve exact draft content, form source provenance, question-catalog receipt, description, timestamps, and optional review session.
- Migrate existing version-1 project collections and the older single-session record without deleting either source record.
- Autosave question selection, ordering, and human-authored rules to the active project.
- Create a project when a human starts a new project or first makes a material draft change.
- Resume human-only projects without requiring a source-demo oracle.
- Fail closed when the current question catalog does not match the draft's pinned catalog receipt.
- Add tests for human-only isolation, both migrations, autosave, resume, and unchanged architecture boundaries.

# Evidence required

Record the merged workbench commit, contract migration receipts, focused and broader test results, visual evidence, and any unrelated baseline failures.

[depends on](implement-multi-project-authoring-workspace.md)

# Completion receipt

- Merged [grants-form-workbench PR #49](https://github.com/mikec-ai/grants-form-workbench/pull/49) as commit `780273ca85fe316e7f7088d2d9a6a7722a3c92f5` on 2026-08-28.
- Introduced explicit digest-bound `portable-form-authoring-projects/v2`; version 1 remains a distinct legacy contract and is upgraded only after its original digest and review sessions validate.
- Version 2 preserves the exact portable draft, pinned question-catalog locator and digest, human description, timestamps, and an optional agent-review session.
- The browser workspace now persists an empty named project immediately, autosaves manual question selection, ordering, and human-authored rules, and resumes human-only work without a source-demo oracle.
- Catalog mismatch is fail-closed and tested; neither legacy collection nor legacy single-session source records are deleted during migration.
- Focused architecture, lifecycle, and UI verification: 42 tests passed.
- Broader consumer/runtime verification: 414 tests passed with 2 expected producer-fixture skips because the local producer checkout does not match the pinned historical revision.
- Typecheck and production build passed.
- Real-browser evidence: created an empty project, manually selected `aor/date-signed`, reloaded the page, selected `Untitled form project · 1 selected`, and resumed the exact human-only draft.
- GitHub Actions run `33166789477` failed before executing any step (`steps: []`; no log was produced). The merge used the complete local evidence above and records this as runner/account infrastructure, not a product-code signal.
