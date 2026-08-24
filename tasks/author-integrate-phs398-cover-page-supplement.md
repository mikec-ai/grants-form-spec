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
  at: '2026-08-24T02:40:21.276Z'
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
- Model animal euthanasia, program-income detail, stem cells, fetal tissue, inventions, change-of-organization workflow, prior investigator identity, attachments, and related HHS policy as declarative, versioned content.
- Reuse shared primitives and blocks only where role-qualified semantic evidence supports them; preserve policy-specific meanings and provenance.
- Express source-backed local conditions declaratively and preserve unresolved cross-form/application-context behavior without invention.
- Validate schema, exact XML/XSD, semantic identity, reuse analysis, evidence, and bounded accessibility/privacy boundaries.
- Add no form-specific compiler or adapter branch.
- Register only after applicable HHS policy, semantic, accessibility, instruction, and operational gates pass.

# Exit evidence

- Draft producer PR: https://github.com/mikec-ai/grants-form-spec/pull/67
- Exact head: `d2bfdc0db9ae070b920572faf1cbd1148ad79b57`.
- Added one declarative form with 33 canonical occurrences and ten new role-qualified HHS policy question identities.
- Reused generic Yes/No vocabulary, `ResearchBudgetAmount14`, person-name and organization-name shapes, and one generic attachment capture mechanism. The two HFT attachment questions remain semantically distinct.
- Preserved all 24 official DAT condition rows. Thirteen exact local UI condition targets compile; remaining DAT capture/navigation/clearing behavior is source-bound uncompiled. Six additional Forms-I cross-form/application-profile conditions are source-bound uncompiled. No calculations are claimed.
- Exact minimal, comprehensive, and boundary Grants.gov XML validates against the pinned full XSD closure. Applicant constraints and XSD envelope conflicts remain explicit.
- Full producer preflight passed: 109 TypeSpec tests and 251 Python tests, 2 skipped; artifact, promotion, packaging, and classified-field gates passed.
- Semantic mappings remain proposed and publish-ineligible.
- Unresolved gates: hESC mutual exclusion/clearing; R&R OPI and R&R SF-424 cross-form applicability; New/Revision restrictions; multi-project and training aggregation/discard behavior; HFT filename validation; stale-value handling; accessibility, privacy, save/reload, locked/print, and production review.
- No generic contract change and no form-specific compiler, adapter, runtime, or policy DSL branch were added.

This profile establishes policy-specific semantic blocks and role-qualified identity reuse that can inform a later Fellowship Supplemental implementation without creating a general policy DSL.

[depends on](release-rr-key-person-expanded-canary.md)
