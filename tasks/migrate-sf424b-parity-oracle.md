---
type: Task
title: Migrate SF-424B through the portable parity oracle
priority: P1
description: >-
  The portable, unregistered SF-424B implementation and public-fork consumer
  canary are merged; remaining human and release work is tracked in Close
  policy-form release gates.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:43:36.435Z'
assignee: sf424b_family_agent
---
# Goal

Replace SGG legacy SF-424B with portable declarative artifacts and establish the versioned assurance-policy bundle pattern.

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

The generic `form-policy-binding/v1` contract, versioned policy content, submission acceptance envelope, response roles, section presentation order, shared AOR/organization primitives, and declarative XML-profile machinery are reusable by SF-424D. SF-424D PR 51 was built directly on the merged SF-424B foundation and uses the same generic projector and contract.

# Implementation receipts

- Producer PR 50 merged green: https://github.com/mikec-ai/grants-form-spec/pull/50
- Immutable producer merge revision: `bc1d60325e52fbffd782756ec40c9dba232fd978`.
- Legacy SGG oracle pinned at revision `30dd50cf`, path `api/src/form_schema/forms/sf424b/form_json.py`, SHA-256 `ca94f236d449f5e4437d03c33ebe09504fe1d02948d7bb17d16fc4a646d7d39a`.
- Base XSD SHA-256: `b0da616d262329e869b7c2a12146396fd8a279d2a1723521271c519f4571075d`.
- Consumer PR 46 merged clean: https://github.com/mikec-ai/simpler-grants-gov/pull/46
- Immutable consumer merge revision: `a90910022ac1ea57e9f417a605f9546eef29aa6b`; producer pin inside is exactly `bc1d60325e52fbffd782756ec40c9dba232fd978`.
- Consumer tests cover oracle constraints, source-correct ownership deltas, missing signature/date before submission, submission population, locked/print shape, exact XML/XSD, artifact locks, and absent registration.
- Local validation: 52 relevant non-DB tests passed; changed-file Ruff and formatting checks passed; mypy passed for 742 source files. DB-backed lifecycle tests are committed; local execution was unavailable because `grants-db` was absent.

# Remaining gates

- Semantic and policy-owner review.
- Accessibility review.
- Hosted consumer lifecycle execution.
- Instruction UUID assignment.
- Explicit production registration.

The task remains in progress; no profile is registered.

[depends on](release-rr-key-person-expanded-canary.md)
