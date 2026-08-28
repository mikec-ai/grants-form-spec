---
type: Task
title: Add portable form-project import and export
priority: P0
assignee: Codex
description: >-
  Define a digest-bound single-project transfer envelope and add safe browser
  import/export without changing producer, renderer, or target-adapter
  boundaries.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-28T11:39:38.782Z'
---
# Outcome

A person can export one exact form-authoring project and import it into another workbench without coupling the authoring contract to browser storage, the agent provider, a renderer, or a target system.

# Scope and acceptance

- Define a digest-bound, versioned single-project transfer envelope separate from the browser project collection.
- Preserve the exact project identity, draft, pinned question-catalog receipt, source provenance, human description, timestamps, and optional review session.
- Reject malformed JSON, unsupported contracts, digest tampering, invalid nested project content, and conflicting imports that reuse an existing project ID with different content.
- Treat an identical repeated import as an idempotent no-op rather than creating a duplicate.
- Fail closed in the UI when an imported project references a different pinned question catalog.
- Add consumer-owned Export project and Import project controls without changing the portable renderer or producer contracts.
- Test contract round trips, tampering, collisions, identical re-imports, successful browser import/export, and mismatch handling.

# Evidence required

Record the merged workbench commit, contract examples, focused and broad test results, a real-browser transfer check, and unrelated infrastructure or baseline failures.

[depends on](persist-human-authored-form-projects.md)

# Completion receipt

- Merged [grants-form-workbench PR #50](https://github.com/mikec-ai/grants-form-workbench/pull/50) as commit `10ec17ebf8685459925e0b64c2308616e42c42e9` on 2026-08-28.
- Added digest-bound `portable-form-authoring-project-transfer/v1` as a single-project exchange envelope separate from the local project collection and browser storage.
- The envelope preserves exact project identity, draft, source and pinned catalog receipts, description, timestamps, and optional review session.
- Import rejects malformed JSON, unsupported contracts, nested project errors, digest tampering, catalog mismatches, and same-ID/different-content collisions. An identical re-import is a byte-stable no-op.
- No-op autosaves now remain byte-stable instead of refreshing `updatedAt`, preventing false transfer conflicts after a resume with no edits.
- Consumer-owned controls export the selected project and import a local project file; no producer, renderer, agent-provider, Simpler, or target-adapter dependency was added.
- Focused lifecycle and UI verification: 40 tests passed. Architecture boundaries: 8 tests passed. Typecheck and production build passed.
- Broad non-agent-tools verification: 419 tests passed and 2 expected producer-fixture tests skipped. One unrelated SF-424 Short state-requiredness assertion failed and reproduces alone; no SF-424, renderer, or behavior code changed in this slice.
- Real-browser evidence: exported an exact human project, imported the separate `Browser transfer proof` envelope, observed both project identities, and resumed the imported project successfully. The UI reported the exact import receipt.
- GitHub Actions run `33167931821` failed before executing any step (`steps: []`; no log was produced). The merge used the local evidence above and records this as runner/account infrastructure, not a product-code signal.
