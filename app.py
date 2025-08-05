import streamlit as st
import pandas as pd

# Título
st.title("Alianzas Internacionales")

# Cargar datos
df = pd.read_csv("alianzas.csv")

# Eliminar filas vacías y asegurar tipos de datos
df = df.dropna(subset=['País', 'Año'])
df['País'] = df['País'].astype(str)
df['Año'] = df['Año'].astype(str)

# Obtener listas únicas para los filtros
paises = sorted(df['País'].unique().tolist())
anios = sorted(df['Año'].unique().tolist())

# Filtros en la barra lateral
st.sidebar.header("Filtros")
pais_sel = st.sidebar.multiselect("País", options=paises, default=paises)
anio_sel = st.sidebar.multiselect("Año", options=anios, default=anios)

# Filtrar DataFrame según selección
df_filtrado = df[df['País'].isin(pais_sel) & df['Año'].isin(anio_sel)]

# Mostrar resultados
st.subheader("Resultados filtrados")
st.write(f"Se encontraron {len(df_filtrado)} registros.")
st.dataframe(df_filtrado)

# Descargar resultados
st.download_button(
    label="📥 Descargar resultados filtrados",
    data=df_filtrado.to_csv(index=False),
    file_name="alianzas_filtradas.csv",
    mime="text/csv"
)

