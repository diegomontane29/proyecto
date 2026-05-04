import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 SBS - Banca Múltiple Perú")

# cargar datos del ETL
df = pd.read_parquet("sbs_data.parquet")

# -----------------------
# FILTROS
# -----------------------
col1, col2 = st.columns(2)

with col1:
    banco = st.selectbox("Banco", df["banco"].unique())

with col2:
    fecha = st.selectbox("Fecha", sorted(df["fecha"].unique()))

indicador = st.selectbox("Indicador", df["indicador"].unique())

sub = st.multiselect(
    "Subindicador",
    df["subindicador"].unique(),
    default=df["subindicador"].unique()
)

# -----------------------
# FILTRO REAL
# -----------------------
df_f = df[
    (df["banco"] == banco) &
    (df["fecha"] <= fecha) &
    (df["indicador"] == indicador) &
    (df["subindicador"].isin(sub))
]

# -----------------------
# RESULTADOS
# -----------------------
st.subheader("📋 Datos")

st.dataframe(df_f)

st.subheader("📈 Evolución")

if not df_f.empty:
    chart = df_f.groupby("fecha")["valor"].mean()
    st.line_chart(chart)
else:
    st.warning("Sin datos para esta selección")
