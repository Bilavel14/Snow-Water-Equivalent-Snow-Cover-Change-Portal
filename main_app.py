# SWE & SCC Portal Streamlit App
# Author: Bilavel Raza | July 2025

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.components.v1 import html
import folium

# =============================
# SECTION: Basic Page Setup
# =============================
st.set_page_config(
    page_title="SWE & SCC Portal",
    layout="wide"
)

# =============================
# SECTION: Sidebar Controls
# =============================
st.sidebar.title("Filter Options")
data_type = st.sidebar.radio("Select Data Type:", ["SWE", "SCC"])
basin = st.sidebar.selectbox("Select Basin:", ["Indus", "Jhelum", "Chenab", "Kabul", "Swat"])

# =============================
# SECTION: Title Display
# =============================
st.title("Himalayan Snow Water & Cover Change Portal")
st.markdown(f"**Selected Data Type:** `{data_type}`")
st.markdown(f"**Selected Basin:** `{basin}`")

# =============================
# SECTION: Data Links
# =============================
gdrive_links = {
    ("Chenab", "SWE"): "https://drive.google.com/uc?id=1uC965Ie0lj-zNSiqIQVnfIp7OFOi-gKQ",
    ("Chenab", "SCC"): "https://drive.google.com/uc?id=1uC965Ie0lj-zNSiqIQVnfIp7OFOi-gKQ",
    ("Indus", "SCC"): "https://drive.google.com/uc?id=1AEI5EiLR9lpXsHs_RlqKT-HoVy-w-toF",
    ("Jhelum", "SCC"): "https://drive.google.com/uc?id=1QsukwcwcFZZthu1Xrj8dBSTQEFbeTcSo",
    ("Kabul", "SCC"): "https://drive.google.com/uc?id=1zLci-sUJHLCd-dPIeG-Cauibd_ZvmhCf",
    ("Swat", "SCC"): "https://drive.google.com/uc?id=1MYXV5c__ue2hz_rVwGQX5dXR2tY68zXg"
}

# =============================
# SECTION: Load & Display Data
# =============================
if (basin, data_type) in gdrive_links:
    if data_type == "SWE":
        st.warning("🔧 Work in progress — SWE results will be added soon.")
    else:
        try:
            df = pd.read_csv(gdrive_links[(basin, data_type)])
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['year'] = df['date'].dt.year

            y_column = 'mean_SCA' if 'mean_SCA' in df.columns else df.columns[2]
            yearly_avg = df.groupby('year')[y_column].mean().reset_index()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("\U0001F4CA Key Statistics")
                st.metric("Mean", f"{df[y_column].mean():.2f} cm")
                st.metric("Max", f"{df[y_column].max():.2f} cm")
                non_zero_min = df[df[y_column] > 0][y_column].min()
                st.metric("Min (non-zero)", f"{non_zero_min:.2f} cm")

            with col2:
                st.subheader("\U0001F4C8 Year-wise Snow Cover")
                fig = px.line(yearly_avg, x='year', y=y_column, title=f'{basin} Basin - Avg {y_column} per Year', markers=True)
                fig.update_layout(template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Failed to load or process data: {e}")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Key Statistics")
        st.info("Statistics (mean, max, anomaly) will appear here.")
    with col2:
        st.subheader("Time Series Plot")
        st.info("Graph will be shown here once data is connected.")

# =============================
# SECTION: 3D Map View Button
# =============================
basin_3d_links = {
    "Chenab": "https://docs.mapbox.com/mapbox-gl-js/example/terrain/",
    "Indus": "https://docs.mapbox.com/mapbox-gl-js/example/terrain/",
    "Jhelum": "https://docs.mapbox.com/mapbox-gl-js/example/terrain/",
    "Kabul": "https://docs.mapbox.com/mapbox-gl-js/example/terrain/",
    "Swat": "https://docs.mapbox.com/mapbox-gl-js/example/terrain/"
}

col3d, _ = st.columns([1, 9])
with col3d:
    if st.button("\U0001F310 View 3D Map"):
        link = basin_3d_links.get(basin)
        if link:
            html(f"<script>window.open('{link}', '_blank')</script>", height=0)

# =============================
# SECTION: Basin AOI Map (Folium)
# =============================
coords = {
    "Chenab": (73.5, 32.5, 76.0, 34.5),
    "Indus": (69.0, 27.0, 77.5, 37.0),
    "Jhelum": (73.0, 33.5, 75.5, 35.5),
    "Kabul": (67.5, 32.5, 71.5, 36.0),
    "Swat": (71.0, 34.0, 73.0, 36.0)
}

if basin in coords:
    min_lon, min_lat, max_lon, max_lat = coords[basin]
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=7,
                   tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
                   attr='CartoDB Positron')
    folium.Rectangle(
        bounds=[[min_lat, min_lon], [max_lat, max_lon]],
        color="blue",
        fill=True,
        fill_opacity=0.2,
        tooltip=f"{basin} Basin AOI"
    ).add_to(m)
    html(m._repr_html_(), height=500)
else:
    st.info("AOI Map will be shown here once the geometry is defined.")

# =============================
# SECTION: Download Center
# =============================
download_links = {
    "Chenab": "https://drive.google.com/file/d/1uC965Ie0lj-zNSiqIQVnfIp7OFOi-gKQ/view?usp=sharing",
    "Indus": "https://drive.google.com/file/d/1AEI5EiLR9lpXsHs_RlqKT-HoVy-w-toF/view?usp=sharing",
    "Jhelum": "https://drive.google.com/file/d/1QsukwcwcFZZthu1Xrj8dBSTQEFbeTcSo/view?usp=sharing",
    "Kabul": "https://drive.google.com/file/d/1zLci-sUJHLCd-dPIeG-Cauibd_ZvmhCf/view?usp=sharing",
    "Swat": "https://drive.google.com/file/d/1MYXV5c__ue2hz_rVwGQX5dXR2tY68zXg/view?usp=sharing"
}

if basin in download_links:
    st.markdown(f"[\U0001F4E5 Download Source CSV]({download_links[basin]})")

# =============================
# SECTION: Footer
# =============================
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by Bilavel Raza | July 2025")
