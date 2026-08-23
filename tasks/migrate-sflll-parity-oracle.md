---
type: Task
title: Migrate SF-LLL through the portable parity oracle
priority: P1
description: >-
  The portable, unregistered SF-LLL implementation and public-fork consumer
  canary are merged; remaining release gates are tracked separately.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:43:37.021Z'
assignee: codex
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

# Progress (2026-08-23)

- Producer: merged `mikec-ai/grants-form-spec#45` at main commit `7db589062431f3db063e847ddf6bfc2046b38c7b`, after rebasing on lifecycle-correction commit `c4a7fa5e722bca4dd92eb66a887bc2f7f6e0a865`.
- Consumer: merged unregistered canary `mikec-ai/simpler-grants-gov#40` at main commit `30dd50cf0493146c32f89f78398979523e040080`; its artifact manifest pins the merged producer commit exactly.
- Factory evidence: `mikec-ai/grants-question-crosswalk@4312f6504b060e2b9ffdbd2307fc41130c3123a0`; source-set SHA-256 `86c5849f65a3f3d8fcdc7da17cfa6070c185008eae9916184e7d6c32cd098b05`.
- Official SF-LLL 2.0 XSD SHA-256: `fff7449d00c715efb79d83b572bc7b1ef3e8171f6a9ba841436b26242e883664`.
- Portable schema, UI, conditions, lifecycle population, evidence, and XML profile are declarative. The consumer additions are generic support for constants, value maps, dynamic attributes, and compile-time flattened wire groups; there is no SF-LLL-specific compiler or adapter branch.
- Exact-XSD validation passes for a fully populated SubAwardee/material-change response with tier zero and two service individuals. After both rebases, the producer preflight passes 93 TypeSpec tests, 90 Python tests, 750 artifact validations, and the 49-field unclassified ratchet; the consumer non-database regression selection passes 212 tests. Ruff and targeted mypy pass. DB-backed save/reload and submit tests are included for CI because the local PostgreSQL service was unavailable.
- Classified source-correct differences from the legacy oracle include: one-to-ten service individuals instead of one, tier minimum zero instead of one, Federal Action Number maximum 110 instead of 120, and a corrected nested canonical-to-XML mapping.
- Per user direction, production registration is intentionally unchanged. Cutover remains gated on CI, semantic/accessibility/instruction review, full legacy differential classification, and a compatibility or migration decision for persisted legacy response shapes.

[depends on](release-rr-key-person-expanded-canary.md)
