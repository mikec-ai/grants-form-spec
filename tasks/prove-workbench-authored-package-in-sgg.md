---
type: Task
title: Prove a workbench-authored package in the SGG consumer
priority: P0
assignee: Codex
description: >-
  Export a human-accepted workbench draft through the portable package boundary
  and verify it in the actual Simpler.Grants.gov consumer without moving
  authoring code downstream.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-28T01:35:18.840Z'
---
# Scope

Prove that a form package produced from the neutral workbench authoring path can cross the existing `resolved-form-package/v1` boundary and load in the actual Simpler.Grants.gov consumer without importing workbench or agent-authoring code.

# Acceptance criteria

- Select one source-dossier proof form that already has a trusted SGG comparison target.
- Export the human-accepted workbench draft as a complete, digest-bound resolved package rather than substituting the existing producer oracle.
- Load the exported package through the SGG consumer's generic resolved-package loader.
- Compare the resulting native Simpler form artifacts and supported behavior against the existing SGG form or oracle, recording intentional differences separately.
- Add automated cross-boundary fixtures or tests at the narrowest reusable seam; do not add form-specific loader or renderer branches.
- Keep semantic mappings proposed/unreviewed and preserve exact source, agent, human-decision, compiler, and package provenance.
- Document whether any incompatibility belongs to the producer/exporter contract or the SGG consumer.

# Result

The proof is implemented with Attachment Form 1.2.

- Workbench PR #46 merged at `196c1b67aed0c598676cb3871882439ac309ec45`.
- SGG proof PR #144 merged at `ff411247d01b88f39d4e35ac7c7d434be49dc6d4` from final branch head `e38f326b1173b1e7bce906f09bcf3dfdf1c9ec34`.
- A generic `@grants-form-workbench/adapter-sgg` projects portable UI and explicit attachment widgets into SGG-native UI/rule artifacts without selecting forms by ID or importing producer/SGG runtime code.
- A generic `grants-form-export-sgg` command writes a digest-bound SGG artifact tree, is idempotent, refuses differing overwrites without `--force`, and can preserve a separately hashed agent/human/compiler provenance bundle.
- The end-to-end workbench test applies 17 accepted recommendations, compiles 2 source-backed content blocks plus 15 attachment occurrences, records 17 human-decision receipts, preserves all 15 semantic mappings as proposed, and reaches exact supported portable parity.
- The SGG proof loads the exported tree through `_load_banked_form` and matches the existing Attachment Form schema, UI schema, and rule schema exactly.

# Verification receipts

- Workbench root TypeScript typecheck: passed.
- Adapter/authoring proof: 4 tests passed.
- Export command: 4 tests passed.
- SGG focused consumer/parity/XML cohort: 7 tests passed.
- SGG Ruff check and format: passed.
- SGG CI formatting and lint stages passed after the final branch repair; broad API and E2E jobs continued as post-merge signals.
- Workbench GitHub Actions job failed before running any steps; local targeted verification is green. The broader agent-tools suite also has unrelated stale-golden failures already present on the branch baseline.

# Architecture finding

The incompatibility was an exporter/target-projection gap, not an SGG runtime-loader gap. The neutral package already carried the schema, UI intent, question occurrences, review state, and source provenance. SGG additionally requires its own section vocabulary and rule schema. Keeping that translation in a separate edge-adapter package preserves the intended boundary: author once, project per consumer, and keep SGG unaware of agent/workbench implementation details.

# Guardrail

The first adapter slice deliberately supports only the portable UI vocabulary proven by this form. Nested layouts and unknown UI elements fail closed instead of being flattened or guessed. Expand those capabilities family-by-family with parity tests.

[depends on](generalize-source-authoring-dossier.md)
