---
type: Task
title: Bank the SF-424B assurance profile family
priority: P1
assignee: sf424b_family_agent
description: >-
  Publish active R&R, Individual, and verified Mandatory SF-424B profiles over
  one portable assurance bundle.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T19:52:13.437Z'
---
# Goal

Bank the active SF-424B assurance variants as versioned profiles over one portable non-construction assurance bundle after the base SF-424B migration establishes the contract.

# Scope

- R&R SF-424B v1.1 (FID 325)
- Individual SF-424B v1.1 (FID 521)
- Mandatory SF-424B v1.1 (FID 328), subject to an explicit current-status check

# Acceptance criteria

- Pin official XSD, DAT, instructions, form identity, version, and hashes for every profile.
- Verify policy text, editable versus prepopulated ownership, labels, and XML namespaces independently; do not infer semantic equivalence from matching wire shapes.
- Reuse one reviewed policy/attestation model and shared identity/signature primitives; keep profile differences declarative.
- Produce separate portable manifests and XML profiles without form-specific adapter branches.
- Exercise differential schema, UI, lifecycle, locked/print, submission, XML, and XSD parity where an SGG oracle exists.
- Do not register a profile until technical, human, policy, and operational gates are recorded.

[depends on](migrate-sf424b-parity-oracle.md)
