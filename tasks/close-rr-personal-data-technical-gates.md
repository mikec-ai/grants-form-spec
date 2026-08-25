---
type: Task
title: Close R&R Personal Data technical gates
priority: P0
assignee: personal_data_closure
description: >-
  Execute the existing declarative R&R Personal Data form through generic
  Simpler runtime paths: five exact PD/PI source-bound name prefills with
  protected editability, four exact DAT exclusivity rules,
  save/reload/XML/browser receipts; keep privacy, policy, semantic acceptance,
  and human release gates separate. Excludes scanner PR 93, narrative PR 103,
  subaward variants, Project Abstract, and Multi-Project Cover.
superbee_progress_status: in_progress
generated:
  by: 'process:superbee'
  at: '2026-08-25T12:34:44.389Z'
superbee_updated_by: codex
---
# Scope

Technical closure only. Preserve exact source/version provenance and current reviewed/proposed semantic statuses. No form-specific compiler or adapter branches.

# Acceptance

Generic runtime execution covers five PD/PI name prefills, protected editability, four exact DAT exclusivity rules, and bounded save/reload/XML/browser receipts. Consumer merge requires root-agent review; privacy/policy/human gates remain explicit.

# Receipts

- Producer PR #108 merged at producer main `5940bdcc8e6b5dee60f36cb723b8c1b0dad0df5c`; five exact XFA-backed PD/PI name prefills and four exact DAT exclusivity rules compile without changing `semanticReview: proposed` or source hashes.
- Producer preflight: 125 TypeSpec tests; 371 Python tests passed with 10 skipped; 35 exact XSD profiles/fixtures; 320 blocks and 1,710 artifacts; zero unclassified records and zero exceptions.
- Generic consumer PR #114 merged in the private fork as `64d57940393019221be0b8e6c918405947cf8263` for protected/read-only schema projection, lower-environment preview behavior execution, exclusive-value MultiSelect execution, composed-schema traversal, and implicit-field XML value maps. It was rebased cleanly onto consumer main `75a0469d318b53e933e50768980b1f56562f5081`, preserving a generic-only diff at reviewed head `d47f38eb315866e8c5d3f022682ee6d6820b5f55`. Focused receipts: 53 API tests passed; 42 frontend tests passed with 1 skipped; repo-wide isort and Black, frontend lint/typecheck, hosted broad API, frontend, accessibility, build, and Storybook checks green.
- The hosted E2E cohort is not a Personal Data failure signal. Attempt 1 shard 4 failed three existing Mobile Chrome attachment-persistence/SF-424A print-view tests while selecting no portable forms (`PORTABLE_BROWSER_FORM_IDS` empty); 31 tests passed and two other existing tests were marked flaky. A clean rerun reproduced only the two existing SF-424A cases: `Total, row 1` was absent where the legacy test expected `100.00`; 36 tests passed. The repeated failures exercise no changed PR #114 path, so production code was not changed. Fail-fast cancelled shards 1–3 after shard 4 failed on both attempts; merge approval treated this exact red signal as conclusively unrelated baseline evidence.
- A temporary exact-package rehearsal loaded all five operational behaviors and generated representative XML that validates against pinned `RR_PersonalData_1_2-V1.2.xsd`.
- EPA admission PR #118 merged the exact current producer pin into consumer main at `000eb82a02e751733e9c8375c030f9ba9c3c1e92`, including the R&R Personal Data manifest, evidence, operational behavior, and the shared project-director/co-project-director blocks. The form remains unregistered and its semantic review remains `proposed`.
- Consumer technical-closure PR #120 is open only in `mikec-ai/simpler-grants-gov` at reviewed head `3cc5dc25a9bf055bf68420448fc97c1d777a56eb`. The exact verifier proves all five source-bound protected PD/PI name prefills execute, all four DAT exclusivity contracts validate, and representative XML validates against `RR_PersonalData_1_2-V1.2.xsd` SHA-256 `5f766d46d573da1f6bb326bcbc13338439ba75399ad09dee2380f65e892402cb`.
- The exact verifier exposed a generic shared-block alias defect: protecting the PD/PI occurrence also protected the co-PD/co-PI occurrence because resolved `$ref` nodes shared Python identity. PR #120 de-aliases JSON occurrences before applying operational editability and makes the browser planner use the same protected projection. The corrected bounded plan reports exactly five protected PD/PI name fields, keeps all co-PD/co-PI name fields editable, and selects 15 editable controls.
- Local PR #120 receipts: 64 focused technical tests passed; the broader form-spec suite reached 425 passed, with only two unrelated SF424A lifecycle setup errors because the host cannot resolve the Docker-only `grants-db` name; Ruff, Black, isort, and `git diff --check` passed. Hosted full CI and bounded save/reload/browser receipts remain pending, so the task stays in progress.
- Privacy, policy, accessibility, semantic acceptance, and human release gates remain open and separate.

[depends on](correct-rr-personal-data-source-parity.md)
