---
type: Task
title: Migrate SF-424B through the portable parity oracle
priority: P1
description: >-
  Replace legacy SF-424B with a portable versioned assurance-policy bundle and
  differential SGG parity.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T15:53:42.231Z'
---
# Goal

Replace SGG's legacy SF-424B with portable declarative artifacts and establish the versioned assurance-policy bundle pattern.

# Evidence starting point

- The research factory records seven source question/structure records, 36 behavior records, and nineteen static-policy items.
- SGG already provides schema, UI, rules, XML mappings, the official XSD, instructions, fixtures, and lifecycle tests.

# Acceptance criteria

- Pin exact official source versions/hashes and the legacy SGG oracle revision.
- Model the assurance text as a versioned authoritative policy bundle with an acceptance/signature envelope, not as nineteen generic questions.
- Keep policy provenance, presentation, signature, acceptance date, technical version, and XML mapping independently inspectable.
- Run acceptance, missing-signature, version, read-only policy, XML, save/reload, locked/print, and submission fixtures through both implementations.
- Validate XML against the exact official XSD and classify all parity differences.
- Add no SF-424B-specific compiler or adapter branch.
- Register only after policy ownership, accessibility, instruction, and release gates pass.

# Exit evidence

Record which assurance-shell artifacts can be reused by SF-424D and its Mandatory and Individual variants without conflating their policy bundles.

[depends on](release-rr-key-person-expanded-canary.md)
