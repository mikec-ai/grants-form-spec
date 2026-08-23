# PHS Assignment Request implementation status

The producer now declares the PHS Assignment Request Form, FID 833, version 4.0 as thirteen
optional, fixed source occurrences composed from five source-local question blocks. The form does
not introduce an assignment workflow, lookup service, consumer rule, form-specific compiler path,
or renderer behavior.

## Source boundary

- Official XSD: `PHS_AssignmentRequestForm_4_0-V4.0.xsd`, SHA-256
  `7e697ee33ea6f72271c0d74fc48c61f4f81faa242a712a4c73e7898f6c4ab976`.
- Official DAT: `PHS_AssignmentRequestForm_4_0-V4.0_F833.xls`, SHA-256
  `e08625bf4ebaee23a66e1ef85346c83e86726a58e36a6c5705f66fffaf867255`.
- Official Grants.gov readonly XFA PDF, retrieved 2026-08-23, SHA-256
  `0fdcbdd7bc136ae2872b76fc61a6cb719d8d02d9a1967257a7c9c2e957e4680a`.
- NIH Forms I general instructions, section G.600, retrieved 2026-08-23, SHA-256
  `e12101cdc12d38cfc9942744e25aec93e28d0a0bee1465cbf615e7187cb64c54`.
- Deterministic crosswalk extraction: revision
  `4312f6504b060e2b9ffdbd2307fc41130c3123a0`, source-set SHA-256
  `63ef51469ecffd0b7a39bd58f827ebe88bc60e8d368ed0789e4608a862660b4b`.

The XSD and DAT establish three component slots of seven characters, three study-section slots of
twenty characters, one 1,000-character rationale, five forty-character expertise slots, and one
1,000-character reviewer-exclusion request. All thirteen source occurrences are optional and
applicant-entered. The source contains no calculation, condition, or enumerated-value contract.

## Declarative reuse

The fixed occurrences reference five portable blocks:

1. suggested awarding component;
2. suggested study section;
3. assignment-suggestion rationale;
4. reviewer expertise; and
5. excluded-reviewer request.

The numbered properties remain explicit because the official XML contract contains thirteen
distinct, ordered element names rather than repeated array elements. This preserves exact source
semantics while making question identity and intra-form reuse visible through standard `$ref`
composition.

## Explicitly unresolved

- Crosswalk concept assignments remain agent-proposed. The evidence sidecar publishes no accepted
  cross-form semantic mappings.
- Awarding-component and study-section entries remain constrained free strings. The sources do not
  define an enum or authorize this specification to select or validate participating components.
- The DAT and readonly PDF disagree on one illustrative study-section code (`BP10` versus `B10`).
  The declarative help omits that disputed example; a source-authority review is required before
  exact visual/instruction parity can be claimed.
- The reviewer-exclusion response is a single source-defined free-text field containing identity,
  affiliation, and rationale. It is not decomposed into reusable person or organization questions.
  Privacy, access-control, retention, logging, and assembled-application handling require consumer
  policy review.
- Save/reload, locked and print views, submission behavior, accessibility, and production
  registration are consumer/runtime acceptance gates. The producer proves schema, UI contract,
  source limits, XML ordering, and exact-XSD conformance only.
