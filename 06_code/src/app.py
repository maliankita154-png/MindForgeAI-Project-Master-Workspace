import os
import pandas as pd
from flask import Flask, render_template, request

# ============================================================
# AETHERA WATER INTELLIGENCE
# ============================================================

app = Flask(__name__)

# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

PROJECT_ROOT = os.path.dirname(BASE_DIR)

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

# IMPORTANT:
# reservoir_2025_2026.csv is EMPTY (0 bytes)
# Therefore use the existing reservoir_demo.csv.
RESERVOIR_FILE = os.path.join(
    CURATED_DIR,
    "reservoir_demo.csv"
)

DEMAND_FILE = os.path.join(
    DATA_DIR,
    "demand_demo.csv"
)

ANIMAL_WATER_FILE = os.path.join(
    DATA_DIR,
    "animal_water_use.csv"
)

GLOBAL_WATER_FILE = os.path.join(
    DATA_DIR,
    "water_use.csv"
)


# ============================================================
# SAFE CSV LOADER
# ============================================================

def load_csv(file_path):

    if not os.path.exists(file_path):

        print("File not found:", file_path)

        return pd.DataFrame()

    try:

        # First try normal CSV
        df = pd.read_csv(file_path)

        # Support TAB separated files
        if len(df.columns) == 1 and "\t" in str(df.columns[0]):

            df = pd.read_csv(
                file_path,
                sep="\t"
            )

        # Clean column names
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
    # LOAD DATASETS
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

    latest_rainfall = 0
    latest_rainfall_month = "N/A"

    if not rainfall_2026_df.empty:

        # Total rainfall
        if "rainfall_mm" in rainfall_2026_df.columns:

            rainfall_2026_total = round(
                pd.to_numeric(
                    rainfall_2026_df["rainfall_mm"],
                    errors="coerce"
                )
                .fillna(0)
                .sum(),
                2
            )

            # Latest rainfall
            latest_rainfall = safe_number(
                rainfall_2026_df[
                    "rainfall_mm"
                ].iloc[-1]
            )

        # Total runoff
        if "runoff_mcm" in rainfall_2026_df.columns:

            runoff_2026_total = round(
                pd.to_numeric(
                    rainfall_2026_df["runoff_mcm"],
                    errors="coerce"
                )
                .fillna(0)
                .sum(),
                2
            )

        # Total groundwater recharge
        if "groundwater_recharge_mcm" in rainfall_2026_df.columns:

            recharge_2026_total = round(
                pd.to_numeric(
                    rainfall_2026_df[
                        "groundwater_recharge_mcm"
                    ],
                    errors="coerce"
                )
                .fillna(0)
                .sum(),
                2
            )

        # Latest month
        if "month" in rainfall_2026_df.columns:

            latest_rainfall_month = str(
                rainfall_2026_df[
                    "month"
                ].iloc[-1]
            )


    # ========================================================
    # 2026 RAINFALL DATA
    # ========================================================

    rainfall_2026_data = []

    if not rainfall_2026_df.empty:

        rainfall_2026_data = (
            rainfall_2026_df
            .fillna("")
            .to_dict(
                orient="records"
            )
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
            "water_demand"
        ]

        for column in demand_columns:

            if column in demand_df.columns:

                demand_value = safe_number(
                    demand_df[
                        column
                    ].iloc[-1]
                )

                break


    # ========================================================
    # RESERVOIR / DAM
    # ========================================================

    reservoir_value = 0

    reservoir_latest_date = "N/A"

    reservoir_name = "N/A"

    reservoir_capacity = 0

    reservoir_inflow = 0

    reservoir_outflow = 0

    reservoir_data = []


    if not reservoir_df.empty:

        # All reservoir records
        reservoir_data = (
            reservoir_df
            .fillna("")
            .to_dict(
                orient="records"
            )
        )

        # Storage percentage
        if "storage_pct" in reservoir_df.columns:

            reservoir_value = safe_number(
                reservoir_df[
                    "storage_pct"
                ].iloc[-1]
            )

        elif "availability_pct" in reservoir_df.columns:

            reservoir_value = safe_number(
                reservoir_df[
                    "availability_pct"
                ].iloc[-1]
            )

        elif "availability" in reservoir_df.columns:

            reservoir_value = safe_number(
                reservoir_df[
                    "availability"
                ].iloc[-1]
            )

        # Latest date
        if "date" in reservoir_df.columns:

            reservoir_latest_date = str(
                reservoir_df[
                    "date"
                ].iloc[-1]
            )

        # Reservoir name
        if "reservoir_name" in reservoir_df.columns:

            reservoir_name = str(
                reservoir_df[
                    "reservoir_name"
                ].iloc[-1]
            )

        # Capacity
        if "capacity_mcm" in reservoir_df.columns:

            reservoir_capacity = safe_number(
                reservoir_df[
                    "capacity_mcm"
                ].iloc[-1]
            )

        # Latest inflow
        if "inflow_mcm" in reservoir_df.columns:

            reservoir_inflow = safe_number(
                reservoir_df[
                    "inflow_mcm"
                ].iloc[-1]
            )

        # Latest outflow
        if "outflow_mcm" in reservoir_df.columns:

            reservoir_outflow = safe_number(
                reservoir_df[
                    "outflow_mcm"
                ].iloc[-1]
            )


    # ========================================================
    # RESERVOIR SUMMARY
    # ========================================================

    reservoir_summary = {

        "name": reservoir_name,

        "storage_pct": round(
            reservoir_value,
            2
        ),

        "capacity_mcm": round(
            reservoir_capacity,
            2
        ),

        "latest_inflow_mcm": round(
            reservoir_inflow,
            2
        ),

        "latest_outflow_mcm": round(
            reservoir_outflow,
            2
        ),

        "latest_date": reservoir_latest_date,

        "records": len(
            reservoir_df
        )
    }


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

                    pd.to_numeric(
                        water_2026_df[
                            column
                        ],
                        errors="coerce"
                    )
                    .fillna(0)
                    .sum(),

                    2
                )


    # ========================================================
    # WATER USE DATA
    # ========================================================

    water_use_2026_data = []

    if not water_2026_df.empty:

        water_use_2026_data = (
            water_2026_df
            .fillna("")
            .to_dict(
                orient="records"
            )
        )


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

        if "Country" in global_df.columns:

            countries = (

                global_df[
                    "Country"
                ]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
                .tolist()
            )

            countries.sort(
                key=str.lower
            )

            water_summary[
                "countries"
            ] = len(
                countries
            )


        for key, column in [

            (
                "agriculture",
                "Agriculture"
            ),

            (
                "industry",
                "Industry"
            ),

            (
                "domestic",
                "Domestic"
            )

        ]:

            if column in global_df.columns:

                water_summary[key] = round(

                    pd.to_numeric(
                        global_df[
                            column
                        ],
                        errors="coerce"
                    )
                    .fillna(0)
                    .mean(),

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

        required = [

            "animals_count",

            "daily_water_litres_per_animal"
        ]


        if all(
            column in animal_df.columns
            for column in required
        ):

            animal_df[
                "animals_count"
            ] = pd.to_numeric(

                animal_df[
                    "animals_count"
                ],

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


            total_animals = int(

                animal_df[
                    "animals_count"
                ].sum()
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


            animal_data = (

                animal_df
                .fillna("")
                .to_dict(
                    orient="records"
                )
            )


    animal_summary = {

        "total_animals":
            total_animals,

        "daily_water":
            total_daily_water,

        "monthly_water":
            total_monthly_water,

        "highest_consumer":
            highest_consumer
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


    rainfall_compare_data = (

        rainfall_compare_df
        .fillna("")
        .to_dict(
            orient="records"
        )
    )


    water_use_compare_data = (

        water_compare_df
        .fillna("")
        .to_dict(
            orient="records"
        )
    )


    reservoir_compare_data = (

        reservoir_df
        .fillna("")
        .to_dict(
            orient="records"
        )
    )


    # ========================================================
    # DASHBOARD DATA
    # ========================================================

    data = {

        "rainfall":
            rainfall_2026_total,

        "latest_rainfall":
            latest_rainfall,

        "latest_rainfall_month":
            latest_rainfall_month,

        "demand":
            demand_value,

        "reservoir":
            reservoir_value
    }


    # ========================================================
    # DEBUG INFORMATION
    # ========================================================

    print()

    print("========================================")

    print(" AETHERA | 2026 WATER INTELLIGENCE")

    print("========================================")

    print(
        "2026 Rainfall:",
        rainfall_2026_total,
        "mm"
    )

    print(
        "Latest Rainfall:",
        latest_rainfall,
        "mm"
    )

    print(
        "Latest Rainfall Month:",
        latest_rainfall_month
    )

    print(
        "2026 Runoff:",
        runoff_2026_total,
        "MCM"
    )

    print(
        "2026 Groundwater Recharge:",
        recharge_2026_total,
        "MCM"
    )

    print(
        "Reservoir:",
        reservoir_name
    )

    print(
        "Reservoir Storage:",
        reservoir_value,
        "%"
    )

    print(
        "Reservoir Capacity:",
        reservoir_capacity,
        "MCM"
    )

    print(
        "Latest Inflow:",
        reservoir_inflow,
        "MCM"
    )

    print(
        "Latest Outflow:",
        reservoir_outflow,
        "MCM"
    )

    print(
        "Reservoir Records:",
        len(reservoir_df)
    )

    print(
        "2026 Water Use:",
        water_use_2026_summary
    )

    print("========================================")

    print()


    # ========================================================
    # RENDER DASHBOARD
    # ========================================================

    return render_template(

        "dashboard.html",

        data=data,

        water_summary=water_summary,

        countries=countries,

        # ---------------------------------------------
        # RAINFALL
        # ---------------------------------------------

        rainfall_2026_data=rainfall_2026_data,

        rainfall_2026_total=
            rainfall_2026_total,

        runoff_2026_total=
            runoff_2026_total,

        recharge_2026_total=
            recharge_2026_total,

        rainfall_compare_data=
            rainfall_compare_data,

        rainfall_data=
            rainfall_2026_data,

        # ---------------------------------------------
        # WATER USE
        # ---------------------------------------------

        water_use_2025_data=(

            water_2025_df
            .fillna("")
            .to_dict(
                orient="records"
            )
        ),

        water_use_2026_data=
            water_use_2026_data,

        water_use_2026_summary=
            water_use_2026_summary,

        water_use_compare_data=
            water_use_compare_data,

        # ---------------------------------------------
        # RESERVOIR / DAM
        # ---------------------------------------------

        reservoir_data=
            reservoir_data,

        reservoir_value=
            reservoir_value,

        reservoir_latest_date=
            reservoir_latest_date,

        reservoir_summary=
            reservoir_summary,

        reservoir_compare_data=
            reservoir_compare_data,

        # ---------------------------------------------
        # DEMAND
        # ---------------------------------------------

        demand_data=(

            demand_df
            .fillna("")
            .to_dict(
                orient="records"
            )
        ),

        # ---------------------------------------------
        # ANIMAL
        # ---------------------------------------------

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
            highest_consumer
    )


# ============================================================
# RAINFALL PAGE
# ============================================================

@app.route("/rainfall")
def rainfall():

    df = load_csv(
        RAINFALL_FILE
    )

    return render_template(

        "rainfall.html",

        rainfall_data=(

            df
            .fillna("")
            .to_dict(
                orient="records"
            )
        )
    )


# ============================================================
# DEMAND PAGE
# ============================================================

@app.route("/demand")
def demand():

    df = load_csv(
        DEMAND_FILE
    )

    return render_template(

        "demand.html",

        demand_data=(

            df
            .fillna("")
            .to_dict(
                orient="records"
            )
        )
    )


# ============================================================
# RESERVOIR PAGE
# ============================================================

@app.route("/reservoir")
def reservoir():

    df = load_csv(
        RESERVOIR_FILE
    )

    return render_template(

        "reservoir.html",

        reservoir_data=(

            df
            .fillna("")
            .to_dict(
                orient="records"
            )
        )
    )


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


    # ========================================================
    # COUNTRY LIST
    # ========================================================

    if (

        not df.empty

        and

        "Country" in df.columns

    ):

        countries = (

            df[
                "Country"
            ]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        countries.sort(
            key=str.lower
        )


    # ========================================================
    # DEFAULT COUNTRY
    # ========================================================

    if (

        not selected_country

        and

        countries

    ):

        selected_country = countries[0]


    # ========================================================
    # SELECT COUNTRY
    # ========================================================

    if (

        not df.empty

        and

        selected_country

        and

        "Country" in df.columns

    ):

        selected_rows = df[

            df[
                "Country"
            ]
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

                "Country": str(

                    row.get(
                        "Country",
                        selected_country
                    )
                ),

                "Year": str(
                    year
                ),

                "Agriculture":
                    agriculture,

                "Industry":
                    industry,

                "Domestic":
                    domestic,

                "Total":
                    total
            }


    # ========================================================
    # GLOBAL SUMMARY
    # ========================================================

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

        (
            "agriculture",
            "Agriculture"
        ),

        (
            "industry",
            "Industry"
        ),

        (
            "domestic",
            "Domestic"
        )

    ]:

        if (

            not df.empty

            and

            column in df.columns

        ):

            values = pd.to_numeric(

                df[column],

                errors="coerce"

            ).dropna()


            if not values.empty:

                water_summary[key] = round(

                    float(
                        values.mean()
                    ),

                    2
                )


    return render_template(

        "global_water.html",

        countries=countries,

        global_water_data=(

            df
            .fillna("")
            .to_dict(
                orient="records"
            )
        ),

        selected_country=
            selected_country,

        selected_data=
            selected_data,

        water_summary=
            water_summary
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
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    return (

        "<h1>AETHERA Server Error</h1>"

        "<p>Something went wrong.</p>"

        "<a href='/'>Return Home</a>"

    ), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print()

    print("========================================")

    print(" AETHERA WATER INTELLIGENCE")

    print("========================================")

    print("Server:")

    print("http://127.0.0.1:8000")

    print("========================================")

    print()

    app.run(

        debug=True,

        host="127.0.0.1",

        port=8000
    )