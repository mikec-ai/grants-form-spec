---
type: Task
title: Author and integrate PHS 398 Cover Page Supplement
priority: P1
description: >-
  Compose a source-bound, versioned HHS research-policy profile from shared
  application, identity, budget, and attachment foundations.
superbee_progress_status: done
superbee_updated_by: promote_new_forms
generated:
  by: 'process:superbee'
  at: '2026-08-24T03:15:04.653Z'
assignee: cover_page_supplement_agent
---
# Goal

Author PHS 398 Cover Page Supplement as a versioned HHS research-policy profile composed with existing application, organization, budget, attachment, and identity foundations.

# Exit evidence

- Draft producer PR: https://github.com/mikec-ai/grants-form-spec/pull/67
- Current exact head: `44bbd335ed1114b937d4e2a124a022c40b649540`, rebased on producer main `70fa65f82f66901f8a6a330aa8ef70479ded9b5e`.
- Physical root fixture SHA-256 is exactly `ec538c9bb5fd233c36ac73ca567d31e60779ee3df2f3c7b456d9395b3ec2dc26`, byte-identical to captured official bytes and matching profile/evidence. The 28-profile generic XSD reconciliation gate passes.
- Added one declarative form with 33 canonical occurrences and ten new role-qualified HHS policy identities. Reused generic Yes/No, `ResearchBudgetAmount14`, person/organization shapes, and one attachment mechanism while preserving two distinct HFT attachment semantics.
- Preserved all 24 DAT conditions plus six Forms-I cross-form/profile conditions. Thirteen exact local UI targets compile; unsupported behavior remains source-bound uncompiled. No calculations are claimed.
- Form-scoped `enabledWhen` overrides emit generically into canonical portable UI and SGG using one shared normalized parser. Equals and set-membership cases have regressions. Collisions with intrinsic or inherited visibility, enabled, or read-only behavior fail closed in both emitters; no precedence path can silently ignore or replace a condition.
- Full producer preflight passed: 112 TypeSpec tests and 260 Python tests, 2 skipped; XSD reconciliation, artifact, promotion, packaging, and classified-field gates passed.
- Semantic mappings remain proposed and publish-ineligible.
- Unresolved gates remain explicit: hESC mutual exclusion/clearing; cross-form/application type; multiproject/training aggregation/discard; filename policy; stale values; accessibility, privacy, operational, and production review.
- No form-specific compiler, adapter, runtime, or policy DSL branch was added.

[depends on](release-rr-key-person-expanded-canary.md)

# Consumer banking receipt

Draft public-consumer PR https://github.com/mikec-ai/simpler-grants-gov/pull/60 banks this producer package from immutable revision `778e9b04cd01886593cbbafab1f34b8c8753c2a9`. The artifact/XSD-only delta adds no runtime identity, registration, preview, or form-specific consumer code. Runtime human semantic, policy, instruction, accessibility, lifecycle, and release gates remain open and are not implied by artifact banking.
