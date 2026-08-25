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
  at: '2026-08-25T11:23:18.415Z'
superbee_updated_by: personal_data_closure
---
# Scope

Technical closure only. Preserve exact source/version provenance and current reviewed/proposed semantic statuses. No form-specific compiler or adapter branches.

# Acceptance

Generic runtime execution covers five PD/PI name prefills, protected editability, four exact DAT exclusivity rules, and bounded save/reload/XML/browser receipts. Consumer merge requires root-agent review; privacy/policy/human gates remain explicit.

# Receipts

- Producer PR #108 merged at producer main `5940bdcc8e6b5dee60f36cb723b8c1b0dad0df5c`; five exact XFA-backed PD/PI name prefills and four exact DAT exclusivity rules compile without changing `semanticReview: proposed` or source hashes.
- Producer preflight: 125 TypeSpec tests; 371 Python tests passed with 10 skipped; 35 exact XSD profiles/fixtures; 320 blocks and 1,710 artifacts; zero unclassified records and zero exceptions.
- Generic consumer PR #114 is open for protected/read-only schema projection, lower-environment preview behavior execution, exclusive-value MultiSelect execution, composed-schema traversal, and implicit-field XML value maps. Focused receipts: 48 API tests; 41 frontend tests passed with 1 skipped; frontend typecheck, Ruff, and Prettier green.
- A temporary exact-package rehearsal loaded all five operational behaviors and generated representative XML that validates against pinned `RR_PersonalData_1_2-V1.2.xsd`.
- Exact artifact repin, save/reload, and bounded browser receipts remain pending the independently owned Multi-Project Cover consumer baseline. Current 42-form sync correctly refuses because consumer main lacks `api/src/services/xml_generation/xsds/RR_SF424_Multi_Project_Cover_4_0-V4.0.xsd`; this lane will not import that file.
- Privacy, policy, accessibility, semantic acceptance, and human release gates remain open and separate.

[depends on](correct-rr-personal-data-source-parity.md)
