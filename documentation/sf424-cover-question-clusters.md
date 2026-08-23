# SF-424 cover question clusters

This slice classifies the 50 cover-field occurrences that remained after the lifecycle,
attestation, and residual-reference passes. It preserves three separate concerns:

- semantic identity: the canonical question block;
- capture actor: who supplies the response in this form occurrence; and
- source authority: the pinned XSD, DAT, PDF, or instructions that constrain the occurrence.

Every mapping remains `proposed`. None contributes to published similarity metrics until a
reviewer accepts it. Similar labels, scalar types, or validation shapes are not treated as proof
of semantic equivalence.

## Conservative partition

| Forms | Occurrences | Canonical blocks | Boundary |
| --- | ---: | ---: | --- |
| SF-424 | 13 | 9 | Standard-cover identities remain distinct from R&R identities. |
| R&R SF-424 | 19 | 8 | Includes the independently resolved previous Grants.gov tracking number. |
| R&R Multi-Project Cover | 18 | 7 | Reuses the R&R blocks while preserving optionality and UI behavior at the occurrence. |

The two R&R forms share submission type, applicant control identifier, prior Federal award
identifier, applicant type, application type, estimated project funding, and State review.
SF-424 uses separate standard-cover blocks for analogous concepts because the current evidence
does not establish cross-family semantic equivalence. Its organizational unit and contact
affiliation fields use domain-specific organization and point-of-contact blocks.

## Evidence boundary

The exact source paths and proposal notes live in the three form evidence sidecars. The primary
pinned sources are:

- SF-424 4.0 XSD, SHA-256 `21670776cc2751c806b1ec43a59d6296628e219733bc654cf518ede5b9ae0364`;
- R&R SF-424 5.0 XSD, SHA-256 `f140f32afed9d7efbe30fc8f299542bbbc3121dbc87a79aa351fcf096163d3bc`;
- R&R SF-424 instructions, SHA-256 `666647fdeb7d9d69f2d36dedc74f09ff6a9540776f87c5a5c5b0593219736bd1`;
- R&R Multi-Project Cover 4.0 XSD, SHA-256 `5d5599068d721e6554fa442df88711f8d9386a5fafc18b01cb1d1becc41f84e7`; and
- R&R Multi-Project DAT, SHA-256 `361e00da500cb092997dadefcac9723cba3be63417a46375d2a5845797beae8e`.

The R&R PDFs are XFA forms whose fallback pages do not expose reliable field semantics outside
Adobe Reader. Their hashes remain pinned, but this pass does not infer semantic equivalence from
the fallback rendering.

## Mechanical guarantees

The emitted field-occurrence index is authoritative for path-qualified form-to-question lineage.
The analyzer supplements flattened JSON Schema references from those exact leaf occurrences only
when the question has an explicitly authored response role. Tests require all 50 source-bound
occurrences to appear at their exact paths, remain proposed and unpublished, and retain
`applicantInput` capture roles. The unclassified-field ratchet now resolves all 76 identities in
its original baseline without deleting or rewriting the baseline.
