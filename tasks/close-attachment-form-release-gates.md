---
type: Task
title: Close Attachment Form release gates
priority: P1
description: >-
  Prove the banked Attachment Form through legacy differential parity, consumer
  lifecycle, accessibility, and release gates.
superbee_progress_status: in_progress
generated:
  by: 'process:superbee'
  at: '2026-08-24T23:37:57.371Z'
assignee: attachment_release
---
# Goal

Close the remaining differential-parity and release gates for the already-banked Attachment Form while preserving one generic ordered-attachment composition.

# Delivered baseline

- Fifteen positional slots compose one reusable ordered-attachment mechanism and shared attachment wire mapping.
- Empty, sparse, full, replacement, removal, and XML/XSD producer cases pass.
- The exact official XSD and portable artifacts are present in the generic consumer bank.
- Production registration remains unchanged.

# Acceptance criteria

- Run portable and legacy implementations against shared empty, single, maximum, ordering, replacement/removal, invalid-attachment, and submission fixtures.
- Exercise attachment ownership and audit behavior, save/reload, locked/print, and lifecycle transitions in the real consumer.
- Complete keyboard, screen-reader, instruction, semantic, and release review.
- Classify every legacy difference as a source correction, approved presentation change, unresolved decision, or regression with evidence.
- Record a catalog browser and differential-parity receipt before any registration cutover.
- Add no Attachment Form-specific compiler or adapter branch.

# Boundary

Official sources remain semantic authority; the legacy implementation is a differential behavior oracle only.

[depends on](migrate-attachment-form-parity-oracle.md)

[depends on](add-portable-form-preview-registration.md)

[depends on](run-portable-catalog-browser-matrix.md)

[depends on](build-uniform-legacy-differential-parity.md)

[depends on](enforce-evidence-backed-parity-deltas.md)

# Automated handoff evidence (2026-08-24)

Consumer PR: [mikec-ai/simpler-grants-gov#88](https://github.com/mikec-ai/simpler-grants-gov/pull/88), head `e54b80587`.

- One shared, source-shaped fixture corpus covers empty, single, sparse/out-of-order, maximum, invalid, and replacement responses.
- The banked portable package matches the existing Simpler Attachment Form oracle for UI schema, rules, rendered fields, and tested behavior. Raw schema differences are mechanically bounded to portable `description` metadata.
- DB-backed consumer tests cover save/reload, slots 1/5/15, replacement, removal, attachment deletion state, exact add/delete audit events, foreign-attachment ownership warnings, successful submission, and post-submission update lockout.
- XML evidence proves out-of-order input serializes as `ATT1`, `ATT5`, `ATT15` and validates against the exact bundled `AttachmentForm_1_2-V1.2.xsd`.
- Bounded lower-environment browser automation covers 15 ordered controls, source instructions, upload, save/reload persistence, replacement/removal, read-only print output and section order, keyboard reachability, and Axe WCAG 2 A/AA plus 2.1 A/AA scanning.
- No production registration, shared runtime, compiler, or adapter changes were made.

Local receipts: five parity/XML tests passed; three DB lifecycle tests passed; isort, Black, Ruff, targeted mypy, frontend Prettier, and frontend ESLint passed; Playwright discovered the test in Chromium, Firefox, WebKit, and Mobile Chrome. Current hosted CI has passed frontend build, lint/type/format/tests, Storybook build, change classification, API image build, and Playwright caching. API checks, Pa11y, and four E2E shards are still running; hosted CI remains the full browser execution receipt.

# Gates deliberately still open

- Human keyboard and screen-reader review.
- Human instruction, semantic, policy, and release review.
- Final catalog browser receipt and hosted CI confirmation.
- Any registration cutover decision; production registration remains unchanged.

Automated checks support handoff but do not constitute human semantic, accessibility, policy, or release approval.

## Hosted closure receipt — 2026-08-24

- Consumer evidence PR [88](https://github.com/mikec-ai/simpler-grants-gov/pull/88) merged at `2026-08-24T22:42:13Z`.
- Bounded run [32783471054](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32783471054) proved preview registration, adapter/API preflight, apply render, initial save/reload, and print render in Chrome, Firefox, WebKit, and mobile Chrome.
- The remaining bounded-run findings were attributed to the shared catalog harness, not Attachment Form: attachment controls were misclassified as editable scalars and Axe included the developer-only test-user selector. Generic repair is isolated in consumer PR [94](https://github.com/mikec-ai/simpler-grants-gov/pull/94).
- Human screen-reader, semantic, policy, and release approvals remain open; the merge records automated handoff evidence and does not imply those approvals.

## Post-harness-repair browser receipt — 2026-08-24

- Main run [32788458690](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32788458690) passed the generic Attachment Form catalog plan in Chrome, Firefox, WebKit, and mobile Chrome: preview registration, adapter/API preflight, Apply render, save/reload, accessibility, and print render all passed.
- Schema implication is not applicable for this form. The workflow-level red result comes from the separate form-specific release spec, not these four generic receipts.
- Human screen-reader, semantic, policy, and release approvals remain open.
