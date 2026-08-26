---
type: Form Usability Run
title: PHS Inclusion Enrollment — persistence and repetition pilot
form_id: phs-inclusion-enrollment-report
scenario: core-persistence-and-repeat-entry/v1
environment: 'local signed-in Simpler preview at localhost:3000'
runtime_commit: b147f0acf23bd1de9c7bd3853a31067ce2d1baef
assignee: codex
producer_commit: 7c3be8e32968b49b5ce48f53a832c00220eb5bee
artifact_manifest_digest: a072b156d6cb701f9a65ee03d79ab36dac5580328005cf38ee599d9728616664
browser_scope: Desktop Chromium via Codex in-app browser
result: pass_with_findings
superbee_progress_status: complete
superbee_updated_by: codex
---
---
type: Form Usability Run
title: PHS Inclusion Enrollment — persistence and repetition pilot
form_id: phs-inclusion-enrollment-report
scenario: core-persistence-and-repeat-entry/v1
environment: 'local signed-in Simpler preview at localhost:3000'
runtime_commit: b147f0acf23bd1de9c7bd3853a31067ce2d1baef
assignee: codex
producer_commit: 7c3be8e32968b49b5ce48f53a832c00220eb5bee
artifact_manifest_digest: a072b156d6cb701f9a65ee03d79ab36dac5580328005cf38ee599d9728616664
browser_scope: Desktop Chromium via Codex in-app browser
result: pass_with_findings
superbee_progress_status: complete
superbee_updated_by: codex
---
# Intent

Exercise one bounded applicant workflow in the portable PHS Inclusion Enrollment Report and separate working runtime behavior from unresolved evidence and presentation gates.

# Preconditions and provenance

- Consumer branch commit: `b147f0acf23bd1de9c7bd3853a31067ce2d1baef` in `mikec-ai/simpler-grants-gov` PR #138.
- Selected producer revision: `7c3be8e32968b49b5ce48f53a832c00220eb5bee`; the earlier closure baseline `c484de1862b44bc93bebf2af1af51bedd4a22a6c` remains recorded by the completed release-gate task.
- Selected form manifest SHA-256: `a072b156d6cb701f9a65ee03d79ab36dac5580328005cf38ee599d9728616664`.
- Local signed-in Simpler preview at `http://localhost:3000`, desktop Chromium through the in-app browser.
- Source audit remains agent-reviewed; semantic mapping remains proposed and does not contribute to reviewed coverage.

# Scenario steps

1. Open the first Inclusion Enrollment Report entry.
2. Enter `2` and `3` in the first two planned-enrollment coordinates.
3. Save, navigate to the same URL again, and verify both values persist.
4. Add a second report entry and verify the numeric-coordinate count doubles.
5. Delete the second entry and verify the minimum entry remains.
6. Inspect visible and programmatic coordinate context.

# Evidence

- Initial numeric-coordinate count: 115.
- After save/reload: first two values remained `2` and `3`.
- After adding report 2: 230 numeric controls; its Delete action was enabled.
- After deleting report 2: 115 numeric controls.
- No functional browser exception was observed; development/HMR informational logs were present.
- The UI renders the 115 coordinates sequentially rather than as a visible row/column matrix.
- The form's exact 8 conditions and 28 calculated targets remain source-bound and uncompiled by design; this run did not infer or claim those behaviors.

# Outcome and follow-up

Result: pass with a material presentation/accessibility finding. Persistence and repeat-entry behavior are verified for the bounded scenario. The next reusable fix is a generic matrix-presentation contract spanning producer and shared runtime, followed by this run as a verification pass. Calculation and conditional execution remain separate evidence-closure work.

[discovers](../usability-findings/phs-inclusion-demographic-matrix-loses-grid-context.md)

[validates](../tasks/close-phs-inclusion-enrollment-release-gates.md)
