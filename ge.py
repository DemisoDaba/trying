import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

st.set_page_config(page_title="Geospatial Dashboard", layout="wide")

# ======================
# Sidebar
# ======================
st.sidebar.title("Data Filters")

REGIONS = {
    "Ethiopia": {"lat": 9.145, "lon": 40.4897, "zoom": 5},
    "East Africa": {"lat": 1.0, "lon": 37.0, "zoom": 4},
    "Horn of Africa": {"lat": 8.0, "lon": 43.0, "zoom": 4},
}

selected_region = st.sidebar.selectbox("Select Region", REGIONS.keys())
date_range = st.sidebar.date_input(
    "Date Range",
    [pd.to_datetime("2021-01-01"), pd.to_datetime("2021-12-31")]
)

# ======================
# Header
# ======================
st.title("🌍 Geospatial Environmental Dashboard")
st.markdown("Remote Sensing • NDVI • Time Series Analysis")

# ======================
# MAP (PyDeck)
# ======================
region = REGIONS[selected_region]

map_df = pd.DataFrame({
    "lat": [region["lat"]],
    "lon": [region["lon"]],
})

layer = pdk.Layer(
    "ScatterplotLayer",
    map_df,
    get_position="[lon, lat]",
    get_radius=40000,
    get_fill_color=[0, 180, 0],
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=region["lat"],
    longitude=region["lon"],
    zoom=region["zoom"],
)

st.subheader("📍 Region Map")
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# ======================
# NDVI STATISTICS
# ======================
ndvi = np.random.rand(100, 100)

col1, col2, col3 = st.columns(3)
col1.metric("Mean NDVI", f"{ndvi.mean():.2f}")
col2.metric("Max NDVI", f"{ndvi.max():.2f}")
col3.metric("Min NDVI", f"{ndvi.min():.2f}")

# ======================
# NDVI TIME SERIES
# ======================
dates = pd.date_range(date_range[0], date_range[1], freq="M")
ndvi_series = np.random.uniform(0.2, 0.8, len(dates))

ts_df = pd.DataFrame({"Date": dates, "NDVI": ndvi_series})

st.subheader("📈 NDVI Time Series")

chart = alt.Chart(ts_df).mark_line(point=True).encode(
    x="Date:T",
    y=alt.Y("NDVI:Q", scale=alt.Scale(domain=[0, 1]))
)
st.altair_chart(chart, use_container_width=True)

st.success("✅ App running without Folium or GIS dependency issues.")
