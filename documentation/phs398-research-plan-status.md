# PHS 398 Research Plan implementation status

PHS 398 Research Plan, Grants.gov FID 797, version 5.0, is authored as thirteen
role-qualified semantic attachment questions over one shared attachment capture mechanism. The
producer preserves the source order, form metadata, applicant limits, XML wrappers, and exact XSD
validation without a form-specific compiler, adapter, renderer, or conformance branch.

## Source boundary

- Official XSD `PHS398_ResearchPlan_5_0-V5.0.xsd`, SHA-256
  `6e7171465d1f44a16eb822f8921423ceede4fa486cb0819bc5dd327121b4bb56`.
- Official DAT `PHS398_ResearchPlan_5_0-V5.0_F797.xls`, SHA-256
  `61af459ba15e7a4ef5ddc4856a598561ce91bccb19f34084e977edb4eb4e7c88`.
- Official read-only PDF, SHA-256
  `1ae85b51a0502315b0370e596660c9c9518458152af3c15f1ef1c1d35638a12b`.
- Official sample XFA PDF, SHA-256
  `587caf4945c63fd5070d28ae79d924d5a24c647231f8fdb32e17040b794b93db`.
  Its form content requires Adobe's XFA runtime, so it is pinned as evidence and is not presented
  as a successfully rendered oracle.
- Deterministic normalized capture of NIH Forms I section G.400, generated from the live HTML and
  downloadable guide without OCR. The capture pins the live HTML, Forms I PDF, release and revision
  labels, selection method, role applicability, and source conflicts.
- Deterministic crosswalk extraction at revision
  `4312f6504b060e2b9ffdbd2307fc41130c3123a0`. Its semantic assignments remain proposals, not a
  legacy implementation oracle or accepted equivalence review.

The XSD closure separately pins Attachments 1.0, Global 1.0, GlobalLibrary 2.0, and the transitively
imported UniversalCodes 2.0. The source XSD's namespace prefix incorrectly names a V4.0 URI; the
profile follows the XSD `targetNamespace`, which is V5.0, and records the source defect.

## Meaning and capture

Each content role has its own draft semantic identity: Introduction, Specific Aims, Research
Strategy, Progress Report Publication List, Vertebrate Animals document, Select Agent Research,
Multiple PD/PI Leadership Plan, Consortium/Contractual Arrangements, Letters of Support, Resource
Sharing Plans, Other Plans, Key Resource Authentication, and Appendix document. All thirteen extend
`generics/attachment` and inherit applicant-input ownership.

The shared attachment block describes how a file reference is captured. It does not make the
content requests equivalent. In particular, the Vertebrate Animals document is not the same
question as the R&R Other Project Information yes/no animal-use response.

## Requiredness and application context

Research Strategy is the only unconditionally required XSD wrapper. Three official requirements
depend on responses held elsewhere in an application:

1. Introduction is enabled and required for Resubmission or Revision.
2. Progress Report Publication List is required for Renewal.
3. Vertebrate Animals is required when the R&R Other Project Information response says animals are
   used.

The normalized instruction artifact represents each condition with its canonical source block,
source path, operator, values, effects, authority, and evidence records. All three are explicitly
`source-bound-unresolved-cross-form`. The current portable contract cannot project application-level
references into a standalone form, so the form does not invent a local context field or emit a
misleading SGG rule. Specific Aims likewise remains optional in the standalone schema because the
guide's requirement can be overridden by a NOFO while the XSD and DAT make it optional.

## Appendix cardinality

The imported XSD type permits zero through 100 `att:AttachedFile` records. The DAT and current NIH
Forms I guide limit applicants to ten PDFs. The portable applicant JSON Schema therefore sets
`maxItems: 10`; the XML profile remains mechanically capable of representing the wider XSD envelope
and validates both limits without claiming that the XSD itself says ten.

Supporting the Appendix required one generic conformance improvement: an attachment mapping may be
flattened into an array's already-declared item element. The contract, reference interpreter, and
synthetic regression test define that operation once. The form profile only declares its wrapper,
item, and shared attached-file mapping.

## Verified producer behavior

Producer tests verify:

- thirteen distinct semantic question references and one transitive attachment mechanism;
- exact form identity, labels, section order, response roles, and attachment validators;
- proposed-only semantic mappings and zero accepted mappings;
- the three structured cross-form conditions without fake local paths;
- the ten-file applicant limit alongside the XSD's 100-file technical envelope;
- minimal, cross-form-applicable, fully populated, and over-ten technical XML payloads;
- exact singleton and Appendix wire order and namespaces;
- offline validation against the pinned XSD closure; and
- failure on a missing required Research Strategy or unresolved attachment reference.

Analysis is generated from the emitted declaration. It reports thirteen semantic questions and one
shared capture mechanism, with the Appendix association at the repeated item path.

## Remaining gates

- The three cross-form conditions need an application-level declarative contract and consumer
  support before they can execute.
- Specific Aims requiredness needs NOFO-aware policy composition rather than a universal local rule.
- Semantic mappings remain proposed and require human acceptance before published coverage.
- PDF/XFA behavior, save/reload, locked and print views, attachment ownership and audit behavior,
  submission, accessibility, registration, and release approval remain consumer or human gates.
- No legacy Simpler implementation was found, so this package claims source conformance rather than
  differential runtime parity.

## Marginal implementation receipt

The form reused the existing attachment reference block, attachment validation inference, attached
file XML field mapping, evidence projection, analysis exporter, zero-unclassified gate, exact-XSD
harness, and target-neutral form compiler. New source consisted of thirteen semantic role
declarations, one form composition, one XML profile, one evidence sidecar, one normalized instruction
capture, source fixtures, and tests. The only reusable capability added was flattened attachment
items inside a declared collection wrapper.
