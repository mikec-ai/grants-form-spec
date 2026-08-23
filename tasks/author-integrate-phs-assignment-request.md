---
type: Task
title: Author and integrate PHS Assignment Request
priority: P1
description: >-
  Deliver the small high-volume assignment-preference profile without
  introducing a PHS-specific workflow engine.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:57:45.454Z'
---
# Goal

Author PHS Assignment Request as a small, high-volume, bounded review-routing profile.

# Evidence starting point

- The research factory records fourteen source question/structure records and thirteen behavior records with a complete behavior partition.
- Two-year usage evidence records 237,461 form instances.

# Acceptance criteria

- Pin and promote exact official XSD, DAT, PDF/XFA, instruction, version, and hash evidence.
- Model awarding-component preferences, study-section preferences, rationales, reviewer expertise, and excluded-reviewer requests declaratively.
- Keep the bounded assignment-preference profile separate from the common application core and from SGG-specific workflow orchestration.
- Reuse canonical identity or organization concepts only where role-qualified semantic evidence supports them.
- Validate optional and repeated preferences, limits, save/reload, locked/print, XML/XSD, submission, and accessibility.
- Add no PHS-specific workflow engine and no form-specific compiler or adapter branch.
- Register only after applicable semantic, privacy, policy, instruction, accessibility, and operational gates pass.

# Exit evidence

Record whether this high-volume form landed without a runtime extension and its marginal implementation effort.

[depends on](release-rr-key-person-expanded-canary.md)

[depends on](build-generic-xml-xsd-conformance-harness.md)

[depends on](enforce-rule-evidence-target-coverage.md)

[consumer delivery follows](automate-cross-repo-form-promotion.md)
