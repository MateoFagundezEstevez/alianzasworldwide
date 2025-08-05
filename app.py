import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Título de la app
st.title("Mapa Interactivo de Alianzas Internacionales")

# Cargar datos
df = pd.read_csv("alianzas.csv")

# Limpiar datos faltantes si es necesario
df = df.dropna(subset=["Latitud", "Longitud"])

# Crear el mapa centrado en coordenadas medias
mapa = folium.Map(location=[0, 0], zoom_start=2)

# Añadir marcadores
for i, row in df.iterrows():
    info_html = f"""
    <b>Nombre:</b> {row['Nombre']}<br>
    <b>País:</b> {row['País']}<br>
    <b>Ciudad:</b> {row['Ciudad']}<br>
    <b>Tipo de Alianza:</b> {row['Tipo Alianza']}<br>
    <b>Año:</b> {row['Año']}<br>
    <b>Descripción:</b> {row['Descripción']}<br>
    <b>Link:</b> <a href="{row['Link Institución']}" target="_blank">Sitio Web</a><br>
    <b>Contacto 1:</b> {row['Contacto 1']}<br>
    <b>Contacto 2:</b> {row['Contacto 2']}
    """

    folium.Marker(
        location=[row['Latitud'], row['Longitud']],
        popup=folium.Popup(info_html, max_width=400),
        tooltip=row['Nombre'],
        icon=folium.Icon(color='blue', icon='briefcase', prefix='fa')
    ).add_to(mapa)

# Mostrar el mapa en Streamlit
folium_static(mapa)
