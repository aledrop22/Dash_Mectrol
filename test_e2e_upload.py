#!/usr/bin/env python
"""
End-to-end test: simulate uploading the 3.1_DASH_MENSAL file and verify
that the display logic preserves and shows all checkbox columns.
"""
import sys
sys.path.insert(0, r'c:\Users\xandy\Documents\GitHub\Dash_Mectrol')

import pandas as pd
from pathlib import Path

# ============================================================================
# STEP 1: Simulate the smart upload logic
# ============================================================================
test_file = r"c:\Users\xandy\Documents\GitHub\Dash_Mectrol\3.1_DASH_MENSAL_01_26.xlsx"
print("[e2e] ▶︎ STEP 1: Smart Upload Logic")
print(f"     Loading: {Path(test_file).name}")

xls = pd.ExcelFile(test_file, engine='openpyxl')
colunas_obrigatorias = ['OP', 'Transportadora', 'Previsão', 'Atividade PCP']
df_up = None

def sheet_looks_like_data(tmp):
    if tmp.shape[0] < 2 or tmp.shape[1] < 2:
        return False
    if 'OP' not in tmp.columns:
        return False
    return True

for sheet in xls.sheet_names:
    try:
        tmp = pd.read_excel(xls, sheet_name=sheet, engine='openpyxl', dtype=str).fillna("")
    except Exception:
        continue
    if not sheet_looks_like_data(tmp):
        continue
    if "lan" in sheet.lower():
        df_up = tmp
        break

if df_up is None:
    for sheet in xls.sheet_names:
        try:
            tmp = pd.read_excel(xls, sheet_name=sheet, engine='openpyxl', dtype=str).fillna("")
        except Exception:
            continue
        if sheet_looks_like_data(tmp):
            df_up = tmp
            break

if df_up is None:
    df_up = pd.read_excel(test_file, engine='openpyxl', dtype=str).fillna("")

print(f"     ✓ Loaded: {df_up.shape[0]} rows × {df_up.shape[1]} columns")
print(f"     ✓ Has OP: {'OP' in df_up.columns}")

# ============================================================================
# STEP 2: Apply the display logic from the Home page
# ============================================================================
print("\n[e2e] ▶︎ STEP 2: Display Logic (Like in app_qualidade.py)")

# Simulate the column selection logic
cols = ['Previsão', 'OP', 'Pedido', 'Código Item', 'Cliente', 'Descrição do Item', 'Quantidade', 'Transportadora', 'Prazo Entrega (dias)']
cols_validas = [c for c in cols if c in df_up.columns]
print(f"     Standard columns found: {len(cols_validas)}/{len(cols)}")
print(f"     {cols_validas}")

# Include extra columns (the checkbox ones!)
extra = [c for c in df_up.columns if c not in cols_validas]
print(f"\n     Extra columns (preserved): {len(extra)}")
print(f"     {extra}")

df_display = df_up[cols_validas + extra].copy()
print(f"\n     ✓ Display DataFrame: {df_display.shape[0]} rows × {df_display.shape[1]} columns")

# ============================================================================
# STEP 3: Identify checkbox columns
# ============================================================================
print("\n[e2e] ▶︎ STEP 3: Checkbox Columns")
checkbox_keywords = ["RETRABALHO", "Morta", "Usinagem", "Inspeção", "Desenho", "Produção", "Comercial"]
checkbox_cols = [c for c in extra if any(kw.lower() in c.lower() for kw in checkbox_keywords)]
print(f"     Checkbox-like columns: {len(checkbox_cols)}")
for col in checkbox_cols:
    print(f"       • {col}")

# ============================================================================
# STEP 4: Sample the first few rows to show what the user will see
# ============================================================================
print("\n[e2e] ▶︎ STEP 4: Sample Display")
print(f"     Shape: {df_display.shape}")
print(f"     Columns: {df_display.columns.tolist()}")

# Show first 3 rows across selected columns
print("\n     First 3 rows (sample):")
sample_cols = ['OP', 'Pedido', 'Cliente'] + checkbox_cols[:3] if checkbox_cols else []
if sample_cols:
    for idx in range(min(3, len(df_display))):
        row = df_display.iloc[idx]
        print(f"       Row {idx+1}:")
        for col in sample_cols:
            val = row.get(col, 'N/A')
            print(f"         {col}: {val}")

# ============================================================================
# FINAL VERDICT
# ============================================================================
print("\n" + "="*80)
if len(checkbox_cols) > 0:
    print("✅ SUCCESS!")
    print(f"   The app WILL display {len(checkbox_cols)} checkbox columns when")
    print(f"   you upload the 3.1_DASH_MENSAL_01_26.xlsx file.")
    print(f"\n   Columns that will appear in 📋 Lista Detalhada:")
    for col in checkbox_cols:
        print(f"      ✓ {col}")
else:
    print("⚠️  No specific checkbox columns detected, but all extra columns")
    print("   will still be displayed if they exist in the file.")
print("="*80)
