import streamlit as st
import leafmap.foliumap as leafmap
from datetime import date
import rasterio
import os

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Geospatial Analysis",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ===============================
# CUSTOM CSS
# ===============================
st.markdown("""
<style>
.header {
    background-color: #0a2342;
    color: white;
    padding: 25px;
    text-align: center;
    font-family: 'Arial', sans-serif;
    margin-bottom: 0px;
    border-radius: 0px;
}
.top-menu {
    background-color: #1f77b4;
    padding: 15px;
    text-align: center;
    margin-top: 0px;
    margin-bottom: 20px;
    border-radius: 0px;
}
.top-menu button {
    background-color: #ffffff;
    color: #1f77b4;
    border: none;
    border-radius: 8px;
    padding: 12px 30px;
    font-size: 16px;
    font-weight: bold;
    margin: 0 15px;
    cursor: pointer;
}
.top-menu button:hover {
    background-color: #d0e4f7;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
}
.element-container iframe {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# HEADER
# ===============================
st.markdown("<div class='header'><h1>Geospatial Analysis</h1></div>", unsafe_allow_html=True)

# ===============================
# TOP MENU BAR
# ===============================
st.markdown("""
<div class='top-menu'>
    <button>Raster</button>
    <button>Vector</button>
    <button>3D Terrain</button>
</div>
""", unsafe_allow_html=True)

# ===============================
# MAIN LAYOUT
# ===============================
left_col, center_col, right_col = st.columns([1,4,1], gap="small")

# -------------------------------
# LEFT: Filters
# -------------------------------
with left_col:
    st.write("### Filters")
    region_name = st.selectbox("Select Region", ["Region A", "Region B", "Region C"])
    uploaded_file = st.file_uploader("Upload SBC TIFF file", type=["tif", "tiff"])
    apply_filter = st.button("Apply Filter")

# -------------------------------
# CENTER: Map
# -------------------------------
with center_col:
    st.write("### Map | Imagery Viewer")
    m = leafmap.Map(center=[9.25, 38.75], zoom=6)
    m.add_basemap("HYBRID")

    # Determine raster path
    raster_path = None
    if uploaded_file is not None:
        raster_path = uploaded_file
    else:
        default_file = "sbc.tiff"
        if os.path.exists(default_file):
            raster_path = default_file

    if apply_filter and raster_path is not None:
        # Read raster with rasterio
        with rasterio.open(raster_path) as src:
            array = src.read(1)
            bounds = src.bounds

        # Add raster using add_raster (works in all versions)
        m.add_raster(
            array,
            bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
            colormap="viridis",
            layer_name="SBC Raster"
        )

        # Zoom to raster
        m.set_center((bounds.left + bounds.right)/2, (bounds.bottom + bounds.top)/2, 10)

    elif apply_filter and raster_path is None:
        st.warning("No raster file found. Please upload a SBC TIFF file.")

    m.to_streamlit(height=650)

# -------------------------------
# RIGHT: Additional Maps
# -------------------------------
with right_col:
    st.write("### Additional Maps")
    st.image("https://via.placeholder.com/200x150", caption="Map 1", use_column_width=True)
    st.image("https://via.placeholder.com/200x150", caption="Map 2", use_column_width=True)
