---
type: Form Usability Run
title: SF-424 — encoded revision verification
form_id: sf424
scenario: encoded-revision-persistence/v1
environment: 'local signed-in Simpler preview at localhost:3000'
runtime_commit: b147f0acf23bd1de9c7bd3853a31067ce2d1baef
assignee: codex
producer_commit: 7c3be8e32968b49b5ce48f53a832c00220eb5bee
artifact_manifest_digest: 2a2aec94910ea74870cebba34c2667c0e62dd21ce6452099f795dcd1c1e6b245
browser_scope: Desktop Chromium via Codex in-app browser
result: pass
superbee_progress_status: complete
superbee_updated_by: codex
---
# Intent

Verify the repaired generic encoded-checkbox flow in the portable SF-424 form.

# Preconditions and provenance

- Exact tested head: `b147f0acf23bd1de9c7bd3853a31067ce2d1baef`; merged consumer commit: `00d9f61cd13032b4cdbae9089439c9cac5c5b290`.
- Selected producer revision: `7c3be8e32968b49b5ce48f53a832c00220eb5bee`.
- Form manifest SHA-256: `2a2aec94910ea74870cebba34c2667c0e62dd21ce6452099f795dcd1c1e6b245`.
- Local signed-in desktop Chromium preview.

# Scenario steps

1. Select Application type Revision.
2. Select revision choices A and D.
3. Verify conflicting B and C choices remain disabled by the source-approved contract.
4. Save and navigate to the same form again.

# Evidence

- The hidden wire value was exactly `AD`.
- A and D remained selected after save/reload.
- B and C remained disabled as required by the encoded-combination contract.
- Focused TypeScript and widget/form tests passed before merge.

# Outcome and follow-up

Pass. The generic repair is merged and verified; no SF-424-specific renderer branch was added.

[discovers](../usability-findings/sf424-revision-selection-disappears-on-rerender.md)

[verifies](../shared-defects/encoded-checkbox-state-races-conditional-rerender.md)

[validates](../tasks/synchronize-encoded-checkbox-form-state.md)
