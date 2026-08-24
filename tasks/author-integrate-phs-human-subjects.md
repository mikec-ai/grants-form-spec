---
type: Task
title: Author and integrate PHS Human Subjects and Clinical Trials
priority: P1
description: >-
  Producer delivery is complete for the dimensional clinical-study foundation;
  consumer, accessibility, semantic, and release gates remain explicit.
superbee_progress_status: done
superbee_updated_by: promote_new_forms
generated:
  by: 'process:superbee'
  at: '2026-08-24T03:06:56.854Z'
assignee: human_subjects_agent
---
# Goal

Establish PHS Human Subjects and Clinical Trials as the next major portable foundation for deeply nested, conditional, repeating clinical-study data.

# Evidence starting point

- The research factory records 305 source question/structure records and 46 behavior records.
- Its pinned F705 DAT contains exactly eleven condition-bearing records and eleven repetitions. Literal compilation remains proposed; the embedded study has no field-level DAT behavior evidence.
- The 115-cell dimensional enrollment model contains 28 total-like coordinates, but the pinned XSD and parent DAT contain zero calculation records.
- Two-year usage evidence records 243,892 form instances.

# Acceptance criteria

- Pin and promote exact XSD, DAT, PDF/XFA, instruction, version, and hash evidence.
- Model application-level determinations, delayed-onset studies, repeated studies, clinical-trial determination, study population, enrollment dimensions, protection/monitoring, protocol, outcomes, regulatory, and dissemination content as composable declarative blocks.
- Represent enrollment as a dimensional structure rather than 115 independent semantic questions.
- Resolve the blocked calculation question from authoritative evidence; do not infer entered versus derived values.
- Emit schema, UI, conditions, validation, calculations, mappings, provenance, and review state through the portable artifact contract.
- Add only demonstrated generic runtime capabilities and no form-specific compiler or adapter branches.
- Validate representative nested/repeated states, conditional transitions, save/reload, locked/print, XML/XSD, submission, and accessibility.
- Register only after applicable human semantic, policy, accessibility, instruction, and operational gates pass.

# Exit evidence

Record which capabilities were genuinely new so PHS Inclusion Enrollment Report can prove reuse rather than reproduce the same model.

# Implementation receipt

- Producer PR [#62](https://github.com/mikec-ai/grants-form-spec/pull/62) merged as `94a4d232f8b96ef09b09f36d4637156d62a25b65` after independent approval at exact corrected head `4a266ff557cdce976b0faa6375a4da5dec7e9471`.
- Exact source bytes pinned: parent XSD `29d859de…`, embedded study XSD `799205de…`, F705 DAT `b02d1877…`, read-only PDF `b56ab18e…`, XFA PDF `1b478db3…`, Forms I guide `97b323be…`, and complete shared XSD closure.
- The full embedded Human Subject Study is structured canonical data. Fifteen narrative document roles remain distinct semantic attachment questions.
- Enrollment is one `clinical-study/inclusion-enrollment-report` semantic composite with 115 unique coordinate-qualified leaf paths. It is not 115 question-bank identities.
- All 28 total-like coordinates remain applicant-entered/observed values. No calculations were emitted. An arithmetically inconsistent but XSD-valid payload is a required negative test.
- The eleven F705 conditions are preserved literally as portable `source-bound-uncompiled` evidence, and one unresolved calculation record accounts explicitly for all 28 total-like coordinates. Zero conditions or calculations are inferred or emitted as executable rules.
- The three official pre-populated determinations are visible read-only system references and excluded from applicant-question coverage. Application id, study id, and report id remain hidden read-only technical controls.
- Narrow human-subject indicator, exemption-status, and exemption-number semantic blocks are composed by both this form and R&R Other Project Information. The PHS occurrences are role-qualified as system-owned/read-only without composing the broader IRB/assurance block.
- Exact parent/embedded XML sequencing validates offline against the complete digest-pinned XSD closure for minimal, delayed-onset, comprehensive all-fields, and structured-study payloads. Both exemption wrappers reject empty arrays; all nested repeat maxima (20, 50, 100, 150, and 200) accept the boundary and reject boundary plus one; source 1..N strings reject empty values.
- One demonstrated generic capability was added: fail-closed flattened scalar array items for direct repeated simple-content XSD elements such as `EnrollmentCountry`, `StudyConditions`, and wrapped `ExemptionNumber`. The contract schema and reference runtime reject illegal context and ignored properties. No form-id branch was added.
- Generic form-local overrides now route inherited fields to sections and project read-only status into both portable JSON Schema and SGG UI without redeclaring question semantics. `visibleReadOnly` distinguishes visible reference/system controls from the existing hidden/null behavior for technical identifiers and fails validation unless paired with `readOnly`. Generic occurrence lineage retains narrow question identity through a form's narrowing redeclaration.
- Generic analysis now resolves local `#/$defs/...` references relative to the external question-bank document that owns them. The enrollment workbook regression reports coordinate leaves as integers bounded `0..999999999`, not object/null.
- Preflight passes: 108 TypeScript tests, 219 Python tests with one existing skip, artifact validation across 230 blocks/1,265 artifacts, promotion validation, packaging verification, and zero unclassified form fields.
- Hosted CI passed at the exact reviewed head. Independent source/architecture review found no remaining producer defects.
- Remaining human gates: semantic acceptance, policy/instruction reconciliation (especially totals), and production/consumer release review. Dimensional grid headers, keyboard navigation, focus/error behavior, and screen-reader rendering remain explicitly unresolved consumer/human accessibility gates; the producer proves only unique coordinate paths and error-routing identity.

[depends on](release-rr-key-person-expanded-canary.md)

[depends on](build-generic-xml-xsd-conformance-harness.md)

[depends on](enforce-rule-evidence-target-coverage.md)

[consumer delivery follows](automate-cross-repo-form-promotion.md)

# Consumer banking receipt

Draft public-consumer PR https://github.com/mikec-ai/simpler-grants-gov/pull/58 banks this producer package from immutable producer revision `70fa65f82f66901f8a6a330aa8ef70479ded9b5e`. After rebasing over automated promotion PR #56 and manifest-derived boundary PR #59, PR #58 adds only PHS Human Subjects and Clinical Trials plus PHS 398 Research Plan; its final base is `c7a3a9e9da217131bc38a9b1bc7d57d3a273796d` and head is `b0ab837dc1be0f1af89cd95a2439ddad0f2fa40c`. The delta is artifact/XSD-only and classifies as bank-only. It adds no runtime identity or registration. Consumer human semantic, accessibility, lifecycle, and release gates remain open and are not implied by artifact banking.
