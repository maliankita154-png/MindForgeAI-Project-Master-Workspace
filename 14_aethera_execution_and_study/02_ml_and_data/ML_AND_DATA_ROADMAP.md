# ML & data roadmap

## Start with one pilot, not the planet

Select one named basin/city/reservoir with accessible history and a domain contact. Build reliable evidence there first. The default demonstration location in the prototype is **Solapur Basin**, but it must not be treated as an approved data source or official model scope until the team defines a real pilot boundary.

## ML work needed, in order

| Priority | Problem | Target | Minimum baseline | Candidate next model | Metrics |
|---|---|---|---|---|---|
| 1 | Rainfall forecast | daily/weekly mm | seasonal-naive / persistence | LightGBM/XGBoost with lag/weather features; later LSTM/Temporal Fusion Transformer only if justified | MAE, RMSE, bias, prediction interval coverage |
| 2 | Reservoir inflow/storage | daily level or volume | last value + seasonal average | gradient boosting or SARIMAX | MAE, RMSE, threshold recall |
| 3 | Water demand | daily MLD by sector | same day previous week | regression with calendar/weather/holiday features | MAE, MAPE/WMAPE, bias by sector |
| 4 | Drought/flood alert | risk class / exceedance | rules from thresholds | calibrated classifier or probabilistic forecast | precision/recall, false-negative rate, Brier score |
| 5 | Allocation scenario | feasible allocation | spreadsheet/rule calculation | linear programming with explicit constraints | feasibility, constraint violations, equity/impact review |

## Required ML discipline

1. **Write the decision first.** Example: “Should the utility start conservation messaging next week?”
2. **Build a naive baseline.** A complex model must beat it on a true future holdout.
3. **Use time-based splits.** Never randomly shuffle chronological observations.
4. **Prevent leakage.** A feature must have been known at prediction time.
5. **Report uncertainty.** Use quantiles, ensembles or calibrated intervals—not only one number.
6. **Test segments.** Check performance across seasons, locations and high-impact events.
7. **Create a model card.** Record owner, data, target, dates, metrics, limitations and rollback condition.

## What to learn

- Python: `pandas`, `numpy`, plots, file paths, virtual environments.
- Data: missing values, outliers, units, timestamps, joins, data dictionaries.
- ML: scikit-learn pipelines, regression, classification, validation and metrics.
- Time series: lags, rolling windows, seasonality, train/validation/test by date.
- GIS: coordinate reference systems, GeoJSON, spatial joins, raster vs vector.
- Optimisation: linear programming, hard constraints vs weighted objectives.
- MLOps: reproducibility, experiment tracking, model/version registry and monitoring.

## Definition of an acceptable first model

An acceptable first model has a registered dataset, reproducible notebook/script, fixed training cutoff, baseline comparison, held-out result, error analysis, uncertainty or conservative threshold, model card and a human reviewer. It is not acceptable just because it produces a graph.
