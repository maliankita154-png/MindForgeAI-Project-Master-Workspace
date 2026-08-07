# Definition of done

## Dataset

- Source, permission/licence, schema, units, geography, time coverage and quality checks are documented.
- Raw input is preserved; curated output is reproducible from code.
- Missingness and limitations are reported.

## Model

- The decision use case, target and cutoff time are written down.
- Time-based baseline comparison and held-out metrics exist.
- Leakage check, error analysis and uncertainty/threshold treatment are included.
- A model card names the owner, training data/version, limitations and rollback condition.

## Application feature

- Inputs are validated and errors are handled.
- Functionality is covered by a test appropriate to the risk.
- UI labels demo/estimated/live data correctly.
- Accessibility basics are checked: keyboard, colour contrast, labels and responsive layout.
- User-facing and technical docs are updated.

## Release

- Tests pass from a clean environment.
- Version, checksum, build command and health check are recorded.
- No secrets or personal/critical data are included.
- Deployment, rollback and owner are specified.
