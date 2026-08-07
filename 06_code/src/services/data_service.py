"""Read Aethera's versioned CSV datasets for the local demonstration."""
from __future__ import annotations

import csv
from pathlib import Path


DATA_DIRECTORY = Path(__file__).resolve().parents[3] / "03_data_and_resources" / "curated"


def _read_rows(filename: str) -> list[dict[str, str]]:
    with (DATA_DIRECTORY / filename).open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def overview_metrics() -> dict[str, object]:
    """Return current values calculated from the synthetic CSV practice data."""
    rainfall = _read_rows("rainfall_demo.csv")
    reservoir = _read_rows("reservoir_demo.csv")
    demand = _read_rows("demand_demo.csv")
    latest_reservoir = reservoir[-1]
    latest_demand = demand[-1]
    last_seven_rainfall = rainfall[-7:]
    return {
        "region": "Solapur demonstration dataset",
        "availability": round(float(latest_reservoir["storage_pct"])),
        "rainfall": round(sum(float(row["rainfall_mm"]) for row in last_seven_rainfall), 1),
        "demand": round(float(latest_demand["demand_mld"]), 1),
        "reservoir": round(float(latest_reservoir["storage_pct"])),
        "updated_at": latest_reservoir["date"],
        "data_label": "Synthetic CSV practice data",
    }


def recent_rainfall(days: int = 7) -> list[dict[str, object]]:
    """Return the most recent observed rows for the rainfall screen."""
    rows = _read_rows("rainfall_demo.csv")[-days:]
    return [{"date": row["date"], "day": row["date"][5:], "rainfall_mm": float(row["rainfall_mm"])} for row in rows]
