"""AETHERA - Interactive Water Intelligence Demonstration Platform."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import csv

import pandas as pd
from flask import Flask, jsonify, render_template, request

from services.data_service import overview_metrics


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CODE_DIR = BASE_DIR / "06_code"
DATA_DIR = CODE_DIR / "data"

WATER_USE_FILE = DATA_DIR / "water_use.csv"

RAINFALL_FILE = (
    BASE_DIR
    / "03_data_and_resources"
    / "curated"
    / "rainfall_demo.csv"
)


# =========================================================
# CREATE APP
# =========================================================

def create_app() -> Flask:

    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="development-only-change-me"
    )

    # =====================================================
    # LOAD RAINFALL DATA
    # =====================================================

    if not RAINFALL_FILE.exists():
        raise FileNotFoundError(
            f"Rainfall CSV not found: {RAINFALL_FILE}"
        )

    rainfall_df = pd.read_csv(RAINFALL_FILE)

    print("=" * 60)
    print("AETHERA")
    print("Rainfall data loaded successfully!")
    print("Rainfall file:", RAINFALL_FILE)
    print("Columns:", list(rainfall_df.columns))
    print("Rows:", len(rainfall_df))
    print("=" * 60)

    print(rainfall_df.head())

    # =====================================================
    # GLOBAL BRAND DATA
    # =====================================================

    @app.context_processor
    def inject_brand():

        return {
            "current_year": datetime.now().year
        }

    # =====================================================
    # HOME
    # =====================================================

    @app.get("/")
    def home():

        return render_template(
            "index.html"
        )

    # =====================================================
    # DASHBOARD
    # =====================================================

    @app.get("/dashboard")
    def dashboard():

        # ---------------------------------------------
        # AETHERA metrics
        # ---------------------------------------------

        data = overview_metrics()

        # ---------------------------------------------
        # Default values
        # ---------------------------------------------

        water_data = []

        # ---------------------------------------------
        # Read water-use CSV
        # ---------------------------------------------

        if WATER_USE_FILE.exists():

            with open(
                WATER_USE_FILE,
                mode="r",
                encoding="utf-8-sig",
                newline=""
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    country = row.get("Country", "").strip()

                    if not country:
                        continue

                    try:

                        agriculture = float(
                            row.get("Agriculture", 0) or 0
                        )

                        industry = float(
                            row.get("Industry", 0) or 0
                        )

                        domestic = float(
                            row.get("Domestic", 0) or 0
                        )

                        total = float(
                            row.get("Total", 0) or 0
                        )

                        year = int(
                            float(
                                row.get("Year", 0) or 0
                            )
                        )

                    except (ValueError, TypeError):

                        continue

                    water_data.append(
                        {
                            "Country": country,
                            "Year": year,
                            "Agriculture": agriculture,
                            "Industry": industry,
                            "Domestic": domestic,
                            "Total": total,
                        }
                    )

        # ---------------------------------------------
        # Calculate water summary
        # ---------------------------------------------

        if water_data:

            total_rows = len(water_data)

            agriculture = round(
                sum(
                    item["Agriculture"]
                    for item in water_data
                ) / total_rows,
                1
            )

            industry = round(
                sum(
                    item["Industry"]
                    for item in water_data
                ) / total_rows,
                1
            )

            domestic = round(
                sum(
                    item["Domestic"]
                    for item in water_data
                ) / total_rows,
                1
            )

        else:

            agriculture = 0
            industry = 0
            domestic = 0

        # ---------------------------------------------
        # IMPORTANT:
        # This object is sent to dashboard.html
        # ---------------------------------------------

        water_summary = {
            "countries": len(
                set(
                    item["Country"]
                    for item in water_data
                )
            ),
            "agriculture": agriculture,
            "industry": industry,
            "domestic": domestic,
        }

        print("Dashboard water summary:")
        print(water_summary)

        # ---------------------------------------------
        # Render dashboard
        # ---------------------------------------------

        return render_template(
            "dashboard.html",
            data=data,
            countries=water_data,
            water_summary=water_summary,
        )

    # =====================================================
    # RAINFALL
    # =====================================================

    @app.get("/rainfall")
    def rainfall():

        data = rainfall_df.to_dict(
            orient="records"
        )

        return render_template(
            "rainfall.html",
            rainfall=data
        )

    # =====================================================
    # DEMAND
    # =====================================================

    @app.get("/demand")
    def demand():

        sectors = [
            {
                "label": "Domestic",
                "value": 42,
                "color": "#33c3d8"
            },
            {
                "label": "Agriculture",
                "value": 35,
                "color": "#6bc785"
            },
            {
                "label": "Industry",
                "value": 15,
                "color": "#a78bfa"
            },
            {
                "label": "Ecological",
                "value": 8,
                "color": "#e5c36a"
            },
        ]

        return render_template(
            "demand.html",
            sectors=sectors
        )

    # =====================================================
    # RESERVOIR
    # =====================================================

    @app.get("/reservoir")
    def reservoir():

        metrics = overview_metrics()

        reservoirs = [
            (
                "Ujani demonstration",
                metrics.get("reservoir", 0),
                "Synthetic"
            )
        ]

        return render_template(
            "reservoir.html",
            reservoirs=reservoirs
        )

    # =====================================================
    # DIGITAL TWIN
    # =====================================================

    @app.get("/digital-twin")
    def digital_twin():

        return render_template(
            "digital_twin.html"
        )

    # =====================================================
    # SUSTAINABILITY
    # =====================================================

    @app.get("/sustainability")
    def sustainability():

        return render_template(
            "sustainability.html"
        )

    # =====================================================
    # ABOUT
    # =====================================================

    @app.get("/about")
    def about():

        return render_template(
            "about.html"
        )

    # =====================================================
    # GLOBAL WATER
    # =====================================================

    @app.get("/global-water")
    def global_water():

        countries = []
        water_data = []

        if WATER_USE_FILE.exists():

            with open(
                WATER_USE_FILE,
                mode="r",
                encoding="utf-8-sig",
                newline=""
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    country = row.get(
                        "Country",
                        ""
                    ).strip()

                    if not country:
                        continue

                    try:

                        row["Agriculture"] = float(
                            row.get("Agriculture", 0) or 0
                        )

                        row["Industry"] = float(
                            row.get("Industry", 0) or 0
                        )

                        row["Domestic"] = float(
                            row.get("Domestic", 0) or 0
                        )

                        row["Total"] = float(
                            row.get("Total", 0) or 0
                        )

                        row["Year"] = int(
                            float(
                                row.get("Year", 0) or 0
                            )
                        )

                    except (ValueError, TypeError):

                        continue

                    water_data.append(row)

                    if country not in countries:
                        countries.append(country)

        countries.sort()

        selected_country = request.args.get(
            "country",
            countries[0] if countries else ""
        )

        selected_data = None

        for row in water_data:

            if row["Country"] == selected_country:

                selected_data = row
                break

        return render_template(
            "global_water.html",
            countries=countries,
            selected_country=selected_country,
            selected_data=selected_data,
            water_data=water_data,
        )

    # =====================================================
    # HEALTH
    # =====================================================

    @app.get("/health")
    def health():

        return jsonify(
            status="ok",
            service="aethera",
            environment="demo"
        )

    # =====================================================
    # API OVERVIEW
    # =====================================================

    @app.get("/api/overview")
    def api_overview():

        return jsonify(
            overview_metrics()
        )

    # =====================================================
    # DIGITAL TWIN SIMULATION API
    # =====================================================

    @app.post("/api/twin/simulate")
    def simulate_twin():

        payload = request.get_json(
            silent=True
        ) or {}

        drought = min(
            max(
                float(
                    payload.get(
                        "drought",
                        25
                    )
                ),
                0
            ),
            100
        )

        growth = min(
            max(
                float(
                    payload.get(
                        "growth",
                        12
                    )
                ),
                0
            ),
            100
        )

        conservation = min(
            max(
                float(
                    payload.get(
                        "conservation",
                        18
                    )
                ),
                0
            ),
            100
        )

        availability = round(
            max(
                0,
                78
                - drought * 0.43
                + conservation * 0.18
            )
        )

        demand_index = round(
            62
            + growth * 0.35
            - conservation * 0.27
        )

        resilience = round(
            min(
                100,
                max(
                    0,
                    91
                    - drought * 0.31
                    - growth * 0.12
                    + conservation * 0.42
                )
            )
        )

        if availability < 60:

            recommendation = (
                "Activate equitable demand measures "
                "and protect ecological minimum flows."
            )

        else:

            recommendation = (
                "Maintain monitored allocation; "
                "prioritise recharge and leakage reduction."
            )

        return jsonify(
            availability=availability,
            demand=demand_index,
            resilience=resilience,
            recommendation=recommendation,
            is_demo=True
        )

    # =====================================================
    # RETURN APP
    # =====================================================

    return app


# =========================================================
# START APPLICATION
# =========================================================

app = create_app()


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )