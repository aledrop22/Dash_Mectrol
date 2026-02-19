import pandas as pd

arquivo = '3.1_DASH_MENSAL_01_26.xlsx'

# Ler PRODUTOS DE REFUGO com header=1 (linha 1)
df_refugo = pd.read_excel(arquivo, sheet_name='PRODUTOS DE REFUGO', header=1, nrows=3)
print("Header=1, primeiras 3 linhas:")
print(df_refugo.to_string())
print("\nColunas:", df_refugo.columns.tolist())
