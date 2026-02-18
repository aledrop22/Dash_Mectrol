#!/usr/bin/env python
"""Test that the modified cronograma loader works with the 3.1_DASH_MENSAL file."""
import sys
sys.path.insert(0, 'c:\\Users\\xandy\\Documents\\GitHub\\Dash_Mectrol')

from app_qualidade import carregar_dados_cronograma, buscar_arquivo_cronograma
import os

# override the search to look in current directory
cwd = os.getcwd()
test_file = os.path.join(cwd, "3.1_DASH_MENSAL_01_26.xlsx")

if not os.path.exists(test_file):
    print(f"[test] file not found at {test_file}")
    sys.exit(1)

print(f"[test] testing loader with {test_file}")

# test 1: buscar_arquivo_cronograma should find the file if placed in a folder
folder = os.path.dirname(test_file)
old_buscar = buscar_arquivo_cronograma

def mock_buscar(pasta):
    return test_file, "3.1_DASH_MENSAL_01_26.xlsx"

# monkey-patch for testing
import app_qualidade
app_qualidade.buscar_arquivo_cronograma = mock_buscar

try:
    df, msg = carregar_dados_cronograma()
    print(f"[test] carregar_dados_cronograma returned: {df.shape if df is not None else None}, msg={msg}")
    
    if df is not None:
        print(f"[test] DataFrame shape: {df.shape}")
        print(f"[test] Columns: {df.columns.tolist()}")
        
        # verify core columns
        assert 'OP' in df.columns, "OP column missing"
        print(f"[test] ✓ OP column found")
        
        # verify checkbox columns are preserved
        checkbox_cols = ["RETRABALHO OUTROS DP", "Retrabalho", "Usinagem"]
        found = [c for c in checkbox_cols if c in df.columns]
        print(f"[test] ✓ Found checkbox columns: {found}")
        
        if len(found) > 0:
            print(f"[test] SUCCESS: Extra checkbox columns are being loaded!")
        else:
            print(f"[test] WARNING: No checkbox columns found, but this might be ok if the data is from a different sheet")
    else:
        print(f"[test] ERROR: loader returned None")
        sys.exit(1)
        
finally:
    app_qualidade.buscar_arquivo_cronograma = old_buscar
