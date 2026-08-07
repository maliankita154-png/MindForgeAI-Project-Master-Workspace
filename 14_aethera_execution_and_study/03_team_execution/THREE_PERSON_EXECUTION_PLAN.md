# Three-person execution plan

## Shared operating rhythm

- **Monday:** 30-minute planning; choose one measurable weekly output per person.
- **Wednesday:** 15-minute blocker review; do not hide missing data or failed experiments.
- **Friday:** demo, evidence review, merge/release decision and project diary entry.
- Use one issue per task. Every issue has an owner, due date, acceptance criteria and linked evidence.
- No one merges their own work without one teammate reviewing it.

## Person 1 — Data & hydrology lead

**Mission:** establish trusted, documented pilot-basin evidence.

| Weeks | Tasks | Deliverable |
|---|---|---|
| 1–2 | Select a pilot boundary; identify permitted rainfall, reservoir, demand and GIS sources; complete data register. | Source map + data dictionary |
| 3–4 | Ingest raw data; build quality-check script; document missingness and units. | Curated v0.1 dataset + QA report |
| 5–6 | Perform exploratory analysis of seasonality, storage and demand. | EDA notebook + insight summary |
| 7–8 | Define water-balance assumptions and thresholds with a mentor/domain source. | Basin assumptions note |
| 9–12 | Maintain refresh process and validate anomalies. | Reproducible data pipeline handoff |

**Study:** hydrology basics, pandas, data quality, GIS/GeoJSON, time zones, reproducibility.

## Person 2 — ML & decision-intelligence lead

**Mission:** build honest baseline models and transparent scenarios.

| Weeks | Tasks | Deliverable |
|---|---|---|
| 1–2 | Define one decision and prediction target per module; specify metric and baseline. | ML problem statements |
| 3–4 | Build seasonal-naive and persistence baselines. | Baseline evaluation report |
| 5–6 | Build rainfall or demand regression pipeline with time-based validation. | Reproducible model v0.1 |
| 7–8 | Add interval/uncertainty output and error analysis. | Model card + calibration result |
| 9–10 | Implement a constrained allocation prototype using transparent rules/linear programming. | Scenario/constraint notebook |
| 11–12 | Package model inference contract for backend integration. | Versioned model artifact + API spec |

**Study:** scikit-learn, time-series validation, statistics, uncertainty, optimisation basics, model cards.

## Person 3 — Platform & product lead

**Mission:** turn verified evidence into a safe, usable and deployable product.

| Weeks | Tasks | Deliverable |
|---|---|---|
| 1–2 | Review the current app; set up Git workflow, issue board and UI acceptance checks. | Engineering operating guide |
| 3–4 | Replace demo data behind one dashboard module with a versioned local API/data read. | Data-backed dashboard slice |
| 5–6 | Add input validation, error pages, loading states and test coverage. | Hardened app v0.2 |
| 7–8 | Integrate the approved model through a narrow service contract. | Model-backed endpoint |
| 9–10 | Add authentication design, audit-event schema and role plan (do not collect user data yet). | Governance/API design |
| 11–12 | Containerise, document environment config and run deployment rehearsal. | Release candidate + operations runbook |

**Study:** Flask, HTTP/REST, testing, SQL/PostgreSQL basics, Docker, security fundamentals, accessibility.

## Shared tasks — everyone participates

1. Read and explain the platform blueprint.
2. Review one another’s outputs weekly.
3. Write a short experiment/development diary after every meaningful change.
4. Present one model/data limitation in each Friday demo.
5. Update reports only from verified work; never invent performance claims.

## First week: exact task list

| Day | Person 1 | Person 2 | Person 3 |
|---|---|---|---|
| 1 | Read data specification; shortlist sources | Read ML roadmap; choose first target | Run current app/tests; map routes/files |
| 2 | Draft pilot boundary and data register | Write rainfall/demand prediction problem | Create issue board and branch rules |
| 3 | Create data dictionary template | Implement seasonal-naive baseline on sample data | Add first code-quality/route review |
| 4 | Inspect missingness/units | Define time split and metrics | Plan data-to-dashboard integration |
| 5 | Present source risks | Present baseline and limitations | Demo app; record integration backlog |
