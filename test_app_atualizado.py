"""
Teste importando a função atualizada do app_qualidade.py
"""
import sys
sys.path.insert(0, 'c:\\Users\\xandy\\Documents\\GitHub\\Dash_Mectrol')

# Importar as funções do app_qualidade
from app_qualidade import detectar_tipo_componente, detectar_classe_precisao

# ===== TESTE COM VARIAÇÕES =====
descricoes_teste = [
    "MECÂNICA INDUSTRIAL M.N. LTDA RETIFICADO 0.008",
    "MECÂNICA INDUSTRIAL M.N. LTDA FUSO RETIFICADO 0.008",
    "FUSO MECÂNICA INDUSTRIAL M.N. LTDA RETIFICADO 0.008",
    "MECÂNICA INDUSTRIAL M.N. LTDA 0.008",  # SEM especificação
    "MECÂNICA INDUSTRIAL M.N. LTDA LAMINADO 0.008",
]

print("=" * 100)
print("TESTE COM APP_QUALIDADE ATUALIZADO")
print("=" * 100)

for desc in descricoes_teste:
    print(f"\n📋 Descrição: {desc}")
    
    # Classificação
    resultado = detectar_classe_precisao(desc)
    
    print(f"   Resultado da Classificação:")
    classificacoes = {k: v for k, v in resultado.items() if v}
    
    if classificacoes:
        for chave in classificacoes:
            print(f"      ✅ {chave}")
    else:
        print(f"      ⚠️ Nenhuma classificação")

print("\n" + "=" * 100)
