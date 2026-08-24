---
type: Task
title: Author and integrate SBIR/STTR Information
priority: P1
description: >-
  Add the source-bound SBIR/STTR supplement using only proven attachment-wire
  and condition-operation reuse; retain its program, eligibility, ownership,
  affiliation, disclosure, and partner-role semantics as distinct.
superbee_progress_status: done
superbee_updated_by: implement_sbir_sttr
generated:
  by: 'process:superbee'
  at: '2026-08-24T04:29:58.456Z'
assignee: implement_sbir_sttr
---
---
type: Task
title: Author and integrate SBIR/STTR Information
priority: P1
description: >-
  Add the source-bound SBIR/STTR supplement using only proven attachment-wire
  and condition-operation reuse; retain its program, eligibility, ownership,
  affiliation, disclosure, and partner-role semantics as distinct.
superbee_progress_status: in_progress
superbee_updated_by: implement_sbir_sttr
generated:
  by: 'process:superbee'
  at: '2026-08-24T04:25:59.204Z'
assignee: implement_sbir_sttr
---
---
type: Task
title: Author and integrate SBIR/STTR Information
priority: P1
description: >-
  Add the source-bound SBIR/STTR supplement using only proven attachment-wire
  and condition-operation reuse; retain its program, eligibility, ownership,
  affiliation, disclosure, and partner-role semantics as distinct.
superbee_progress_status: in_progress
superbee_updated_by: implement_sbir_sttr
generated:
  by: 'process:superbee'
  at: '2026-08-24T04:16:59.046Z'
assignee: implement_sbir_sttr
---
---
type: Task
title: Author and integrate SBIR/STTR Information
priority: P1
description: >-
  Add the source-bound SBIR/STTR supplement using only proven attachment-wire
  and condition-operation reuse; retain its program, eligibility, ownership,
  affiliation, disclosure, and partner-role semantics as distinct.
superbee_progress_status: in_progress
superbee_updated_by: implement_sbir_sttr
generated:
  by: 'process:superbee'
  at: '2026-08-24T04:15:01.704Z'
assignee: implement_sbir_sttr
---
---
type: Task
title: Author and integrate SBIR/STTR Information
priority: P1
description: >-
  Add the source-bound SBIR/STTR supplement using only proven attachment-wire
  and condition-operation reuse; retain its program, eligibility, ownership,
  affiliation, disclosure, and partner-role semantics as distinct.
superbee_progress_status: in_progress
superbee_updated_by: implement_sbir_sttr
generated:
  by: 'process:superbee'
  at: '2026-08-24T03:59:17.979Z'
assignee: implement_sbir_sttr
---
# Goal

Author SBIR/STTR Information as a source-bound declarative supplemental form and measure how much of its structure composes from the established portable library.

# Bounded producer audit (2026-08-23)

This audit used deterministic XSD, XLS, HTML, PDF metadata, embedded-text, and XFA-packet inspection. OCR was not used. It made no producer implementation, consumer change, or HHS/upstream change.

## Exact active source set

- Grants.gov FID 787 lists **SBIR/STTR Information**, version **3.0**, as active: `https://www.grants.gov/forms/form-items-description/fid/787`.
- Root XSD: `https://apply07.grants.gov/apply/forms/schemas/SBIR_STTR_Information_3_0-V3.0.xsd`; SHA-256 `32ed46a450c1b77d9ef64ebf2a4086ab90b076aa2d3cdfedfab8c00324adcebf`.
- DAT workbook: `https://apply07.grants.gov/apply/forms/sample/SBIR_STTR_Information_3_0-V3.0_F787.xls`; SHA-256 `c0e8d91e583b9f7e6339cc6239f1e4d51e9d93299b893b34efd1bbbc435c6e9b`. The Form Info sheet identifies FID 787, version 3, OMB 4040-0001, expiration 01/31/2029, and the SF-424 R&R family.
- Current Grants.gov sample/XFA PDF: `https://apply07.grants.gov/apply/forms/sample/SBIR_STTR_Information_3_0-V3.0.pdf`; SHA-256 `bd36dbc83d8fcfcd309cd45236d496a5f34f1401b4cf51d5aaeac2f22e45ce1e`. It contains nine XFA packets; the template packet SHA-256 is `cd8a6f6570fefe639ffe1196933bdb02195558097a03508c786c9445807b7c6b` and carries the 01/31/2029 expiration.
- NIH's reference copy at `https://www.grants.nih.gov/sites/default/files/uploaded/SBIR_STTR_Information_3_0-V3.0.pdf` is older: PDF SHA-256 `87529b99eba4ea08b10035f60c5d4fdd4629b4c6e9324c00559205a2e776754a`, XFA template SHA-256 `b5d1e86a63b545c19386434bba6f47442dab9b123ea9296c400bf8002640cd97`, and expiration 11/30/2025. Retain it as conflict/history evidence, not the current form oracle.
- Current Forms-I G.440 HTML: `https://grants.nih.gov/grants/how-to-apply-application-guide/forms-i/general/g.440-sbir-sttr-information-form.htm`; observed SHA-256 `b7a3db230317e52c34be840fef12fcc845b004388755d2400a9f5961c2918929`. The live HTML is mutable, so record the retrieval digest rather than treating the URL alone as a stable version.
- Current filtered Forms-I SBIR/STTR instructions PDF: `https://www.grants.nih.gov/grants/how-to-apply-application-guide/forms-i/sbir-sttr-forms-i.pdf`; SHA-256 `e5525ea946e4ed84c5037351a6b7c574430d37ce26cfd8913a656ec8c2491c84`.
- Exact XSD dependency closure is already established elsewhere in the producer: Attachments V1.0 `ae2ebb3618f7d8fb337be2309b3096e9121b4af659e913af423aab85d13dcb1d`, Universal Codes V2.0 `78f33338e9319ef31a052d1328b8984931a4380db2485493bcc78ab9e2c11f3a`, Global Library V2.0 `ff0214de91b95a4209f50f0fe08a18d0f3d17f280ab8c8bbcb52878f37de7be8`, and Global V1.0 `4b338db919152eb8b96a1a846902d04ef8bca8d08127b21f80f927eaa62283cb`.

## Deterministic structure and current factory evidence

- The root XSD has one ordered root, fixed `FormVersion="3.0"`, 27 applicant-facing elements, and no repeating group. Three elements are distinct semantic attachments: non-domestic performance explanation, commercialization plan, and SBIR commercialization history. Their shared `att:AttachedFileDataType` expands to twelve technical leaf records, yielding the existing 40-record extraction: 1 container, 27 questions, 12 technical fields.
- The DAT has 78 rows, but that is not 78 behavioral rules. Sixteen rows contain Business Rules. One is a pure nine-digit validation. Ten conditional rows account for the factory's 19 executable effect records. Five source condition/clearing rows are absent from that executable set: Other Agency, three clear/remove-on-answer rules, and the compound Commercialization Plan requirement.
- Existing crosswalk proof: `artifacts/proof/grantsgov-SBIRSTTRInformation.jsonl`, SHA-256 `9dc414cbf8ca2bf0445a4272c5b9949d739c0c4eb52dc88c8998b0be55d4d4b6`; manifest SHA-256 `c9d17fdcf7e28d4f9de2c1741e2e6ac7b5b629806b7760301e61f1f7adbd480b`.
- Existing runtime migration evidence: `artifacts/authoring/priority-runtime/SBIRSTTRInformation.runtime.json`, SHA-256 `19ff32f8e708271625bc8df5463da6878b7a4dbcbbf84880d19eb39ade923549`; resolved AST SHA-256 `562eb8add91bf4f55556f86bc693b33868abbaead58564b236bc5b01c01e675e`. Both remain agent-proposed and publish-ineligible.
- Do not import those 19 effects as parity truth. The DAT and XFA say affected controls are **disabled/protected**, while the migration artifact frequently records `visible`; it also uses display values `Yes`/`No` where the XSD wire values are `Y: Yes`/`N: No`. Reconcile against the exact DAT/XFA and canonical response vocabulary.
- The current XFA has 89 scripts: 32 initialize, 24 exit, 18 change, 9 click, and 4 enter events, plus 2 script objects. These primarily implement mandatory marking, enable/disable, clear/remove, attachment add/view/delete, validation, and focus traversal. There are no source calculations.
- Non-Adobe rendering displays only the standard “requires Adobe Reader” fallback page. PDF visual parity and accessibility cannot be inferred from ordinary browser/Poppler rendering.

## Reuse boundary

True reusable material is narrower than the original task wording implied:

- Reuse the generic `AttachmentRef` **capture mechanism** and the existing attached-file XML mapping. Keep all three attachment questions semantically distinct.
- Reuse exact Yes/No wire vocabulary and generic equality/set-membership condition machinery as shapes/operations, not as proof that the questions share one semantic identity.
- The STTR `SAMUEI` field is the UEI of the **non-profit research partner**, not the applicant organization. It must be a new role-qualified question; do not map it to `primary-org/uei` even though the twelve-character shape is reusable.
- The form collects no person identity block and no applicant organization block. References to the PD/PI, small business, subcontractors, and research partner establish role-specific program questions, not reusable person/organization objects.
- Agency, Other Agency, SBC Control ID, program type, SBIR/STTR application type, letter-of-intent number, agency topic/subtopic, employee count, eligibility certification, VCOC ownership, faculty/student ownership, federal subcontracts, HUBZone status, domestic performance, equivalent work, disclosure permission, TABA, SBIR history/employment, and STTR commitment/work-share questions are new SBIR/STTR semantic identities unless later reviewed evidence proves otherwise.
- `SubcontractorNames` is free-text names of Federal laboratories/agencies. It is not a subaward-recipient organization collection.

## Source-backed behavior partition

Use the existing declarative equals/in-set condition capability for the bounded local rules. Preserve source semantics as **enabled** and **required**, not hidden, where the DAT says disabled:

- Other Agency enabled and required when Agency is Other.
- Agency Topic/Subtopic required when Agency is DOE; otherwise it stays optional.
- Federal laboratory/agency names enabled and required when Subcontracts Included is Yes.
- Non-domestic explanation enabled and required when Domestic Performance is No.
- Other Federal agencies enabled and required when Equivalent Work is Yes.
- SBIR Phase II history question and PD/PI primary-employment question enabled and required for SBIR or Both.
- Commercialization History enabled and required when the Phase II awards answer is Yes.
- The two STTR questions and non-profit research-partner UEI enabled and required for STTR or Both.

Keep these exact source behaviors declarative but uncompiled until a separately justified generic capability exists:

- clear Other Agency when Agency is not Other;
- clear Federal laboratory/agency names when Subcontracts Included is No;
- remove the non-domestic attachment when Domestic Performance is Yes;
- clear other-agency names when Equivalent Work is No;
- the compound Commercialization Plan requirement, because the DAT's cross-agency rule and current NIH instructions differ and the current simple condition contract does not need to become a policy DSL.

No calculation declaration is needed.

## Source conflicts and policy boundaries

- The XSD and DAT require a nine-character, nine-digit SBC Control ID, while current NIH prose gives an example with an `SBC_` prefix. Preserve the exact XSD/DAT constraint and record the instruction conflict.
- The federal form permits Program Type `Both` and eight application types. Current HHS instructions disallow `Both`, Phase IIA, and Phase IIC; disallow Direct Phase II for STTR; and make other choices NOFO-dependent. These are HHS/NOFO policy overlays, not changes to the cross-agency base form.
- The DAT's Commercialization Plan condition is Phase I+DOE or Phase II/Fast-Track. Current NIH instructions require it for a different HHS set including Direct Phase II, Phase IIB, and Commercialization Readiness Program. Do not silently choose one universal rule.
- `SmallBusinessEligibility` is an applicant certification, not an automated eligibility determination. VCOC, faculty/student ownership, HUBZone, work-share, employment, and commitment responses likewise must not become inferred eligibility decisions.
- A Yes VCOC response triggers a cross-form instruction to provide a certification under R&R Other Project Information; this form does not own that attachment.

## Recommended minimal declarative slice

1. Add one `sbir-sttr` question-bank module with 27 source-bound question identities. Compose the established attachment mechanism three times and use source-exact scalar constraints/enums. Do not add a person block, applicant-organization block, eligibility engine, or policy framework.
2. Add one form composition with clear All Applicants, SBIR, and STTR sections. Preserve exact long prompts and concise instructions/tooltips from the pinned DAT/instruction evidence.
3. Emit only the simple local enabled/required rules listed above using current generic operators. Record clearing and the disputed compound Commercialization Plan rule as source-bound uncompiled evidence.
4. Add one declarative Grants.gov XML profile for the ordered 27-element root, the fixed version attribute, and three standard attached-file nodes. Existing XML composition is sufficient; no new generic XML capability is required.
5. Test minimal, fully populated, SBIR, STTR, Both, every direct condition transition, invalid SBC ID/employee count/UEI, attachment resolution, omitted optionals, save/reload, and exact XML/XSD validation. Keep clear/remove behavior, agency overlays, locked/print, and production release as explicit gates.

## Human and release gates

- **Semantic/policy:** approve all proposed question identities; adjudicate cross-agency versus HHS/NOFO rules; verify certifications and disclosures do not imply automated eligibility; decide stale-value clearing and XML non-emission.
- **Privacy/security:** the disclosure-permission answer authorizes downstream disclosure of project and signing-official contact information; commercialization/equivalent-work content and attachments may be confidential or proprietary. Verify access control, logs, analytics, exports, retention, attachment malware/content checks, and disclosure workflows.
- **Accessibility:** verify fieldset/legend semantics for radio groups, long compound-question reading order, conditional enablement and required-state announcements, attachment status and focus, error summary, keyboard order, save/reload, and locked/print presentation. The XFA fallback cannot serve as browser accessibility evidence.
- **Operational/release:** human instruction review, agency-profile review, consumer behavior verification, attachment lifecycle, exact XSD validation, round-trip/submission testing, and production approval remain open. Banking or compiling the package must not imply release readiness.

# Acceptance criteria

- Pin and promote the exact active sources and retain the older NIH PDF only as explicit conflict/history evidence.
- Keep deterministic extraction separate from proposed semantic mappings; only reviewed mappings contribute to published metrics.
- Add no form-specific compiler, adapter, loader, renderer, conformance branch, eligibility engine, or policy DSL.
- Record reusable versus new artifacts and all unresolved gates in producer evidence.

# Scope boundary

The audit shows no new generic architecture capability is required for the minimal slice. Do not introduce one speculatively.

# Producer implementation receipt (2026-08-24)

- Draft PR: `https://github.com/mikec-ai/grants-form-spec/pull/70`
- Review head: `a3e3f77eb16c656344d03916b560d6d67cda7f14`
- Scope: producer only; no consumer or HHS/upstream changes; no OCR.
- Composition: 27 new source-specific semantic question identities and three distinct attachment questions composing only `generics/attachment` capture and the shared attached-file XML mapping. The STTR partner UEI remains distinct from `primary-org/uei`; no applicant-organization or person identity is reused.
- Evidence: 27 applicant questions, 12 technical attachment leaves, one root structure record, 78 DAT rows, 16 DAT Business Rules rows, 11 portable conditional-required targets, 10 consumer enablement targets, and zero calculations. All 27 proposed semantic identities now have direct, unique XSD source paths.
- Behavior disposition: all 11 exact portable enable/require targets compile through generic equals or in-set operations. Five source behaviors remain source-bound uncompiled: four clear/remove effects and the disputed compound Commercialization Plan rule. Agency Topic/Subtopic is correctly classified as compiled in the portable source of truth; its required-only consumer projection gap remains separately explicit.
- Exact sources: root XSD `32ed46a450c1b77d9ef64ebf2a4086ab90b076aa2d3cdfedfab8c00324adcebf`; DAT `c0e8d91e583b9f7e6339cc6239f1e4d51e9d93299b893b34efd1bbbc435c6e9b`; current Grants.gov XFA PDF `bd36dbc83d8fcfcd309cd45236d496a5f34f1401b4cf51d5aaeac2f22e45ce1e`. The older NIH PDF remains explicit history/conflict evidence.
- Verification: full producer preflight passed after independent-review hardening, with 114 TypeScript tests, 282 Python tests and 2 skips, 30 exact root-XSD fixtures, 1,533 validated emitted artifacts, 1,062 packaged artifacts, zero unclassified fields, and zero exceptions. Canonical AJV tests exercise all 11 required/optional transitions, and the UI test asserts all 10 consumer enablement conditions with exact scopes, values, and effects.
- State: review-ready and intentionally unmerged pending independent semantic/source review and hosted CI.

# Independent exact-head review receipt (2026-08-24)

- Reviewed exact head `a3e3f77eb16c656344d03916b560d6d67cda7f14` against the pinned root XSD, DAT workbook, source audit, emitted portable and SGG artifacts, XML profile, and task acceptance criteria. OCR was not used.
- Initial findings were corrected before approval: all 11 portable conditional-required transitions and all 10 consumer enablement rules now have direct regression coverage; all 27 semantic identities have unique proposed XSD mappings; employee-count and TABA catalog classifications are accurate; and Agency Topic/Subtopic is classified as compiled in the portable source of truth while its consumer projection gap remains explicit.
- Verified the three attachments remain distinct semantic questions over one generic capture mechanism, `SAMUEI` remains the non-profit research-partner UEI rather than applicant-organization reuse, policy conflicts remain unresolved rather than inferred, and no form-specific compiler, adapter, loader, renderer, conformance, eligibility, or policy branch was added.
- Independent local `npm run preflight` passed: 114 TypeScript tests, 282 Python tests with 2 skips, 30 exact-XSD profiles/fixtures, 1,533 validated emitted artifacts, 1,062 verified packaged artifacts, and zero unclassified fields or exceptions.
- Hosted CI run `32689957291` passed at the exact head in 1m27s. No actionable findings remain. GitHub cannot record an `APPROVE` review because the configured credential owns the PR, so this bundle receipt is the durable independent approval record.

[consumer delivery follows](automate-cross-repo-form-promotion.md)

# Merge receipt (2026-08-24)

- Producer PR #70 merged to `main` as `88aee1a3406c3f860bc50c9bcc92c6022b9dda3b` after the independent exact-head review found no actionable issues and hosted CI run `32689957291` passed.
- The merged producer baseline now contains 39 portable forms. This receipt closes producer authoring only; consumer banking, runtime registration, human semantic and policy acceptance, accessibility review, privacy/security review, and production release remain separate gates.
- No consumer or HHS/upstream repository was changed as part of this task. Consumer promotion continues under the linked cross-repository promotion task.
