# Aethera

**Aethera** is an AI-powered water-intelligence platform prototype developed as an industry internship initiative under **Chatake Innoworks Pvt. Ltd. · MindforgeAI Division**.

It demonstrates a premium decision-support experience for rainfall intelligence, demand and allocation, reservoir monitoring, sustainability signals, and a transparent water digital twin.

> Status: research and product prototype. The interface uses clearly labelled demonstration data and is not an operational water-control system.

## Run locally

```powershell
cd 06_code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/app.py
```

Open `http://127.0.0.1:5000`. Run checks with `python -m unittest discover -s tests -v`.

## Project map

- `06_code/` — Flask application, test suite, Docker deployment package
- `01_project_definition/` — problem definition and structured abstract
- `02_research_and_sources/` — research log and evidence register
- `08_project_report/` — report structure and project report
- `11_deployment/` — deployment checklist
- `docs/` — Aethera architecture, delivery blueprint, prompt and internship report

## Documentation

- [Architecture and delivery blueprint](docs/architecture/AETHERA_PLATFORM_BLUEPRINT.md)
- [AI build prompt](docs/prompts/AETHERA_MASTER_PROMPT.md)
- [Project report](docs/reports/AETHERA_PROJECT_REPORT.md)
- [Internship report](docs/reports/CHATake_INNOWORKS_INTERNSHIP_REPORT.md)
- [Deployment guide](deploy/README.md)

## Brand usage

Aethera is the project/platform name. The project should be presented as **“Aethera — a MindforgeAI internship engineering initiative by Chatake Innoworks Pvt. Ltd.”** until a formal product and trademark review is completed.
