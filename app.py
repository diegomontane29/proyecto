import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 SBS - Banca Múltiple Perú")

# -----------------------------
# 🏦 DATA (SIMULADA REALISTA)
# -----------------------------
df = pd.DataFrame({
    "banco": [
        "BCP", "BCP", "BCP",
        "BBVA", "BBVA", "BBVA",
        "Interbank", "Interbank", "Interbank"
    ],
    "fecha": [
        "2024-01", "2024-01", "2024-01",
        "2024-01", "2024-01", "2024-01",
        "2024-01", "2024-01", "2024-01"
    ],
    "categoria_riesgo": [
        "Liquidez", "Liquidez", "Liquidez",
        "Liquidez", "Liquidez", "Liquidez",
        "Liquidez", "Liquidez", "Liquidez"
    ],
    "subindicador": [
        "MN", "ME", "Cobertura",
        "MN", "ME", "Cobertura",
        "MN", "ME", "Cobertura"
    ],
    "valor": [1.2, 0.9, 1.5, 1.3, 1.0, 1.6, 1.1, 0.8, 1.4]
})

# -----------------------------
# 🎛 FILTROS
# -----------------------------
st.sidebar.header("Filtros")

banco = st.sidebar.multiselect(
    "Banco",
    df["banco"].unique(),
    default=df["banco"].unique()
)

riesgo = st.sidebar.selectbox(
    "Tipo de riesgo",
    df["categoria_riesgo"].unique()
)

# 🔥 subindicadores dinámicos
sub_df = df[df["categoria_riesgo"] == riesgo]
subindicador = st.sidebar.multiselect(
    "Subindicador",
    sub_df["subindicador"].unique(),
    default=sub_df["subindicador"].unique()
)

# -----------------------------
# 🔍 FILTRO FINAL
# -----------------------------
df_filtrado = df[
    (df["banco"].isin(banco)) &
    (df["categoria_riesgo"] == riesgo) &
    (df["subindicador"].isin(subindicador))
]

# -----------------------------
# 📊 VISUALIZACIÓN
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Datos por banco")
    st.dataframe(df_filtrado)

with col2:
    st.subheader("📈 Evolución")

    graf = df_filtrado.groupby("banco")["valor"].mean()
    st.bar_chart(graf)
