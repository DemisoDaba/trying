import streamlit as st
import leafmap.foliumap as leafmap
import os
import tempfile

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
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tif') as tmp_file:
            tmp_file.write(uploaded_file.read())
            raster_path = tmp_file.name
    else:
        default_file = "sbc.tiff"
        if os.path.exists(default_file):
            raster_path = default_file

    if apply_filter and raster_path is not None:
        try:
            # Method 1: Try using localtileserver (requires localtileserver package)
            m.add_local_tile(raster_path, layer_name="SBC Raster")
            m.zoom_to_layer("SBC Raster")
            
        except Exception as e:
            st.error(f"Error with localtileserver: {str(e)}")
            st.info("Trying alternative raster loading method...")
            
            try:
                # Method 2: Use add_geotiff if available
                m.add_geotiff(raster_path, band=[1,2,3], layer_name="SBC Raster")
                m.zoom_to_layer("SBC Raster")
                
            except Exception as e2:
                st.error(f"Error with add_geotiff: {str(e2)}")
                
                try:
                    # Method 3: Use rasterio directly with folium
                    import rasterio
                    from rasterio.plot import show
                    import folium
                    from folium.raster_layers import ImageOverlay
                    import numpy as np
                    
                    # Open raster with rasterio
                    with rasterio.open(raster_path) as src:
                        # Read first band (or RGB bands)
                        if src.count >= 3:
                            # For RGB images
                            band1 = src.read(1)
                            band2 = src.read(2)
                            band3 = src.read(3)
                            img_array = np.dstack((band1, band2, band3))
                        else:
                            # For single band
                            img_array = src.read(1)
                        
                        # Normalize for display
                        img_array = (img_array - img_array.min()) / (img_array.max() - img_array.min())
                        img_array = (img_array * 255).astype(np.uint8)
                        
                        # Get bounds
                        bounds = [
                            [src.bounds.bottom, src.bounds.left],
                            [src.bounds.top, src.bounds.right]
                        ]
                        
                        # Add as image overlay
                        img_overlay = ImageOverlay(
                            img_array,
                            bounds=bounds,
                            name="SBC Raster",
                            opacity=0.7,
                            interactive=True,
                        )
                        img_overlay.add_to(m)
                        
                        m.fit_bounds(bounds)
                        
                except Exception as e3:
                    st.error(f"All raster loading methods failed: {str(e3)}")
                    st.info("Please check if your TIFF file is a valid GeoTIFF file.")
            
        finally:
            # Clean up temporary file if it was created
            if uploaded_file is not None and os.path.exists(raster_path):
                os.unlink(raster_path)

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
