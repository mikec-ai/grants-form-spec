---
type: Task
title: Implement deterministic source-evidence authoring scaffolder
priority: P0
assignee: Codex
description: >-
  Add a design-time agent CLI that converts pinned deterministic form extraction
  into a strict portable-form authoring draft, without adding runtime or
  renderer dependencies. Prove the boundary on a second genuinely new form.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T16:12:35.098Z'
---
# Scope

Build the scaffolding step between deterministic extraction evidence and the existing portable-form authoring compiler. The output is a reviewable draft, never semantic authority.

# Acceptance evidence

- Design-time package only; an architecture test forbids consumer/runtime dependencies on agent-tools.
- Exact input and per-record provenance survive in machine-readable source annotations and receipts.
- Similar wording never auto-promotes semantic equivalence.
- Every generated source question remains unreviewed.
- Unknown flags and unsupported or unprovenanced records fail closed with structured TOON and exit code 2 or 1.
- PHS Additional Indirect Costs, absent from the portable baseline, now scaffolds, compiles, catalogs, and renders through both consumer presets.
- The proof preserves two nested repeatable levels and row requiredness; 12 applicant-question occurrences remain unreviewed, 30 behavior records remain deferred, and 4 technical attachment-transport fields are excluded from applicant-question counts.
- PR #26 (foundation): https://github.com/mikec-ai/grants-form-workbench/pull/26, merged as 4dd19a119fc52c92ffc6ca074619f2d38bc17d4c.
- PR #27 (new-form proof): https://github.com/mikec-ai/grants-form-workbench/pull/27, merged as 716919a04454e6941642020d2d8732749fd9a801.
- Local verification: 51 agent-tool tests and 92 architecture/two-preset rendering checks passed; TypeScript passed; catalog current at 28 forms across 3 cohorts. GitHub CI on both PRs had zero executed steps because the account billing gate refused job startup.
