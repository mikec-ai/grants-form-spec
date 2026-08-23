---
type: Task
title: Migrate SF-LLL through the portable parity oracle
priority: P1
description: >-
  Replace the legacy SGG SF-LLL definition with portable artifacts while using
  legacy schema, UI, rules, XML, XSD, and lifecycle behavior as a differential
  oracle.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T15:53:41.577Z'
---
# Goal

Replace the legacy SGG SF-LLL definition with portable declarative artifacts while using the existing SGG implementation as a differential parity oracle.

# Evidence starting point

- The research factory records 76 source question/structure records, 86 behavior records, one static-policy item, nine proposed components, and sixteen working conditions.
- SGG already provides JSON Schema, UI schema, rules, Grants.gov XML mappings, the official XSD, instructions, fixtures, and lifecycle tests.

# Acceptance criteria

- Pin exact official SF-LLL source versions and hashes and the legacy SGG oracle revision before authoring.
- Promote deterministic evidence into a form-spec sidecar while keeping semantic mappings agent-proposed until reviewed.
- Author disclosure, registrant/client identity, lobbying entities, signature/certification, presentation, conditions, and XML mappings declaratively.
- Reuse canonical identity and contact blocks only where role-qualified semantic evidence supports the mapping.
- Run minimal, fully populated, conditional, invalid, and XML fixtures through both legacy and portable implementations; classify every difference.
- Validate portable XML against the exact official XSD and exercise save/reload, locked/print, and submission behavior.
- Add no SF-LLL-specific compiler or adapter branch.
- Cut registration over only after applicable semantic, accessibility, instruction, and release gates pass.

# Scope boundary

SF-LLL remains distinct from the Grants.gov Lobbying Form. Shared identity and attestation primitives do not imply that the two disclosures are semantically interchangeable.

[depends on](release-rr-key-person-expanded-canary.md)
