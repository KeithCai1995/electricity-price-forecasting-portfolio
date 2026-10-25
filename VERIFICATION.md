# Verification

The current checks cover 35 unit and pipeline tests, five saved-output
comparisons and three rolling-control replays. Their execution metadata and
results are recorded in [verification/current_checks.json](verification/current_checks.json),
with output in [unit_tests.txt](verification/unit_tests.txt),
[saved_outputs.txt](verification/saved_outputs.txt) and
[rolling_controls.txt](verification/rolling_controls.txt).

Run these commands from the repository root after installing
`requirements-lock.txt`:

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/check_saved_outputs.py
python -B scripts/check_rolling_control.py
```

| Check | What it checks |
| --- | --- |
| 35 tests | Conformal ranks and infinite bounds, time ordering, configuration changes, reference-output protection, PDF link targets, plot axes, and a small real-model pipeline run |
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

The five forecasting runs are in `corrected_v110/`; the fixed-alpha study, shared
raw forecasts and execution manifest are in
`corrected_v110/supplementary_20261021/`. These records retain their actual
execution dates, configurations and software versions. Reference experiment logs
are in `corrected_v110/logs/`. The commands above verify saved results and replay
the calibration wrappers; they do not retrain all five reference models.

[PUBLICATION.md](PUBLICATION.md) describes the distributed material and its file
inventory.
