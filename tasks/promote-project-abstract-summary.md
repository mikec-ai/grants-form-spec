---
type: Task
title: Promote Project Abstract Summary through the crosswalk staging seam
priority: P0
assignee: codex
description: >-
  Project Abstract Summary now compiles from revision-pinned crosswalk evidence
  through the portable form specification; the public Simpler fork has a merged
  parity canary while its existing XML-capable implementation remains runtime
  authority.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T20:54:54.386Z'
---
# Result

- Producer PR #18 merged to `main` at `3c36c6987`; the canonical package pins crosswalk revision `dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef`.
- Deterministic promotion staged 6 source records, 10 source behaviors, 3 exact provenance sources, 5 open review gates, and 6 semantic proposals. It accepted zero semantic mappings.
- The portable form composes five questions, including a direct-text Project Abstract question. It uses no attachment capture mechanism.
- A generic form-use constraint now preserves the genuine Project Title variation: 250 characters here, 200 on SF-424 and SF-424 Short, with no global constraint incorrectly attached to the shared question.
- Public-fork adapter PR #13 merged to `main` at `788185921`. UI and rules match the existing Simpler implementation; generated validation behavior matches across the mutation corpus.
- Three source-derived field descriptions are explicit applicant-visible additions, not silently treated as parity.
- Simpler's existing Project Abstract implementation remains registered because the portable contract does not yet emit its XML mapping. The canary records that boundary instead of discarding XML behavior.
- Producer preflight passed with 410 reproducible artifacts, 56 TypeScript tests, and 24 Python tests. Adapter form-spec tests, Ruff, formatting, and mypy passed.
- No HHS upstream state changed.

[depends on](spike-crosswalk-promotion-importer.md)
