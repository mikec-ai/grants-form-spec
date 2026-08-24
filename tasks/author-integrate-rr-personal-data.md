---
type: Task
title: Author and integrate R&R Personal Data
priority: P1
description: >-
  Bank a high-use, bounded person-data form using role-qualified identity reuse
  while keeping privacy-sensitive semantics and production release gated.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T00:38:09.000Z'
---
# Goal

Author R&R Personal Data declaratively as a controlled test of role-qualified person and identity reuse without conflating structurally similar demographic or biographical concepts.

# Evidence starting point

- Two-year usage evidence records 39,237 form instances.
- The research factory records 25 question/structure records and 54 behavior records across two person-role models.
- One policy-sensitive item remains blocked and must not be inferred from structural similarity.

# Acceptance criteria

- Pin and promote exact official XSD, DAT, PDF/XFA, instructions, versions, and hashes.
- Reuse canonical person and identity questions only where role, subject, purpose, constraints, and XML meaning match.
- Preserve demographic, biographical, privacy, and access-control distinctions as explicit semantic and policy evidence.
- Resolve or explicitly retain the blocked policy-sensitive item without fabricating behavior.
- Validate representative role, optionality, invalid, save/reload, locked/print, and XML/XSD cases.
- Add no form-specific compiler, adapter, loader, renderer, or conformance branch.
- Permit source-conformant consumer banking before release approval, but do not register or expose the form until privacy, policy, accessibility, lifecycle, and operational gates pass.
- Record marginal effort and every reused versus newly introduced artifact.

# Scope boundary

Banking source-bound artifacts is separable from handling production applicant data. Privacy review gates runtime enablement, not faithful declarative authoring.

[consumer delivery follows](automate-cross-repo-form-promotion.md)
