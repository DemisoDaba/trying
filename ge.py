import streamlit as st
import leafmap.foliumap as leafmap
from datetime import date

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
/* HEADER */
.header {
    background-color: #0a2342;  /* Dark blue */
    color: white;
    padding: 25px;
    text-align: center;
    font-family: 'Arial', sans-serif;
    margin-bottom: 0px;  /* No space below header */
    border-radius: 0px;  /* Remove rounded corners */
}

/* TOP MENU BAR */
.top-menu {
    background-color: #1f77b4;  /* Different from header */
    padding: 15px;
    text-align: center;
    margin-top: 0px;   /* No space above */
    margin-bottom: 20px;
    border-radius: 0px;  /* Remove rounded corners */
}

.top-menu button {
    background-color: #ffffff;  /* Button white */
    color: #1f77b4;            /* Text color matches menu */
    border: none;
    border-radius: 8px;        /* Buttons still slightly rounded */
    padding: 12px 30px;
    font-size: 16px;
    font-weight: bold;
    margin: 0 15px;
    cursor: pointer;
}

.top-menu button:hover {
    background-color: #d0e4f7;  /* Light hover */
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
    border-radius: 10px;  /* Keep map slightly rounded */
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

# LEFT: Filters
with left_col:
    st.write("### Filters")
    region = st.selectbox("Select Region", ["Region A", "Region B", "Region C"])
    dataset = st.selectbox("Select Dataset", ["Dataset 1", "Dataset 2", "Dataset 3"])
    start_date = st.date_input("Start Date", value=date(2025,1,1))
    end_date = st.date_input("End Date", value=date(2025,12,31))
    apply_filter = st.button("Apply Filter")

# CENTER: Map
with center_col:
    st.write("### Map | Imagery Viewer")
    m = leafmap.Map(center=[0,0], zoom=2)
    m.add_basemap("HYBRID")
    m.to_streamlit(height=650)

# RIGHT: Additional Maps
with right_col:
    st.write("### Additional Maps")
    st.image("https://via.placeholder.com/200x150", caption="Map 1", use_column_width=True)
    st.image("https://via.placeholder.com/200x150", caption="Map 2", use_column_width=True)
