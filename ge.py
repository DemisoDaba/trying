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
# CUSTOM CSS
# ===============================
st.markdown(
    """
    <style>
    /* HEADER */
    .header {
        background-color: #0a2342;
        color: white;
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }

    /* TOP BUTTONS */
    .top-buttons button {
        margin: 0 10px;
        background-color: #1f77b4;
        color: white;
        border-radius: 8px;
        padding: 10px 25px;
        font-size: 16px;
        font-weight: bold;
    }

    /* SIDEBAR HEADER */
    .sidebar .sidebar-content h2 {
        color: #0a2342;
        font-weight: bold;
    }

    /* MAP SPACE */
    .element-container iframe {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ===============================
# HEADER
# ===============================
st.markdown("<div class='header'><h1>Geospatial Analysis</h1></div>", unsafe_allow_html=True)

# ===============================
# TOP BUTTONS
# ===============================
st.markdown("<div class='top-buttons' style='text-align:center;'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.button("Raster")
with col2:
    st.button("Vector")
with col3:
    st.button("3D Terrain")
st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# SIDEBAR FILTERS
# ===============================
st.sidebar.header("Filters")
region = st.sidebar.selectbox("Select Region", ["Region A", "Region B", "Region C"])
dataset = st.sidebar.selectbox("Select Dataset", ["Dataset 1", "Dataset 2", "Dataset 3"])
start_date = st.sidebar.date_input("Start Date", value=date(2025,1,1))
end_date = st.sidebar.date_input("End Date", value=date(2025,12,31))
apply_filter = st.sidebar.button("Apply Filter")

# ===============================
# MAIN LAYOUT
# ===============================
# Map in center, right panel for additional maps
center_col, right_col = st.columns([4,1], gap="large")

# CENTER: Map / Satellite imagery
with center_col:
    st.write("### Map / Imagery Viewer")
    m = leafmap.Map(center=[0,0], zoom=2)
    m.add_basemap("HYBRID")  # Satellite + Labels
    m.to_streamlit(height=650)

# RIGHT: Additional Maps / Layers
with right_col:
    st.write("### Additional Maps")
    st.image("https://via.placeholder.com/200x150", caption="Map 1", use_column_width=True)
    st.image("https://via.placeholder.com/200x150", caption="Map 2", use_column_width=True)
