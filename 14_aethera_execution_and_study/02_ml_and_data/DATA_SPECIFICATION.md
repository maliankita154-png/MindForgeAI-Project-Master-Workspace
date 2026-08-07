# Data specification — what to collect

## Data register first

For every dataset complete `03_data_and_resources/RESOURCE_REGISTER.md` with: owner, licence/permission, update frequency, geography, time coverage, units, known gaps, sensitivity, storage location and approved use. Do not download or publish restricted utility or personal data without written authority.

## Minimum pilot dataset

| Domain | Fields | Granularity | Why it matters |
|---|---|---|---|
| Rainfall | timestamp, station_id, latitude, longitude, rainfall_mm, quality_flag | hourly/daily | forecasting and catchment input |
| Reservoir | timestamp, reservoir_id, storage_volume, capacity, water_level, inflow, outflow, quality_flag | daily | storage state and alerting |
| River/groundwater | timestamp, site_id, discharge or level, unit, quality_flag | daily/weekly | basin balance and trend context |
| Demand | timestamp, area/sector_id, volume_mld, sector, meter_quality | daily/monthly | load prediction and allocation evidence |
| Weather | timestamp, temperature, humidity, wind, evapotranspiration if available | daily | forecasting features |
| GIS boundaries | basin, sub-basin, reservoir, service-zone polygons; CRS | versioned | map joins and aggregation |
| Context | population, crop calendar, holidays, land use | monthly/seasonal | explainable demand features |

## Optional high-value data

Satellite precipitation/vegetation, soil moisture, water-body extent, leakage/pressure telemetry, water quality, irrigation schedules, wastewater/reuse volumes, environmental flow targets and declared policy constraints.

## Canonical file conventions

```text
03_data_and_resources/
  raw/<source>/<YYYY-MM-DD>/                 # immutable source copy
  interim/<dataset_name>/                    # cleaned but reversible work
  curated/<dataset_name>/<version>/          # model-ready, documented data
  metadata/<dataset_name>_data_dictionary.md
```

Use ISO timestamps with a named timezone, SI units, explicit missing values and stable IDs. Keep raw data immutable; transformation code creates new curated versions. Never encode a missing value as zero unless zero is the observed value.

## First data-quality checks

- duplicate timestamp/site combinations;
- invalid or mixed units (mm vs cm, MLD vs litres);
- impossible values (negative rainfall/storage); 
- missingness by time and location;
- inconsistent reservoir capacity;
- timestamp timezone/day-boundary mismatch;
- geographic points outside the expected basin;
- sudden jumps that require source confirmation.
