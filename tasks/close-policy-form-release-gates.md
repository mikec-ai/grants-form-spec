---
type: Task
title: Close policy-form release gates
description: >-
  Complete the human, environment, registration, and operational gates for the
  already-landed assurance and lobbying form bank.
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-25T02:34:19.983Z'
priority: P1
superbee_progress_status: blocked
assignee: human-review
---
# Goal

Close the human, environment-backed, registration, instruction, accessibility, and operational release gates for the already-landed portable policy-form bank.

# Delivered implementation baseline

Producer and public-fork consumer implementations are merged for SF-424B and its active profiles, the SF-424D family, SF-LLL, CD-511, and the Grants.gov Lobbying Form. They remain intentionally unregistered. This task does not reopen their portable declarations, generic compiler, adapter, policy contracts, or exact-source evidence.

# Remaining gates

- Human semantic and policy-owner acceptance where required.
- Instruction-content and accessibility review.
- Provisioned database lifecycle execution where local infrastructure was unavailable.
- Persisted-response compatibility decisions where legacy shapes differ.
- Production FormType metadata, registration, and release approval.

# Current snapshot

The consumer fork contains 28 selected forms pinned to producer revision `e0b0fb24`. Only the five R&R Budget-family profiles are registered. Historical form-count and classification-debt figures in individual delivery receipts are labeled as point-in-time evidence, not current state.

[depends on](migrate-sf424b-parity-oracle.md)

[depends on](migrate-sf424b-profile-family.md)

[depends on](migrate-sf424d-assurance-family.md)

[depends on](migrate-sflll-parity-oracle.md)

[depends on](migrate-cd511-parity-oracle.md)

[depends on](migrate-gg-lobbying-parity-oracle.md)

## Six-profile assurance browser closure, 2026-08-25

- Consumer PR [101](https://github.com/mikec-ai/simpler-grants-gov/pull/101) merged as `8ea7bd63e80d6bb51fee610e80d6d981007a11ee` at `2026-08-25T02:32:32Z`. Its exact pre-merge proof head was `55c8a09a1bb0805f36a077901326c201590d7c19`.
- The implementation adds one generic `staticContent` browser-plan capability. It discovers section-level descriptions from projected UI artifacts, preserves a SHA-256 for each exact description, and verifies every declared heading and paragraph in Apply. No form-specific compiler, adapter, runtime, renderer, or browser-harness branch was added.
- Exact bounded run [32800937425](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32800937425) selected `sf424b`, `mandatory-sf424b`, `individual-sf424b`, `sf424d`, `mandatory-sf424d`, and `individual-sf424d`. Artifact `portable-catalog-local-1` has ID `9546700959`.
- The run produced 24 exact form/browser receipts over Chrome, Firefox, WebKit, and mobile Chrome against manifest SHA-256 `08ed3c12892ce9c5526b1545192078b7ca56eb94385baecf40adc7995032b9b8` and producer revision `4d3d969a398e1d6a19095bf5ec00eaa66a36a830`.
- All four browser summaries set `releaseGate: true`: 168 probes passed, 24 schema-implication probes were correctly not applicable, and zero probes failed or were inconclusive. Every save/reload receipt recorded zero validation warnings; accessibility recorded zero automated violations; print previews exposed zero interactive controls.
- SF-424B profiles rendered and verified description hashes `2a222e99c455ee8889c8155b5e595c86a3215595ae6d52748339e3cd6090c247` and `bb4e80639905d40c86db3791373d1c29962ac2b51a84828e927735c02b4169cd`. SF-424D profiles rendered and verified `4643e7f10553f12aa9b838b71f0865dc0fd8045ee21a41ca00c37611497e6b25` and `539245612ad30e595d9d157a21a03d8709842e95ce37441e532506844eec94d3`.
- R&R SF-424B remains deliberately outside this technical cohort. Its exact artifacts are banked, but it has no approved SGG runtime identity. This work does not infer or assign one.
- This receipt closes the bounded technical browser evidence for the six runtime-identifiable assurance profiles only. It does not accept proposed semantic mappings, approve policy or instruction content, constitute human accessibility review, settle persisted-response compatibility, or authorize production registration.
