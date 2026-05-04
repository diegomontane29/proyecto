import pandas as pd
import glob
import os
import re

mes_map = {
    "en": "01", "fe": "02", "mr": "03", "ab": "04",
    "ma": "05", "jn": "06", "jl": "07", "ag": "08",
    "se": "09", "oc": "10", "no": "11", "di": "12"
}

def parse_fecha(file):

    name = os.path.basename(file).replace(".XLS", "")

    match = re.search(r"([a-z]{2})(\d{4})", name)

    mes = match.group(1)
    anio = match.group(2)

    return f"{anio}-{mes_map[mes]}"

def build_dataset():

    files = glob.glob("data_sbs/B-2340*.XLS")

    dfs = []

    for file in files:

        df = pd.read_excel(file)

        df.columns = df.columns.str.lower().str.strip()

        df["fecha"] = parse_fecha(file)

        dfs.append(df)

    df_final = pd.concat(dfs, ignore_index=True)

    df_final = df_final.rename(columns={
        "banco": "banco",
        "indicador": "indicador",
        "subindicador": "subindicador",
        "valor": "valor"
    })

    df_final = df_final[
        ["banco", "fecha", "indicador", "subindicador", "valor"]
    ]

    df_final = df_final.sort_values(["banco", "fecha"])

    df_final.to_parquet("sbs_data.parquet", index=False)

    print("✔ Dataset consolidado generado")


if __name__ == "__main__":
    build_dataset()
