# XML/XSD conformance harness

`conformance.grants_gov_xml` is a target-neutral reference interpreter for the resolved
`grants-gov-xml-profile/v1` contract. It exists to verify producer artifacts. It is not a
submission runtime and does not decide form semantics.

The interpreter executes only declarations already present in a resolved profile: namespaces,
root and item attributes, values, nested objects, flattened or wrapped groups, arrays,
attachments, source pointers, constants, value maps, leaf containers, and required empty-object
emission. It contains no form IDs or form-specific branches.

`ExactXsdFixture` keeps validation offline and reproducible. A form test supplies:

- the entrypoint XSD filename;
- each local XSD fixture path and its exact SHA-256 digest;
- the official source digest recorded in the resolved profile when the checked-in fixture was
  normalized for local dependency resolution; and
- any nonstandard remote dependency URI prefix used by the pinned XSD set.

The harness verifies all digests, rewrites only declared dependency filenames to their pinned
local copies, and invokes `xmllint --nonet`. It does not retrieve schemas during tests.

A new form test should therefore contain only representative canonical responses, attachment
metadata when applicable, pinned XSD fixture declarations, expected validity, and semantic XML
assertions such as element order or namespace-qualified values. SF-424C, SF-LLL, and R&R Senior/
Key Person Profile (Expanded) are the initial structurally distinct examples.

Exact XSD validity is necessary but does not establish semantic equivalence. Form-specific
assertions and source/version provenance remain with each form test and evidence sidecar.
