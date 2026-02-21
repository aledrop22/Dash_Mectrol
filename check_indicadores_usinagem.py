import pandas as pd

# Ler a planilha
df = pd.read_excel('3.1_DASH_MENSAL_01_26.xlsx', sheet_name='Indicadores Usinagem', header=None)

print("Shape:", df.shape)
print("\n=== PRIMEIRAS 35 LINHAS E PRIMEIRAS 8 COLUNAS ===")
print(df.iloc[0:35, 0:8].to_string())

print("\n=== LINHA 28 (índice 27) COLUNAS A-E ===")
print(df.iloc[27, 0:5])

print("\n=== VALORES COLUNA B-D LINHA 28 ===")
print(f"B28: {df.iloc[27, 1]}")
print(f"C28: {df.iloc[27, 2]}")
print(f"D28: {df.iloc[27, 3]}")
