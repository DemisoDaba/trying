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
        margin-bottom: 10px;
    }

    /* TOP MENU BAR */
    .top-menu {
        background-color: #0a2342;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }

    .top-menu button {
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: bold;
        margin: 0 15px;
        cursor: pointer;
    }

    .top-menu button:hover {
        background-color: #3a9ad9;
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
# TOP MENU BAR
# ===============================
st.markdown(
    """
    <div class='top-menu'>
        <button>Raster</button>
        <button>Vector</button>
        <button>3D Terrain</button>
    </div>
    """,
    unsafe_allow_html=True,
)

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
center_col, right_col = st.columns([4,1], gap="large")

# CENTER: Map / Satellite imagery
with center_col:
    st.write("### Map / Imagery Viewer")
    m = leafmap.Map(center=[0,0], zoom=2)
    m.add_basemap("HYBRID")
    m.to_streamlit(height=650)

# RIGHT: Additional Maps / Layers
with right_col:
    st.write("### Additional Maps")
    st.image("https://via.placeholder.com/200x150", caption="Map 1", use_column_width=True)
    st.image("https://via.placeholder.com/200x150", caption="Map 2", use_column_width=True)
