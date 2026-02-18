#!/usr/bin/env python
"""Diagnóstico de carregamento de dados."""
import pandas as pd
import os
from datetime import date

mes_ano_atual = date.today().strftime("%m-%y")
PASTA_CRONOGRAMA = f"CRONOGRAMA {mes_ano_atual}"

print(f"📁 Procurando em: {PASTA_CRONOGRAMA}")
print(f"📅 Mês/Ano: {mes_ano_atual}\n")

# Verificar pasta
if not os.path.exists(PASTA_CRONOGRAMA):
    print(f"❌ Pasta NÃO encontrada!")
else:
    print(f"✅ Pasta encontrada\n")
    
    # Listar arquivos
    arquivos = os.listdir(PASTA_CRONOGRAMA)
    print(f"Arquivos na pasta:")
    for f in arquivos:
        print(f"  - {f}")
    
    # Buscar cronograma
    candidatos = [f for f in arquivos if "CRONOGRAMA" in f.upper() and f.endswith(".xlsx") and not f.startswith("~$")]
    
    if not candidatos:
        print(f"\n❌ Nenhum arquivo CRONOGRAMA_*.xlsx encontrado")
    else:
        candidatos.sort(reverse=True)
        arquivo = candidatos[0]
        caminho = os.path.join(PASTA_CRONOGRAMA, arquivo)
        
        print(f"\n✅ Arquivo selecionado: {arquivo}")
        print(f"📄 Caminho completo: {caminho}")
        print(f"📊 Tamanho: {os.path.getsize(caminho)} bytes\n")
        
        # Tentar carregar
        try:
            df = pd.read_excel(caminho, engine='openpyxl').fillna("")
            print(f"✅ Arquivo carregado com sucesso!")
            print(f"   - Linhas: {len(df)}")
            print(f"   - Colunas: {len(df.columns)}")
            print(f"\n📋 Colunas encontradas:")
            for col in df.columns:
                print(f"    ✓ {col}")
            
            # Verificar colunas obrigatórias
            colunas_obrigatorias = ['OP', 'Transportadora', 'Previsão', 'Atividade PCP']
            faltantes = [c for c in colunas_obrigatorias if c not in df.columns]
            
            if faltantes:
                print(f"\n⚠️ Colunas FALTANTES: {faltantes}")
            else:
                print(f"\n✓ Todas as colunas obrigatórias encontradas!")
                
            # Mostrar primeiras linhas
            print(f"\n📊 Primeiras linhas:")
            print(df.head(3))
            
        except Exception as e:
            print(f"❌ Erro ao carregar: {type(e).__name__}: {e}")
