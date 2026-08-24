---
type: Task
title: Author and integrate PHS 398 Cover Page Supplement
priority: P1
description: >-
  Compose a source-bound, versioned HHS research-policy profile from shared
  application, identity, budget, and attachment foundations.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T02:52:10.666Z'
assignee: cover_page_supplement_agent
---
# Goal

Author PHS 398 Cover Page Supplement as a versioned HHS research-policy profile composed with existing application, organization, budget, attachment, and identity foundations.

# Evidence starting point

- Official FID 698, version 5.0, OMB 0925-0001.
- Exact physical XSD, DAT, read-only PDF, XFA PDF, XFA packet, and NIH Forms-I guide hashes are pinned without OCR.
- Factory-derived inventories remain implementation evidence: 38 XSD question/structure records, 56 DAT rows, 37 normalized behavior records, and 22 partial runtime effects.

# Acceptance criteria

- Pin and promote exact official XSD, DAT, PDF/XFA, instruction, version, and hash evidence.
- Model the policy questions as declarative, versioned content with role-qualified reuse.
- Preserve source-backed local conditions and unresolved cross-form/application-context behavior without invention.
- Validate exact XML/XSD, semantic identity, reuse analysis, evidence, and bounded accessibility/privacy boundaries.
- Add no form-specific compiler or adapter branch.

# Exit evidence

- Draft producer PR: https://github.com/mikec-ai/grants-form-spec/pull/67
- Rebased exact head: `14ffe06b8a6a26e6597902e9763590011eb09d50` on producer main `70fa65f82f66901f8a6a330aa8ef70479ded9b5e`.
- Physical root fixture SHA-256 is exactly `ec538c9bb5fd233c36ac73ca567d31e60779ee3df2f3c7b456d9395b3ec2dc26`, byte-identical to the official captured XSD, the XML profile, and root evidence record. The new 28-profile generic reconciliation gate passes.
- Added one declarative form with 33 canonical occurrences and ten new role-qualified HHS policy question identities.
- Reused generic Yes/No vocabulary, `ResearchBudgetAmount14`, person-name and organization-name shapes, and one generic attachment capture mechanism. The two HFT attachment questions remain semantically distinct.
- Preserved all 24 official DAT condition rows. Thirteen exact local UI condition targets compile; remaining DAT capture/navigation/clearing behavior is source-bound uncompiled. Six additional Forms-I cross-form/profile conditions are source-bound uncompiled. No calculations are claimed.
- Form-scoped `enabledWhen` overrides now emit generically into canonical portable UI and the SGG target from one shared normalized parser. Equals and set-membership cases have regressions; intrinsic/override collisions fail closed. No form-specific branch was added.
- Full producer preflight passed after rebase: 110 TypeSpec tests and 260 Python tests, 2 skipped; XSD reconciliation, artifact, promotion, packaging, and classified-field gates passed.
- Semantic mappings remain proposed and publish-ineligible.
- Unresolved gates: hESC mutual exclusion/clearing; cross-form/application type; multiproject/training aggregation/discard; filename policy; stale values; a11y/privacy/operational/production review.

This profile establishes policy-specific semantic blocks and role-qualified identity reuse that can inform a later Fellowship Supplemental implementation without creating a general policy DSL.

[depends on](release-rr-key-person-expanded-canary.md)
