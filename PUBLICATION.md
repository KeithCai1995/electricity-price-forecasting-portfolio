# Publication snapshot — 23 October 2026

This is a focused distribution of corrected v1.1.0 and the 21 October
rolling-window control. It retains the active source, tests, configurations,
simulated data, corrected reference results and report.

The source revision is `72d137a5c21464f74a265284606162b61b69393c`, merged into the
development repository as `4242f2734ce62d8b81f2ed24cd2cc2294db58c16`. The publication
copy updates navigation and report publication details; experiment code and
numerical reference results are retained.

The new repository starts with one snapshot commit. It does not contain earlier
Git commits, the superseded v1.0.2 archive or the development `evidence/` directory.
The original repository and its history are not deleted by this publication.
References to earlier results in the report describe earlier experiments, not
additional files distributed here.

## Manifests and dated records

- `PUBLICATION_MANIFEST.json` inventories the files in this publication snapshot
  with SHA-256 hashes. The manifest itself is excluded from its own inventory.
- `corrected_v110/release_verification.json` contains the dated saved-output
  verification record. Its source paths and hashes describe that revision; some refer
  to development files not distributed here.
- `corrected_v110/supplementary_20261021/study_manifest.json` records the
  supplementary study's execution snapshot and reference-input checks, not the
  entire current repository.

Recorded source hashes, experiment dates and numerical values have not been
rewritten to make these older records describe this publication. `<WORKSPACE>`
in a path is a redacted machine-specific prefix, not an executable directory.

Current verification commands are in [VERIFICATION.md](VERIFICATION.md). GitHub
Actions results belong to the commit checked in this repository; development
repository runs are not substitutes for those results.
