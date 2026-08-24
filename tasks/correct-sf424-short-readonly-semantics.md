---
type: Task
title: Correct SF-424 Short prepopulation versus read-only semantics
priority: P0
assignee: implement_operational_evidence
description: >-
  Implement the six-field source-audited declarative correction from
  tasks/reconcile-sf424-family-portable-cutover-deltas: remove unconditional UI
  readOnly, retain SGG prepopulation, preserve conflicts as durable evidence,
  and prove emitted behavior without adapter branches.
superbee_progress_status: in_progress
superbee_updated_by: implement_operational_evidence
generated:
  by: 'process:superbee'
  at: '2026-08-24T05:25:17.968Z'
---
# Scope

Implement the six-field source-audited declarative correction from `tasks/reconcile-sf424-family-portable-cutover-deltas`: remove unconditional UI `readOnly`, retain SGG prepopulation, preserve conflicts as durable evidence, and prove emitted behavior without adapter branches.

# Implementation receipt

- Producer branch: `codex/sf424-short-readonly-semantics`
- Producer base: `5be73fd5c222e4007639b40cef87aea205c5342e`
- Reviewed implementation head: `273d1ba8da96a958448d9c19209a50b8cbe2c0dc`
- Draft PR: `https://github.com/mikec-ai/grants-form-spec/pull/73`
- Declaration: removed `@UI.readOnly` from exactly `/agencyName`, `/assistanceListingNumber`, `/assistanceListingProgramTitle`, `/fundingOpportunityNumber`, `/fundingOpportunityTitle`, and `/samUei`; all six `@Sgg.prePopulate` entries remain unchanged.
- Projection result: all six canonical schema properties omit `readOnly`; the SGG UI emits editable `field` controls; the SGG rule schema retains the exact six prepopulation rule names. Date Received, AOR Signature, and Date Signed remain read-only submission-populated outputs.
- Durable evidence: `research/sf424-short/source-audit.json` pins exact XSD, DAT, read-only PDF, sample XFA PDF, instruction PDF, and FID 711 provenance. It preserves the SAM UEI editability conflict, Assistance Listing cardinality conflict, and Funding Opportunity Title source-name discrepancy without resolving them by inference.
- Boundary: no compiler, adapter, runtime, or form-ID branch; no operational evidence inferred from annotations; no production cutover; no HHS upstream write.

# Verification

`./scripts/preflight.sh` passed after rebasing onto the exact producer main. Results: 116 TypeScript tests passed; 294 Python tests passed with 2 skipped; exact XSD fixtures, artifact validation, promotion validation, packaging verification, analysis, classified-field, and independent TypeSpec compilation gates passed. GitHub CI passed in 2 minutes at draft PR head `273d1ba8da96a958448d9c19209a50b8cbe2c0dc`.

# Remaining gate

Keep this task in progress until independent review completes. Do not merge from this task.
