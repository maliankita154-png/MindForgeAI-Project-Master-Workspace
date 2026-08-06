# Data and Resource Register

| Resource | Type | Source / owner | Licence / permission | Location | Version | Sensitive? | Validation | Notes |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

Do not commit private raw datasets. Document how an authorised member can obtain or regenerate them.

# Data and Resource Register

| Resource | Type | Source / Owner | Licence / Permission | Location | Version | Sensitive? | Validation | Notes |
|----------|------|----------------|----------------------|----------|---------|------------|------------|-------|
| NASA GRACE | Satellite Dataset | NASA | Open Data | https://grace.jpl.nasa.gov | Latest | No | Verified | Groundwater monitoring |
| CHIRPS | Rainfall Dataset | Climate Hazards Center (UCSB) | Open Data | https://www.chc.ucsb.edu/data/chirps | v2.0 | No | Verified | Rainfall prediction |
| ERA5 | Climate Dataset | ECMWF (Copernicus) | Open Licence | https://cds.climate.copernicus.eu | Latest | No | Verified | Climate analysis |
| OpenWeather API | Weather API | OpenWeather | Free API | https://openweathermap.org/api | Current | No | API Tested | Real-time weather data |
| OpenStreetMap | GIS Data | OpenStreetMap Foundation | ODbL | https://www.openstreetmap.org | Latest | No | Verified | Base map for GIS |
| Leaflet.js | JavaScript Library | Leaflet | BSD-2-Clause | https://leafletjs.com | Latest | No | Tested | Interactive maps |
| Flask | Web Framework | Pallets Projects | BSD-3-Clause | Local Environment | Latest | No | Installed | Backend development |
| Python 3.12 | Programming Language | Python Software Foundation | PSF Licence | Local Environment | 3.12 | No | Installed | Core development |
| Scikit-learn | ML Library | Scikit-learn Developers | BSD Licence | Local Environment | Latest | No | Tested | Machine learning |
| Pandas | Data Analysis Library | Pandas Development Team | BSD Licence | Local Environment | Latest | No | Tested | Data preprocessing |
| NumPy | Numerical Library | NumPy Developers | BSD Licence | Local Environment | Latest | No | Tested | Numerical computation |
| Plotly | Visualization Library | Plotly | MIT Licence | Local Environment | Latest | No | Tested | Charts and dashboards |
| SQLite | Database | SQLite | Public Domain | Local Environment | Latest | No | Tested | Data storage |
| GitHub Repository | Version Control | GitHub | Private Repository | GitHub | v1.0 | No | Version Controlled | Source code backup |
| Visual Studio Code | IDE | Microsoft | Free | Local Computer | Latest | No | Installed | Project development |

---

## Notes

- Only public and open-source datasets are used in this project.
- No private or confidential raw datasets are stored in the repository.
- API keys are stored locally in a `.env` file and are **not** committed to GitHub.
- Authorised members can download datasets from their official websites and place them in the `03_data_and_resources/datasets/raw/` folder before running the project.