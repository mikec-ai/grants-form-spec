# Source version provenance

Form evidence records two different version concepts and never substitutes one for the other:

- `block.formVersion` identifies the canonical form artifact described by the sidecar. For form
  evidence, the projector verifies this value against the emitted package manifest.
- `sources[].nativeVersion` records the version stated by that exact XSD, DAT, PDF, instruction,
  or implementation source. A dependency keeps its own native version even when it supports a
  differently versioned form.

`nativeVersion: null` means the source does not state a version or the version is unknown. Null is
preferable to copying the form version, parsing a nearby source, or inventing a PDF, DAT, or
instruction version. The URI and SHA-256 still pin the exact source bytes.

The evidence projector checks the authorized XSD filename format, such as
`GlobalLibrary-V2.0.xsd`. A version-looking XSD filename in another format fails with an actionable
error instead of silently becoming unknown. The crosswalk promotion importer applies the same
rule.

A `V` token in a DAT, PDF, instruction, or implementation filename is not enough to establish that
source's native version; it may describe the containing form or another publication context. The
importer emits null for those source types unless independent evidence supplies an exact native
version. These checks concern source identity only; they do not accept or alter semantic mappings.

## Known R&R SF-424B schema metadata defect

The official `RRSF424_SF424B-V1.1.xsd` is retained byte-for-byte at SHA-256
`511de9a5594a739ce596a33a92d3dec1bac2a32f193a2fe6b4799b45f29ff296`. Its
`xsd:schema/@version` value is `1.0`, while its official URL and filename, target namespace,
fixed root `FormVersion`, and required `FormVersionIdentifier` all identify version `1.1`.

This discrepancy is treated as an upstream schema-document metadata defect rather than a wire
version conflict. The XML Schema specification defines the schema `version` attribute as a token
for user convenience and assigns it no validation semantics. Generated R&R SF-424B XML uses the
1.1 namespace and version values and validates against the exact pinned official XSD. The source
bytes must not be edited to make the metadata internally consistent.

Specification: <https://www.w3.org/TR/xmlschema-1/#declare-schema>
