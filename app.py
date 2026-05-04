import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(layout="wide")

st.title("📊 SBS - Banca Múltiple (Perú)")

# -----------------------------
# 📊 DATA (base inicial)
# -----------------------------
df = pd.DataFrame({
    "empresa": ["Banco A", "Banco B", "Banco C", "Banco A", "Banco B", "Banco C"],
    "fecha": ["2024-01", "2024-01", "2024-01", "2024-02", "2024-02", "2024-02"],
    "liquidez": [1.2, 1.5, 1.1, 1.3, 1.6, 1.2],
    "credito": [2.1, 2.3, 2.0, 2.2, 2.4, 2.1],
    "mercado": [0.8, 1.0, 0.9, 0.85, 1.05, 0.95]
})

# -----------------------------
# 🎛 SIDEBAR FILTROS
# -----------------------------
st.sidebar.header("Filtros")

empresas = st.sidebar.multiselect(
    "Banco",
    df["empresa"].unique(),
    default=df["empresa"].unique()
)

mes = st.sidebar.selectbox(
    "Mes",
    sorted(df["fecha"].unique())
)

indicador = st.sidebar.selectbox(
    "Indicador",
    ["liquidez", "credito", "mercado"]
)

# -----------------------------
# 🔍 FILTRADO
# -----------------------------
df_filtrado = df[
    (df["empresa"].isin(empresas)) &
    (df["fecha"] <= mes)
]

# -----------------------------
# 📊 VISUALIZACIÓN
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Datos")
    st.dataframe(df_filtrado)

with col2:
    st.subheader("📈 Evolución")

    graf = df_filtrado.groupby("fecha")[indicador].mean()
    st.line_chart(graf)

# -----------------------------
# 📥 DESCARGA
# -----------------------------
st.subheader("⬇ Descargar datos")

def convertir_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="SBS")
    return output.getvalue()

col3, col4 = st.columns(2)

with col3:
    csv = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Descargar CSV",
        csv,
        "sbs_banca_multiple.csv",
        "text/csv"
    )

with col4:
    excel = convertir_excel(df_filtrado)
    st.download_button(
        "Descargar Excel",
        excel,
        "sbs_banca_multiple.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
