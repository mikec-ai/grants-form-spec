---
type: Convention
title: View
governs: View
path: views-registry/
fields:
  required:
    - title
    - entry
    - access
  optional:
    - description
    - entry_version
    - presentation
  values:
    access:
      - none
      - bundle-read
      - bundle-propose
    presentation:
      - workspace
      - inline
      - adaptive
  terminal: {}
---
# View

A registered self-contained bundle View. `bundle-read` grants only the read bridge; mutations stay
in trusted CLI or shell workflows.
