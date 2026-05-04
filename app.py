import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 Dashboard SBS - Sistema Financiero Peruano")

# 🔥 DATOS MOCK (reemplaza luego por ETL real)
data = {
    "empresa": ["A", "A", "B", "B"],
    "fecha": ["2024-01", "2024-02", "2024-01", "2024-02"],
    "liquidez": [1.2, 1.3, 2.1, 2.2],
    "credito": [3.1, 3.2, 2.9, 3.0],
    "mercado": [0.8, 0.9, 1.1, 1.3],
}

df = pd.DataFrame(data)

# filtros
empresa = st.multiselect("Empresa", df["empresa"].unique())
if empresa:
    df = df[df["empresa"].isin(empresa)]

st.dataframe(df)

# gráficos
col = st.selectbox("Indicador", ["liquidez", "credito", "mercado"])
st.line_chart(df.groupby("fecha")[col].mean())
