import pandas as pd

xls = pd.ExcelFile('3.1_DASH_MENSAL_01_26.xlsx')
print("📄 Abas disponíveis:", xls.sheet_names)
print()

# Ler primeira aba "Lançamentos"
df = pd.read_excel('3.1_DASH_MENSAL_01_26.xlsx', sheet_name='Lançamentos', nrows=1)
print("📊 Colunas da aba 'Lançamentos':")
cols_list = df.columns.tolist()
for i, col in enumerate(cols_list):
    print(f"  {i:2d} ({chr(65 + (i if i < 26 else i-26))}): {col}")

print(f"\nTotal: {len(cols_list)} colunas")

# De R (17) em diante
print("\n🔍 Colunas R-AF (possíveis checkboxes):")
for i in range(17, min(32, len(cols_list))):
    col_letter = chr(65 + i) if i < 26 else chr(65 + i - 26)
    print(f"  {col_letter}: {cols_list[i]}")
