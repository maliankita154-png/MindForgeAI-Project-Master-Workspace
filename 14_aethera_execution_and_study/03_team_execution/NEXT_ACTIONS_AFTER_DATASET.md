# Next actions after dataset setup

## Completed now

- Three synthetic practice CSV datasets exist in `03_data_and_resources/curated/`.
- The Flask dashboard reads current rainfall, reservoir and demand values from those CSV files.
- The Rainfall page displays the latest seven rainfall CSV rows.

## Team tasks for this week

### Person 1 — Data

1. Open all three `*_demo.csv` files in Excel and understand every column.
2. Complete a data dictionary using `04_templates/DATA_DICTIONARY_TEMPLATE.md`.
3. Find one approved real historical rainfall source; register its permission, link, unit and coverage.

### Person 2 — ML

1. Create `06_code/notebooks/rainfall_baseline.ipynb`.
2. Read `rainfall_demo.csv` with pandas.
3. Create a simple baseline: tomorrow's rainfall = today's rainfall.
4. Measure MAE and RMSE; write results and limitations in a model card.

### Person 3 — Backend and website

1. Read `06_code/src/services/data_service.py` and explain how it reads CSV files.
2. Run `python src/app.py`, then open Dashboard and Rainfall pages.
3. Confirm numbers change if a CSV value is changed, then restore it.
4. Add a test for the CSV-backed `/api/overview` response.

## Do not do yet

- Do not call synthetic values real Solapur data.
- Do not use LSTM/deep learning or a database before baseline and data-quality work are complete.
- Do not overwrite raw/real source data; retain source and version information.
