import pandas as pd

# ---------------------------------------------------
# 🔵 AQUÍ SIMULAMOS ESTRUCTURA REAL SBS (BASE LIMPIA)
# Luego aquí conectamos descarga oficial
# ---------------------------------------------------

def generar_base_sbs():
    data = [
        ["Interbank", "2024-01", "Liquidez", "MN", 38.52],
        ["Interbank", "2024-02", "Liquidez", "MN", 37.80],
        ["BCP", "2024-01", "Liquidez", "MN", 42.10],
        ["BBVA", "2024-01", "Liquidez", "MN", 35.20],
        ["Interbank", "2024-01", "Liquidez", "ME", 12.40],
        ["BCP", "2024-01", "Liquidez", "ME", 13.10],
    ]

    df = pd.DataFrame(data, columns=[
        "banco", "fecha", "indicador", "subindicador", "valor"
    ])

    df.to_parquet("sbs_data.parquet", index=False)

    print("✔ Base SBS creada correctamente")


if __name__ == "__main__":
    generar_base_sbs()
