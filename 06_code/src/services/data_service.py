from pathlib import Path
import csv


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

WATER_USE_FILE = DATA_DIR / "water_use.csv"


# ---------------------------------------------------------
# READ WATER USE DATA
# ---------------------------------------------------------

def load_water_use():

    data = []

    if not WATER_USE_FILE.exists():
        return data

    with open(
        WATER_USE_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row.get("Country"):
                data.append(row)

    return data


# ---------------------------------------------------------
# OVERVIEW METRICS
# ---------------------------------------------------------

def overview_metrics():

    return {
        "region": "Solapur / Global Demonstration",
        "availability": 72,
        "rainfall": 124,
        "demand": 420,
        "reservoir": 72,
        "updated_at": "2025",
        "data_label": "CSV + Demonstration Data"
    }


# ---------------------------------------------------------
# GLOBAL WATER SUMMARY
# ---------------------------------------------------------

def global_water_summary():

    data = load_water_use()

    if not data:

        return {
            "countries": 0,
            "agriculture": 0,
            "industry": 0,
            "domestic": 0
        }

    agriculture = []
    industry = []
    domestic = []

    for row in data:

        try:
            agriculture.append(
                float(row.get("Agriculture", 0))
            )

            industry.append(
                float(row.get("Industry", 0))
            )

            domestic.append(
                float(row.get("Domestic", 0))
            )

        except ValueError:
            continue

    return {
        "countries": len(data),

        "agriculture": round(
            sum(agriculture) / len(agriculture), 1
        ) if agriculture else 0,

        "industry": round(
            sum(industry) / len(industry), 1
        ) if industry else 0,

        "domestic": round(
            sum(domestic) / len(domestic), 1
        ) if domestic else 0
    }


# ---------------------------------------------------------
# COUNTRY WATER USE
# ---------------------------------------------------------

def country_water_use():

    return load_water_use()