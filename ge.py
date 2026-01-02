import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

st.set_page_config(page_title="Geospatial Dashboard", layout="wide")

# ---------------- Sidebar ----------------
st.sidebar.title("Filters")

REGIONS = {
    "Ethiopia": (9.145, 40.4897, 5),
    "Horn of Africa": (8.0, 43.0, 4),
    "East Africa": (1.0, 37.0, 4),
}

region_name = st.sidebar.selectbox("Select Region", REGIONS.keys())
start, end = st.sidebar.date_input(
    "Date Range",
    [pd.to_datetime("2021-01-01"), pd.to_datetime("2021-12-31")]
)

lat, lon, zoom = REGIONS[region_name]

# ---------------- Header ----------------
st.title("🌍 Geospatial Environmental Dashboard")
st.markdown("Remote Sensing • NDVI • Time Series")

# ---------------- Map ----------------
df_map = pd.DataFrame({"lat": [lat], "lon": [lon]})

layer = pdk.Layer(
    "ScatterplotLayer",
    df_map,
    get_position="[lon, lat]",
    get_radius=50000,
    get_fill_color=[0, 160, 0],
)

view = pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom)

st.subheader("📍 Region Map")
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))

# ---------------- NDVI Stats ----------------
ndvi = np.random.rand(100, 100)

c1, c2, c3 = st.columns(3)
c1.metric("Mean NDVI", f"{ndvi.mean():.2f}")
c2.metric("Max NDVI", f"{ndvi.max():.2f}")
c3.metric("Min NDVI", f"{ndvi.min():.2f}")

# ---------------- Time Series ----------------
dates = pd.date_range(start, end, freq="M")
ndvi_ts = np.random.uniform(0.3, 0.8, len(dates))

df_ts = pd.DataFrame({"Date": dates, "NDVI": ndvi_ts})

st.subheader("📈 NDVI Time Series")
chart = alt.Chart(df_ts).mark_line(point=True).encode(
    x="Date:T",
    y=alt.Y("NDVI:Q", scale=alt.Scale(domain=[0, 1]))
)

st.altair_chart(chart, use_container_width=True)

st.success("✅ Running safely on Streamlit Cloud (no Folium).")
