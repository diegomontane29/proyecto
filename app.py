import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

st.title("📊 SBS - Banca Múltiple (Robusto)")

FILE = "sbs_data.parquet"

# -----------------------------
# 🧠 1. CREAR DATA SI NO EXISTE
# -----------------------------
if not os.path.exists(FILE):

    st.info("📦 No se encontró base de datos. Generando dataset inicial...")

    data = [
        ["Interbank", "2024-01", "Liquidez", "MN", 38.52],
        ["Interbank", "2024-02", "Liquidez", "MN", 37.80],
        ["BCP", "2024-01", "Liquidez", "MN", 42.10],
        ["BBVA", "2024-01", "Liquidez", "MN", 35.20],

        ["Interbank", "2024-01", "Liquidez", "ME", 12.40],
        ["BCP", "2024-01", "Liquidez", "ME", 13.10],
        ["BBVA", "2024-01", "Liquidez", "ME", 11.90],
    ]

    df_init = pd.DataFrame(data, columns=[
        "banco", "fecha", "indicador", "subindicador", "valor"
    ])

    df_init.to_parquet(FILE, index=False)

# -----------------------------
# 📥 2. CARGAR DATOS
# -----------------------------
df = pd.read_parquet(FILE)

# -----------------------------
# 🎛 3. FILTROS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    banco = st.selectbox("Banco", sorted(df["banco"].unique()))

with col2:
    indicador = st.selectbox("Indicador", sorted(df["indicador"].unique()))

with col3:
    sub = st.multiselect(
        "Subindicador",
        df["subindicador"].unique(),
        default=df["subindicador"].unique()
    )

fecha = st.selectbox("Fecha", sorted(df["fecha"].unique()))

# -----------------------------
# 🔍 4. CONSULTA
# -----------------------------
df_f = df[
    (df["banco"] == banco) &
    (df["indicador"] == indicador) &
    (df["subindicador"].isin(sub)) &
    (df["fecha"] <= fecha)
]

# -----------------------------
# 📊 5. RESULTADOS
# -----------------------------
st.subheader("📋 Datos")

st.dataframe(df_f, use_container_width=True)

st.subheader("📈 Evolución")

if not df_f.empty:
    chart = df_f.groupby("fecha")["valor"].mean()
    st.line_chart(chart)
else:
    st.warning("Sin datos disponibles")
