import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# AETHERA - Streamlit Application
# ============================================================

st.set_page_config(
    page_title="AETHERA | Water Intelligence",
    page_icon="💧",
    layout="wide"
)

# ------------------------------------------------------------
# DATA PATH
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


# ------------------------------------------------------------
# LOAD CSV SAFELY
# ------------------------------------------------------------

def load_csv(filename):
    file_path = DATA_DIR / filename

    if file_path.exists():
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            st.error(f"Error reading {filename}: {e}")
            return pd.DataFrame()

    return pd.DataFrame()


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

rainfall_df = load_csv("rainfall_2026.csv")
water_use_df = load_csv("water_use_2026.csv")
reservoir_df = load_csv("reservoir_demo.csv")


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.title("💧 AETHERA")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Rainfall Prediction",
        "Water Demand",
        "Reservoir",
        "Water Quality",
        "Water Allocation",
        "Risk & Alerts",
        "Digital Twin",
        "Sustainability",
        "Analytics"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.title("💧 AETHERA")
    st.subheader("Water Intelligence & Decision Support System")

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌧️ Rainfall Records",
            len(rainfall_df)
        )

    with col2:
        st.metric(
            "💧 Water Use Records",
            len(water_use_df)
        )

    with col3:
        st.metric(
            "🏞️ Reservoir Records",
            len(reservoir_df)
        )

    with col4:
        st.metric(
            "📅 Monitoring Year",
            "2026"
        )

    st.markdown("---")

    # Rainfall
    st.subheader("🌧️ Rainfall Data")

    if not rainfall_df.empty:
        st.dataframe(
            rainfall_df,
            use_container_width=True
        )
    else:
        st.warning("Rainfall data not found.")

    # Water use
    st.subheader("💧 Water Usage Data")

    if not water_use_df.empty:
        st.dataframe(
            water_use_df,
            use_container_width=True
        )
    else:
        st.warning("Water-use data not found.")

    # Reservoir
    st.subheader("🏞️ Reservoir Data")

    if not reservoir_df.empty:
        st.dataframe(
            reservoir_df,
            use_container_width=True
        )
    else:
        st.warning("Reservoir data not found.")


# ============================================================
# RAINFALL
# ============================================================

elif page == "Rainfall Prediction":

    st.title("🌧️ Rainfall Prediction")

    if rainfall_df.empty:
        st.warning("Rainfall data not found.")
    else:
        st.dataframe(
            rainfall_df,
            use_container_width=True
        )

        st.subheader("Rainfall Visualization")

        numeric_columns = rainfall_df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_columns) > 0:
            st.line_chart(
                rainfall_df[numeric_columns]
            )


# ============================================================
# WATER DEMAND
# ============================================================

elif page == "Water Demand":

    st.title("💧 Water Demand")

    if water_use_df.empty:
        st.warning("Water-use data not found.")
    else:
        st.dataframe(
            water_use_df,
            use_container_width=True
        )

        numeric_columns = water_use_df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_columns) > 0:
            st.bar_chart(
                water_use_df[numeric_columns]
            )


# ============================================================
# RESERVOIR
# ============================================================

elif page == "Reservoir":

    st.title("🏞️ Reservoir Monitoring")

    if reservoir_df.empty:
        st.warning("Reservoir data not found.")
    else:
        st.dataframe(
            reservoir_df,
            use_container_width=True
        )

        numeric_columns = reservoir_df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_columns) > 0:
            st.line_chart(
                reservoir_df[numeric_columns]
            )


# ============================================================
# OTHER MODULES
# ============================================================

elif page == "Water Quality":

    st.title("🧪 Water Quality")
    st.info("Water quality monitoring module.")

elif page == "Water Allocation":

    st.title("🚰 Water Allocation")
    st.info("Water allocation module.")

elif page == "Risk & Alerts":

    st.title("⚠️ Risk & Alerts")
    st.info("Risk monitoring and AI alerts module.")

elif page == "Digital Twin":

    st.title("🖥️ Digital Twin")
    st.info("AETHERA Digital Twin module.")

elif page == "Sustainability":

    st.title("🌱 Sustainability")
    st.info("Sustainability monitoring module.")

elif page == "Analytics":

    st.title("📊 Analytics")
    st.info("Advanced analytics module.")