import streamlit as st
import leafmap.foliumap as leafmap
from datetime import date

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Geospatial Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===============================
# HEADER
# ===============================
st.markdown("<h1 style='text-align: center; color: darkblue;'>Geospatial Analysis</h1>", unsafe_allow_html=True)

# ===============================
# TOP BUTTONS
# ===============================
col1, col2, col3 = st.columns(3)
with col1:
    raster_btn = st.button("Raster")
with col2:
    vector_btn = st.button("Vector")
with col3:
    terrain_btn = st.button("3D Terrain")

# ===============================
# LEFT SIDEBAR FILTERS
# ===============================
st.sidebar.header("Filters")
region = st.sidebar.selectbox("Select Region", ["Region A", "Region B", "Region C"])
dataset = st.sidebar.selectbox("Select Dataset", ["Dataset 1", "Dataset 2", "Dataset 3"])
start_date = st.sidebar.date_input("Start Date", value=date(2025,1,1))
end_date = st.sidebar.date_input("End Date", value=date(2025,12,31))

# ===============================
# MAIN LAYOUT
# ===============================
left_col, center_col, right_col = st.columns([1,3,1])

# LEFT: maybe additional info or small preview
with left_col:
    st.write("### Info / Preview")
    st.image("https://via.placeholder.com/150", caption="Preview")

# CENTER: Map / Satellite imagery
with center_col:
    st.write("### Map / Imagery Viewer")
    m = leafmap.Map(center=[0,0], zoom=2)
    m.add_basemap("HYBRID")  # Satellite + Labels
    m.to_streamlit(height=600)

# RIGHT: Extra maps or layers
with right_col:
    st.write("### Additional Maps")
    st.image("https://via.placeholder.com/150", caption="Map 1")
    st.image("https://via.placeholder.com/150", caption="Map 2")
