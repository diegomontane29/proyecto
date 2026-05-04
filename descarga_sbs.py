import pandas as pd

def obtener_datos_sbs():
    # aquí luego conectas a SBS real
    data = {
        "empresa": ["A", "A", "B", "B"],
        "fecha": ["2024-01", "2024-02", "2024-01", "2024-02"],
        "liquidez": [1.2, 1.3, 2.1, 2.2],
        "credito": [3.1, 3.2, 2.9, 3.0],
        "mercado": [0.8, 0.9, 1.1, 1.3],
    }
    return pd.DataFrame(data)
