# Attachment Form portable parity

Attachment Form (Grants.gov FID 540, version 1.2) is authored as 15 optional, ordered
attachment positions. It is deliberately not collapsed into one attachment array. The official
XSD defines the ordered wrappers `ATT1` through `ATT15`; when a wrapper is present, its
corresponding `ATTnFile` child is required.

## Authority and provenance

The form evidence sidecar pins the exact official XSD, DAT workbook, instructions PDF, read-only
PDF, and sample PDF by URL, native version where stated, and SHA-256 digest. The physical official
form XSD has SHA-256
`c6b7f40614a2077818f5f3b5df72959f867611b887c5b888005df8adeaa5e8e9`.
The checked-in conformance fixture is a whitespace-normalized copy with its own separately checked
digest; the resolved profile continues to require the official digest.

The differential SGG oracle is the pre-prototype upstream revision
`f84313418e237526adb90c5e57edef0b1bef0490`. Its form declaration is pinned as implementation
evidence, not treated as source or semantic authority. The UUID in that implementation is not
promoted into the portable contract because it is an implementation identity rather than an
official Grants.gov identifier.

## Reuse and semantics

All 15 properties compose `generics/ordered-attachment-slot`, which itself composes the existing
`generics/attachment` capture mechanism. Both blocks are classified as capture mechanisms. The
form therefore adds zero semantic-question identities. Which information an agency expects in a
given position comes from external agency instructions and must not be inferred from the slot
number or the repeated control shape.

The prior crosswalk proposal that all slots share an “ordered generic attachment” concept remains
unreviewed and is excluded from published semantic coverage. XML and UI occurrence bindings are
source-bound independently of that proposal.

## Verified producer parity

The producer test suite verifies:

- no attachment position is required at the form level;
- all 15 labels, descriptions, sections, and attachment-validation rules match the pinned SGG
  oracle;
- the exact narrative instructions and sequence warning appear in both the portable UI artifact
  and the SGG projection;
- empty, single, sparse, replaced, removed, and fully populated responses render without a
  form-specific compiler or interpreter branch;
- sparse and full XML preserve the official `ATT1` through `ATT15` sequence;
- present wrappers always contain their required `ATTnFile` leaf and standard attached-file data;
- empty, single, sparse, and fully populated XML validate offline against the pinned XSD closure;
  and
- an unresolved attachment reference fails closed.

The portable schema uses one additional standard `$ref` hop through
`generics/ordered-attachment-slot`, rather than copying the legacy schema's attachment fragment 15
times. The resolved value contract remains the same UUID-formatted attachment reference. This is
an intentional composition difference, not a semantic or runtime difference.

## Remaining consumer and release gates

Save/reload, locked view, print view, attachment ownership/audit behavior, and application
submission are runtime lifecycle concerns. The legacy tests at the pinned SGG revision establish
the differential oracle, but this producer repository does not claim to execute those services.
The supervised producer-to-SGG promotion task must run those cases against the portable package
before registration. Accessibility, semantic acceptance, instructions review, and release
approval remain separate human gates.
