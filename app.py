import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 SBS - Sistema Bancario Perú")

# cargar dataset consolidado
df = pd.read_parquet("sbs_data.parquet")

df.columns = df.columns.str.lower().str.strip()

# -------------------------
# FILTROS
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    banco = st.selectbox("Banco", sorted(df["banco"].unique()))

df_b = df[df["banco"] == banco]

with col2:
    indicador = st.selectbox("Indicador", df_b["indicador"].unique())

df_i = df_b[df_b["indicador"] == indicador]

with col3:
    sub = st.selectbox("Subindicador", df_i["subindicador"].unique())

df_f = df_i[df_i["subindicador"] == sub]

# -------------------------
# FECHA
# -------------------------
df_f["fecha"] = pd.to_datetime(df_f["fecha"])

df_f = df_f.sort_values("fecha")

df_f = df_f[df_f["fecha"] >= df_f["fecha"].max() - pd.DateOffset(months=60)]

# -------------------------
# GRÁFICO
# -------------------------
st.subheader("📈 Evolución últimos 60 meses")

chart = df_f.groupby(df_f["fecha"].dt.to_period("M"))["valor"].mean()
chart.index = chart.index.astype(str)

st.line_chart(chart)

# -------------------------
# TABLA
# -------------------------
st.subheader("📋 Datos")
st.dataframe(df_f, use_container_width=True)

# -------------------------
# DESCARGA
# -------------------------
st.subheader("⬇️ Descargar datos")

csv = df_f.to_csv(index=False).encode("utf-8")

st.download_button(
    "Descargar CSV",
    data=csv,
    file_name="sbs_banco.csv",
    mime="text/csv"
)
