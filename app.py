import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# 📥 cargar datos
df = pd.read_parquet("data/datos_sbs.parquet")

st.title("📊 Dashboard SBS - Sistema Financiero Peruano")

# 🧠 NORMALIZA (ajusta según columnas reales)
# IMPORTANTE: adapta esto a tu Excel real
df.columns = df.columns.str.lower()

# Sidebar filtros
st.sidebar.header("Filtros")

# Ajusta nombres reales de columnas
empresa_col = "empresa" if "empresa" in df.columns else df.columns[0]

empresas = st.sidebar.multiselect(
    "Empresas",
    df[empresa_col].dropna().unique()
)

fecha_max = st.sidebar.selectbox(
    "Mes hasta",
    sorted(df["fecha"].unique())
)

# Filtrado acumulado
df_filtrado = df[
    (df[empresa_col].isin(empresas)) &
    (df["fecha"] <= fecha_max)
]

# ⚠️ Si aún no tienes tipo_riesgo, crea uno dummy
if "tipo_riesgo" not in df_filtrado.columns:
    df_filtrado["tipo_riesgo"] = "general"

# Separación
liq = df_filtrado[df_filtrado["tipo_riesgo"] == "liquidez"]
cred = df_filtrado[df_filtrado["tipo_riesgo"] == "credito"]
merc = df_filtrado[df_filtrado["tipo_riesgo"] == "mercado"]

# 📊 Layout
col1, col2, col3 = st.columns(3)

def plot(df, titulo):
    if df.empty:
        st.write("Sin datos")
        return
    
    try:
        pivot = df.pivot(index="fecha", columns=empresa_col, values=df.columns[-1])
        st.line_chart(pivot)
    except:
        st.write("Error en gráfico")

with col1:
    st.subheader("Liquidez")
    plot(liq, "Liquidez")

with col2:
    st.subheader("Crédito")
    plot(cred, "Crédito")

with col3:
    st.subheader("Mercado")
    plot(merc, "Mercado")