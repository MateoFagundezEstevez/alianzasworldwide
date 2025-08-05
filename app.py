import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Configuración de la página
st.set_page_config(page_title="Mapa de Alianzas Internacionales", layout="wide")
st.title("🌍 Mapa Interactivo de Alianzas Internacionales")

# Cargar datos
df = pd.read_csv("alianzas.csv")
df = df.dropna(subset=["Latitud", "Longitud"])

# Selección de vista
modo_agrupado = st.checkbox("Ver marcadores agrupados", value=True)

# Crear mapa
mapa = folium.Map(location=[df["Latitud"].mean(), df["Longitud"].mean()],
                  zoom_start=2,
                  tiles="CartoDB positron")

if modo_agrupado:
    marker_cluster = MarkerCluster().add_to(mapa)

for _, row in df.iterrows():
    html = f"""
    <div style="font-size: 14px;">
        <strong>🏛 {row['Nombre']}</strong><br>
        <b>📍 País:</b> {row['País']}<br>
        <b>🏙 Ciudad:</b> {row['Ciudad']}<br>
        <b>🤝 Tipo:</b> {row['Tipo Alianza']}<br>
        <b>📅 Año:</b> {row['Año']}<br>
        <b>📝 Descripción:</b> {row['Descripción']}<br>
        <b>🌐 Link:</b> <a href="{row['Link Institución']}" target="_blank">Sitio Web</a><br>
        <b>📧 Contacto 1:</b> {row['Contacto 1']}<br>
        <b>📞 Contacto 2:</b> {row['Contacto 2']}
    </div>
    """

    marker = folium.Marker(
        location=[row["Latitud"], row["Longitud"]],
        popup=folium.Popup(html, max_width=300),
        tooltip=row["Nombre"],
        icon=folium.Icon(color="cadetblue", icon="globe", prefix="fa")
    )

    if modo_agrupado:
        marker.add_to(marker_cluster)
    else:
        marker.add_to(mapa)

# Mostrar mapa
folium_static(mapa, width=1200, height=700)
