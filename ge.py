import streamlit as st
import pydeck as pdk

st.set_page_config(layout="wide")
st.title("🌍 Simple Map Dashboard (Arba Minch)")

# Center coordinates for Arba Minch
lat_center, lon_center = 6.04, 37.56
zoom_level = 10  # adjust zoom for small area

# Define the map view
view = pdk.ViewState(
    latitude=lat_center,
    longitude=lon_center,
    zoom=zoom_level
)

# Create the map
st.subheader("🗺️ Map Around Arba Minch")
st.pydeck_chart(
    pdk.Deck(
        layers=[],  # no layers yet
        initial_view_state=view,
        map_style="mapbox://styles/mapbox/satellite-v9"  # satellite map
    )
)

st.success("✅ Map loaded successfully")
