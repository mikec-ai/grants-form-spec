---
type: Task
title: Make form banking safe and measured by default
priority: P1
description: >-
  Harden the existing additive promotion path so routine local and hosted use
  cannot accidentally replace the bank, skips redundant work, runs native
  gates, and emits comparable elapsed-time receipts.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T01:38:10Z'
---
# Goal

Turn the existing supervised promotion machinery into the obvious one-command path for banking a newly merged portable form.

# Acceptance criteria

- Routine documentation and examples use `--add-forms`; exact selection replacement is renamed or requires an explicit destructive-intent flag.
- Promotion starts from a fetched clean consumer `origin/main` and records the base SHA.
- The receipt reports added forms, removed forms, selected artifact count, producer SHA, bundle hash, start/end timestamps, and elapsed time by build, selection, verification, and consumer-test phase.
- Ordinary additive promotion fails if any previously selected form or artifact closure is removed.
- The workflow checks for open promotion PRs and shared-hotspot overlap before local manual promotion.
- Repository-native format/lint/test targets are part of the documented local gate; Ruff alone is not treated as the SGG format gate.
- A verified producer bundle is cached or downloaded by immutable SHA so retries do not rerun the same full producer preflight unless the cache is absent or invalid.
- The NIFA run can be replayed as one additive invocation without manual reconstruction of the 32-form selection.

# Evidence

The NIFA run used exact `--form` selection instead of the already-available additive option, briefly proposed deleting 12 banked forms, reran producer preflight multiple times, and later failed hosted formatting because local checks omitted `isort`.

[depends on](automate-cross-repo-form-promotion.md)

[informed by](../context-notes/nifa-supplemental-banking-retrospective.md)
