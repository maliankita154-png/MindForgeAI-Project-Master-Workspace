"""Aethera — interactive water intelligence demonstration platform."""
from __future__ import annotations

from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="development-only-change-me")

    def overview() -> dict:
        return {
            "region": "Solapur Basin · Demonstration workspace",
            "availability": 78,
            "rainfall": 124,
            "demand": 62,
            "reservoir": 81,
            "sustainability": 91,
            "updated_at": datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC"),
        }

    @app.context_processor
    def inject_brand():
        return {"current_year": datetime.now().year}

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/dashboard")
    def dashboard():
        return render_template("dashboard.html", data=overview())

    @app.get("/rainfall")
    def rainfall():
        return render_template("rainfall.html", forecast=[102, 124, 118, 96, 74, 61, 82])

    @app.get("/demand")
    def demand():
        sectors = [
            {"label": "Domestic", "value": 42, "color": "#33c3d8"},
            {"label": "Agriculture", "value": 35, "color": "#6bc785"},
            {"label": "Industry", "value": 15, "color": "#a78bfa"},
            {"label": "Ecological", "value": 8, "color": "#e5c36a"},
        ]
        return render_template("demand.html", sectors=sectors)

    @app.get("/reservoir")
    def reservoir():
        reservoirs = [
            ("Ujani", 76, "Watch"), ("Khadakwasla", 81, "Healthy"),
            ("Bhima", 68, "Watch"), ("Veer", 88, "Healthy"),
        ]
        return render_template("reservoir.html", reservoirs=reservoirs)

    @app.get("/digital-twin")
    def digital_twin():
        return render_template("digital_twin.html")

    @app.get("/sustainability")
    def sustainability():
        return render_template("sustainability.html")

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.get("/health")
    def health():
        return jsonify(status="ok", service="aethera", environment="demo")

    @app.get("/api/overview")
    def api_overview():
        return jsonify(overview())

    @app.post("/api/twin/simulate")
    def simulate_twin():
        payload = request.get_json(silent=True) or {}
        drought = min(max(float(payload.get("drought", 25)), 0), 100)
        growth = min(max(float(payload.get("growth", 12)), 0), 100)
        conservation = min(max(float(payload.get("conservation", 18)), 0), 100)
        availability = round(max(0, 78 - drought * 0.43 + conservation * 0.18))
        demand_index = round(62 + growth * 0.35 - conservation * 0.27)
        resilience = round(min(100, max(0, 91 - drought * 0.31 - growth * 0.12 + conservation * 0.42)))
        recommendation = (
            "Activate equitable demand measures and protect ecological minimum flows."
            if availability < 60 else
            "Maintain monitored allocation; prioritise recharge and leakage reduction."
        )
        return jsonify(availability=availability, demand=demand_index, resilience=resilience,
                       recommendation=recommendation, is_demo=True)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
