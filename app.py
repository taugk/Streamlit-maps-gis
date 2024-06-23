import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Inisialisasi koordinat tengah peta
latitude = -3.539241
longitude = 118.941828

def display_map():
    # Membuat peta dasar menggunakan folium
    map = folium.Map(
        location=[latitude, longitude],
        zoom_start=14,  # Perbesar peta dengan menaikkan zoom_start
        scrollWheelZoom=False,
    )

    # Menggunakan GeoJSON sebagai data geografis (contoh)
    geo_data = "banggae.json"
    
    # Menggunakan data CSV untuk menampilkan informasi
    data_kepadatan = pd.read_csv("data_kepadatan_penduduk.csv")
    data_curah_hujan = pd.read_csv("data_curah_hujan.csv")
    
    # Drop NaN values in Latitude and Longitude columns
    data_curah_hujan = data_curah_hujan.dropna(subset=['Latitude', 'Longitude'])

    # Judul aplikasi Streamlit
    st.title("Kepadatan Penduduk dan Curah Hujan - Banggae, Majene, Sulawesi Barat")

    # Membuat choropleth map untuk kepadatan penduduk
    choropleth_kepadatan = folium.Choropleth(
        geo_data=geo_data,
        data=data_kepadatan,
        columns=["DESA", "KEPADATAN"],
        key_on="feature.properties.DESA",
        fill_color="YlGn",  # Mengubah ke skala warna Kuning-Hijau
        fill_opacity=0.7,  # Mengurangi opacity untuk peta dasar
        line_opacity=0.2,  # Mengurangi opacity garis batas
        threshold_scale=[0, 3000, 6000, 9000, 12000],
        legend_name="Kepadatan Penduduk",  # Judul legenda untuk choropleth map
    ).add_to(map)

    # Menambahkan tooltip yang informatif untuk kepadatan penduduk
    choropleth_kepadatan.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=["DESA", "KEPADATAN"],
            aliases=["Desa:", "Kepadatan Penduduk:"],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )

    # Menambahkan lapisan Marker Cluster untuk curah hujan
    marker_cluster = MarkerCluster().add_to(map)
    
    # Menambahkan marker untuk setiap data curah hujan
    for idx, row in data_curah_hujan.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"Curah Hujan: {row['Curah Hujan (mm)']} mm",
            icon=folium.Icon(color='blue', icon='cloud'),
        ).add_to(marker_cluster)

    # Menampilkan peta menggunakan streamlit-folium
    folium_static(map, width=800, height=800)  # Menentukan ukuran peta yang lebih besar

    # Membagi layout untuk legenda
    col1, col2 = st.columns(2)

    # Menampilkan legenda untuk kepadatan penduduk di kolom pertama
    with col1:
        st.subheader("Legenda Kepadatan Penduduk:")
        st.dataframe(data_kepadatan[['DESA', 'KEPADATAN']].set_index('DESA'))

    # Menampilkan legenda untuk curah hujan di kolom kedua
    with col2:
        st.subheader("Legenda Curah Hujan:")
        st.dataframe(data_curah_hujan[['Latitude', 'Longitude', 'Curah Hujan (mm)']].set_index(['Latitude', 'Longitude']))

# Memanggil fungsi untuk menampilkan peta dan legenda
display_map()
