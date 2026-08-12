from flask import Flask, render_template
import os
import pandas as pd


app = Flask(__name__)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

RAINFALL_FILE = os.path.join(DATA_DIR, "rainfall_demo.csv")
DEMAND_FILE = os.path.join(DATA_DIR, "demand_demo.csv")
RESERVOIR_FILE = os.path.join(DATA_DIR, "reservoir_demo.csv")
ANIMAL_WATER_FILE = os.path.join(DATA_DIR, "animal_water_use.csv")
GLOBAL_WATER_FILE = os.path.join(DATA_DIR, "water_use.csv")


# ============================================================
# SAFE CSV LOADER
# ============================================================

def load_csv(file_path):

    if os.path.exists(file_path):

        try:
            return pd.read_csv(file_path)

        except Exception as e:

            print(f"Error reading {file_path}: {e}")

    else:

        print(f"File not found: {file_path}")

    return pd.DataFrame()


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# ABOUT
# ============================================================

@app.route("/about")
def about():

    return render_template("about.html")


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    # --------------------------------------------------------
    # LOAD DATASETS
    # --------------------------------------------------------

    rainfall_df = load_csv(RAINFALL_FILE)
    demand_df = load_csv(DEMAND_FILE)
    reservoir_df = load_csv(RESERVOIR_FILE)
    animal_df = load_csv(ANIMAL_WATER_FILE)
    global_df = load_csv(GLOBAL_WATER_FILE)


    # ========================================================
    # RAINFALL VALUE
    # ========================================================

    rainfall_value = 0

    if not rainfall_df.empty:

        rainfall_columns = [
            "rainfall_mm",
            "rainfall",
            "Rainfall",
            "precipitation_mm",
            "precipitation"
        ]

        for column in rainfall_columns:

            if column in rainfall_df.columns:

                rainfall_value = rainfall_df[column].iloc[-1]

                break


    # ========================================================
    # DEMAND VALUE
    # ========================================================

    demand_value = 0

    if not demand_df.empty:

        demand_columns = [
            "demand_mld",
            "demand",
            "Demand",
            "water_demand_mld",
            "water_demand"
        ]

        for column in demand_columns:

            if column in demand_df.columns:

                demand_value = demand_df[column].iloc[-1]

                break


    # ========================================================
    # RESERVOIR VALUE
    # ========================================================

    reservoir_value = 0

    if not reservoir_df.empty:

        reservoir_columns = [
            "availability_pct",
            "availability",
            "reservoir_pct",
            "storage_pct",
            "storage",
            "level_pct"
        ]

        for column in reservoir_columns:

            if column in reservoir_df.columns:

                reservoir_value = reservoir_df[column].iloc[-1]

                break


    # ========================================================
    # ANIMAL WATER CALCULATION
    # ========================================================

    total_animals = 0
    total_daily_water = 0
    total_monthly_water = 0
    highest_consumer = "N/A"

    animal_data = []


    if not animal_df.empty:

        required_columns = [
            "animals_count",
            "daily_water_litres_per_animal"
        ]

        if all(
            column in animal_df.columns
            for column in required_columns
        ):

            animal_df["animals_count"] = pd.to_numeric(
                animal_df["animals_count"],
                errors="coerce"
            ).fillna(0)

            animal_df["daily_water_litres_per_animal"] = pd.to_numeric(
                animal_df["daily_water_litres_per_animal"],
                errors="coerce"
            ).fillna(0)


            # Total water per animal category

            animal_df["total_daily_water"] = (
                animal_df["animals_count"]
                *
                animal_df[
                    "daily_water_litres_per_animal"
                ]
            )


            # Total animals

            total_animals = int(
                animal_df["animals_count"].sum()
            )


            # Total daily water

            total_daily_water = float(
                animal_df["total_daily_water"].sum()
            )


            # Monthly water

            total_monthly_water = (
                total_daily_water * 30
            )


            # Highest water consuming animal

            if not animal_df.empty:

                highest_index = (
                    animal_df[
                        "total_daily_water"
                    ].idxmax()
                )

                highest_consumer = str(
                    animal_df.loc[
                        highest_index,
                        "animal"
                    ]
                )


            # Convert dataframe to records

            animal_data = animal_df.to_dict(
                orient="records"
            )


    # ========================================================
    # ANIMAL SUMMARY
    # ========================================================

    animal_summary = {

        "total_animals": total_animals,

        "daily_water": round(
            total_daily_water,
            2
        ),

        "monthly_water": round(
            total_monthly_water,
            2
        ),

        "highest_consumer": highest_consumer
    }


    # ========================================================
    # GLOBAL WATER SUMMARY
    # ========================================================

    countries = []

    water_summary = {

        "countries": 0,

        "agriculture": 0,

        "industry": 0,

        "domestic": 0
    }


    if not global_df.empty:

        # ----------------------------------------------------
        # Country records
        # ----------------------------------------------------

        countries = global_df.to_dict(
            orient="records"
        )


        # ----------------------------------------------------
        # Number of countries
        # ----------------------------------------------------

        if "Country" in global_df.columns:

            water_summary["countries"] = int(
                global_df["Country"]
                .nunique()
            )


        # ----------------------------------------------------
        # Agriculture
        # ----------------------------------------------------

        if "Agriculture" in global_df.columns:

            water_summary["agriculture"] = round(
                pd.to_numeric(
                    global_df["Agriculture"],
                    errors="coerce"
                ).mean(),
                2
            )


        # ----------------------------------------------------
        # Industry
        # ----------------------------------------------------

        if "Industry" in global_df.columns:

            water_summary["industry"] = round(
                pd.to_numeric(
                    global_df["Industry"],
                    errors="coerce"
                ).mean(),
                2
            )


        # ----------------------------------------------------
        # Domestic
        # ----------------------------------------------------

        if "Domestic" in global_df.columns:

            water_summary["domestic"] = round(
                pd.to_numeric(
                    global_df["Domestic"],
                    errors="coerce"
                ).mean(),
                2
            )


    # ========================================================
    # DASHBOARD DATA
    # ========================================================

    data = {

        "rainfall": rainfall_value,

        "demand": demand_value,

        "reservoir": reservoir_value
    }


    # ========================================================
    # DASHBOARD TEMPLATE
    # ========================================================

    return render_template(

        "dashboard.html",

        data=data,

        water_summary=water_summary,

        countries=countries,

        rainfall_data=rainfall_df.to_dict(
            orient="records"
        ),

        demand_data=demand_df.to_dict(
            orient="records"
        ),

        reservoir_data=reservoir_df.to_dict(
            orient="records"
        ),

        animal_data=animal_data,

        animal_summary=animal_summary,

        total_animals=total_animals,

        total_daily_water=total_daily_water,

        total_monthly_water=total_monthly_water,

        highest_consumer=highest_consumer
    )


# ============================================================
# RAINFALL
# ============================================================

@app.route("/rainfall")
def rainfall():

    df = load_csv(RAINFALL_FILE)

    return render_template(

        "rainfall.html",

        rainfall_data=df.to_dict(
            orient="records"
        )
    )


# ============================================================
# DEMAND
# ============================================================

@app.route("/demand")
def demand():

    df = load_csv(DEMAND_FILE)

    return render_template(

        "demand.html",

        demand_data=df.to_dict(
            orient="records"
        )
    )


# ============================================================
# RESERVOIR
# ============================================================

@app.route("/reservoir")
def reservoir():

    df = load_csv(RESERVOIR_FILE)

    return render_template(

        "reservoir.html",

        reservoir_data=df.to_dict(
            orient="records"
        )
    )


# ============================================================
# GLOBAL WATER
# ============================================================

@app.route("/global-water")
def global_water():

    df = load_csv(GLOBAL_WATER_FILE)

    countries = df.to_dict(
        orient="records"
    )

    water_summary = {

        "countries": 0,

        "agriculture": 0,

        "industry": 0,

        "domestic": 0
    }


    if not df.empty:

        if "Country" in df.columns:

            water_summary["countries"] = int(
                df["Country"].nunique()
            )


        if "Agriculture" in df.columns:

            water_summary["agriculture"] = round(
                pd.to_numeric(
                    df["Agriculture"],
                    errors="coerce"
                ).mean(),
                2
            )


        if "Industry" in df.columns:

            water_summary["industry"] = round(
                pd.to_numeric(
                    df["Industry"],
                    errors="coerce"
                ).mean(),
                2
            )


        if "Domestic" in df.columns:

            water_summary["domestic"] = round(
                pd.to_numeric(
                    df["Domestic"],
                    errors="coerce"
                ).mean(),
                2
            )


    return render_template(

        "global_water.html",

        countries=countries,

        water_summary=water_summary
    )


# ============================================================
# SUSTAINABILITY
# ============================================================

@app.route("/sustainability")
def sustainability():

    return render_template(
        "sustainability.html"
    )


# ============================================================
# DIGITAL TWIN
# ============================================================

@app.route("/digital-twin")
def digital_twin():

    return render_template(
        "digital_twin.html"
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000
    )