---
type: Task
title: Compile accepted agent form without oracle substitution
description: >-
  Extend the neutral agent exchange with occurrence-level authoring and prove
  the accepted draft compiles into the rendered PHS preview.
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-28T00:21:08.209Z'
priority: P1
assignee: Codex
superbee_progress_status: done
---
# Scope

Remove the PHS reference demo's oracle-substitution shortcut. Extend the neutral authoring exchange so an agent can propose exact field occurrences, let a human accept those recommendations into the working draft, compile that draft through the generic portable compiler, and compare the result with the known PHS package strictly as an oracle.

# Acceptance criteria

- The exchange supports repeated field occurrences with explicit path, question ID, label, description, presentation widget, cardinality, and proposed review state.
- Validation fails closed for unknown questions, duplicate paths, unsupported paths, or malformed presentation metadata.
- Accepted recommendations compile into the package used by the applicant preview; the oracle is never substituted as the preview package.
- The PHS source dossier supplied to the agent excludes the oracle package and retains exact source provenance.
- A machine-readable parity report distinguishes exact matches, intentional provenance differences, and unresolved differences.
- Tests cover the generic contract, repeated occurrences, review boundaries, compiled preview, and parity report.

# Authority boundary

Human acceptance applies recommendations to a working draft only. It does not semantically approve mappings, affect published coverage, or approve a form for production.

# Outcome

Completed and merged in [grants-form-workbench PR #44](https://github.com/mikec-ai/grants-form-workbench/pull/44), merge commit `88abc6a9460f91ff0183e2d0c8b8d954a8fd34ae`.

- Added the neutral `add-field` operation for exact field occurrences, including repeated use of a semantic question at distinct paths.
- Withheld the known portable package from the agent. The agent received five digest-bound evidence references: four pinned source artifacts and the deterministic source dossier.
- Applied explicit human acceptance decisions through the authoring exchange and compiled the resulting draft through the generic portable compiler.
- Rendered the compiled candidate in the applicant preview. The oracle is used only afterward for a machine-readable comparison.
- Kept `semanticReview` and `responseRoleReview` at `proposed`; operational acceptance did not change semantic authority or published coverage.

# Exact receipts

- Live Codex run: 13 `add-field` recommendations, 13 compiled runtime fields, 5 unique question-bank concepts, all 13 expected paths matched, and every occurrence remained proposed.
- Focused implementation suite: 52 tests passed across the authoring workspace, exchange, runner, source demo, and end-to-end portal.
- Broad verified suite: 392 tests passed and 2 documented tests skipped when the external producer checkout was explicitly omitted.
- Type checks, question-catalog integrity, production build, and diff checks passed.
- Question catalog: 152 exact records; SHA-256 `670428059f0d9a0391aeb07955be27e850709e73be7d641a32a3008a7249b115`.
- GitHub Actions run `33129370236` failed before executing any steps because the account cannot start the job; it is not a code/test failure. The merge used the complete local verification receipts above.

[depends on](demo-evidence-to-simpler-preview-workflow.md)
