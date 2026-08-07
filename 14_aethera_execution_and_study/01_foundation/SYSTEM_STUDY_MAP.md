# System study map — what Aethera actually is

## The simple mental model

**Rain falls → water moves and is stored → people and ecosystems use it → choices change the next state.** Aethera helps observe that system, estimate what may happen, compare choices and record why a choice was made.

```text
Atmosphere → rainfall → catchment / river → reservoir / groundwater
                                      ↓                 ↓
                         farms · homes · industry · habitats
                                      ↓
               observations → forecasts → scenarios → human decision
```

## Five layers to study

| Layer | Question it answers | Learn first |
|---|---|---|
| Hydrology | Where does water come from and go? | watershed, rainfall-runoff, storage, evapotranspiration, groundwater |
| Data/GIS | What do we know, where and when? | CSV/Parquet, time series, coordinates, CRS, GeoJSON, quality checks |
| ML | What could happen next? | baselines, features, time-series split, metrics, uncertainty |
| Optimisation/policy | Which option best respects the rules? | constraints, objectives, trade-offs, ecological minimum flow |
| Software/governance | Can people safely use and trust it? | APIs, databases, testing, roles, audit trail, security |

## Platform modules and implementation order

1. **Data foundation:** choose one basin, create a data dictionary and validate input data.
2. **Observation:** visualise rainfall, storage and demand history without ML.
3. **Forecasting:** add one baseline forecast per target, then compare it with a simple ML model.
4. **Scenario engine:** allow assumptions to vary, label them and show impacts.
5. **Allocation:** formulate constraints first; optimisation comes only after policy and data are reviewed.
6. **Governance:** add users, approvals, explanations, logs and monitoring before operational use.

## What not to confuse

- A dashboard is not an AI system; it becomes useful when its data, assumptions and decisions are traceable.
- A prediction is not a recommendation; recommendations need policy constraints and accountable owners.
- A demo simulation is not a calibrated digital twin; calibration needs observed data and domain validation.
- High model accuracy is not enough; time leakage, fairness, physical plausibility and uncertainty matter.

## Study deliverable

Each team member should explain this map in five minutes, then draw how one piece of real data becomes a dashboard insight. If you cannot explain its origin, transformation, model, confidence and decision use, do not build it yet.
