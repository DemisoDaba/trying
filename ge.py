import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

st.set_page_config(layout="wide")

st.title("🌍 Geospatial Dashboard (Cloud Safe)")

# Sidebar
region = st.sidebar.selectbox(
    "Select Region",
    ["Ethiopia", "Horn of Africa", "East Africa"]
)

regions = {
    "Ethiopia": (9.145, 40.4897, 6),
    "Horn of Africa": (8.0, 43.0, 5),
    "East Africa": (1.0, 37.0, 5),
}

lat, lon, zoom = regions[region]

# Map
df = pd.DataFrame({"lat": [lat], "lon": [lon]})

layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position="[lon, lat]",
    get_radius=60000,
    get_fill_color=[0, 180, 0],
)

view = pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom)

st.subheader("🗺️ Map")
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))

# NDVI Stats
ndvi = np.random.rand(100, 100)

c1, c2, c3 = st.columns(3)
c1.metric("Mean NDVI", f"{ndvi.mean():.2f}")
c2.metric("Max NDVI", f"{ndvi.max():.2f}")
c3.metric("Min NDVI", f"{ndvi.min():.2f}")

# Time series
dates = pd.date_range("2021-01-01", "2021-12-31", freq="M")
df_ts = pd.DataFrame({
    "Date": dates,
    "NDVI": np.random.uniform(0.3, 0.8, len(dates))
})

chart = alt.Chart(df_ts).mark_line(point=True).encode(
    x="Date:T",
    y=alt.Y("NDVI:Q", scale=alt.Scale(domain=[0, 1]))
)

st.subheader("📈 NDVI Time Series")
st.altair_chart(chart, use_container_width=True)

st.success("✅ Deployed successfully on Streamlit Cloud")
