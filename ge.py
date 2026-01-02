# geospatial_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import folium
from streamlit_folium import st_folium

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.title("Data Filters")
region = st.sidebar.selectbox("Select Region", ["Region A", "Region B", "Region C"])
dataset = st.sidebar.selectbox("Select Dataset", ["NDVI"])
date_range = st.sidebar.date_input("Date Range", [pd.to_datetime("2021-06-01"), pd.to_datetime("2021-06-30")])
elevation = st.sidebar.slider("Elevation (m)", 0, 2000, 500)
if st.sidebar.button("Apply Filters"):
    st.sidebar.success("Filters applied!")

# -----------------------
# Main Dashboard
# -----------------------
st.title("Geospatial Dashboard - Environmental Analysis")
st.markdown("Interactive Geospatial Analysis & Remote Sensing Visualization")

# Tabs
tab1, tab2, tab3 = st.tabs(["Raster Analysis", "Vector Data", "3D Terrain"])

with tab1:
    st.subheader("NDVI Map")
    # Create a dummy NDVI raster (replace with real raster data)
    ndvi_data = np.random.rand(100, 100)
    
    # Folium map
    m = folium.Map(location=[12.0, -2.0], zoom_start=5)
    folium.raster_layers.ImageOverlay(
        image=ndvi_data,
        bounds=[[10, -5], [15, 2]],
        colormap=lambda x: (1-x, x, 0, 0.6),
        opacity=0.7,
        name="NDVI"
    ).add_to(m)
    st_data = st_folium(m, width=700, height=450)

    # Statistics
    st.subheader("Statistics")
    st.write(f"Mean NDVI: {ndvi_data.mean():.2f}")
    st.write(f"Max NDVI: {ndvi_data.max():.2f}")
    st.write(f"Min NDVI: {ndvi_data.min():.2f}")

    # NDVI Time Series (dummy)
    st.subheader("NDVI Time Series")
    dates = pd.date_range(start=date_range[0], end=date_range[1])
    ndvi_series = np.random.rand(len(dates)) * 0.5 + 0.3
    ts_df = pd.DataFrame({"Date": dates, "NDVI": ndvi_series})
    chart = alt.Chart(ts_df).mark_line(point=True).encode(
        x="Date",
        y="NDVI"
    )
    st.altair_chart(chart, use_container_width=True)

    # Land Cover Pie Chart
    st.subheader("Land Cover Distribution")
    land_cover = pd.DataFrame({
        'Land Cover': ['Forest', 'Agriculture', 'Water', 'Urban'],
        'Percentage': [45, 30, 15, 10]
    })
    pie = alt.Chart(land_cover).mark_arc().encode(
        theta=alt.Theta(field="Percentage", type="quantitative"),
        color=alt.Color(field="Land Cover", type="nominal"),
        tooltip=['Land Cover', 'Percentage']
    )
    st.altair_chart(pie, use_container_width=True)

# Buttons
st.button("Download Data")
st.button("Generate Report")
st.button("About this Dashboard")
