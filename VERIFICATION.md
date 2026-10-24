# Verification

The 23 October 2026 publication copy passed all 28 tests, all five saved-output
comparisons and all three rolling-control replays locally. Source, tests,
configurations, data, corrected reference files and the workflow were also
byte-checked against the source revision. These local checks are separate from
the new repository's GitHub Actions results.

Run these commands from the repository root after installing
`requirements-lock.txt`:

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/check_saved_outputs.py
python -B scripts/check_rolling_control.py
```

| Check | What it checks |
| --- | --- |
| 28 tests | Conformal ranks and infinite bounds, time ordering, configuration changes, output protection, plot axes, and a small real-model pipeline run |
| Saved-output check, five runs | Recomputed interval metrics, forecast ordering and timestamps against the saved results |
| Rolling-control replay, three seeds | Fixed-alpha and adaptive interval paths and metrics reconstructed from the saved raw forecasts |

The last two checks read the reference files without fitting models or rewriting
them. The pipeline smoke test fits a small dataset; it is not a full rerun of the
420-day reference experiments.

## Workflow

[The workflow](.github/workflows/verification.yml) runs the same three commands
on Ubuntu and Windows with Python 3.11 and 3.13. Results for this repository are
listed in [GitHub Actions](https://github.com/KeithCai1995/electricity-price-forecasting-portfolio/actions).
A result applies to its checked commit, not automatically to later revisions or
to another repository.

## Reference records

The reference outputs retain their original execution dates. Logs are in
`corrected_v110/logs/`; the fixed-alpha study and its manifest are in
`corrected_v110/supplementary_20261021/`. The original 18 October suite had 16
tests. Subsequent regression tests brought the current suite to 28.

During the 21 October development update, a full default rerun matched all six
baseline CSVs byte-for-byte, including the forecast used by the storage project.
That dated comparison is separate from the lightweight checks above. Repeating
it requires a new full run, not just a passing unit-test job.

The [publication notes](PUBLICATION.md) distinguish dated run manifests from the
current snapshot's file inventory.
