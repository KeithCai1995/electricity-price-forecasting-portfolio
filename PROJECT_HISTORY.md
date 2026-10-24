# Project history

This repository is a publication snapshot prepared on 23 October 2026. Its new
Git history starts with this snapshot, not with the start of the project. The
development repository and older material are retained separately.

## Timeline

- **22 September 2026:** the development project was placed under version control;
  imported material predates that history.
- **18 October 2026:** corrected v1.1.0 adds finite-sample conformal rank fixes,
  regression tests, five corrected reference runs and seed checks.
- **19 October 2026:** a personal rerun completed the original 16-test suite and
  baseline, matching the reference metrics. Those personal logs are stored
  separately, not included in this snapshot.
- **21 October 2026:** configuration-aware quantiles and plot targets, output
  safeguards, future-information tests and a real-model smoke test were added.
  A full default rerun reproduced all six baseline CSVs byte-for-byte. The
  supplementary study compares fixed and adaptive alpha using the same raw
  forecasts and 30-score buffers. Feedback narrows intervals but slightly worsens
  interval score for all three seeds.
- **21 October 2026, presentation follow-up:** machine-specific workspace prefixes
  in published records were replaced with `<WORKSPACE>`. Five rolling-coverage
  figures were redrawn from saved forecasts to show the full 0–1 range, and a
  plot regression brought the suite to 28 tests. No model refitting was needed.
- **22 October 2026:** documentation and comments were simplified without changing
  the experiment logic or numerical outputs.
- **23 October 2026:** this distribution snapshot keeps the current code, tests,
  corrected outputs, rolling-control study and report. Superseded reports,
  development archives and the old Git history are not copied into this repository.
  Publication references and report front matter were updated for this layout.

## Sources

Initial code and reference analyses were supplied. Method sources are credited in
[RELATED_WORK.md](RELATED_WORK.md). Dated run records retain their original
execution metadata; the publication date does not replace those dates.

See [PUBLICATION.md](PUBLICATION.md) for the source revision and file inventory.
