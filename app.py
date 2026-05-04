import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# 📊 DATA DE EJEMPLO (luego lo reemplazamos por SBS real)
df = pd.DataFrame({
    "empresa": ["Banco A", "Banco A", "Banco A", "Banco B", "Banco B", "Banco B"],
    "fecha": ["2024-01", "2024-02", "2024-03", "2024-01", "2024-02", "2024-03"],
    "liquidez": [1.2, 1.3, 1.25, 1.8, 1.7, 1.6],
    "credito": [2.1, 2.0, 2.2, 1.9, 2.0, 2.1],
    "mercado": [0.8, 0.85, 0.9, 1.1, 1.05, 1.0]
})

st.title("📊 Sistema Financiero Peruano - Dashboard SBS")

# ------------------------
# 🎛 FILTROS (IZQUIERDA)
# ------------------------
st.sidebar.header("Filtros")

empresas = st.sidebar.multiselect(
    "Selecciona empresa",
    df["empresa"].unique(),
    default=df["empresa"].unique()
)

mes = st.sidebar.selectbox(
    "Hasta el mes",
    sorted(df["fecha"].unique())
)

df = df[
    (df["empresa"].isin(empresas)) &
    (df["fecha"] <= mes)
]

# ------------------------
# 📊 CONTENIDO (DERECHA)
# ------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Datos filtrados")
    st.dataframe(df)

with col2:
    st.subheader("📈 Indicadores")

    indicador = st.selectbox(
        "Selecciona indicador",
        ["liquidez", "credito", "mercado"]
    )

    chart = df.groupby("fecha")[indicador].mean()
    st.line_chart(chart)
