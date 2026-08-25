---
type: Task
title: Close narrative attachment release gates
priority: P1
assignee: codex_narrative_attachment_closure
description: >-
  Prove Project Narrative Attachment, Budget Narrative Attachment, and Other
  Narrative Attachments end to end as three distinct semantic roles reusing one
  generic attachment-capture mechanism.
superbee_progress_status: done
superbee_updated_by: codex-scanner-defect-review
generated:
  by: 'process:superbee'
  at: '2026-08-25T12:40:46.063Z'
---
# Scope

Close bounded release-evidence gates for Project Narrative Attachment, Budget Narrative Attachment, and Other Narrative Attachments in the current portable architecture.

These are three distinct semantic narrative roles that reuse one generic attachment-capture mechanism. Do not collapse them into one semantic question, and do not add form-id branches.

# Acceptance criteria

- Verify exact producer/consumer pins, official XSD version/hash, extraction provenance, and runtime identities for all three forms.
- Exercise the generic API and browser plan across attachment selection/upload, validation, save/reload, print, and bounded accessibility checks where the environment supports them.
- Record exact commits, hosted run/artifact IDs and hashes, pass/fail/inconclusive counts, and unavailable or human-only gates.
- Keep all work in mikec-ai forks and avoid active R&R Subaward Budget 10YR/30, PHS Inclusion, and PHS Additional Indirect Costs files.

# Progress receipts

- Consumer PR: `mikec-ai/simpler-grants-gov#103` on `codex/narrative-attachment-release-evidence`; current head `391cd5b8e679a248ebe67652b5e6c4ad8627d48d`. Do not merge before review; rebase after scanner PR `mikec-ai/simpler-grants-gov#93` merges.
- Isolated change: a generic capability-driven attachment upload/save/reload/print receipt plus matrix-contract coverage; no form-ID branches and no producer, runtime, adapter, or registration changes.
- Local checks: browser-plan API `24 passed`; focused attachment parity/provenance/registration/differential/preview `49 passed`; TypeScript matrix contract `11 passed`; focused Prettier and ESLint passed.
- Hosted frontend build, lint/type/format/unit, Storybook, and pa11y checks passed on the first PR revision. The broad Mobile Chrome smoke failure is unrelated: ten existing tests failed across legacy attachment, SF-424, performance-site, and SF-424A flows.
- Exact three-form hosted run `32806480571` at head `391cd5b8e679a248ebe67652b5e6c4ad8627d48d` produced 12 receipts (three forms across Chrome, Firefox, WebKit, and Mobile Chrome): `48 passed`, `24 not_applicable`, `12 inconclusive`, and `24 failed`. Portable artifact ID `9548568570`, GitHub digest `sha256:d7d202edddda5b93197d96e389afc099800860acaa87fbbf239dd303bccf9485`; blob artifact ID `9548564443`, digest `sha256:5d1fdf5e79563f77b17c82585d034460b4b6ac5fa6a87bb3ab47be4d0bb3f8c4`.
- The exact boundary is explicit rather than treated as a pass: all 12 `attachment_upload_reload` probes are `inconclusive` at the timeout/harness boundary because the hosted scanner leaves uploads pending; the delayed `/attachments/create` response is HTTP 422 (`Pending file status is not valid for processing`). Those delayed responses then appear during the independent save/print probes, producing the 24 downstream failures. Stop adding harness workarounds; rebase and rerun after PR #93 supplies the hosted scanner fix.
- Provenance remains pinned and unchanged: Project Narrative Attachment v1.2 XSD SHA `4628fd76a69cd3ce90b22892de65e2e63cc8c19e2535d4c826562b41ce280ddb`; Budget Narrative Attachment v1.2 XSD SHA `33c8bc63905589adae9508ddf08e69c7d8f900b394960f12fdd9b77cbfeb4feb`; Other Narrative Attachments v1.2 XSD SHA `38b9c9869db4c22220b92da5ca09bdd61f69a4484b6cf39139ea0fd09d6d388f`. All use crosswalk revision `dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef` while retaining distinct semantic IDs (`project/narrative`, `budget/narrative`, `application/other-narrative`) and `semanticReview: unreviewed`.

# Remaining gates

- Human visual acceptance, policy review, and semantic review; bounded automated accessibility receipts are not an accessibility-conformance determination.
- Production registration/promotion and upstream review remain separate release decisions.

# Automated closure — 2026-08-25

- Scanner/isolation PR #93 merged as `75a0469d318b53e933e50768980b1f56562f5081`. PR #103 was then rebased cleanly onto that fork-main revision; rebased head `27ad94568878d602b6424ec57fef45283c66ac5b` remained limited to three generic portable-catalog test files with no form-specific producer, adapter, runtime, renderer, or registration changes.
- Focused local verification on the rebased head passed: browser-plan producer `27 passed`; TypeScript matrix consumer `11 passed`; targeted Prettier and ESLint passed; `git diff --check` passed. The generated plan contained exactly `project-narrative-attachments`, `budget-narrative-attachments`, and `other-narrative-attachments`, each with the mechanically addressable `/properties/attachments` declaration.
- [Bounded hosted run 32847064884](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32847064884) completed successfully on the exact rebased head: `4 passed`, `4 skipped` Playwright cases in 3.4 minutes using six workers and one shard. The portable receipt artifact is ID `9563144954`, digest `sha256:ba13fa1df1da21f42c2860a4abb0748dbc2a31ec934ef663848acfe433d56326`; the blob report is ID `9563139418`, digest `sha256:926ac5a8702c9554a71b29965f4d9b301b8efc84fe3bb66656b667012037963b`.
- All 12 form-by-browser receipts (three narrative roles across Chrome, Firefox, Mobile Chrome, and WebKit) report `attachment_upload_reload: passed`, `persistedAfterReload: true`, and `sample-upload-kb.pdf`. All 12 `print_render` probes passed with the same filename and zero interactive controls. There were zero failed or inconclusive probes.
- Automatic full run [32847062542](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32847062542) reproduced the documented unrelated SF-424A baseline: shard 1 ran 44 tests with six workers and finished `34 passed`, `6 skipped`, `2 flaky`, `2 failed` in 10.3 minutes. The only hard failures were the SF-424A Organization and Individual Chrome cases, each unable to locate `Total, row 1` on every retry. Two legacy attachment-history cases were retry-flaky and then passed. No hard failure was attributable to this narrative attachment change.
- [PR #103](https://github.com/mikec-ai/simpler-grants-gov/pull/103) admin-squash-merged as `4db9540cb7efea7a0ff898809d124774f75d2e92` after GitHub recalculated onto concurrently advanced fork main `64d57940393019221be0b8e6c918405947cf8263`. The merge commit itself changes exactly the same three generic portable-catalog files.
- The automated upload, scan, save/reload, read-only print, and bounded accessibility evidence gate is complete. Human semantic, policy, visual, accessibility-conformance, production-promotion, and upstream-review decisions remain explicitly separate.
