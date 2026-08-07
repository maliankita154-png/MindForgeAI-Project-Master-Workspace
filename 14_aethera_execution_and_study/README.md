# Aethera execution & study centre

This is the team’s working curriculum and delivery plan for taking Aethera from a polished prototype to a credible, executable pilot. It is intentionally separate from application source so learning notes, experiments and planning do not destabilise the release baseline.

## Read in this order

1. [System study map](01_foundation/SYSTEM_STUDY_MAP.md) — understand the whole platform.
2. [ML and data roadmap](02_ml_and_data/ML_AND_DATA_ROADMAP.md) — learn exactly what must be modelled and why.
3. [Data specification](02_ml_and_data/DATA_SPECIFICATION.md) — know what to collect before training anything.
4. [Three-person execution plan](03_team_execution/THREE_PERSON_EXECUTION_PLAN.md) — take your assigned work.
5. [Definition of done](03_team_execution/DEFINITION_OF_DONE.md) — know when a task is genuinely complete.

## Rule for the team

Do not put experimental notebooks, downloaded data or model files inside `06_code/src`. Use `03_data_and_resources`, `06_code/notebooks` and `07_models_and_artifacts`. Only merge an experiment into the application after it has a dataset record, reproducible code, evaluation result, limitations and review.

## 12-week outcome

By the end of the first 12 weeks, the team should have one **pilot-basin decision-support demonstration** with documented data provenance, baseline models, uncertainty display, an API-backed dashboard, tests and a reviewable deployment package. It should not claim authority to control a water system.
