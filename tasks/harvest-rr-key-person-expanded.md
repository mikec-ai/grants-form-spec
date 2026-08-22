---
type: Task
title: Author and integrate R&R Senior/Key Person Profile (Expanded)
superbee_progress_status: done
priority: P1
assignee: codex
description: >-
  Use the deterministic promotion pipeline to author the next high-value
  foundation form. Establish portable repeating senior/key person, role,
  organization, address, credential, profile attachment, and support attachment
  concepts; preserve exact XSD/DAT/PDF provenance; keep all semantic mappings
  unaccepted until reviewed; validate through the public Simpler adapter without
  form-specific runtime code.
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T23:19:15.769Z'
---
# Objective

Add R&R Senior/Key Person Profile (Expanded) as a source-bound declarative foundation for repeating research-person information.

# Completed result

- Producer PR #23 added the form and reusable research-person declarations; producer PR #24 corrected generic repeated-row conditions to use Simpler item scope.
- Adapter PR #20 pinned producer revision 7b1977294129d452e5810c35695d259d8060dd20 and proved the form loads with no form-specific adapter code.
- The form emits 57 fields, a 99-person repeat limit, seven attachment validations, exact project-role wire values, and six typed UI conditions.
- Per-person biographical sketch and support requirements remain semantic questions; the three overflow uploads are explicitly capture mechanisms.
- Deterministic evidence is pinned to crosswalk revision 4312f6504b060e2b9ffdbd2307fc41130c3123a0 and source-set hash 8866396d99e32eeec6618ea63c52c2b205718dc481482b27ab61699ecd2efeb0.
- No semantic mapping is accepted. XML, human semantic review, accessibility, and production release remain explicit gates.

# Validation

Producer preflight passed with 539 artifacts, 64 TypeScript tests, 34 Python tests, and reproducible packaging. The public-fork adapter passed 80 form-spec tests plus focused Ruff and mypy checks.
