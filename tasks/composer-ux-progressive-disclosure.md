---
type: Task
title: Simplify the human-agent composer workflow
priority: P1
assignee: Codex
description: >-
  Apply a bounded live UI/UX review to the form composer: clarify the human
  decisions, progressively disclose rules and provenance, improve question-bank
  scanability, and preserve the neutral authoring boundary.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T21:00:11.824Z'
---
# Acceptance criteria

- Present a clear choose questions → add rules → preview flow.
- Keep raw provenance available without making it primary interface content.
- Explain disabled or unavailable actions in visible language.
- Make question reuse and review status understandable without internal terminology.
- Preserve keyboard-accessible controls and the existing neutral authoring contract.
- Verify the revised flow through interaction tests and a live browser pass.

# Outcome

Completed in `mikec-ai/grants-form-workbench` PR #39 at commit `74bc4110fb003fb48d28e39200249b375e0910a0`.

- Reframed the composer around three human decisions: choose questions, add rules, and try the form.
- Kept exact hashes, IDs, evidence, and technical JSON available behind optional disclosures.
- Replaced internal rule syntax with human-readable conditional statements while retaining machine-readable receipts.
- Added accessible names for reorder controls and clear explanations for actions that are not yet available.
- Added a draft-preview validation mode that suppresses premature errors without changing the renderer default.

# Verification receipts

- 42 focused, renderer, and workspace-architecture tests passed.
- Workspace TypeScript typecheck passed.
- Production build passed for every package.
- Live desktop and phone-sized browser passes completed.
- Conditional preview showed zero premature validation messages before interaction.
- CI created no execution steps; local evidence is authoritative for this change pending restoration of GitHub Actions capacity.

[depends on](implement-visual-form-rule-builder.md)
