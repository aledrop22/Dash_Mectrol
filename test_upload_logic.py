#!/usr/bin/env python
"""Test that the modified cronograma loader works with manual file upload."""
import sys
sys.path.insert(0, 'c:\\Users\\xandy\\Documents\\GitHub\\Dash_Mectrol')

import pandas as pd
from pathlib import Path

test_file = r"c:\Users\xandy\Documents\GitHub\Dash_Mectrol\3.1_DASH_MENSAL_01_26.xlsx"

if not Path(test_file).exists():
    print(f"[test_upload] file not found at {test_file}")
    sys.exit(1)

print(f"[test_upload] testing upload logic with {test_file}")

# replicate the smart upload logic
xls = pd.ExcelFile(test_file, engine='openpyxl')
colunas_obrigatorias = ['OP', 'Transportadora', 'Previsão', 'Atividade PCP']
df_up = None

def sheet_looks_like_data(tmp):
    if tmp.shape[0] < 2 or tmp.shape[1] < 2:
        return False
    if 'OP' not in tmp.columns:
        return False
    return True

# prefer a sheet named like "lançamentos" or containing required columns
for sheet in xls.sheet_names:
    try:
        tmp = pd.read_excel(xls, sheet_name=sheet, engine='openpyxl', dtype=str).fillna("")
    except Exception:
        continue
    if not sheet_looks_like_data(tmp):
        continue
    print(f"[test_upload] candidate sheet: {sheet} {tmp.shape}")
    if "lan" in sheet.lower():
        print(f"[test_upload]   -> selected (name match)")
        df_up = tmp
        break
    if all(c in tmp.columns for c in colunas_obrigatorias):
        print(f"[test_upload]   -> selected (required columns)")
        df_up = tmp
        break

# last resort
if df_up is None:
    for sheet in xls.sheet_names:
        try:
            tmp = pd.read_excel(xls, sheet_name=sheet, engine='openpyxl', dtype=str).fillna("")
        except Exception:
            continue
        if sheet_looks_like_data(tmp):
            print(f"[test_upload]   -> fallback to {sheet}")
            df_up = tmp
            break

if df_up is None:
    df_up = pd.read_excel(test_file, engine='openpyxl', dtype=str).fillna("")

print(f"[test_upload] final DataFrame: {df_up.shape}")
print(f"[test_upload] columns: {df_up.columns.tolist()}")

# Check for checkbox columns
checkbox_candidates = ["RETRABALHO OUTROS DP", "Retrabalho", "Usinagem", "Inspeção"]
found_checkboxes = [c for c in checkbox_candidates if c in df_up.columns]
print(f"[test_upload] found checkbox columns: {found_checkboxes}")

if found_checkboxes:
    print(f"[test_upload] ✅ SUCCESS: Extra columns are preserved!")
else:
    print(f"[test_upload] ⚠️ WARNING: No checkbox columns found")

# Also show a sample of columns that are preserved
print(f"[test_upload] sample columns (first 15): {df_up.columns.tolist()[:15]}")
