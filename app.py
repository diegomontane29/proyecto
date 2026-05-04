import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# 📥 cargar datos
df = pd.read_parquet("datos_sbs.parquet")

st.title("📊 Dashboard SBS - Sistema Financiero Peruano")

# 🧠 normalizar columnas
df.columns = df.columns.str.lower()

# 🔍 filtros
st.sidebar.header("Filtros")

# empresa (si existe)
if "empresa" in df.columns:
    empresas = st.sidebar.multiselect(
        "Empresas",
        df["empresa"].dropna().unique()
    )
    if empresas:
        df = df[df["empresa"].isin(empresas)]

# mes
if "fecha" in df.columns:
    fecha_max = st.sidebar.selectbox(
        "Mes máximo",
        sorted(df["fecha"].unique())
    )
    df = df[df["fecha"] <= fecha_max]

# 📊 vista datos
st.subheader("Vista de datos")
st.dataframe(df.head())

# 📈 gráficos automáticos
num_cols = df.select_dtypes(include="number").columns

if len(num_cols) > 0:
    indicador = st.selectbox("Indicador", num_cols)
    st.line_chart(df.groupby("fecha")[indicador].mean())
else:
    st.warning("No hay columnas numéricas para graficar")
