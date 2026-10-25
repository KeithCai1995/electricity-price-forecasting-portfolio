# P1: Probabilistic electricity-price forecasting under regime shift

Reference implementation v1.1.0

**SIMULATED BENCHMARK — NOT FIELD DATA.** This report concerns a research-training
portfolio, not a named electricity market, employer, Tarim Oilfield or trading system.
The reference experiments compare established forecasting and calibration methods
on simulated data. Configurations, inputs and execution metadata accompany the
saved results; [VERIFICATION.md](../VERIFICATION.md) explains the current checks.

## Purpose and experimental design

The question is how raw quantile forecasts, static conformal calibration and a
rolling adaptive wrapper trade coverage against interval width when a simulated
electricity-price process changes regime. This is an implementation and evaluation
exercise using established methods; no new foundational algorithm is proposed.

The simulator produces 420 hourly days from 1 January 2024, with stable, volatile
and renewable-shift regimes. Its 10,080 rows yield 9,888 direct forecast examples
after eight days of history. Chronological issue-day splits contain 247 training,
82 calibration and 83 final-evaluation days. The final 1,992 targets span
3 December 2024–23 February 2025 and all belong to the renewable-shift regime.
The final block is reused for gamma sensitivities and is not an untouched test
set after that exploration.

Seven pooled histogram-gradient-boosting models estimate quantiles .05, .10, .25,
.50, .75, .90 and .95, using horizon as a feature. Each has 140 iterations; row-wise
sorting repairs quantile crossings. Features combine calendar variables, past
price summaries and simulated forecast proxies. Future realised covariates and
regime labels are excluded from model features. Static CQR uses either pooled
calibration scores or separate horizon scores. The adaptive wrapper retains 30
scores per horizon, target miscoverage .20 and reference gamma .015.

## Main baseline: seed 20260817

| Method | Coverage | Mean width | Interval score |
| --- | ---: | ---: | ---: |
| Raw quantiles | .556225 | 11.896091 | 34.007247 |
| Static CQR, pooled | .924197 | 27.580914 | 32.176642 |
| Static CQR, by horizon | .923695 | 28.378878 | 33.032735 |
| Adaptive CQR | .806225 | 21.274739 | 30.727504 |

Width is in EUR/MWh. Lower interval score is better. The median model MAE is
6.299118 versus 11.268044 for the seasonal-naive forecast; mean pinball loss is
2.016259. The reported approximate CRPS, 4.501505, integrates only the available
.05–.95 quantile grid and omits the tails; it is not exact full-distribution CRPS.
All methods share the same raw quantiles, so these point/quantile metrics cannot
distinguish interval wrappers. This sample does not establish general superiority.

<!-- PAGE -->

## Finite-sample conformal rank: implementation details

For calibration score `s_i = max(lower_i - y_i, y_i - upper_i)` and `n` finite
scores, set `k = ceil((n+1)*(1-alpha))`. For `1 <= k <= n`, the correction is sorted
score `s_(k)`, indexed `k-1` in code. If `k > n`, the augmented conformal score is
positive infinity and the interval becomes unbounded. Alpha must be finite and
strictly between zero and one. Empty, non-vector or nonfinite scores are rejected.

Passing `k/n` to `np.quantile(..., method='higher')` is not equivalent to selecting
`s_(k)`: NumPy maps that probability using `n-1` positions. For scores 0–19, alpha
.20 gives `k=17`: the required value is 16, whereas that quantile call returns 17.
Capping `k>n` at the largest finite score would also lose the augmented
infinity. Decimal alpha text is used for rank arithmetic to avoid `.7` at `n=9`
becoming the wrong integer through binary roundoff; adjacent representable alpha
values are tested separately.

The score convention is based on established
[conformalized quantile regression](https://arxiv.org/abs/1905.03222). Its standard
finite-sample coverage justification requires the relevant exchangeability
conditions. Changing the rank does not make those conditions hold in this
dependent, shifted simulator. The current rank selection and unattainable-rank
behavior are covered by regression tests.

![Corrected baseline coverage versus unconditional mean width.](../corrected_v110/baseline/outputs/figures/figure_2_coverage_width.png)

<!-- PAGE -->

## Gamma sensitivity and seed robustness

The reference gamma remains .015. The .030 and .050 runs are exploratory
sensitivities using the same seed, raw model and final block. They are not an
independent basis for selecting a universally optimal adaptation rate.

| Gamma | Adaptive coverage | Mean width | Interval score |
| --- | ---: | ---: | ---: |
| .015 | .806225 | 21.274739 | 30.727504 |
| .030 | .798193 | 21.107557 | 30.833048 |
| .050 | .795181 | 20.784492 | 30.999364 |

Here larger gamma slightly narrows intervals and reduces coverage; the interval
score worsens. This result is more cautious than a claim that faster
adaptation necessarily improves reliability. Static and raw metrics are unchanged
across these gamma runs, as expected.

Two additional simulation seeds use the entire unchanged baseline configuration,
including 420 days, seven quantile models, gamma .015 and all three rolling folds.
Together with the reference they give three baseline market simulations.

| Seed | Raw coverage | Adaptive coverage | Adaptive width | Adaptive score |
| --- | ---: | ---: | ---: | ---: |
| 20260817 | .556225 | .806225 | 21.274739 | 30.727504 |
| 20260818 | .539157 | .814257 | 22.176603 | 32.236669 |
| 20260819 | .558735 | .817269 | 22.474140 | 32.780810 |

Adaptive coverage ranges .806225–.817269 across these three seeds. These runs are
a limited simulator check, not a confidence interval for real-market coverage.
Changing the seed also changes the model's random seed; this experiment does not
separate model stochasticity from simulated-market variation.

<!-- PAGE -->

## Fixed-alpha rolling-window control

The static by-horizon method fixes a correction using all 82 calibration days;
the adaptive wrapper both rolls a 30-score buffer and updates alpha. A
gamma=0 control retains the identical rolling buffers, raw quantiles and alpha
target .20, isolating feedback from the rolling-window effect. Each of the three
baseline models was reconstructed once, and its test raw quantiles and
adaptive bounds matched the preserved reference exactly before comparison.

| Seed | Fixed coverage | Fixed width | Fixed score | Adaptive score |
| --- | ---: | ---: | ---: | ---: |
| 20260817 | .820281 | 21.768209 | 30.592811 | 30.727504 |
| 20260818 | .822289 | 22.472269 | 32.070489 | 32.236669 |
| 20260819 | .825803 | 22.681780 | 32.514927 | 32.780810 |

Feedback narrows widths by .208–.493 EUR/MWh and moves coverage nearer .80, but
worsens interval score in all three seeds by .135–.266. These data do not establish
an interval-score advantage for alpha feedback alone. The adaptive/static
comparison evaluates the combined wrapper. Shared raw frames, interval paths,
metrics and execution records are in `corrected_v110/supplementary_20261021/`.
This control reuses the existing final blocks rather than an untouched test set.

## Infinity and clipping are part of the method boundary

The update uses `alpha_next = clip(alpha + gamma*(.20-error), .01, .99)` and a
rolling score distribution. It is inspired by
[Adaptive Conformal Inference](https://arxiv.org/abs/2106.00170), but clipping
changes the unmodified recursion. The usual telescoping argument for that
recursion cannot be transferred to this wrapper without a new analysis.

With 30 scores, an alpha below `1/31` requires an infinite conformal bound. The
code honors that case, and the test suite verifies propagation into adaptive
intervals. In all five completed runs, final-test unbounded fractions are zero.
This observation does not justify replacing future infinities with finite caps.
If an unbounded interval occurs, unconditional mean width and interval score
remain infinite. Explicit `finite_only_mean_width` and `finite_only_interval_score`
columns describe the finite subset only; they do not replace full-sample metrics.

<!-- PAGE -->

## Stress subsets reveal conditional failures

Overall adaptive coverage close to .80 hides much poorer coverage among extremes
and flagged examples. Price extremes are the lower and upper empirical deciles
of the final outcomes, selected retrospectively for evaluation. They are not
issuance-time labels. The OOD flag uses a training-standardised feature-distance
score and a training 95th-percentile threshold; it is a simple diagnostic, not a
validated detector of operational failure.

| Subset | Rows | Raw coverage | Pooled coverage | Adaptive coverage |
| --- | ---: | ---: | ---: | ---: |
| All | 1,992 | .556225 | .924197 | .806225 |
| Price extremes | 400 | .350000 | .775000 | .605000 |
| OOD flag | 131 | .465649 | .832061 | .694656 |

For price extremes, adaptive mean width is 22.455469 and score is 53.229701,
compared with pooled width 29.173814 and score 47.900275. Adaptive calibration
does not dominate pooled calibration on this subset. OOD adaptive width is
22.096972 and score 38.840207. These small, dependent subsets do not support
precise inferential claims.

![Coverage by stress subset. Renewable shift and All refer to the same final rows.](../corrected_v110/baseline/outputs/figures/figure_5_subset_coverage.png)

All final-evaluation rows are renewable-shift examples: `Renewable shift` repeats
`All`. This table contains no volatile-regime rows and cannot establish performance
in that regime. The rolling diagnostics below cover earlier periods.

## Rolling-origin diagnostic

Each chronological expanding-window fold uses 42 calibration days, followed by
28 evaluation days (672 hours). Folds share one constructed timeline and are not
independent replications.

| Fold | Evaluation start | Raw coverage | Pooled coverage | Adaptive coverage |
| --- | --- | ---: | ---: | ---: |
| 1 | 2024-07-16 | .671131 | .791667 | .805060 |
| 2 | 2024-09-02 | .486607 | .578869 | .720238 |
| 3 | 2024-10-20 | .395833 | .784226 | .808036 |

Fold 2 adaptive coverage is only .720238. Reporting the final .806225 alone would
therefore hide a material reliability failure under a different segment of shift.

<!-- PAGE -->

## Timing and joint uncertainty limitations

Daily issue time is midnight and target horizon 1 is that same midnight.
Thus horizon 1 is nowcast-like and
the other targets have lead times 1–23 hours. A claim of operational 24-hour
day-ahead forecasting requires an adapter with a genuine prior issuance cutoff.

Price lags and summary features use past history. Forward fill uses observations
available before issuance; incomplete leading history is rejected rather than
backfilled from future values. Nonetheless, the load, renewable and temperature
forecast proxies are constructed from simulated realised series with added noise.
They are assumed available at issuance and may be more informative than actual
forecasts. There are no publication-vintage or revision records to prove real
availability. This distinction must carry into any downstream scheduling study.

Adaptive buffers are separate by horizon. An earlier horizon's outcome on the
same issue day does not update a later horizon's buffer. A horizon uses earlier
days' outcomes before its next prediction, assuming immediate publication once
the target is observed. Delays, settlement revisions and data outages require an
explicit operational availability model before deployment.

![First two weeks of corrected evaluation forecasts, with marginal adaptive intervals.](../corrected_v110/baseline/outputs/figures/figure_1_forecast_window.png)

An 80% hourly marginal interval does not imply an 80% chance that all 24 hourly
prices lie inside their intervals. These models do not calibrate a daily maximum
score, a simultaneous band, a temporal copula or joint scenario distribution.
Passing these marginal quantiles or widths into downstream optimisation does not
establish joint price-path calibration, guarantee a dispatch risk level, or prove
that a chosen CVaR objective is calibrated to realised losses.

Row-wise sorting also alters the original fitted quantile functions. Only seven
quantile levels are available; tail shape between and beyond them is not learned
by this report. The simple OOD score ignores temporal structure and feature
correlations. These are concrete directions for validation, not claims of solved
operational risk management.

<!-- PAGE -->

## Reproducibility and verification

Version metadata and runtime version are both 1.1.0. The reference environment
uses Windows Python 3.13.15, NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0 and
scikit-learn 1.8.0. Configurations, software versions and data fingerprints are
recorded with each run; `requirements-lock.txt` gives the reference dependencies.

The current verification consists of 28 unit and pipeline tests, checks of all
five saved reference runs, and replay of all three fixed/adaptive rolling-control
comparisons. The suite covers exact conformal ranks, alpha boundaries, ties,
invalid inputs, infinity propagation, conditional diagnostics, configured
quantile/coverage targets, plot ranges and protected output paths. Temporal tests
check chronological separation, forbidden future features, leading missing
history, horizon separation, and independence from an interval's own outcome.
Small real-model pipeline tests exercise the complete path without fitting the
full 420-day reference models.

The saved-output checker recalculates timing and interval metrics; the control
checker replays both rolling wrappers from saved raw forecasts. Neither checker
retrains a model or changes the reference files.
The GitHub workflow runs on Ubuntu and Windows with Python 3.11 and 3.13; its
results are in this repository's Actions tab. These are checks of specific
invariants and saved results, not a proof against every defect or of real-market
validity.

Five full corrected experiment runs are saved under `corrected_v110/`: baseline,
gamma .030, gamma .050, and additional baseline seeds 20260818/20260819. Each has
a manifest, four tables, six figures, simulated data and forecast exports.
Reference execution logs are in `corrected_v110/logs/`. Run and study manifests
retain the actual execution dates, software versions, source hashes and input
fingerprints. Current check results and output are in `verification/`. The separate
`PUBLICATION_MANIFEST.json` lists the distributed files and their hashes.

The baseline CSV has 1,992 rows and includes raw quantiles, pooled/horizon static
bounds, adaptive bounds, alpha, correction and OOD columns. To run the tests,
saved-result checks or a new experiment, follow the commands in
[README.md](../README.md). [VERIFICATION.md](../VERIFICATION.md) describes the
checks in more detail. Method references are in [RELATED_WORK.md](../RELATED_WORK.md).

Overall adaptive coverage is near .80 in the evaluated final blocks, while
stress subsets and one rolling fold fail.
Three simulated seeds do not establish real-market external validity, arbitrary
time-series coverage, or jointly reliable daily paths. A next study would need
real publication vintages, a true issuance gap, delayed-label handling, additional
untouched temporal blocks and an explicitly validated joint uncertainty model.

## Relevant verified primary references

Romano, Y., Patterson, E., and Candès, E. J. (2019).
[Conformalized Quantile Regression](https://arxiv.org/abs/1905.03222).
Source of the quantile-based conformity score and static CQR framework.

Gibbs, I., and Candès, E. (2021).
[Adaptive Conformal Inference Under Distribution Shift](https://arxiv.org/abs/2106.00170).
Source motivating the adaptive update; its guarantees are not asserted for this
clipped, rolling implementation.
