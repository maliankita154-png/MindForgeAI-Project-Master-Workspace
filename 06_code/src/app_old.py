from flask import Flask, render_template, request
import os
import pandas as pd


# ============================================================
# AETHERA APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

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

WATER_USE_2026_FILE = os.path.join(
    CURATED_DIR,
    "water_use_2026.csv"
)

DEMAND_FILE = os.path.join(
    DATA_DIR,
    "demand_demo.csv"
)

RESERVOIR_FILE = os.path.join(
    DATA_DIR,
    "reservoir_demo.csv"
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

    if os.path.exists(file_path):

        try:

            df = pd.read_csv(file_path)

            # Clean column names
            df.columns = (
                df.columns
                .astype(str)
                .str.strip()
            )

            return df

        except Exception as e:

            print(
                f"Error reading file: {file_path}"
            )

            print(e)

    else:

        print(
            f"File not found: {file_path}"
        )

    return pd.DataFrame()


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

    # --------------------------------------------------------
    # LOAD DATASETS
    # --------------------------------------------------------

    rainfall_df = load_csv(
        RAINFALL_FILE
    )

    water_use_2026_df = load_csv(
        WATER_USE_2026_FILE
    )

    demand_df = load_csv(
        DEMAND_FILE
    )

    reservoir_df = load_csv(
        RESERVOIR_FILE
    )

    animal_df = load_csv(
        ANIMAL_WATER_FILE
    )

    global_df = load_csv(
        GLOBAL_WATER_FILE
    )


    # --------------------------------------------------------
    # RAINFALL
    # --------------------------------------------------------

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

                rainfall_value = rainfall_df[
                    column
                ].iloc[-1]

                break


    # --------------------------------------------------------
    # DEMAND
    # --------------------------------------------------------

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

                demand_value = demand_df[
                    column
                ].iloc[-1]

                break


    # --------------------------------------------------------
    # RESERVOIR
    # --------------------------------------------------------

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

                reservoir_value = reservoir_df[
                    column
                ].iloc[-1]

                break


    # --------------------------------------------------------
    # ANIMAL WATER
    # --------------------------------------------------------

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


            # Total daily water

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


            # Total animals

            total_animals = int(
                animal_df[
                    "animals_count"
                ].sum()
            )


            # Total daily water

            total_daily_water = float(
                animal_df[
                    "total_daily_water"
                ].sum()
            )


            # Monthly water

            total_monthly_water = (
                total_daily_water * 30
            )


            # Highest consumer

            if not animal_df.empty:

                highest_index = (
                    animal_df[
                        "total_daily_water"
                    ].idxmax()
                )

                if "animal" in animal_df.columns:

                    highest_consumer = str(
                        animal_df.loc[
                            highest_index,
                            "animal"
                        ]
                    )


            # Records

            animal_data = animal_df.to_dict(
                orient="records"
            )


    # --------------------------------------------------------
    # ANIMAL SUMMARY
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # GLOBAL WATER SUMMARY
    # --------------------------------------------------------

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
            ] = len(countries)


        if "Agriculture" in global_df.columns:

            water_summary[
                "agriculture"
            ] = round(

                pd.to_numeric(
                    global_df[
                        "Agriculture"
                    ],
                    errors="coerce"
                )
                .fillna(0)
                .mean(),

                2
            )


        if "Industry" in global_df.columns:

            water_summary[
                "industry"
            ] = round(

                pd.to_numeric(
                    global_df[
                        "Industry"
                    ],
                    errors="coerce"
                )
                .fillna(0)
                .mean(),

                2
            )


        if "Domestic" in global_df.columns:

            water_summary[
                "domestic"
            ] = round(

                pd.to_numeric(
                    global_df[
                        "Domestic"
                    ],
                    errors="coerce"
                )
                .fillna(0)
                .mean(),

                2
            )


    # --------------------------------------------------------
    # 2026 WATER USE SUMMARY
    # --------------------------------------------------------

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


    if not water_use_2026_df.empty:

        columns_map = {

            "agriculture":
                "agriculture_mcm",

            "industry":
                "industry_mcm",

            "domestic":
                "domestic_mcm",

            "power":
                "power_mcm",

            "animal":
                "animal_husbandry_mcm",

            "environment":
                "environment_mcm",

            "other":
                "other_mcm",

            "total":
                "total_use_mcm"

        }


        for key, column in columns_map.items():

            if column in water_use_2026_df.columns:

                water_use_2026_summary[
                    key
                ] = round(

                    pd.to_numeric(
                        water_use_2026_df[
                            column
                        ],
                        errors="coerce"
                    )
                    .fillna(0)
                    .sum(),

                    2

                )


    # --------------------------------------------------------
    # DASHBOARD DATA
    # --------------------------------------------------------

    data = {

        "rainfall": rainfall_value,

        "demand": demand_value,

        "reservoir": reservoir_value

    }


    # --------------------------------------------------------
    # RENDER DASHBOARD
    # --------------------------------------------------------

    return render_template(

        "dashboard.html",

        data=data,

        water_summary=water_summary,

        countries=countries,

        rainfall_2026_data=(
            rainfall_df.to_dict(
                orient="records"
            )
        ),

        water_use_2026_data=(
            water_use_2026_df.to_dict(
                orient="records"
            )
        ),

        water_use_2026_summary=(
            water_use_2026_summary
        ),

        rainfall_data=(
            rainfall_df.to_dict(
                orient="records"
            )
        ),

        demand_data=(
            demand_df.to_dict(
                orient="records"
            )
        ),

        reservoir_data=(
            reservoir_df.to_dict(
                orient="records"
            )
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

    df = load_csv(
        RAINFALL_FILE
    )

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

    df = load_csv(
        DEMAND_FILE
    )

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

    df = load_csv(
        RESERVOIR_FILE
    )

    return render_template(

        "reservoir.html",

        reservoir_data=df.to_dict(
            orient="records"
        )

    )


# ============================================================
# GLOBAL WATER INTELLIGENCE
# ============================================================

@app.route("/global-water")
def global_water():

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    df = load_csv(
        GLOBAL_WATER_FILE
    )


    countries = []

    selected_country = ""

    selected_data = None


    # --------------------------------------------------------
    # NORMALIZE DATA
    # --------------------------------------------------------

    if not df.empty:

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )


    # --------------------------------------------------------
    # COUNTRY LIST
    # --------------------------------------------------------

    if (
        not df.empty
        and "Country" in df.columns
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


    # --------------------------------------------------------
    # GET COUNTRY FROM URL
    # --------------------------------------------------------

    selected_country = request.args.get(
        "country",
        ""
    ).strip()


    # --------------------------------------------------------
    # DEFAULT COUNTRY
    # --------------------------------------------------------

    if (
        not selected_country
        and countries
    ):

        selected_country = countries[0]


    # --------------------------------------------------------
    # SELECT COUNTRY
    # --------------------------------------------------------

    if (
        not df.empty
        and selected_country
        and "Country" in df.columns
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


            # ------------------------------------------------
            # SAFE NUMBER FUNCTION
            # ------------------------------------------------

            def number_value(
                column_name
            ):

                if column_name not in row.index:

                    return 0


                value = pd.to_numeric(

                    row[
                        column_name
                    ],

                    errors="coerce"

                )


                if pd.isna(value):

                    return 0


                return round(
                    float(value),
                    2
                )


            # ------------------------------------------------
            # COUNTRY DATA
            # ------------------------------------------------

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


            # ------------------------------------------------
            # AUTO TOTAL
            # ------------------------------------------------

            if total == 0:

                total = round(

                    agriculture
                    +
                    industry
                    +
                    domestic,

                    2

                )


            # ------------------------------------------------
            # YEAR
            # ------------------------------------------------

            year = row.get(
                "Year",
                "N/A"
            )


            if pd.isna(year):

                year = "N/A"


            # ------------------------------------------------
            # SELECTED DATA
            # ------------------------------------------------

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


    # --------------------------------------------------------
    # GLOBAL WATER SUMMARY
    # --------------------------------------------------------

    water_summary = {

        "countries":
            len(countries),

        "agriculture": 0,

        "industry": 0,

        "domestic": 0

    }


    if not df.empty:


        # ----------------------------------------------------
        # AGRICULTURE
        # ----------------------------------------------------

        if "Agriculture" in df.columns:

            agriculture_values = (
                pd.to_numeric(
                    df["Agriculture"],
                    errors="coerce"
                )
                .dropna()
            )

            if not agriculture_values.empty:

                water_summary[
                    "agriculture"
                ] = round(

                    float(
                        agriculture_values.mean()
                    ),

                    2

                )


        # ----------------------------------------------------
        # INDUSTRY
        # ----------------------------------------------------

        if "Industry" in df.columns:

            industry_values = (
                pd.to_numeric(
                    df["Industry"],
                    errors="coerce"
                )
                .dropna()
            )

            if not industry_values.empty:

                water_summary[
                    "industry"
                ] = round(

                    float(
                        industry_values.mean()
                    ),

                    2

                )


        # ----------------------------------------------------
        # DOMESTIC
        # ----------------------------------------------------

        if "Domestic" in df.columns:

            domestic_values = (
                pd.to_numeric(
                    df["Domestic"],
                    errors="coerce"
                )
                .dropna()
            )

            if not domestic_values.empty:

                water_summary[
                    "domestic"
                ] = round(

                    float(
                        domestic_values.mean()
                    ),

                    2

                )


    # --------------------------------------------------------
    # COMPLETE GLOBAL WATER DATA
    # --------------------------------------------------------

    global_water_data = []


    if not df.empty:

        global_water_data = (
            df.to_dict(
                orient="records"
            )
        )


    # --------------------------------------------------------
    # DEBUG INFORMATION
    # --------------------------------------------------------

    print(
        "\n========================================"
    )

    print(
        "AETHERA | GLOBAL WATER INTELLIGENCE"
    )

    print(
        "========================================"
    )

    print(
        "Dataset:",
        GLOBAL_WATER_FILE
    )

    print(
        "Rows:",
        len(df)
    )

    print(
        "Columns:",
        df.columns.tolist()
        if not df.empty
        else []
    )

    print(
        "Countries:",
        len(countries)
    )

    print(
        "Selected Country:",
        selected_country
    )

    print(
        "Selected Data:",
        selected_data
    )

    print(
        "========================================\n"
    )


    # --------------------------------------------------------
    # RENDER GLOBAL WATER PAGE
    # --------------------------------------------------------

    return render_template(

        "global_water.html",

        countries=countries,

        global_water_data=global_water_data,

        selected_country=selected_country,

        selected_data=selected_data,

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
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    return """

    <div style="
        font-family: Arial;
        padding: 40px;
        text-align: center;
    ">

        <h1>
            AETHERA Server Error
        </h1>

        <p>
            Something went wrong while
            loading this page.
        </p>

        <a href="/">
            Return to Home
        </a>

    </div>

    """, 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print(
        "\n========================================"
    )

    print(
        "        AETHERA WATER INTELLIGENCE"
    )

    print(
        "========================================"
    )

    print(
        "Server:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print(
        "========================================\n"
    )


    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000

    )

