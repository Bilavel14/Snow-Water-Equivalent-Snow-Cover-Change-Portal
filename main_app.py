# main_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.components.v1 import html
import folium

# -------------------------------
# Basic Page Setup
# -------------------------------
st.set_page_config(
    page_title="SWE & SCC Portal",
    layout="wide"
)

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.title("Filter Options")

data_type = st.sidebar.radio("Select Data Type:", ["SWE", "SCC"])
basin = st.sidebar.selectbox("Select Basin:", ["Indus", "Jhelum", "Chenab", "Kabul", "Swat"])

# -------------------------------
# Title and Selection Display
# -------------------------------
st.title("Himalayan Snow Water & Cover Change Portal")
st.markdown(f"**Selected Data Type:** `{data_type}`")
st.markdown(f"**Selected Basin:** `{basin}`")

# -------------------------------
# Google Drive Links
# -------------------------------
gdrive_links = {
    ("Chenab", "SWE"): "https://drive.google.com/uc?id=1uC965Ie0lj-zNSiqIQVnfIp7OFOi-gKQ",
    ("Chenab", "SCC"): "https://drive.google.com/uc?id=1uC965Ie0lj-zNSiqIQVnfIp7OFOi-gKQ",
    ("Indus", "SCC"): "https://drive.google.com/uc?id=1AEI5EiLR9lpXsHs_RlqKT-HoVy-w-toF",
    ("Jhelum", "SCC"): "https://drive.google.com/uc?id=1QsukwcwcFZZthu1Xrj8dBSTQEFbeTcSo",
    ("Kabul", "SCC"): "https://drive.google.com/uc?id=1zLci-sUJHLCd-dPIeG-Cauibd_ZvmhCf",
    ("Swat", "SCC"): "https://drive.google.com/uc?id=1MYXV5c__ue2hz_rVwGQX5dXR2tY68zXg"
}

# -------------------------------
# Load and Display Data
# -------------------------------
if (basin, data_type) in gdrive_links:
    if data_type == "SWE":
        st.warning("🔧 Work in progress — SWE results will be added soon.")
    else:
        try:
            df = pd.read_csv(gdrive_links[(basin, data_type)])
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['year'] = df['date'].dt.year

            # Dynamic y-column detection
            if 'mean_snow_depth_cm' in df.columns:
                y_column = 'mean_snow_depth_cm'
            elif 'mean_SCA' in df.columns:
                y_column = 'mean_SCA'
            else:
                y_column = df.columns[2]  # fallback

            yearly_avg = df.groupby('year')[y_column].mean().reset_index()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Key Statistics")
                st.metric("Mean", f"{df[y_column].mean():.2f} cm")
                st.metric("Max", f"{df[y_column].max():.2f} cm")
                st.metric("Min", f"{df[y_column].min():.2f} cm")

            with col2:
                st.subheader("📈 Year-wise Snow Cover")
                fig = px.line(
                    yearly_avg,
                    x='year',
                    y=y_column,
                    title=f'{basin} Basin - Avg {y_column} per Year',
                    markers=True,
                    labels={y_column: 'Value (cm)', 'year': 'Year'}
                )
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

# -------------------------------
# Basin AOI Map (Folium)
# -------------------------------
st.subheader("Basin Map (Interactive)")

if basin == "Chenab":
    min_lon, min_lat = 73.5, 32.5
    max_lon, max_lat = 76.0, 34.5
    label = "Chenab Basin AOI"
elif basin == "Indus":
    min_lon, min_lat = 69.0, 27.0
    max_lon, max_lat = 77.5, 37.0
    label = "Indus Basin AOI"
elif basin == "Jhelum":
    min_lon, min_lat = 73.0, 33.5
    max_lon, max_lat = 75.5, 35.5
    label = "Jhelum Basin AOI"
elif basin == "Kabul":
    min_lon, min_lat = 67.5, 32.5
    max_lon, max_lat = 71.5, 36.0
    label = "Kabul Basin AOI"
elif basin == "Swat":
    min_lon, min_lat = 71.0, 34.0
    max_lon, max_lat = 73.0, 36.0
    label = "Swat Basin AOI"
else:
    min_lon = min_lat = max_lon = max_lat = None
    label = None

if label:
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=7, tiles="OpenStreetMap")
    folium.Rectangle(
        bounds=[[min_lat, min_lon], [max_lat, max_lon]],
        color="blue",
        fill=True,
        fill_opacity=0.2,
        tooltip=label
    ).add_to(m)
    html(m._repr_html_(), height=500)
else:
    st.info("AOI Map will be shown here once the geometry is defined.")

# -------------------------------
# Download Buttons Section
# -------------------------------
st.subheader("Download Center")

download_links = {
    "Chenab": "https://drive.google.com/file/d/1uC965Ie0lj-zNSiqIQVnfIp7OFOi-gKQ/view?usp=sharing",
    "Indus": "https://drive.google.com/file/d/1AEI5EiLR9lpXsHs_RlqKT-HoVy-w-toF/view?usp=sharing",
    "Jhelum": "https://drive.google.com/file/d/1QsukwcwcFZZthu1Xrj8dBSTQEFbeTcSo/view?usp=sharing",
    "Kabul": "https://drive.google.com/file/d/1zLci-sUJHLCd-dPIeG-Cauibd_ZvmhCf/view?usp=sharing",
    "Swat": "https://drive.google.com/file/d/1MYXV5c__ue2hz_rVwGQX5dXR2tY68zXg/view?usp=sharing"
}

if basin in download_links:
    st.markdown(f"[📥 Download Source CSV]({download_links[basin]})")

# -------------------------------
# Footer
# -------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by Bilavel Raza | July 2025")
