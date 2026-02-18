import pandas as pd

# Ler o arquivo Excel
file_path = r'c:\Users\xandy\Documents\GitHub\Dash_Mectrol\CRONOGRAMA 02-26\CRONOGRAMA_QUALIDADE_17-02.xlsx'
df = pd.read_excel(file_path)

# Exibir as colunas
print("=" * 60)
print("COLUNAS ENCONTRADAS NO ARQUIVO:")
print("=" * 60)
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")
print("=" * 60)
print(f"Total de colunas: {len(df.columns)}")
