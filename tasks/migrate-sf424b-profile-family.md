---
type: Task
title: Bank the SF-424B assurance profile family
priority: P1
assignee: sf424b_family_agent
description: >-
  Publish active R&R, Individual, and verified Mandatory SF-424B profiles over
  one portable assurance bundle.
superbee_progress_status: in_progress
superbee_updated_by: sf424b_family_agent
generated:
  by: 'process:superbee'
  at: '2026-08-23T20:43:34.278Z'
---
# Goal

Bank the active SF-424B assurance variants as versioned profiles over one portable non-construction assurance bundle after the base SF-424B migration establishes the contract.

# Scope

- R&R SF-424B v1.1 (FID 325)
- Individual SF-424B v1.1 (FID 521)
- Mandatory SF-424B v1.1 (FID 328), verified active from official evidence

# Acceptance criteria

- Pin official XSD, DAT, instructions, form identity, version, and hashes for every profile.
- Verify policy text, editable versus prepopulated ownership, labels, and XML namespaces independently; do not infer semantic equivalence from matching wire shapes.
- Reuse one reviewed policy/attestation model and shared identity/signature primitives; keep profile differences declarative.
- Produce separate portable manifests and XML profiles without form-specific adapter branches.
- Exercise differential schema, UI, lifecycle, locked/print, submission, XML, and XSD parity where an SGG oracle exists.
- Do not register a profile until technical, human, policy, and operational gates are recorded.

# Implementation receipts

- Producer PR 50 merged green: https://github.com/mikec-ai/grants-form-spec/pull/50
- Immutable producer merge revision: `bc1d60325e52fbffd782756ec40c9dba232fd978`.
- One source-pinned non-construction assurance bundle is bound declaratively to base, R&R, Mandatory, and Individual profiles. Each profile independently pins official XSD, DAT, instructions, PDF, identity, labels, ownership, root, namespace, and version wires.
- Exact XSD SHA-256 values: base `b0da616d262329e869b7c2a12146396fd8a279d2a1723521271c519f4571075d`; R&R `511de9a5594a739ce596a33a92d3dec1bac2a32f193a2fe6b4799b45f29ff296`; Mandatory `bcbe0010ba734ebeb0e3b6bd331a936d716b9896446231be90a11b005faf9579`; Individual `1fe96cd37f1933f1c251efbbfbafae85c2e4869359f216a645024860ee29c983`.
- Consumer PR 46 merged clean: https://github.com/mikec-ai/simpler-grants-gov/pull/46
- Immutable consumer merge revision: `a90910022ac1ea57e9f417a605f9546eef29aa6b`, selecting base, Mandatory, and Individual only, with generic projections, runtime identities, exact XML canaries/XSDs, lifecycle/submission tests, and no registrations.
- Individual identity remains applicant input/editable; base and Mandatory identity is system-owned/read-only; signature and date are submission-owned for all imported profiles.

# Explicit block and remaining gates

R&R is intentionally producer-only and excluded from the SGG allowlist. The official R&R V1.1 URL, namespace, and fixed form version identify 1.1, but its XSD document declares `schema version="1.0"`; this source inconsistency requires an authoritative operational decision before consumer release.

Base, Mandatory, and Individual remain unregistered pending semantic/policy-owner review, accessibility review, hosted lifecycle execution, instruction UUID assignment, and explicit production registration. The task remains in progress.

[depends on](migrate-sf424b-parity-oracle.md)
