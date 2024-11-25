import pandas as pd

# Cargar el archivo CSV
csv_path = "./data/df_ventas_extra_extra_small.csv"  # Reemplaza con la ruta de tu archivo CSV
data = pd.read_csv(csv_path)

# Calcular el número de filas para la mitad
half_rows = len(data) // 10

# Recortar a la mitad
data_half = data.iloc[:half_rows]

# Guardar el archivo reducido
output_path = "./data/df_ventas_extra_extra_extra_small.csv"  # Reemplaza con la ruta de salida
data_half.to_csv(output_path, index=False)

print(f"Archivo recortado guardado en: {output_path}")
