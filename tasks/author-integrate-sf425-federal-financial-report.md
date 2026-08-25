---
type: Task
title: Author and integrate SF-425 Federal Financial Report
priority: P2
assignee: codex_sf425_producer
description: >-
  Create the currently absent SF-425 while explicitly establishing its reporting
  lifecycle and consumer boundary.
superbee_progress_status: in_progress
superbee_updated_by: codex-scanner-defect-review
generated:
  by: 'process:superbee'
  at: '2026-08-25T12:44:59.769Z'
---
# Goal

Author the SF-425 Federal Financial Report as a source-evidenced portable form and determine its correct consumer/runtime boundary before banking or registration.


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

# Claim — 2026-08-25

- Claimed by `codex_sf425_producer` after auditing the canonical catalog, active worktrees, branches, and pull requests. No existing SF-425 producer branch or PR was found.
- The first slice is deterministic source/provenance and source-declared structure only. The crosswalk cache identifies `SF425_3_0-V3.0.xsd` with SHA-256 `0f5cd6705399fb4c2dd4310150de49e3f9f0abd00349d3bc2983aa9bc13eee69` and `SF425_3_0-V3.0_F751.xls` with SHA-256 `6f44d8d685dd84f28df66b390f79d237b78a26a81e4ca1b412df1c39f429eb7d`.
- There is no stable Simpler legacy runtime oracle. Semantic mappings remain proposed and unreviewed; application lifecycle, runtime behavior, consumer readiness, banking, and registration must not be inferred from the source inventory.
