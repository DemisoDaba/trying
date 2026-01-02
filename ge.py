import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

st.set_page_config(layout="wide")
st.title("🌍 Geospatial Dashboard (Arba Minch Area)")

# -----------------------------
# Map Center and Zoom
# -----------------------------
lat_center, lon_center = 6.04, 37.56  # Arba Minch
zoom_level = 10  # zoom for small area

# Rectangle bounds around Arba Minch
lat_range = (5.90, 6.18)
lon_range = (37.40, 37.72)

# Generate random points within the rectangle for demonstration
np.random.seed(42)
n_points = 50
lats = np.random.uniform(lat_range[0], lat_range[1], n_points)
lons = np.random.uniform(lon_range[0], lon_range[1], n_points)
df = pd.DataFrame({"lat": lats, "lon": lons})

# PyDeck Scatterplot Layer
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position="[lon, lat]",
    get_radius=2000,  # small radius for local points
    get_fill_color=[0, 180, 0],
    pickable=True
)

# Map view
view = pdk.ViewState(latitude=lat_center, longitude=lon_center, zoom=zoom_level)

st.subheader("🗺️ Map Around Arba Minch")
st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        map_style="mapbox://styles/mapbox/satellite-v9"  # <-- satellite background
    )
)

# -----------------------------
# NDVI Stats (demo data)
# -----------------------------
ndvi = np.random.rand(100, 100)
c1, c2, c3 = st.columns(3)
c1.metric("Mean NDVI", f"{ndvi.mean():.2f}")
c2.metric("Max NDVI", f"{ndvi.max():.2f}")
c3.metric("Min NDVI", f"{ndvi.min():.2f}")

# -----------------------------
# NDVI Time Series
# -----------------------------
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
