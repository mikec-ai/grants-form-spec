# Portable form proof package

The proof package is a generated, review-oriented index of claims that the implementation can
currently support. Its authored source is `proof-package/v1/proof-package.json`; generated files
belong under `build/proof-package/` and are not runtime source.

Build it with:

```shell
npm run proof-package
```

The command produces:

- `build/proof-package/index.md`, a short human-readable evidence index;
- `build/proof-package/proof-manifest.json`, the same claims with resolved source links, exact
  revisions, and SHA-256 digests for producer evidence files.

The builder fails when a claim lacks evidence, reproducibility steps, or an explicit limitation.
Producer evidence is read from the exact pinned Git revision rather than the current working tree.
Consumer browser receipts remain generated build outputs and are reproduced from their pinned fork
commits; the package records their expected paths without checking bulky media or oracles into this
repository.

The reviewed pairwise claim points to the corrected analysis contract and generated outputs. Those
outputs currently report zero accepted occurrence mappings, so reviewed pairwise values are blank,
not zero. Exploratory similarity remains available as a separately labeled implementation-derived
artifact and is not published semantic coverage.

CI publishes the generated index and manifest as the `portable-form-proof-package-<revision>` build
artifact. Generated output remains ignored locally and is never committed as runtime source.
Because exact historical evidence is part of the contract, CI checks out full Git history and the
builder fails closed when a declared revision or path cannot be resolved.
