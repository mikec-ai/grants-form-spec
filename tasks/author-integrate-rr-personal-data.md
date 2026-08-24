---
type: Task
title: Author and integrate R&R Personal Data
priority: P1
description: >-
  Bank a high-use, bounded person-data form using role-qualified identity reuse
  while keeping privacy-sensitive semantics and production release gated.
superbee_progress_status: in_progress
superbee_updated_by: audit_rr_personal_data
generated:
  by: 'process:superbee'
  at: '2026-08-24T03:08:19.721Z'
assignee: audit_rr_personal_data
---
# Goal

Author R&R Personal Data declaratively as a controlled test of role-qualified person and identity reuse without conflating structurally similar demographic or biographical concepts.

# Evidence starting point

- Two-year usage evidence records 39,237 form instances.
- The research factory records 25 question/structure records and 54 behavior records across two person-role models.
- One policy-sensitive item remains blocked and must not be inferred from structural similarity.

# Acceptance criteria

- Pin and promote exact official XSD, DAT, PDF/XFA, instructions, versions, and hashes.
- Reuse canonical person and identity questions only where role, subject, purpose, constraints, and XML meaning match.
- Preserve demographic, biographical, privacy, and access-control distinctions as explicit semantic and policy evidence.
- Resolve or explicitly retain the blocked policy-sensitive item without fabricating behavior.
- Validate representative role, optionality, invalid, save/reload, locked/print, and XML/XSD cases.
- Add no form-specific compiler, adapter, loader, renderer, or conformance branch.
- Permit source-conformant consumer banking before release approval, but do not register or expose the form until privacy, policy, accessibility, lifecycle, and operational gates pass.
- Record marginal effort and every reused versus newly introduced artifact.

# Scope boundary

Banking source-bound artifacts is separable from handling production applicant data. Privacy review gates runtime enablement, not faithful declarative authoring.

[consumer delivery follows](automate-cross-repo-form-promotion.md)

# Bounded source and architecture audit (2026-08-23)

## Exact official source set

All four source URLs were fetched directly from `apply07.grants.gov` during the audit. No OCR was used.

| Source | Official URL | SHA-256 | Audit note |
|---|---|---|---|
| Root XSD | `https://apply07.grants.gov/apply/forms/schemas/RR_PersonalData_1_2-V1.2.xsd` | `5f766d46d573da1f6bb326bcbc13338439ba75399ad09dee2380f65e892402cb` | Byte-identical to the existing factory source; native form version `1.2`, root namespace `http://apply.grants.gov/forms/RR_PersonalData_1_2-V1.2`. |
| DAT workbook, FID 357 | `https://apply07.grants.gov/apply/forms/sample/RR_PersonalData_1_2-V1.2_F357.xls` | `2c0eaf828c93162854bf1488e4687f0b1d85ab4d5b5ca7c922acdf87229ceaf7` | Byte-identical to the research-factory input; 54 extracted behavior records: 40 applicant-entered and 14 presentation records. |
| Current sample XFA PDF | `https://apply07.grants.gov/apply/forms/sample/RR_PersonalData_1_2-V1.2.pdf` | `2b95182ff1078f3f27c44025e9210755c6613aefa016811b69141fc04992f227` | One-page dynamic XFA, modified 2026-01-29. Extracted XFA `template` packet SHA-256 `deeba464ce8daae11fda78002fd79721b504952a0e39a8894acd3bedd16f55b0`; `datasets` packet SHA-256 `4835bed2b37c639b136d59fc1c3f5d78e79f16ff0b0333e3c21af9f79cbc3d1b`. |
| Current instructions PDF | `https://apply07.grants.gov/apply/forms/instructions/RR_PersonalData_1_2-V1.2-Instructions.pdf` | `ccdda8fd35b28a069ce1b7908097380562b4bed5cc7802ccc6e6d92c71e12fad` | Two tagged, text-native pages, created 2026-01-29; version `1.2`, OMB `4040-0001`, expiration `2029-01-31`. |

The exact XSD closure is root plus `Attachments-V1.0.xsd` (`ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d`), `GlobalLibrary-V2.0.xsd` (`ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8`), `Global-V1.0.xsd` (`4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb`), and transitive `UniversalCodes-V2.0.xsd` (`78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a`). The root imports Attachments even though it does not use an attachment field; preserve the exact closure rather than simplifying the official schema.

The factory's aggregate source-set SHA `fdd095e73979c74d7457b5c032b5a0ef54a50812ab31c15f5d973314d5e25136` is extraction provenance, not the physical root-XSD digest. Do not substitute one for the other.

## Exact form shape and likely question reuse

- The wire root contains one required `ProjectDirector` and zero to four `Co-ProjectDirector` occurrences. Both use the exact same XSD `DirectorType`: name, sex/gender-coded value, race array, ethnicity, disability-status array, and citizenship.
- Reuse `generics/person-name` for the five-part name shape. Its limits match `GlobalLibrary-V2.0` exactly; apply required `firstName` and `lastName` at the profile occurrence. Preserve the parent properties as the Project Director/Principal Investigator and Co-Project Director/Co-Principal Investigator roles. Do not create ten new leaf identities merely because the same name parts occur under two roles.
- Introduce one reusable, source-specific research-person personal-data profile containing five new semantic questions: reported sex, race, ethnicity, disability status, and citizenship. Compose that profile under both role-qualified occurrences. The shared `DirectorType` is stronger evidence of reuse than similar labels, while the two occurrence paths preserve whose data it is.
- Do not reuse clinical-study enrollment sex/race/ethnicity concepts. Those are aggregate enrollment coordinates, not self-reported attributes of a named PD/PI.
- The source itself is terminologically inconsistent: the XSD path/type says `Gender`, while the DAT, XFA label, and current instructions say `Sex`, with values Male/Female/Do Not Wish to Provide. Use a source-faithful semantic name such as `reportedSex` and map it to XML `Gender`; keep the inconsistency in evidence rather than silently choosing a policy interpretation.
- The XFA displays ethnicity `Non-Hispanic or Latino` but writes the exact XSD value `Not Hispanic or Latino`; it displays `Do Not Wish to Provide` but writes `Do Not Wish To Provide`. Keep canonical display values and use the existing declarative XML `valueMap` for the exact wire spellings. No compiler extension is needed for these differences.

The prior factory's 20 role-qualified concepts remain agent-proposed evidence, not accepted identities. Its useful result is the warning against losing role context; the declarative composition above preserves that context without duplicating every question by role.

## Behaviors and architecture boundary

- Domain calculations: zero. XFA `calculate` scripts maintain PDF presentation/data-binding state and do not establish applicant-facing calculated outputs.
- Conditional visibility: zero source-bound field visibility predicates.
- Repetition: one generic zero-to-four Co-PD/PI list. Existing array limits, inferred field-list UI, and validate-before-add adapter option cover authoring; exact focus, add/delete, and save/reload behavior remain consumer acceptance cases.
- Selection constraints: four instances of one reusable rule family. Race makes `Do Not Wish to Provide` exclusive. Disability makes both `None` and `Do Not Wish to Provide` exclusive from every other value and from each other. These apply once to the PD/PI and once per Co-PD/PI.
- The current portable compiler has no declarative array-member exclusivity primitive. This is not required to author, compile, analyze, or bank the source-conformant form: retain the four rules as source-bound uncompiled evidence and keep runtime enablement gated. If production parity is pursued, add one generic, tested `exclusiveValues`/mutually-exclusive-array validation capability; do not add a form-specific branch. It should enforce canonical JSON Schema validity and expose enough portable metadata for an adapter to clear or reject conflicting selections accessibly.
- Current flattened scalar-array XML projection covers repeated `Race` and `DisabilityStatus` elements. The five-part name mapping is already reusable. No new XML projector, loader, renderer, or form-specific compiler logic is indicated.

## Privacy, accessibility, and release gates

The XFA's source notice says submission is voluntary and not a precondition of award; after receipt the form is separated from the application, is not duplicated, is not part of review, and the data is confidential. Treat those as source-bound lifecycle and access-control requirements, not ordinary help text. Banking may proceed, but registration/runtime exposure must remain blocked until the product can demonstrate restricted authorization, separation from reviewer-visible application content and ordinary exports, confidentiality-appropriate logging/telemetry, retention/deletion behavior, and an approved policy/privacy determination.

Accessibility acceptance must cover semantic fieldsets and legends for race/disability groups, keyboard and screen-reader behavior when exclusive answers clear other choices, an announced change or validation error, accessible repeatable-person add/delete controls with predictable focus, preservation of entered values across save/reload, and clear voluntary-status/help text. Locked/print and reviewer/export views must prove the confidential data is absent where policy requires, not merely visually hidden.

## Recommended implementation slice

Proceed with a producer-only declarative canary after rebasing on the exact-XSD gate: exact evidence and source audit; one new personal-data question-bank profile; one form composing that profile for the two roles; a generic XML profile and exact fixture closure; source-bound unresolved records for the four exclusivity instances; representative schema, XML/XSD, mapping, and evidence tests. Do not register or expose the form. A separate architecture task may add the generic exclusive-array-values primitive if the team chooses production interaction parity now; otherwise it is a named release dependency, not a blocker to banking.
