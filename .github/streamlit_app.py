import os
import pandas as pd
import numpy as np

import streamlit as st
from jinja2 import Environment, FileSystemLoader, select_autoescape


# ============================================================
# AETHERA WATER INTELLIGENCE - STREAMLIT
# ============================================================

class _JSONProxy:
    def __init__(self):
        self.default = lambda value: value


class _RouteApp:
    """Compatibility layer: keeps the existing route functions while Streamlit runs the UI."""
    def __init__(self, template_folder):
        self.template_folder = template_folder
        self.json = _JSONProxy()

    def route(self, *args, **kwargs):
        def decorator(func):
            return func
        return decorator

    def errorhandler(self, *args, **kwargs):
        def decorator(func):
            return func
        return decorator


APP_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_FILE_DIR)
CODE_DIR = os.path.join(PROJECT_ROOT, "06_code")
SRC_DIR = os.path.join(CODE_DIR, "src")
TEMPLATE_DIR = os.path.join(SRC_DIR, "templates")
STATIC_DIR = os.path.join(SRC_DIR, "static")
app = _RouteApp(TEMPLATE_DIR)


class _RequestArgs:
    def get(self, key, default=""):
        try:
            value = st.query_params.get(key, default)
            if isinstance(value, list):
                return value[0] if value else default
            return value
        except Exception:
            return default


class _Request:
    args = _RequestArgs()


request = _Request()


def render_template(template_name, **kwargs):
    template_path = os.path.join(TEMPLATE_DIR, template_name)
    if not os.path.exists(template_path):
        return f"<div style='padding:40px;font-family:Arial;background:#06131f;color:white'><h1>AETHERA WATER INTELLIGENCE</h1><h2>{template_name}</h2><p>Template file not found.</p></div>"
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html", "xml"]))

    # The original pages were written for Flask.  Streamlit renders them in an
    # iframe, so local Flask URLs are not available.  Navigation is supplied by
    # the Streamlit sidebar and the stylesheet is embedded below.
    env.globals["url_for"] = lambda endpoint, **values: "#"
    rendered = env.get_template(template_name).render(**kwargs)

    style_path = os.path.join(STATIC_DIR, "css", "style.css")
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as style_file:
            rendered = rendered.replace(
                "</head>",
                f"<style>{style_file.read()}</style></head>",
                1,
            )

    return rendered


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = CODE_DIR

DATA_DIR = os.path.join(
    CODE_DIR,
    "data"
)

SRC_DATA_DIR = os.path.join(
    SRC_DIR,
    "data"
)

CURATED_DIR = os.path.join(
    PROJECT_ROOT,
    "03_data_and_resources",
    "curated"
)


# ============================================================
# DATA FILES
# ============================================================

RAINFALL_FILE = os.path.join(
    CURATED_DIR,
    "rainfall_2026.csv"
)

RAINFALL_2025_FILE = os.path.join(
    CURATED_DIR,
    "rainfall_2025.csv"
)

WATER_USE_2026_FILE = os.path.join(
    CURATED_DIR,
    "water_use_2026.csv"
)

WATER_USE_2025_FILE = os.path.join(
    CURATED_DIR,
    "water_use_2025.csv"
)

RESERVOIR_FILE = os.path.join(
    CURATED_DIR,
    "reservoir_2025_2026.csv"
)

RESERVOIR_DEMO_FILE = os.path.join(
    CURATED_DIR,
    "reservoir_demo.csv"
)

DEMAND_FILE = os.path.join(
    SRC_DATA_DIR,
    "demand_demo.csv"
)

# Compatibility / fallback files
DEMAND_DEMO_FILE = DEMAND_FILE

WATER_USE_FILE = os.path.join(
    DATA_DIR,
    "water_use.csv"
)

ANIMAL_WATER_FILE = os.path.join(
    DATA_DIR,
    "animal_water_use.csv"
)

GLOBAL_WATER_FILE = os.path.join(
    DATA_DIR,
    "water_use.csv"
)

MAHARASHTRA_WATER_FILE = os.path.join(
    STATIC_DIR,
    "css",
    "maharashtra_water_resources.csv"
)


# ============================================================
# SAFE CSV LOADER
# ============================================================

def load_csv(file_path):

    if not os.path.exists(file_path):

        print("File not found:", file_path)

        return pd.DataFrame()

    try:

        df = pd.read_csv(file_path)

        # ----------------------------------------------------
        # TAB SEPARATED FILE SUPPORT
        # ----------------------------------------------------

        if len(df.columns) == 1:

            first_column = str(
                df.columns[0]
            )

            if "\t" in first_column:

                df = pd.read_csv(
                    file_path,
                    sep="\t"
                )

        # ----------------------------------------------------
        # CLEAN COLUMN NAMES
        # ----------------------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        return df

    except Exception as e:

        print("Error reading:", file_path)
        print(e)

        return pd.DataFrame()


# ============================================================
# SAFE NUMBER
# ============================================================

def safe_number(value):

    number = pd.to_numeric(
        value,
        errors="coerce"
    )

    if pd.isna(number):

        return 0

    return float(number)


# ============================================================
# JSON SAFE VALUE
# ============================================================

def make_json_safe(value):

    if isinstance(value, dict):

        return {
            str(key): make_json_safe(val)
            for key, val in value.items()
        }

    if isinstance(value, list):

        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, tuple):

        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, np.integer):

        return int(value)

    if isinstance(value, np.floating):

        return float(value)

    if isinstance(value, np.bool_):

        return bool(value)

    if isinstance(value, np.ndarray):

        return value.tolist()

    if value is None:

        return None

    try:

        if pd.isna(value):

            return None

    except Exception:

        pass

    return value


# ============================================================
# DATAFRAME -> JSON SAFE RECORDS
# ============================================================

def dataframe_records(df):

    if df is None or df.empty:

        return []

    records = (
        df.fillna("")
        .to_dict(
            orient="records"
        )
    )

    return make_json_safe(records)


# ============================================================
# TEMPLATE HELPER
# ============================================================

def template_exists(template_name):

    template_path = os.path.join(
        app.template_folder or "",
        template_name
    )

    return os.path.exists(
        template_path
    )


def render_existing_template(
    template_name,
    **kwargs
):

    if template_exists(template_name):

        return render_template(
            template_name,
            **kwargs
        )

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AETHERA</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                padding: 40px;
                background: #06131f;
                color: white;
            }}

            a {{
                text-decoration: none;
                color: #59d8ff;
            }}

        </style>

    </head>

    <body>

        <h1>AETHERA WATER INTELLIGENCE</h1>

        <h2>{template_name}</h2>

        <p>
            This page is available from the
            AETHERA dashboard.
        </p>

        <p>
            <a href="/dashboard">
                ← Back to Dashboard
            </a>
        </p>

    </body>
    </html>
    """


# ============================================================
# BUILD DASHBOARD DATA
# ============================================================

def build_dashboard_context():

    # ========================================================
    # LOAD DATA
    # ========================================================

    rainfall_2026_df = load_csv(
        RAINFALL_FILE
    )

    rainfall_2025_df = load_csv(
        RAINFALL_2025_FILE
    )

    water_2026_df = load_csv(
        WATER_USE_2026_FILE
    )

    water_2025_df = load_csv(
        WATER_USE_2025_FILE
    )

    reservoir_df = load_csv(
        RESERVOIR_FILE
    )

    # Reservoir fallback

    if reservoir_df.empty:

        print(
            "reservoir_2025_2026.csv not found/empty."
        )

        print(
            "Using reservoir_demo.csv."
        )

        reservoir_df = load_csv(
            RESERVOIR_DEMO_FILE
        )

    demand_df = load_csv(
        DEMAND_FILE
    )

    animal_df = load_csv(
        ANIMAL_WATER_FILE
    )

    global_df = load_csv(
        GLOBAL_WATER_FILE
    )


    # ========================================================
    # 2026 RAINFALL
    # ========================================================

    rainfall_2026_total = 0
    runoff_2026_total = 0
    recharge_2026_total = 0

    if not rainfall_2026_df.empty:

        if "rainfall_mm" in rainfall_2026_df.columns:

            rainfall_2026_total = round(
                float(
                    pd.to_numeric(
                        rainfall_2026_df["rainfall_mm"],
                        errors="coerce"
                    )
                    .fillna(0)
                    .sum()
                ),
                2
            )

        if "runoff_mcm" in rainfall_2026_df.columns:

            runoff_2026_total = round(
                float(
                    pd.to_numeric(
                        rainfall_2026_df["runoff_mcm"],
                        errors="coerce"
                    )
                    .fillna(0)
                    .sum()
                ),
                2
            )

        if "groundwater_recharge_mcm" in rainfall_2026_df.columns:

            recharge_2026_total = round(
                float(
                    pd.to_numeric(
                        rainfall_2026_df[
                            "groundwater_recharge_mcm"
                        ],
                        errors="coerce"
                    )
                    .fillna(0)
                    .sum()
                ),
                2
            )


    # ========================================================
    # LATEST RAINFALL
    # ========================================================

    latest_rainfall = 0
    latest_rainfall_month = "N/A"

    if not rainfall_2026_df.empty:

        if "rainfall_mm" in rainfall_2026_df.columns:

            latest_rainfall = safe_number(
                rainfall_2026_df[
                    "rainfall_mm"
                ].iloc[-1]
            )

        if "month" in rainfall_2026_df.columns:

            latest_rainfall_month = str(
                rainfall_2026_df[
                    "month"
                ].iloc[-1]
            )


    rainfall_2026_data = dataframe_records(
        rainfall_2026_df
    )


    # ========================================================
    # DEMAND
    # ========================================================

    demand_value = 0

    if not demand_df.empty:

        demand_columns = [
            "demand_mld",
            "demand",
            "Demand",
            "water_demand_mld",
            "water_demand",
            "total_demand"
        ]

        for column in demand_columns:

            if column in demand_df.columns:

                numeric_values = pd.to_numeric(
                    demand_df[column],
                    errors="coerce"
                ).dropna()

                if not numeric_values.empty:

                    demand_value = float(
                        numeric_values.iloc[-1]
                    )

                break


    # ========================================================
    # RESERVOIR
    # ========================================================

    reservoir_value = 0
    reservoir_latest_date = "N/A"

    reservoir_data = []

    if not reservoir_df.empty:

        reservoir_data = dataframe_records(
            reservoir_df
        )

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

                numeric_values = pd.to_numeric(
                    reservoir_df[column],
                    errors="coerce"
                ).dropna()

                if not numeric_values.empty:

                    reservoir_value = round(
                        float(
                            numeric_values.iloc[-1]
                        ),
                        2
                    )

                break

        if "date" in reservoir_df.columns:

            reservoir_latest_date = str(
                reservoir_df["date"].iloc[-1]
            )


    # ========================================================
    # RESERVOIR SUMMARY
    # ========================================================

    reservoir_summary = {

        "latest_storage_pct": reservoir_value,

        "latest_date": reservoir_latest_date,

        "rows": int(
            len(reservoir_df)
        ),

        "reservoirs": 0,

        "average_storage_pct": 0,

        "max_storage_pct": 0,

        "min_storage_pct": 0,

        "total_capacity_mcm": 0,

        "latest_inflow_mcm": 0,

        "latest_outflow_mcm": 0
    }


    if not reservoir_df.empty:

        # Number of reservoirs

        if "reservoir_name" in reservoir_df.columns:

            reservoir_summary["reservoirs"] = int(
                reservoir_df["reservoir_name"]
                .dropna()
                .astype(str)
                .nunique()
            )

        elif "reservoir_id" in reservoir_df.columns:

            reservoir_summary["reservoirs"] = int(
                reservoir_df["reservoir_id"]
                .dropna()
                .astype(str)
                .nunique()
            )


        # Storage

        storage_column = None

        for column in [
            "storage_pct",
            "availability_pct",
            "reservoir_pct",
            "level_pct"
        ]:

            if column in reservoir_df.columns:

                storage_column = column
                break


        if storage_column:

            values = pd.to_numeric(
                reservoir_df[storage_column],
                errors="coerce"
            ).dropna()

            if not values.empty:

                reservoir_summary[
                    "average_storage_pct"
                ] = round(
                    float(values.mean()),
                    2
                )

                reservoir_summary[
                    "max_storage_pct"
                ] = round(
                    float(values.max()),
                    2
                )

                reservoir_summary[
                    "min_storage_pct"
                ] = round(
                    float(values.min()),
                    2
                )


        # Capacity

        if "capacity_mcm" in reservoir_df.columns:

            values = pd.to_numeric(
                reservoir_df["capacity_mcm"],
                errors="coerce"
            ).dropna()

            if not values.empty:

                reservoir_summary[
                    "total_capacity_mcm"
                ] = round(
                    float(values.sum()),
                    2
                )


        # Inflow

        if "inflow_mcm" in reservoir_df.columns:

            values = pd.to_numeric(
                reservoir_df["inflow_mcm"],
                errors="coerce"
            ).dropna()

            if not values.empty:

                reservoir_summary[
                    "latest_inflow_mcm"
                ] = round(
                    float(values.iloc[-1]),
                    2
                )


        # Outflow

        if "outflow_mcm" in reservoir_df.columns:

            values = pd.to_numeric(
                reservoir_df["outflow_mcm"],
                errors="coerce"
            ).dropna()

            if not values.empty:

                reservoir_summary[
                    "latest_outflow_mcm"
                ] = round(
                    float(values.iloc[-1]),
                    2
                )


    # ========================================================
    # 2026 WATER USE
    # ========================================================

    water_use_2026_summary = {

        "agriculture": 0,
        "industry": 0,
        "domestic": 0,
        "power": 0,
        "animal": 0,
        "environment": 0,
        "other": 0,
        "total": 0
    }


    water_columns = {

        "agriculture": "agriculture_mcm",

        "industry": "industry_mcm",

        "domestic": "domestic_mcm",

        "power": "power_mcm",

        "animal": "animal_husbandry_mcm",

        "environment": "environment_mcm",

        "other": "other_mcm",

        "total": "total_use_mcm"
    }


    if not water_2026_df.empty:

        for key, column in water_columns.items():

            if column in water_2026_df.columns:

                water_use_2026_summary[key] = round(
                    float(
                        pd.to_numeric(
                            water_2026_df[column],
                            errors="coerce"
                        )
                        .fillna(0)
                        .sum()
                    ),
                    2
                )


    # ========================================================
    # GLOBAL WATER
    # ========================================================

    countries = []

    water_summary = {

        "countries": 0,
        "agriculture": 0,
        "industry": 0,
        "domestic": 0
    }


    if not global_df.empty:

        if "Country" in global_df.columns:

            countries = (
                global_df["Country"]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
                .tolist()
            )

            countries.sort(
                key=str.lower
            )

            water_summary["countries"] = len(
                countries
            )


        for key, column in [
            ("agriculture", "Agriculture"),
            ("industry", "Industry"),
            ("domestic", "Domestic")
        ]:

            if column in global_df.columns:

                values = pd.to_numeric(
                    global_df[column],
                    errors="coerce"
                ).dropna()

                if not values.empty:

                    water_summary[key] = round(
                        float(values.mean()),
                        2
                    )


    # ========================================================
    # ANIMAL WATER
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

            animal_df[
                "daily_water_litres_per_animal"
            ] = pd.to_numeric(
                animal_df[
                    "daily_water_litres_per_animal"
                ],
                errors="coerce"
            ).fillna(0)

            animal_df["total_daily_water"] = (
                animal_df["animals_count"]
                *
                animal_df[
                    "daily_water_litres_per_animal"
                ]
            )

            total_animals = int(
                animal_df["animals_count"].sum()
            )

            total_daily_water = round(
                float(
                    animal_df[
                        "total_daily_water"
                    ].sum()
                ),
                2
            )

            total_monthly_water = round(
                total_daily_water * 30,
                2
            )

            if "animal" in animal_df.columns:

                index = animal_df[
                    "total_daily_water"
                ].idxmax()

                highest_consumer = str(
                    animal_df.loc[
                        index,
                        "animal"
                    ]
                )

            animal_data = dataframe_records(
                animal_df
            )


    animal_summary = {

        "total_animals": int(
            total_animals
        ),

        "daily_water": float(
            total_daily_water
        ),

        "monthly_water": float(
            total_monthly_water
        ),

        "highest_consumer": str(
            highest_consumer
        )
    }


    # ========================================================
    # WATER AVAILABLE
    # ========================================================

    water_available = 0

    capacity = reservoir_summary[
        "total_capacity_mcm"
    ]

    if capacity > 0 and reservoir_value > 0:

        water_available = round(
            capacity
            *
            reservoir_value
            /
            100,
            2
        )

    if water_available == 0:

        water_available = round(
            runoff_2026_total
            +
            recharge_2026_total,
            2
        )


    # ========================================================
    # RISK LEVEL
    # ========================================================

    risk_level = "Normal"

    if reservoir_value > 0:

        if reservoir_value < 30:

            risk_level = "High"

        elif reservoir_value < 50:

            risk_level = "Moderate"

        else:

            risk_level = "Low"


    if latest_rainfall > 200:

        risk_level = "High"


    # ========================================================
    # MAIN DASHBOARD DATA
    # ========================================================

    data = {

        "water_available":
            float(water_available),

        "rainfall":
            float(rainfall_2026_total),

        "rainfall_2026_total":
            float(rainfall_2026_total),

        "runoff_2026_total":
            float(runoff_2026_total),

        "groundwater_2026_total":
            float(recharge_2026_total),

        "latest_rainfall":
            float(latest_rainfall),

        "latest_rainfall_month":
            str(latest_rainfall_month),

        "demand":
            float(demand_value),

        "reservoir":
            float(reservoir_value),

        "reservoir_name":
            "AETHERA Reservoir",

        "reservoir_capacity":
            float(
                reservoir_summary[
                    "total_capacity_mcm"
                ]
            ),

        "reservoir_inflow":
            float(
                reservoir_summary[
                    "latest_inflow_mcm"
                ]
            ),

        "reservoir_outflow":
            float(
                reservoir_summary[
                    "latest_outflow_mcm"
                ]
            ),

        "reservoir_latest_date":
            str(reservoir_latest_date),

        "risk_level":
            risk_level
    }


    # ========================================================
    # COMPARISON DATA
    # ========================================================

    rainfall_compare_df = pd.concat(
        [
            rainfall_2025_df,
            rainfall_2026_df
        ],
        ignore_index=True
    )

    water_compare_df = pd.concat(
        [
            water_2025_df,
            water_2026_df
        ],
        ignore_index=True
    )


    rainfall_compare_data = dataframe_records(
        rainfall_compare_df
    )

    water_use_compare_data = dataframe_records(
        water_compare_df
    )

    reservoir_compare_data = dataframe_records(
        reservoir_df
    )


    # ========================================================
    # FINAL CONTEXT
    # ========================================================

    return {

        "data":
            make_json_safe(data),

        "water_summary":
            make_json_safe(water_summary),

        "countries":
            countries,

        "rainfall_2026_data":
            rainfall_2026_data,

        "rainfall_2025_data":
            dataframe_records(
                rainfall_2025_df
            ),

        "rainfall_2026_total":
            rainfall_2026_total,

        "runoff_2026_total":
            runoff_2026_total,

        "recharge_2026_total":
            recharge_2026_total,

        "rainfall_compare_data":
            rainfall_compare_data,

        "water_use_compare_data":
            water_use_compare_data,

        "reservoir_compare_data":
            reservoir_compare_data,

        "reservoir_data":
            reservoir_data,

        "reservoir_value":
            reservoir_value,

        "reservoir_latest_date":
            reservoir_latest_date,

        "reservoir_summary":
            make_json_safe(
                reservoir_summary
            ),

        "water_use_2025_data":
            dataframe_records(
                water_2025_df
            ),

        "water_use_2026_data":
            dataframe_records(
                water_2026_df
            ),

        "water_use_2026_summary":
            make_json_safe(
                water_use_2026_summary
            ),

        "rainfall_data":
            rainfall_2026_data,

        "demand_data":
            dataframe_records(
                demand_df
            ),

        "animal_data":
            animal_data,

        "animal_summary":
            make_json_safe(
                animal_summary
            ),

        "total_animals":
            total_animals,

        "total_daily_water":
            total_daily_water,

        "total_monthly_water":
            total_monthly_water,

        "highest_consumer":
            highest_consumer
    }


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("home.html")


# ============================================================
# ABOUT
# ============================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    context = build_dashboard_context()

    return render_template(
        "dashboard.html",
        **context
    )


# ============================================================
# ANALYTICS
# ============================================================

@app.route("/analytics")
def analytics():

    return render_existing_template(
        "analytics.html"
    )


# ============================================================
# RAINFALL
# ============================================================

@app.route("/rainfall")
def rainfall():

    rainfall_2025_df = load_csv(
        RAINFALL_2025_FILE
    )

    rainfall_2026_df = load_csv(
        RAINFALL_FILE
    )

    combined_df = pd.concat(
        [rainfall_2025_df, rainfall_2026_df],
        ignore_index=True
    )

    if "date" in combined_df.columns:
        combined_df = combined_df.sort_values("date")

    def rainfall_total(df, column):
        if column not in df.columns:
            return 0

        return round(
            pd.to_numeric(
                df[column],
                errors="coerce"
            ).fillna(0).sum(),
            2
        )

    return render_template(
        "rainfall_2026.html",
        rainfall_data=dataframe_records(combined_df),
        rainfall_2025_total=rainfall_total(
            rainfall_2025_df,
            "rainfall_mm"
        ),
        rainfall_2026_total=rainfall_total(
            rainfall_2026_df,
            "rainfall_mm"
        ),
        runoff_2025_total=rainfall_total(
            rainfall_2025_df,
            "runoff_mcm"
        ),
        runoff_2026_total=rainfall_total(
            rainfall_2026_df,
            "runoff_mcm"
        ),
        recharge_2025_total=rainfall_total(
            rainfall_2025_df,
            "groundwater_recharge_mcm"
        ),
        recharge_2026_total=rainfall_total(
            rainfall_2026_df,
            "groundwater_recharge_mcm"
        )
    )


# ============================================================
# RAINFALL 2026
# ============================================================

@app.route("/rainfall-2026")
def rainfall_2026():

    df = load_csv(
        RAINFALL_FILE
    )

    return render_existing_template(

        "rainfall_2026.html",

        rainfall_data=
            dataframe_records(df),

        rainfall_2026_data=
            dataframe_records(df)
    )


# ============================================================
# DEMAND
# ============================================================

@app.route("/demand")
def demand():

    df = load_csv(
        DEMAND_FILE
    )

    return render_template(

        "demand.html",

        demand_data=
            dataframe_records(df)
    )


# ============================================================
# RESERVOIR
# ============================================================

@app.route("/reservoir")
def reservoir():

    df = load_csv(
        RESERVOIR_FILE
    )

    if df.empty:

        df = load_csv(
            RESERVOIR_DEMO_FILE
        )

    return render_template(

        "reservoir.html",

        reservoir_data=
            dataframe_records(df)
    )


# ============================================================
# WATER QUALITY
# ============================================================

@app.route("/water-quality")
def water_quality():

    if template_exists(
        "water_quality.html"
    ):

        return render_template(
            "water_quality.html"
        )

    return render_template(
        "sustainability.html"
    )


# ============================================================
# WATER ALLOCATION
# ============================================================

@app.route("/water-allocation")
def water_allocation():

    # --------------------------------------------------------
    # LOAD WATER DEMAND DATA
    # --------------------------------------------------------

    demand_df = load_csv(
        DEMAND_FILE
    )

    # Fallback to demo demand file
    if demand_df.empty:

        demand_df = load_csv(
            DEMAND_DEMO_FILE
        )

    # --------------------------------------------------------
    # LOAD WATER USE DATA
    # --------------------------------------------------------

    water_df = load_csv(
        WATER_USE_2026_FILE
    )

    if water_df.empty:

        water_df = load_csv(
            WATER_USE_FILE
        )

    # --------------------------------------------------------
    # DEFAULT VALUES
    # --------------------------------------------------------

    total_demand = 0.0

    agriculture = 0.0
    domestic = 0.0
    industry = 0.0
    power = 0.0
    animal = 0.0
    environment = 0.0
    other = 0.0

    # --------------------------------------------------------
    # DEMAND DATA
    # --------------------------------------------------------

    if not demand_df.empty:

        possible_demand_columns = [

            "total_demand",

            "demand_mld",

            "demand",

            "Demand",

            "water_demand_mld",

            "water_demand",

            "total_use_mcm"
        ]

        for col in possible_demand_columns:

            if col in demand_df.columns:

                values = pd.to_numeric(
                    demand_df[col],
                    errors="coerce"
                ).dropna()

                if not values.empty:

                    total_demand = float(
                        values.iloc[-1]
                    )

                    break

    # --------------------------------------------------------
    # WATER USE SECTOR DATA
    # --------------------------------------------------------

    if not water_df.empty:

        sector_columns = {

            "agriculture": [
                "agriculture_mcm"
            ],

            "domestic": [
                "domestic_mcm"
            ],

            "industry": [
                "industry_mcm"
            ],

            "power": [
                "power_mcm"
            ],

            "animal": [
                "animal_husbandry_mcm"
            ],

            "environment": [
                "environment_mcm"
            ],

            "other": [
                "other_mcm"
            ]
        }

        def get_sector_total(names):

            for name in names:

                if name in water_df.columns:

                    values = pd.to_numeric(
                        water_df[name],
                        errors="coerce"
                    ).fillna(0)

                    return float(
                        values.sum()
                    )

            return 0.0

        agriculture = get_sector_total(
            sector_columns["agriculture"]
        )

        domestic = get_sector_total(
            sector_columns["domestic"]
        )

        industry = get_sector_total(
            sector_columns["industry"]
        )

        power = get_sector_total(
            sector_columns["power"]
        )

        animal = get_sector_total(
            sector_columns["animal"]
        )

        environment = get_sector_total(
            sector_columns["environment"]
        )

        other = get_sector_total(
            sector_columns["other"]
        )

    # --------------------------------------------------------
    # IF DEMAND IS ZERO, CALCULATE FROM SECTORS
    # --------------------------------------------------------

    sector_total = (

        agriculture
        + domestic
        + industry
        + power
        + animal
        + environment
        + other
    )

    if total_demand <= 0:

        total_demand = sector_total

    # --------------------------------------------------------
    # ALLOCATION
    # --------------------------------------------------------

    total_allocation = sector_total

    ecological_minimum = environment

    available_water = total_demand

    deficit = max(
        total_demand - total_allocation,
        0
    )

    surplus = max(
        total_allocation - total_demand,
        0
    )

    # --------------------------------------------------------
    # SECTOR TABLE
    # --------------------------------------------------------

    sectors = [

        {
            "name": "Domestic",
            "icon": "🏠",
            "demand": domestic,
            "allocation": domestic,
            "status": "Protected"
        },

        {
            "name": "Agriculture",
            "icon": "🌾",
            "demand": agriculture,
            "allocation": agriculture,
            "status": "Monitored"
        },

        {
            "name": "Industry",
            "icon": "🏭",
            "demand": industry,
            "allocation": industry,
            "status": "Normal"
        },

        {
            "name": "Power",
            "icon": "⚡",
            "demand": power,
            "allocation": power,
            "status": "Normal"
        },

        {
            "name": "Animal Husbandry",
            "icon": "🐄",
            "demand": animal,
            "allocation": animal,
            "status": "Normal"
        },

        {
            "name": "Environment",
            "icon": "🌱",
            "demand": environment,
            "allocation": environment,
            "status": "Protected"
        },

        {
            "name": "Other",
            "icon": "💧",
            "demand": other,
            "allocation": other,
            "status": "Normal"
        }
    ]

    # --------------------------------------------------------
    # SHARE %
    # --------------------------------------------------------

    for sector in sectors:

        if total_allocation > 0:

            sector["share"] = round(

                (
                    sector["allocation"]
                    /
                    total_allocation
                ) * 100,

                1
            )

        else:

            sector["share"] = 0

        sector["label"] = sector["name"]
        sector["value"] = sector["share"]
        sector["color"] = {
            "Domestic": "#2f80ed",
            "Agriculture": "#27ae60",
            "Industry": "#f2994a",
            "Power": "#9b51e0",
            "Animal Husbandry": "#eb5757",
            "Environment": "#219653",
            "Other": "#56ccf2"
        }.get(
            sector["name"],
            "#56ccf2"
        )

    # --------------------------------------------------------
    # 14-DAY OUTLOOK
    # --------------------------------------------------------

    outlook_change = 7.1

    outlook = []

    for day in range(1, 15):

        factor = (

            1
            +
            (
                outlook_change
                /
                100
            )
            *
            (
                day
                /
                14
            )
        )

        outlook.append(

            round(
                total_demand * factor,
                2
            )
        )

    # --------------------------------------------------------
    # POLICY
    # --------------------------------------------------------

    policy_scenario = "Balanced"

    confidence = 86

    # --------------------------------------------------------
    # SEND DATA TO TEMPLATE
    # --------------------------------------------------------

    return render_template(

        "demand.html",

        total_demand=round(
            total_demand,
            2
        ),

        total_allocation=round(
            total_allocation,
            2
        ),

        available_water=round(
            available_water,
            2
        ),

        deficit=round(
            deficit,
            2
        ),

        surplus=round(
            surplus,
            2
        ),

        ecological_minimum=round(
            ecological_minimum,
            2
        ),

        outlook_change=outlook_change,

        outlook=outlook,

        policy_scenario=policy_scenario,

        confidence=confidence,

        sectors=sectors,

        allocation_summary={

            "domestic": domestic,

            "agriculture": agriculture,

            "industry": industry,

            "power": power,

            "animal": animal,

            "environment": environment,

            "other": other
        }
    )


# ============================================================
# RISK ALERTS
# ============================================================

@app.route("/risk-alerts")
def risk_alerts():

    rainfall_df = load_csv(
        RAINFALL_FILE
    )

    reservoir_df = load_csv(
        RESERVOIR_FILE
    )

    if reservoir_df.empty:

        reservoir_df = load_csv(
            RESERVOIR_DEMO_FILE
        )

    alerts = []

    # --------------------------------------------------------
    # Rainfall alert
    # --------------------------------------------------------

    if not rainfall_df.empty:

        if "rainfall_mm" in rainfall_df.columns:

            values = pd.to_numeric(
                rainfall_df["rainfall_mm"],
                errors="coerce"
            ).dropna()

            if not values.empty:

                latest_rainfall = float(
                    values.iloc[-1]
                )

                if latest_rainfall > 200:

                    alerts.append(
                        "High rainfall detected. Flood risk may increase."
                    )

                elif latest_rainfall < 5:

                    alerts.append(
                        "Very low rainfall detected. Water availability may be affected."
                    )

    # --------------------------------------------------------
    # Reservoir alert
    # --------------------------------------------------------

    if not reservoir_df.empty:

        for column in [

            "storage_pct",

            "availability_pct",

            "reservoir_pct",

            "level_pct"
        ]:

            if column in reservoir_df.columns:

                values = pd.to_numeric(
                    reservoir_df[column],
                    errors="coerce"
                ).dropna()

                if not values.empty:

                    latest = float(
                        values.iloc[-1]
                    )

                    if latest < 30:

                        alerts.append(
                            "Reservoir storage is below 30%."
                        )

                    elif latest > 90:

                        alerts.append(
                            "Reservoir storage is above 90%."
                        )

                    break

    # --------------------------------------------------------
    # Default alert
    # --------------------------------------------------------

    if not alerts:

        alerts.append(
            "No major water risk alerts detected from available data."
        )

    alert_items = "".join(

        f"<li>{alert}</li>"

        for alert in alerts
    )

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>AETHERA | Risk Alerts</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                padding: 40px;
                background: #06131f;
                color: white;
            }}

            .card {{
                background: rgba(255,255,255,0.08);
                padding: 25px;
                border-radius: 12px;
                margin-top: 20px;
                border: 1px solid rgba(255,255,255,0.1);
            }}

            a {{
                text-decoration: none;
                color: #59d8ff;
            }}

            li {{
                margin: 12px 0;
            }}

        </style>

    </head>

    <body>

        <h1>AETHERA WATER INTELLIGENCE</h1>

        <h2>Risk Alerts</h2>

        <div class="card">

            <ul>

                {alert_items}

            </ul>

        </div>

        <p>

            <a href="/dashboard">
                ← Back to Dashboard
            </a>

        </p>

    </body>

    </html>
    """


# ============================================================
# GLOBAL WATER
# ============================================================

@app.route("/global-water")
def global_water():

    df = load_csv(
        GLOBAL_WATER_FILE
    )

    countries = []

    selected_country = request.args.get(
        "country",
        ""
    ).strip()

    selected_data = None

    if not df.empty:

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

    if (
        not df.empty
        and "Country" in df.columns
    ):

        countries = (
            df["Country"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        countries.sort(
            key=str.lower
        )

    if (
        not selected_country
        and countries
    ):

        selected_country = countries[0]

    if (
        not df.empty
        and selected_country
        and "Country" in df.columns
    ):

        selected_rows = df[
            df["Country"]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            selected_country.lower()
        ]

        if not selected_rows.empty:

            row = selected_rows.iloc[0]

            def number_value(column):

                if column not in row.index:

                    return 0

                value = pd.to_numeric(
                    row[column],
                    errors="coerce"
                )

                if pd.isna(value):

                    return 0

                return round(
                    float(value),
                    2
                )

            agriculture = number_value(
                "Agriculture"
            )

            industry = number_value(
                "Industry"
            )

            domestic = number_value(
                "Domestic"
            )

            total = number_value(
                "Total"
            )

            if total == 0:

                total = round(
                    agriculture
                    +
                    industry
                    +
                    domestic,
                    2
                )

            year = row.get(
                "Year",
                "N/A"
            )

            if pd.isna(year):

                year = "N/A"

            selected_data = {

                "Country":
                    str(
                        row.get(
                            "Country",
                            selected_country
                        )
                    ),

                "Year":
                    str(year),

                "Agriculture":
                    agriculture,

                "Industry":
                    industry,

                "Domestic":
                    domestic,

                "Total":
                    total
            }

    water_summary = {

        "countries":
            len(countries),

        "agriculture":
            0,

        "industry":
            0,

        "domestic":
            0
    }

    for key, column in [

        ("agriculture", "Agriculture"),

        ("industry", "Industry"),

        ("domestic", "Domestic")

    ]:

        if (
            not df.empty
            and column in df.columns
        ):

            values = pd.to_numeric(
                df[column],
                errors="coerce"
            ).dropna()

            if not values.empty:

                water_summary[key] = round(
                    float(values.mean()),
                    2
                )

    return render_template(

        "global_water.html",

        countries=countries,

        global_water_data=
            dataframe_records(df),

        selected_country=
            selected_country,

        selected_data=
            make_json_safe(
                selected_data
            ),

        water_summary=
            make_json_safe(
                water_summary
            )
    )


# ============================================================
# WATER RESOURCES
# ============================================================

@app.route("/water-resources")
def water_resources():

    if template_exists(
        "water_resources.html"
    ):

        return render_template(
            "water_resources.html"
        )

    if template_exists(
        "water_resorces.html"
    ):

        return render_template(
            "water_resorces.html"
        )

    return render_existing_template(
        "water_resources.html"
    )


# ============================================================
# OLD / MISSPELLED WATER RESOURCES
# ============================================================

@app.route("/water-resorces")
def water_resorces():

    if template_exists(
        "water_resorces.html"
    ):

        return render_template(
            "water_resorces.html"
        )

    if template_exists(
        "water_resources.html"
    ):

        return render_template(
            "water_resources.html"
        )

    return render_existing_template(
        "water_resorces.html"
    )


# ============================================================
# MAHARASHTRA WATER
# ============================================================

@app.route("/maharashtra-water")
def maharashtra_water():
    maharashtra_df = load_csv(
        MAHARASHTRA_WATER_FILE
    )

    data = dataframe_records(
        maharashtra_df
    )

    def maharashtra_numbers(column):
        if column not in maharashtra_df.columns:
            return pd.Series(dtype="float64")

        return pd.to_numeric(
            maharashtra_df[column],
            errors="coerce"
        ).fillna(0)

    summary = {
        "districts": int(maharashtra_df["district"].nunique()) if "district" in maharashtra_df.columns else 0,
        "rivers": int(maharashtra_df["river"].nunique()) if "river" in maharashtra_df.columns else 0,
        "dams": int(maharashtra_df["dam"].nunique()) if "dam" in maharashtra_df.columns else 0,
        "capacity": round(maharashtra_numbers("reservoir_capacity_mcm").sum(), 2),
        "available": round(maharashtra_numbers("water_available_mcm").sum(), 2),
        "storage": round(maharashtra_numbers("storage_pct").mean(), 2) if not maharashtra_numbers("storage_pct").empty else 0,
        "water_use": round(maharashtra_numbers("water_use_mcm").sum(), 2)
    }

    return render_template(
        "maharashtra_water.html"
        , data=data
        , summary=summary
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

@app.route("/aethyra-platform")
def aethyra_platform():

    return render_template(
        "aethyra_platform.html"
    )


@app.route("/aethyra-universal")
def aethyra_universal():

    return render_template(
        "aethyra_universal_platform.html"
    )


@app.route("/aethyra-command-center")
def aethyra_command_center():

    return render_template(
        "aethyra_command_center.html"
    )


@app.route("/aethyra-isro-nasa")
def aethyra_isro_nasa():

    return render_template(
        "aethyra_isro_nasa_platform.html"
    )


@app.route("/digital_twin")
def digital_twin():

    rainfall_df = load_csv(
        RAINFALL_FILE
    )

    water_use_2026_df = load_csv(
        WATER_USE_2026_FILE
    )

    reservoir_df = load_csv(
        RESERVOIR_FILE
    )

    if reservoir_df.empty:

        reservoir_df = load_csv(
            RESERVOIR_DEMO_FILE
        )

    # --------------------------------------------------------
    # RAINFALL DATA
    # --------------------------------------------------------
    rainfall_total = 0
    latest_rainfall = 0

    try:
        if rainfall_df is not None and not rainfall_df.empty:

            rainfall_columns = [
                "rainfall_mm",
                "rainfall",
                "Rainfall",
                "precipitation_mm",
                "precipitation"
            ]

            rainfall_col = next(
                (c for c in rainfall_columns if c in rainfall_df.columns),
                None
            )

            if rainfall_col:
                rainfall_values = pd.to_numeric(
                    rainfall_df[rainfall_col],
                    errors="coerce"
                ).dropna()

                if len(rainfall_values) > 0:
                    rainfall_total = float(rainfall_values.sum())
                    latest_rainfall = float(rainfall_values.iloc[-1])

    except Exception as e:
        print("Digital Twin rainfall error:", e)


    # --------------------------------------------------------
    # WATER DEMAND DATA
    # --------------------------------------------------------
    demand_total = 0

    try:
        if water_use_2026_df is not None and not water_use_2026_df.empty:

            demand_columns = [
                "total_use_mcm",
                "total_demand_mcm",
                "demand_mcm"
            ]

            demand_col = next(
                (c for c in demand_columns if c in water_use_2026_df.columns),
                None
            )

            if demand_col:
                demand_values = pd.to_numeric(
                    water_use_2026_df[demand_col],
                    errors="coerce"
                ).dropna()

                if len(demand_values) > 0:
                    demand_total = float(demand_values.sum())

    except Exception as e:
        print("Digital Twin demand error:", e)


    # --------------------------------------------------------
    # RESERVOIR DATA
    # --------------------------------------------------------
    reservoir_level = 0
    reservoir_capacity = 0

    try:
        if reservoir_df is not None and not reservoir_df.empty:

            level_columns = [
                "storage_mcm",
                "reservoir_storage",
                "storage",
                "level_mcm",
                "level"
            ]

            capacity_columns = [
                "capacity_mcm",
                "reservoir_capacity",
                "capacity"
            ]

            level_col = next(
                (c for c in level_columns if c in reservoir_df.columns),
                None
            )

            capacity_col = next(
                (c for c in capacity_columns if c in reservoir_df.columns),
                None
            )

            if level_col:

                level_values = pd.to_numeric(
                    reservoir_df[level_col],
                    errors="coerce"
                ).dropna()

                if len(level_values) > 0:
                    reservoir_level = float(level_values.iloc[-1])

            if capacity_col:

                capacity_values = pd.to_numeric(
                    reservoir_df[capacity_col],
                    errors="coerce"
                ).dropna()

                if len(capacity_values) > 0:
                    reservoir_capacity = float(capacity_values.iloc[-1])

    except Exception as e:
        print("Digital Twin reservoir error:", e)


    # --------------------------------------------------------
    # RESERVOIR PERCENTAGE
    # --------------------------------------------------------
    reservoir_percent = 0

    if reservoir_capacity > 0:
        reservoir_percent = (
            reservoir_level / reservoir_capacity
        ) * 100

    reservoir_percent = max(
        0,
        min(100, reservoir_percent)
    )


    # --------------------------------------------------------
    # SCENARIO BASE VALUES
    # --------------------------------------------------------
    base_availability = max(
        0,
        min(
            100,
            reservoir_percent + (rainfall_total * 0.02)
        )
    )

    base_demand_index = min(
        100,
        50 + (demand_total * 0.03)
    )

    base_resilience = max(
        0,
        min(
            100,
            60
            + (rainfall_total * 0.02)
            + (reservoir_percent * 0.25)
            - (demand_total * 0.01)
        )
    )


    # --------------------------------------------------------
    # DIGITAL TWIN DATA
    # --------------------------------------------------------
    digital_twin_data = {

        "rainfall_total": round(
            rainfall_total, 2
        ),

        "latest_rainfall": round(
            latest_rainfall, 2
        ),

        "demand_total": round(
            demand_total, 2
        ),

        "reservoir_level": round(
            reservoir_level, 2
        ),

        "reservoir_capacity": round(
            reservoir_capacity, 2
        ),

        "reservoir_percent": round(
            reservoir_percent, 1
        ),

        "availability": round(
            base_availability, 1
        ),

        "demand_index": round(
            base_demand_index, 1
        ),

        "resilience": round(
            base_resilience, 1
        )
    }


    return render_template(
        "digital_twin.html",
        digital_twin=digital_twin_data
    )

# ============================================================
# ERROR 404
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    if template_exists(
        "404.html"
    ):

        return render_template(
            "404.html"
        ), 404

    return (
        "<h1>404 - Page Not Found</h1>"
        "<a href='/dashboard'>Dashboard</a>"
    ), 404


# ============================================================
# ERROR 500
# ============================================================

@app.errorhandler(500)
def internal_server_error(error):

    return (
        "<h1>AETHERA Server Error</h1>"
        "<p>Something went wrong.</p>"
        "<a href='/dashboard'>Return Dashboard</a>"
    ), 500


# ============================================================
# STREAMLIT RUNNER
# ============================================================

st.set_page_config(
    page_title="AETHERA Water Intelligence",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp { background:#06131f; }
[data-testid="stSidebar"] { background:#071b2a; }
.block-container { padding-top:1rem; padding-bottom:2rem; }
</style>
""", unsafe_allow_html=True)


def _render_page(html):
    if html is None:
        st.error("Unable to render this page.")
        return
    st.components.v1.html(html, height=1400, scrolling=True)


def _safe_call(fn):
    try:
        return fn()
    except Exception as exc:
        st.error(f"AETHERA page error: {exc}")
        return None


PAGES = {
    "Home": home,
    "About": about,
    "Dashboard": dashboard,
    "Analytics": analytics,
    "Rainfall": rainfall,
    "Rainfall 2026": rainfall_2026,
    "Water Demand": demand,
    "Reservoir": reservoir,
    "Water Quality": water_quality,
    "Water Allocation": water_allocation,
    "Risk & Alerts": risk_alerts,
    "Global Water": global_water,
    "Water Resources": water_resources,
    "Maharashtra Water": maharashtra_water,
    "Sustainability": sustainability,
    "Digital Twin": digital_twin,
    "AETHERA Platform": aethyra_platform,
    "AETHERA Universal": aethyra_universal,
    "Command Center": aethyra_command_center,
    "AETHERA ISRO-NASA": aethyra_isro_nasa,
}

st.sidebar.markdown("# 💧 AETHERA")
st.sidebar.markdown("### WATER INTELLIGENCE")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", list(PAGES.keys()), index=0)
st.sidebar.markdown("---")
st.sidebar.caption("AETHERA Water Intelligence")

html = _safe_call(PAGES[page])
_render_page(html)
