# Aethera deployment checklist

**Release candidate:** `aethera-deployment-0.1.0.zip`
**Current scope:** public research/demo prototype; no live operational water decisions.

- [x] Application dependencies declared in `06_code/requirements.txt`
- [x] Flask route, health and scenario API tests pass locally
- [x] Dockerfile, Compose file and deployment guide provided
- [x] Health endpoint available at `/health`
- [x] Demo data and simulation boundary disclosed in the interface and documentation
- [ ] Company hosting runtime and reverse-proxy configuration approved
- [ ] HTTPS certificate/domain configuration completed
- [ ] Production secret management completed (required before authentication/data collection)
- [ ] Accessibility, security and dependency review completed
- [ ] Monitoring, error tracking, logs and deployment owner assigned
- [ ] Real data contracts, domain review and model validation completed
- [ ] Rollback procedure tested on the target host

## Pre-hosting smoke test

1. Run `python -m unittest discover -s tests -v` from `06_code`.
2. Run `python src/app.py`, visit `http://127.0.0.1:5000`, and check each module.
3. Confirm `http://127.0.0.1:5000/health` returns `{"status":"ok", ...}`.
4. Run a scenario in the Digital Twin and confirm its values update.
5. Build/run the container with `docker compose up --build` before company hosting.
