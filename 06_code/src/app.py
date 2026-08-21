from flask import Flask, render_template, request, jsonify
from pathlib import Path
import pandas as pd

# ============================================================
# AETHERA WATER INTELLIGENCE
# ============================================================

app = Flask(__name__)

# ============================================================
# PROJECT PATHS
# ============================================================

CODE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CODE_DIR.parent.parent

CURATED_DIR = PROJECT_ROOT / "03_data_and_resources" / "curated"
DATA_DIR = CODE_DIR / "data"

print("\n========================================")
print(" AETHERA WATER INTELLIGENCE")
print("========================================")
print("PROJECT ROOT :", PROJECT_ROOT)
print("CURATED DIR  :", CURATED_DIR)
print("DATA DIR     :", DATA_DIR)
print("========================================\n")


# ============================================================
# FILE FINDER
# ============================================================

def find_data_file(*names):

    for name in names:

        candidates = [
            CURATED_DIR / name,
            DATA_DIR / name,
        ]

        for path in candidates:

            if path.exists():
                return path

    return CURATED_DIR / names[0]


RAINFALL_FILE = find_data_file(
    "rainfall_2026.csv",
    "rainfall_2025_2026.csv",
)

RAINFALL_2025_FILE = find_data_file(
    "rainfall_2025.csv",
)

WATER_USE_2026_FILE = find_data_file(
    "water_use_2026.csv",
)

WATER_USE_2025_FILE = find_data_file(
    "water_use_2025.csv",
)

DEMAND_FILE = find_data_file(
    "demand_2025_2026.csv",
    "demand_demo.csv",
)

RESERVOIR_FILE = find_data_file(
    "reservoir_2025_2026.csv",
    "reservoir_demo.csv",
)

ANIMAL_FILE = find_data_file(
    "animal_water_use.csv",
)

GLOBAL_WATER_FILE = find_data_file(
    "water_use.csv",
)


# ============================================================
# SAFE CSV LOADER
# ============================================================

def load_csv(path):

    try:

        if not path.exists():

            print("FILE NOT FOUND:", path)

            return pd.DataFrame()

        df = pd.read_csv(
            path,
            sep=None,
            engine="python"
        )

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
        )

        print(
            "LOADED:",
            path.name,
            "| rows:",
            len(df)
        )

        print(
            "COLUMNS:",
            df.columns.tolist()
        )

        return df

    except Exception as e:

        print(
            "CSV ERROR:",
            path,
            e
        )

        return pd.DataFrame()


# ============================================================
# NUMBER SERIES
# ============================================================

def number_series(df, column):

    if df.empty or column not in df.columns:

        return pd.Series(dtype=float)

    return pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0)


# ============================================================
# LAST NUMBER
# ============================================================

def last_number(df, columns, default=1):

    if df.empty:
        return default

    for column in columns:

        if column in df.columns:

            values = number_series(
                df,
                column
            )

            if not values.empty:

                value = float(values.iloc[-1])

                if value > 0:

                    return round(value, 2)

    return default


# ============================================================
# SAFE RECORDS
# ============================================================

def safe_records(df):

    if df.empty:
        return []

    clean = df.copy()

    for col in clean.columns:

        if pd.api.types.is_datetime64_any_dtype(
            clean[col]
        ):

            clean[col] = clean[col].astype(str)

    clean = clean.where(
        pd.notnull(clean),
        ""
    )

    return clean.to_dict(
        orient="records"
    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


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

    # ========================================================
    # LOAD ALL DATA
    # ========================================================

    rainfall_df = load_csv(
        RAINFALL_FILE
    )

    rainfall_2025_df = load_csv(
        RAINFALL_2025_FILE
    )

    water_use_2026_df = load_csv(
        WATER_USE_2026_FILE
    )

    water_use_2025_df = load_csv(
        WATER_USE_2025_FILE
    )

    demand_df = load_csv(
        DEMAND_FILE
    )

    reservoir_df = load_csv(
        RESERVOIR_FILE
    )

    animal_df = load_csv(
        ANIMAL_FILE
    )

    global_df = load_csv(
        GLOBAL_WATER_FILE
    )

    # ========================================================
    # RAINFALL 2026
    # ========================================================

    rainfall_2026_total = round(
        number_series(
            rainfall_df,
            "rainfall_mm"
        ).sum(),
        2
    )

    if rainfall_2026_total <= 0:
        rainfall_2026_total = 184.70

    latest_rainfall = last_number(
        rainfall_df,
        [
            "rainfall_mm",
            "rainfall"
        ],
        12.80
    )

    if latest_rainfall <= 0:
        latest_rainfall = 12.80

    latest_rainfall_month = "Aug"

    if (
        not rainfall_df.empty
        and
        "month" in rainfall_df.columns
    ):

        value = str(
            rainfall_df.iloc[-1]["month"]
        ).strip()

        if value:
            latest_rainfall_month = value

    runoff_2026_total = round(
        number_series(
            rainfall_df,
            "runoff_mcm"
        ).sum(),
        2
    )

    if runoff_2026_total <= 0:
        runoff_2026_total = 251.10

    groundwater_2026_total = round(
        number_series(
            rainfall_df,
            "groundwater_recharge_mcm"
        ).sum(),
        2
    )

    if groundwater_2026_total <= 0:
        groundwater_2026_total = 169.50

    # ========================================================
    # RAINFALL 2025
    # ========================================================

    if rainfall_2025_df.empty:

        rainfall_2025_df = pd.DataFrame({

            "year": [
                2025,
                2025,
                2025,
                2025
            ],

            "month": [
                "Jan",
                "Feb",
                "Mar",
                "Apr"
            ],

            "rainfall_mm": [
                2.8,
                2.1,
                4.5,
                18.2
            ]

        })

    # ========================================================
    # WATER USE 2026
    # ========================================================

    water_columns = {

        "agriculture":
            "agriculture_mcm",

        "industry":
            "industry_mcm",

        "domestic":
            "domestic_mcm",

        "animal":
            "animal_husbandry_mcm",

        "power":
            "power_mcm",

        "environment":
            "environment_mcm",

        "other":
            "other_mcm",

        "total":
            "total_use_mcm",
    }

    water_use_2026_summary = {}

    water_use_defaults = {

        "agriculture": 8420.50,

        "industry": 3160.75,

        "domestic": 2280.40,

        "animal": 960.25,

        "power": 1940.60,

        "environment": 740.35,

        "other": 410.20,

        "total": 17912.05,

    }

    for key, column in water_columns.items():

        value = round(
            number_series(
                water_use_2026_df,
                column
            ).sum(),
            2
        )

        if value <= 0:
            value = water_use_defaults[key]

        water_use_2026_summary[key] = value

    # ========================================================
    # RESERVOIR
    # ========================================================

    reservoir_name = "Ujani Demonstration"

    reservoir_storage = 1842.50

    reservoir_capacity = 3071.00

    reservoir_value = 60.00

    reservoir_inflow = 128.40

    reservoir_outflow = 96.70

    reservoir_latest_date = "2026-08-20"

    try:

        if not reservoir_df.empty:

            # ------------------------------------------------
            # SORT BY DATE
            # ------------------------------------------------

            if "date" in reservoir_df.columns:

                temp_date = pd.to_datetime(
                    reservoir_df["date"],
                    errors="coerce"
                )

                reservoir_df = (
                    reservoir_df
                    .assign(
                        _sort_date=temp_date
                    )
                    .sort_values(
                        "_sort_date"
                    )
                    .drop(
                        columns=[
                            "_sort_date"
                        ]
                    )
                    .reset_index(
                        drop=True
                    )
                )

            # ------------------------------------------------
            # LATEST ROW
            # ------------------------------------------------

            latest = reservoir_df.iloc[-1]

            # ------------------------------------------------
            # NAME
            # ------------------------------------------------

            for col in [
                "reservoir_name",
                "name",
                "reservoir"
            ]:

                if col in reservoir_df.columns:

                    value = latest[col]

                    if (
                        pd.notna(value)
                        and
                        str(value).strip()
                    ):

                        reservoir_name = str(
                            value
                        ).strip()

                        break

            # ------------------------------------------------
            # CAPACITY
            # ------------------------------------------------

            for col in [

                "capacity_mcm",
                "reservoir_capacity_mcm",
                "capacity",
                "total_capacity_mcm",
                "gross_capacity_mcm"

            ]:

                if col in reservoir_df.columns:

                    value = pd.to_numeric(
                        latest[col],
                        errors="coerce"
                    )

                    if (
                        pd.notna(value)
                        and
                        float(value) > 0
                    ):

                        reservoir_capacity = round(
                            float(value),
                            2
                        )

                        break

            # ------------------------------------------------
            # STORAGE
            # ------------------------------------------------

            for col in [

                "storage_mcm",
                "current_storage_mcm",
                "reservoir_storage_mcm",
                "level_mcm",
                "water_level_mcm",
                "storage",
                "current_level"

            ]:

                if col in reservoir_df.columns:

                    value = pd.to_numeric(
                        latest[col],
                        errors="coerce"
                    )

                    if (
                        pd.notna(value)
                        and
                        float(value) > 0
                    ):

                        reservoir_storage = round(
                            float(value),
                            2
                        )

                        break

            # ------------------------------------------------
            # PERCENTAGE
            # ------------------------------------------------

            for col in [

                "storage_pct",
                "availability_pct",
                "reservoir_pct",
                "level_pct",
                "storage_percent",
                "availability_percent",
                "level_percent"

            ]:

                if col in reservoir_df.columns:

                    value = pd.to_numeric(
                        latest[col],
                        errors="coerce"
                    )

                    if (
                        pd.notna(value)
                        and
                        float(value) > 0
                    ):

                        reservoir_value = round(
                            float(value),
                            2
                        )

                        break

            # ------------------------------------------------
            # CALCULATE PERCENTAGE
            # ------------------------------------------------

            if (
                reservoir_storage > 0
                and
                reservoir_capacity > 0
            ):

                reservoir_value = round(
                    (
                        reservoir_storage
                        /
                        reservoir_capacity
                    ) * 100,
                    2
                )

            # ------------------------------------------------
            # INFLOW
            # ------------------------------------------------

            for col in [

                "inflow_mcm",
                "inflow",
                "water_inflow_mcm"

            ]:

                if col in reservoir_df.columns:

                    value = pd.to_numeric(
                        latest[col],
                        errors="coerce"
                    )

                    if (
                        pd.notna(value)
                        and
                        float(value) > 0
                    ):

                        reservoir_inflow = round(
                            float(value),
                            2
                        )

                        break

            # ------------------------------------------------
            # OUTFLOW
            # ------------------------------------------------

            for col in [

                "outflow_mcm",
                "outflow",
                "release_mcm",
                "release",
                "water_outflow_mcm"

            ]:

                if col in reservoir_df.columns:

                    value = pd.to_numeric(
                        latest[col],
                        errors="coerce"
                    )

                    if (
                        pd.notna(value)
                        and
                        float(value) > 0
                    ):

                        reservoir_outflow = round(
                            float(value),
                            2
                        )

                        break

            # ------------------------------------------------
            # DATE
            # ------------------------------------------------

            for col in [

                "date",
                "timestamp",
                "record_date"

            ]:

                if col in reservoir_df.columns:

                    value = latest[col]

                    if pd.notna(value):

                        text_value = str(
                            value
                        ).strip()

                        if text_value:

                            reservoir_latest_date = (
                                text_value
                            )

                            break

    except Exception as e:

        print(
            "RESERVOIR ERROR:",
            e
        )

    # ========================================================
    # RESERVOIR FINAL FALLBACK
    # ========================================================

    if reservoir_capacity <= 0:
        reservoir_capacity = 3071.00

    if reservoir_storage <= 0:
        reservoir_storage = 1842.50

    if reservoir_value <= 0:

        reservoir_value = round(
            (
                reservoir_storage
                /
                reservoir_capacity
            ) * 100,
            2
        )

    if reservoir_inflow <= 0:
        reservoir_inflow = 128.40

    if reservoir_outflow <= 0:
        reservoir_outflow = 96.70

    if (
        not reservoir_latest_date
        or
        reservoir_latest_date == "N/A"
    ):

        reservoir_latest_date = "2026-08-20"

    # ========================================================
    # WATER AVAILABLE
    # ========================================================

    water_available = round(
        reservoir_storage,
        2
    )

    if water_available <= 0:

        water_available = 1842.50

    # ========================================================
    # DEMAND
    # ========================================================

    demand = last_number(

        demand_df,

        [
            "demand_mld",
            "demand",
            "water_demand_mld",
            "water_demand"
        ],

        612.50
    )

    if demand <= 0:
        demand = 612.50

    # ========================================================
    # RISK
    # ========================================================

    if reservoir_value >= 70:

        risk_level = "LOW"

    elif reservoir_value >= 40:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    # ========================================================
    # ALERTS
    # ========================================================

    alerts = []

    if reservoir_value >= 60:

        alerts.append(
            "LOW: Reservoir storage is currently stable."
        )

    else:

        alerts.append(
            "MEDIUM: Reservoir storage requires monitoring."
        )

    alerts.append(
        f"Rainfall runoff recorded: "
        f"{runoff_2026_total} MCM."
    )

    alerts.append(
        f"Groundwater recharge: "
        f"{groundwater_2026_total} MCM."
    )

    # ========================================================
    # ANIMAL WATER
    # ========================================================

    total_animals = 1250

    total_daily_water = 18450

    total_monthly_water = 553500

    highest_consumer = "Cattle"

    animal_data = []

    if not animal_df.empty:

        if "animals_count" in animal_df.columns:

            animal_df[
                "animals_count"
            ] = number_series(
                animal_df,
                "animals_count"
            )

        if (
            "daily_water_litres_per_animal"
            in animal_df.columns
        ):

            animal_df[
                "daily_water_litres_per_animal"
            ] = number_series(
                animal_df,
                "daily_water_litres_per_animal"
            )

        if (
            "animals_count"
            in animal_df.columns
            and
            "daily_water_litres_per_animal"
            in animal_df.columns
        ):

            animal_df[
                "total_daily_water"
            ] = (

                animal_df[
                    "animals_count"
                ]

                *

                animal_df[
                    "daily_water_litres_per_animal"
                ]

            )

            calculated_animals = int(
                animal_df[
                    "animals_count"
                ].sum()
            )

            calculated_daily = round(
                float(
                    animal_df[
                        "total_daily_water"
                    ].sum()
                ),
                2
            )

            if calculated_animals > 0:
                total_animals = calculated_animals

            if calculated_daily > 0:
                total_daily_water = calculated_daily

            total_monthly_water = round(
                total_daily_water * 30,
                2
            )

            if "animal" in animal_df.columns:

                idx = animal_df[
                    "total_daily_water"
                ].idxmax()

                consumer = str(
                    animal_df.loc[
                        idx,
                        "animal"
                    ]
                ).strip()

                if consumer:
                    highest_consumer = consumer

            animal_data = safe_records(
                animal_df
            )

    # ========================================================
    # ANIMAL FINAL FALLBACK
    # ========================================================

    if total_animals <= 0:
        total_animals = 1250

    if total_daily_water <= 0:
        total_daily_water = 18450

    if total_monthly_water <= 0:

        total_monthly_water = (
            total_daily_water * 30
        )

    if (
        not highest_consumer
        or
        highest_consumer == "N/A"
    ):

        highest_consumer = "Cattle"

    animal_summary = {

        "total_animals":
            total_animals,

        "daily_water":
            total_daily_water,

        "monthly_water":
            total_monthly_water,

        "highest_consumer":
            highest_consumer,

    }

    # ========================================================
    # GLOBAL WATER
    # ========================================================

    countries = []

    global_water_data = []

    if not global_df.empty:

        if "country" in global_df.columns:

            countries = sorted(

                global_df[
                    "country"
                ]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
                .tolist()

            )

        for _, row in global_df.iterrows():

            def row_value(names):

                for name in names:

                    if name in row.index:

                        value = pd.to_numeric(
                            row[name],
                            errors="coerce"
                        )

                        if (
                            pd.notna(value)
                            and
                            float(value) > 0
                        ):

                            return round(
                                float(value),
                                2
                            )

                return 1

            global_water_data.append({

                "Country":
                    str(
                        row.get(
                            "country",
                            "India"
                        )
                    ),

                "Year":
                    str(
                        row.get(
                            "year",
                            "2026"
                        )
                    ),

                "Agriculture":
                    row_value([
                        "agriculture"
                    ]),

                "Industry":
                    row_value([
                        "industry"
                    ]),

                "Domestic":
                    row_value([
                        "domestic"
                    ]),

            })

    # ========================================================
    # GLOBAL FALLBACK
    # ========================================================

    if not countries:

        countries = [
            "India",
            "USA",
            "China",
            "Brazil",
            "Australia"
        ]

    if not global_water_data:

        global_water_data = [

            {
                "Country": "India",
                "Year": "2026",
                "Agriculture": 8420,
                "Industry": 3160,
                "Domestic": 2280
            },

            {
                "Country": "USA",
                "Year": "2026",
                "Agriculture": 6210,
                "Industry": 2840,
                "Domestic": 1950
            },

            {
                "Country": "China",
                "Year": "2026",
                "Agriculture": 7310,
                "Industry": 4020,
                "Domestic": 2140
            },

            {
                "Country": "Brazil",
                "Year": "2026",
                "Agriculture": 5140,
                "Industry": 2180,
                "Domestic": 1430
            },

            {
                "Country": "Australia",
                "Year": "2026",
                "Agriculture": 2940,
                "Industry": 1280,
                "Domestic": 860
            }

        ]

    # ========================================================
    # GLOBAL SUMMARY
    # ========================================================

    water_summary = {

        "countries":
            len(countries),

        "agriculture":
            round(
                sum(
                    x["Agriculture"]
                    for x in global_water_data
                )
                /
                len(global_water_data),
                2
            ),

        "industry":
            round(
                sum(
                    x["Industry"]
                    for x in global_water_data
                )
                /
                len(global_water_data),
                2
            ),

        "domestic":
            round(
                sum(
                    x["Domestic"]
                    for x in global_water_data
                )
                /
                len(global_water_data),
                2
            ),

    }

    # ========================================================
    # SUPPLY VS DEMAND
    # ========================================================

    supply_demand_data = []

    months = [

        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"

    ]

    # Demo supply values
    demo_supply = {

        "Jan": 68,
        "Feb": 65,
        "Mar": 63,
        "Apr": 61,
        "May": 58,
        "Jun": 55,
        "Jul": 57,
        "Aug": 60,
        "Sep": 62,
        "Oct": 64,
        "Nov": 66,
        "Dec": 69

    }

    # Demo demand values
    demo_demand = {

        "Jan": 540,
        "Feb": 550,
        "Mar": 565,
        "Apr": 580,
        "May": 600,
        "Jun": 620,
        "Jul": 615,
        "Aug": 612,
        "Sep": 590,
        "Oct": 575,
        "Nov": 560,
        "Dec": 545

    }

    for month in months:

        storage = demo_supply[month]

        month_demand = demo_demand[month]

        # Try actual reservoir data
        if (
            not reservoir_df.empty
            and
            "month" in reservoir_df.columns
        ):

            r = reservoir_df[
                reservoir_df[
                    "month"
                ]
                .astype(str)
                .str.lower()
                ==
                month.lower()
            ]

            if not r.empty:

                actual_storage = last_number(

                    r,

                    [
                        "storage_pct",
                        "availability_pct",
                        "reservoir_pct",
                        "level_pct"
                    ],

                    storage
                )

                if actual_storage > 0:

                    storage = actual_storage

                else:

                    storage_mcm = last_number(

                        r,

                        [
                            "storage_mcm",
                            "current_storage_mcm"
                        ],

                        1
                    )

                    capacity_mcm = last_number(

                        r,

                        [
                            "capacity_mcm",
                            "reservoir_capacity_mcm"
                        ],

                        reservoir_capacity
                    )

                    if (
                        storage_mcm > 0
                        and
                        capacity_mcm > 0
                    ):

                        storage = round(
                            (
                                storage_mcm
                                /
                                capacity_mcm
                            ) * 100,
                            2
                        )

        # Try actual demand data
        if (
            not demand_df.empty
            and
            "month" in demand_df.columns
        ):

            d = demand_df[
                demand_df[
                    "month"
                ]
                .astype(str)
                .str.lower()
                ==
                month.lower()
            ]

            if not d.empty:

                actual_demand = last_number(

                    d,

                    [
                        "demand_mld",
                        "demand",
                        "water_demand_mld"
                    ],

                    month_demand
                )

                if actual_demand > 0:

                    month_demand = actual_demand

        supply_demand_data.append({

            "month":
                month,

            "supply":
                storage,

            "demand":
                month_demand,

        })

    # ========================================================
    # FINAL DATA OBJECT
    # ========================================================

    data = {

        "water_available":
            water_available,

        "demand":
            demand,

        "reservoir":
            reservoir_value,

        "reservoir_storage":
            reservoir_storage,

        "rainfall_2026_total":
            rainfall_2026_total,

        "latest_rainfall":
            latest_rainfall,

        "latest_rainfall_month":
            latest_rainfall_month,

        "runoff_2026_total":
            runoff_2026_total,

        "groundwater_2026_total":
            groundwater_2026_total,

        "risk_level":
            risk_level,

        "reservoir_name":
            reservoir_name,

        "reservoir_capacity":
            reservoir_capacity,

        "reservoir_inflow":
            reservoir_inflow,

        "reservoir_outflow":
            reservoir_outflow,

        "reservoir_latest_date":
            reservoir_latest_date,

    }

    # ========================================================
    # DEBUG
    # ========================================================

    print("\n========================================")
    print(" AETHERA DASHBOARD DATA")
    print("========================================")

    print(
        "Water available :",
        water_available
    )

    print(
        "Demand          :",
        demand
    )

    print(
        "Reservoir %     :",
        reservoir_value
    )

    print(
        "Reservoir storage:",
        reservoir_storage
    )

    print(
        "Reservoir name  :",
        reservoir_name
    )

    print(
        "Capacity        :",
        reservoir_capacity
    )

    print(
        "Inflow          :",
        reservoir_inflow
    )

    print(
        "Outflow         :",
        reservoir_outflow
    )

    print(
        "Latest date     :",
        reservoir_latest_date
    )

    print(
        "Rainfall 2026   :",
        rainfall_2026_total
    )

    print(
        "Demand          :",
        demand
    )

    print(
        "Animal count    :",
        total_animals
    )

    print(
        "Animal daily    :",
        total_daily_water
    )

    print(
        "Water use       :",
        water_use_2026_summary
    )

    print("========================================\n")

    # ========================================================
    # RENDER DASHBOARD
    # ========================================================

    return render_template(

        "dashboard.html",

        data=data,

        water_summary=water_summary,

        countries=countries,

        global_water_data=global_water_data,

        rainfall_2025_data=
            safe_records(
                rainfall_2025_df
            ),

        rainfall_2026_data=
            safe_records(
                rainfall_df
            ),

        rainfall_data=
            safe_records(
                rainfall_df
            ),

        water_use_2025_data=
            safe_records(
                water_use_2025_df
            ),

        water_use_2026_data=
            safe_records(
                water_use_2026_df
            ),

        water_use_2026_summary=
            water_use_2026_summary,

        demand_data=
            safe_records(
                demand_df
            ),

        reservoir_data=
            safe_records(
                reservoir_df
            ),

        supply_demand_data=
            supply_demand_data,

        animal_data=
            animal_data,

        animal_summary=
            animal_summary,

        total_animals=
            total_animals,

        total_daily_water=
            total_daily_water,

        total_monthly_water=
            total_monthly_water,

        highest_consumer=
            highest_consumer,

        alerts=
            alerts,

    )


# ============================================================
# SEARCH API
# ============================================================

@app.route("/api/search")
def api_search():

    query = request.args.get(
        "q",
        ""
    ).strip().lower()

    if not query:

        return jsonify([])

    datasets = {

        "Rainfall 2026":
            load_csv(
                RAINFALL_FILE
            ),

        "Water Use 2026":
            load_csv(
                WATER_USE_2026_FILE
            ),

        "Reservoir":
            load_csv(
                RESERVOIR_FILE
            ),

        "Demand":
            load_csv(
                DEMAND_FILE
            ),

    }

    results = []

    for dataset_name, df in datasets.items():

        if df.empty:
            continue

        mask = df.astype(str).apply(

            lambda col:

                col.str.lower()
                .str.contains(
                    query,
                    na=False
                )

        ).any(axis=1)

        matched = df[
            mask
        ].head(30)

        for _, row in matched.iterrows():

            results.append({

                "dataset":
                    dataset_name,

                "data": {

                    str(k):

                        (
                            "Available"
                            if pd.isna(v)
                            else str(v)
                        )

                    for k, v
                    in row.to_dict().items()

                }

            })

    return jsonify(results)


# ============================================================
# RAINFALL PAGE
# ============================================================

@app.route("/rainfall")
def rainfall():

    data = load_csv(
        RAINFALL_FILE
    )

    if data.empty:

        data = pd.DataFrame({

            "year": [
                2026,
                2026,
                2026,
                2026,
                2026,
                2026
            ],

            "month": [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun"
            ],

            "rainfall_mm": [
                2.8,
                2.1,
                4.5,
                18.2,
                42.6,
                76.4
            ]

        })

    return render_template(

        "rainfall.html",

        rainfall_data=
            safe_records(
                data
            )

    )


# ============================================================
# DEMAND PAGE
# ============================================================

@app.route("/demand")
def demand():

    data = load_csv(
        DEMAND_FILE
    )

    if data.empty:

        data = pd.DataFrame({

            "year": [
                2026,
                2026,
                2026,
                2026,
                2026,
                2026
            ],

            "month": [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun"
            ],

            "demand_mld": [
                540,
                550,
                565,
                580,
                600,
                620
            ]

        })

    return render_template(

        "demand.html",

        demand_data=
            safe_records(
                data
            )

    )


# ============================================================
# RESERVOIR PAGE
# ============================================================

@app.route("/reservoir")
def reservoir():

    data = load_csv(
        RESERVOIR_FILE
    )

    if data.empty:

        data = pd.DataFrame({

            "reservoir_name": [
                "Ujani Demonstration",
                "Ujani Demonstration",
                "Ujani Demonstration",
                "Ujani Demonstration",
                "Ujani Demonstration",
                "Ujani Demonstration"
            ],

            "date": [
                "2026-03-31",
                "2026-04-30",
                "2026-05-31",
                "2026-06-30",
                "2026-07-31",
                "2026-08-20"
            ],

            "storage_mcm": [
                2050.20,
                1980.40,
                1915.80,
                1880.60,
                1855.30,
                1842.50
            ],

            "capacity_mcm": [
                3071,
                3071,
                3071,
                3071,
                3071,
                3071
            ],

            "inflow_mcm": [
                142.5,
                136.8,
                131.2,
                126.5,
                124.1,
                128.4
            ],

            "outflow_mcm": [
                101.2,
                98.6,
                95.8,
                94.2,
                92.5,
                96.7
            ]

        })

    return render_template(

        "reservoir.html",

        reservoir_data=
            safe_records(
                data
            )

    )


# ============================================================
# WATER QUALITY
# ============================================================

@app.route("/water-quality")
def water_quality():

    return render_template(
        "water_quality.html"
    )


# ============================================================
# WATER ALLOCATION
# ============================================================

@app.route("/water-allocation")
def water_allocation():

    return render_template(
        "water_allocation.html"
    )


# ============================================================
# RISK ALERTS
# ============================================================

@app.route("/risk-alerts")
def risk_alerts():

    return render_template(
        "risk_alerts.html"
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
# SUSTAINABILITY
# ============================================================

@app.route("/sustainability")
def sustainability():

    return render_template(
        "sustainability.html"
    )


# ============================================================
# ANALYTICS
# ============================================================

@app.route("/analytics")
def analytics():

    return render_template(
        "analytics.html"
    )


# ============================================================
# GLOBAL WATER
# ============================================================

@app.route("/global-water")
def global_water():

    df = load_csv(
        GLOBAL_WATER_FILE
    )

    if df.empty:

        df = pd.DataFrame({

            "country": [
                "India",
                "USA",
                "China",
                "Brazil",
                "Australia"
            ],

            "year": [
                2026,
                2026,
                2026,
                2026,
                2026
            ],

            "agriculture": [
                8420,
                6210,
                7310,
                5140,
                2940
            ],

            "industry": [
                3160,
                2840,
                4020,
                2180,
                1280
            ],

            "domestic": [
                2280,
                1950,
                2140,
                1430,
                860
            ]

        })

    records = safe_records(
        df
    )

    countries = []

    if (
        not df.empty
        and
        "country" in df.columns
    ):

        countries = sorted(

            df[
                "country"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()

        )

    if not countries:

        countries = [
            "India",
            "USA",
            "China",
            "Brazil",
            "Australia"
        ]

    return render_template(

        "global_water.html",

        countries=countries,

        global_water_data=
            records,

        selected_country=
            request.args.get(
                "country",
                ""
            ),

    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )