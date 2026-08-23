---
type: Task
title: Migrate Grants.gov Lobbying Form through the portable parity oracle
priority: P1
description: >-
  Replace the legacy Grants.gov Lobbying Form while reusing reviewed identity
  and attestation primitives without conflating it with SF-LLL.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T15:53:42.558Z'
---
# Goal

Replace SGG's legacy Grants.gov Lobbying Form with portable artifacts as a derivative of the SF-LLL disclosure and shared identity/attestation foundations.

# Evidence starting point

- The research factory records eleven source question/structure records, twenty behavior records, four static-policy items, and four proposed components.
- SGG already provides schema, UI, rules, XML mappings, the official XSD, fixtures, and lifecycle behavior.
- Two-year usage evidence records 39,941 form instances.

# Acceptance criteria

- Pin exact official source versions/hashes and the legacy SGG oracle revision.
- Reuse reviewed identity, representative, signature, date, and attestation primitives without importing SF-LLL-specific disclosure semantics.
- Preserve the Grants.gov Lobbying Form as its own versioned certification profile.
- Run complete, missing-attestation, signature/date, application-context, XML, save/reload, locked/print, and submission fixtures through legacy and portable implementations.
- Validate XML against the exact official XSD and classify every parity difference.
- Add no form-specific compiler or adapter branch.
- Register only after applicable semantic, policy, accessibility, instruction, and release gates pass.

# Exit evidence

Record actual reuse from SF-LLL and the remaining bounded differences so the disclosure family economics remain falsifiable.

[depends on](migrate-sflll-parity-oracle.md)
