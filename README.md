# Electricity-price forecasting under regime shift

A simulated benchmark comparing quantile forecasts, static conformalized quantile
regression (CQR), and a rolling adaptive CQR wrapper. It asks how their coverage,
interval width and interval score change when the price-generating regime shifts.

## Main findings

The baseline uses a 420-day simulator, a chronological train/calibration/test
split, and an 80% hourly marginal coverage target. Its 83-day final test contains
1,992 hourly targets in the renewable-shift regime.

| Method | Coverage | Mean width (EUR/MWh) | Interval score |
| --- | ---: | ---: | ---: |
| Raw quantiles | .556225 | 11.896091 | 34.007247 |
| Static CQR, pooled | .924197 | 27.580914 | 32.176642 |
| Static CQR, by horizon | .923695 | 28.378878 | 33.032735 |
| Adaptive CQR | .806225 | 21.274739 | 30.727504 |

Lower interval score is better. These are seed 20260817 results with adaptive
gamma=.015, not a general ranking of methods.

The [rolling-window control](corrected_v110/supplementary_20261021/README.md)
keeps the same raw forecasts and 30-score buffers while setting gamma=0. Across
the three existing seeds, alpha feedback narrows intervals and brings coverage
closer to .80, but slightly worsens interval score in every seed. The comparison
with static CQR combines rolling-window and feedback effects; the control
separates them.

The [report source](report/report_v110.md) and
[PDF report](report/Haorui_Cai_Forecasting_Report_v110.pdf) give the full results,
calibration details, stress subsets and rolling-origin diagnostics.

## Run and check

Use Python >=3.11. From the repository root, create and activate a virtual
environment, then run the following in PowerShell:

```powershell
python -m pip install -r requirements-lock.txt
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONPATH=(Join-Path (Get-Location).Path 'src')
$env:MPLCONFIGDIR=(Join-Path (Get-Location).Path '.matplotlib')
$env:OMP_NUM_THREADS='2'
python -B -m unittest discover -s tests -v
python -B scripts/check_saved_outputs.py
python -B scripts/check_rolling_control.py
python -B scripts/run_experiment.py --config configs/base.yaml --output-root local_runs/baseline
```

The tests include small real-model pipeline runs. The two saved-result checks
do not fit models or change the reference files. See [VERIFICATION.md](VERIFICATION.md)
for the scope of the 35 tests, five saved-output checks, three rolling-control
replays and the GitHub workflow.

To reproduce the remaining reference experiments, choose a new output directory
for each run:

```powershell
python -B scripts/run_experiment.py --config configs/gamma_030.yaml --output-root local_runs/gamma_030
python -B scripts/run_experiment.py --config configs/gamma_sensitivity.yaml --output-root local_runs/gamma_050
python -B scripts/run_seed_check.py --seed 20260818 --output-root local_runs/seed_20260818
python -B scripts/run_seed_check.py --seed 20260819 --output-root local_runs/seed_20260819
python -B scripts/run_rolling_control.py --output-root local_runs/rolling_control
```

The scripts import this checkout's `src`, even if another editable installation
exists. New runs record their configuration, software versions and data
fingerprint. A nonempty output directory can only be reused with `--overwrite`
and a recognized P1 marker or run manifest; source and reference directories are
protected. `local_runs/` and `.matplotlib/` are ignored by Git.

To rebuild the report, install `requirements-report.txt` and run
`python scripts/build_report.py`. This rewrites the report PDF, not the experiments;
inspect the rendered pages after changing the report source.

## Repository map

| Location | Contents |
| --- | --- |
| `src/energy_forecasting/` | Simulator, features, models, calibration, metrics and output handling |
| `tests/` | Regression tests and pipeline smoke tests |
| `configs/` | Baseline and gamma-sensitivity configurations |
| `data/` | Original simulated input and data notes |
| `corrected_v110/baseline/` | Corrected reference run, seed 20260817, gamma .015 |
| `corrected_v110/gamma_030/`, `gamma_050/` | Same-seed gamma sensitivities |
| `corrected_v110/seed_20260818/`, `seed_20260819/` | Additional full baseline seeds |
| `corrected_v110/supplementary_20261021/` | Fixed-alpha control, raw forecasts and replay results |
| `corrected_v110/logs/` | Reference experiment execution logs |
| `verification/` | Current test results, saved-output checks and rolling-control replays |
| `report/` | Current report source and PDF |

The baseline forecast exported for the downstream storage project is
`corrected_v110/baseline/outputs/forecast_quantiles_test.csv` (1,992 rows).
Run and study manifests record execution dates, inputs and software versions;
`PUBLICATION_MANIFEST.json` inventories the distributed files. See
[PUBLICATION.md](PUBLICATION.md) for the scope of this repository.

## Scope and limitations

The data are simulated, not employer, Tarim Oilfield, named-market or live-trading
data. Forecast proxies use noisy simulated realised covariates rather than actual
publication vintages. Lagged prices use past history without future backfill.
Daily issue time equals the first target time, making horizon 1 nowcast-like;
operational day-ahead use needs a genuine prior issuance cutoff.

The intervals are hourly marginal intervals, not jointly calibrated 24-hour paths.
The adaptive wrapper uses 30 past scores per horizon and clips alpha to [.01,.99],
changing the original ACI recursion. Outcomes are assumed available immediately
for the next update. Dependence, regime shifts, data delays and revisions limit
what these measured coverages establish.

The conformal rank is `ceil((n+1)*(1-alpha))`; an unattainable rank produces an
infinite correction. Full-sample metrics retain infinite means, with
`finite_only_*` diagnostics reported separately. The five reference runs have no
unbounded final-test intervals; this does not make all future runs finite.

The same final block is reused for gamma diagnostics. All final-test rows belong
to the renewable-shift regime, so that subset repeats the overall result. Earlier
rolling folds show coverage failures. Three seeds offer a small robustness check,
not an untouched evaluation set or population-level inference.

The methods are established; references and contribution boundaries are in
[RELATED_WORK.md](RELATED_WORK.md). [RESPONSIBLE_USE.md](RESPONSIBLE_USE.md) covers
the data-use scope.

## Reading the study

Start with the [report](report/Haorui_Cai_Forecasting_Report_v110.pdf) for the
experimental design, results and limitations. [VERIFICATION.md](VERIFICATION.md)
explains the checks and their scope; [PUBLICATION.md](PUBLICATION.md) describes
the distributed material and file inventory.
