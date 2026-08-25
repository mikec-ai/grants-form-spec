---
type: Task
title: Author and integrate SF-425 Federal Financial Report
priority: P2
assignee: root_sf425_boundary
description: >-
  Create the currently absent SF-425 while explicitly establishing its reporting
  lifecycle and consumer boundary.
superbee_progress_status: in_progress
superbee_updated_by: root_sf425_boundary
generated:
  by: 'process:superbee'
  at: '2026-08-24T11:50:59.142Z'
---
# Goal

Author the SF-425 Federal Financial Report as a source-evidenced portable form and determine its correct consumer/runtime boundary before banking or registration.

## 2026-08-24 bounded claim

- `root_sf425_boundary` claims only the source-backed reporting-lifecycle and consumer-boundary
  assessment. This lane must not author or register the form until the correct runtime boundary is
  established, and it must not assume the application-form lifecycle is authoritative.

# Verified starting state

SF-425 is absent from the current 39-form producer catalog and consumer bank. Because it is a financial-reporting form rather than an ordinary application component, the task must not assume that the existing application-form lifecycle is the correct production target.

# Acceptance criteria

- Pin exact official XSD, DAT, PDF/XFA, instructions, and applicable reporting-policy sources with versions and digests.
- Establish the intended lifecycle and consumer boundary explicitly before treating Simpler application behavior as authoritative.
- Keep deterministic extraction separate from proposed semantic question mappings.
- Reuse financial, organization, period, and certification concepts only where semantic evidence supports equivalence.
- Compile portable artifacts generically and prove schema, UI, calculations/conditions, and XML/XSD behavior without form-specific compiler logic.
- If banked in Simpler, keep it unregistered until the reporting lifecycle, accessibility, policy, and release gates are accepted.
- Record genuinely new reporting capabilities and marginal implementation effort.
