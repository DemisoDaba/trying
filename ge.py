import streamlit as st
import leafmap.foliumap as leafmap
from datetime import date
import ee

# ===============================
# INITIALIZE EARTH ENGINE
# ===============================
try:
    ee.Initialize(project='ee-dforengine2')
except Exception:
    ee.Authenticate()  # opens browser to log in your Google account
    ee.Initialize(project='ee-dforengine2')

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Geospatial Analysis",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ===============================
# CUSTOM CSS (unchanged)
# ===============================
st.markdown("""
<style>
/* HEADER */
.header {
    background-color: #0a2342;  /* Dark blue */
    color: white;
    padding: 25px;
    text-align: center;
    font-family: 'Arial', sans-serif;
    margin-bottom: 0px;
    border-radius: 0px;
}

/* TOP MENU BAR */
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

/* MINIMIZE COLUMN GAP */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
}

/* MAP SPACE */
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
    dataset = st.selectbox("Select Dataset", ["Sentinel-2 NDVI"])
    start_date = st.date_input("Start Date", value=date(2025,1,1))
    end_date = st.date_input("End Date", value=date(2025,12,31))
    apply_filter = st.button("Apply Filter")

# -------------------------------
# CENTER: Map & NDVI
# -------------------------------
with center_col:
    st.write("### Map | Imagery Viewer")
    
    # Default map
    m = leafmap.Map(center=[9.25, 38.75], zoom=6)
    m.add_basemap("HYBRID")
    
    if apply_filter and dataset == "Sentinel-2 NDVI":
        # Define Region A bounding box (min_lon, min_lat, max_lon, max_lat)
        regions = {
            "Region A": [38.5, 9.0, 39.0, 9.5],
            "Region B": [39.0, 9.5, 39.5, 10.0],
            "Region C": [38.0, 8.5, 38.5, 9.0]
        }
        min_lon, min_lat, max_lon, max_lat = regions[region_name]
        region_geom = ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])
        
        # Filter Sentinel-2
        s2 = (ee.ImageCollection("COPERNICUS/S2_SR")
              .filterBounds(region_geom)
              .filterDate(str(start_date), str(end_date))
              .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 30)))
        
        # Median image & NDVI
        image = s2.median().clip(region_geom)
        ndvi = image.normalizedDifference(["B8","B4"]).rename("NDVI")
        
        # NDVI visualization
        vis_params = {"min": -1, "max": 1, "palette":["purple","blue","white","green","darkgreen"]}
        m.addLayer(ndvi, vis_params, "NDVI")
        
        # Zoom to region
        m.setCenter((min_lon+max_lon)/2, (min_lat+max_lat)/2, 12)
    
    m.to_streamlit(height=650)

# -------------------------------
# RIGHT: Additional Maps
# -------------------------------
with right_col:
    st.write("### Additional Maps")
    st.image("https://via.placeholder.com/200x150", caption="Map 1", use_column_width=True)
    st.image("https://via.placeholder.com/200x150", caption="Map 2", use_column_width=True)
