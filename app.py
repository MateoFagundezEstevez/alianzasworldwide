import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Configuración de la página
st.set_page_config(page_title="Mapa de Alianzas Internacionales", layout="wide")
st.title("🌐 Mapa Interactivo de Alianzas Internacionales")

# Cargar datos desde archivo CSV
df = pd.read_csv("alianzas.csv")
df = df.dropna(subset=["Latitud", "Longitud"])

# Sidebar con filtros
st.sidebar.header("🔍 Filtrar por:")

paises = df['País'].dropna().unique().tolist()
anios = sorted(df['Año'].dropna().unique().tolist())

pais_sel = st.sidebar.multiselect("País", opciones=paises, default=paises)
anio_sel = st.sidebar.multiselect("Año", opciones=anios, default=anios)

# Filtrar datos según selección
df_filtrado = df[(df['País'].isin(pais_sel)) & (df['Año'].isin(anio_sel))]

# Centrar mapa en promedio de coordenadas
lat_media = df_filtrado["Latitud"].mean()
lon_media = df_filtrado["Longitud"].mean()

# Crear mapa con estilo moderno
mapa = folium.Map(location=[lat_media, lon_media], zoom_start=2, tiles="CartoDB dark_matter")

# Crear cluster de marcadores
marker_cluster = MarkerCluster().add_to(mapa)

# Añadir marcadores al cluster
for i, row in df_filtrado.iterrows():
    popup_html = f"""
    <div style="width: 250px;">
        <strong>{row['Nombre']}</strong><br>
        📍 <b>{row['Ciudad']}, {row['País']}</b><br>
        📅 <b>Año:</b> {row['Año']}<br>
        🤝 <b>Tipo:</b> {row['Tipo Alianza']}<br><br>
        {row['Descripción']}<br><br>
        🔗 <a href="{row['Link Institución']}" target="_blank">Sitio Web</a><br><br>
        ✉️ <b>Contacto 1:</b> {row['Contacto 1']}<br>
        ✉️ <b>Contacto 2:</b> {row['Contacto 2']}
    </div>
    """
    folium.Marker(
        location=[row['Latitud'], row['Longitud']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row['Nombre'],
        icon=folium.Icon(color='green', icon='globe', prefix='fa')
    ).add_to(marker_cluster)

# Mostrar mapa en la app
folium_static(mapa, width=1200, height=650)

# Mostrar cantidad de alianzas activas filtradas
st.markdown(f"🔎 <b>{len(df_filtrado)} alianzas</b> encontradas con los filtros seleccionados.", unsafe_allow_html=True)
