# Aethera deployment handoff

## Local acceptance

From `06_code`, create a virtual environment, install `requirements.txt`, run `python src/app.py`, then visit `http://127.0.0.1:5000`. Check `/health` and run the test suite before each handoff.

For Windows, the simplest option is to double-click `START_AETHERA_LOCAL.bat`. Keep its Command Prompt window open; closing it stops the local server and causes `ERR_CONNECTION_REFUSED` in the browser.

## Container deployment

```bash
cd 06_code
docker compose up --build -d
```

The container listens on port `8000`; publish it behind the company reverse proxy with TLS. Set a real `SECRET_KEY` before adding authentication, sessions or user data.

## Production readiness boundary

This package is suitable for a static/demo deployment. Before operational use, add authenticated roles, a managed database, secrets management, audit logs, dataset validation, model monitoring, rate limiting, accessibility review, security testing and domain-specific hydrology validation.
