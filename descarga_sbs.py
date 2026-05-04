import pandas as pd
import requests
from io import BytesIO

# 🔧 CONFIG BASE (ajustable según el cuadro SBS)
BASE_URL = "https://extranet.sbs.gob.pe/iece/descargar"

PARAMS_BASE = {
    "codClasificadora": "001196",
    "numArchivo": "4",
    "numVersion": "1"
}

# 📅 generar últimos 60 meses
def generar_periodos(n=60):
    fechas = pd.date_range(end=pd.Timestamp.today(), periods=n, freq="M")
    return [f"{f.year}{f.month:02d}" for f in fechas]


# 📥 descargar un mes
def descargar_mes(periodo):
    params = PARAMS_BASE.copy()
    params["codPeriodo"] = periodo

    try:
        r = requests.get(BASE_URL, params=params)
        r.raise_for_status()

        df = pd.read_excel(BytesIO(r.content))
        df["fecha"] = periodo

        return df

    except Exception as e:
        print(f"Error en {periodo}: {e}")
        return None


# 🧹 limpieza básica
def limpiar(df):
    df = df.dropna(how="all")
    df.columns = df.columns.str.strip()
    return df


# 🚀 ejecutar proceso completo
def main():
    periodos = generar_periodos(60)

    dfs = []

    for p in periodos:
        print(f"Descargando {p}...")
        df = descargar_mes(p)

        if df is not None:
            df = limpiar(df)
            dfs.append(df)

    historico = pd.concat(dfs, ignore_index=True)

    historico.to_parquet("datos_sbs.parquet")

    print("✔ Dataset creado correctamente")


if __name__ == "__main__":
    main()
