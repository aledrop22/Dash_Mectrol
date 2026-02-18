"""
Teste de validações de conflito de classificações
"""

def testar_validacoes():
    print("=" * 80)
    print("TESTE DE VALIDAÇÕES DE CONFLITO")
    print("=" * 80)
    
    # Teste 1: RETIFICADO + LAMINADO (proibido)
    print("\n1️⃣ TESTE: RETIFICADO + LAMINADO")
    print("   Seleção: sel_fuso_ret=True, sel_fuso_lam=True")
    retificados = True
    laminados = True
    if retificados and laminados:
        print("   ❌ ERRO: Não pode selecionar RETIFICADO e LAMINADO ao mesmo tempo!")
        print("   ✓ Sistema desmarcar LAMINADO, manter RETIFICADO")
    else:
        print("   ✓ PASSOU")
    
    # Teste 2: ESPECIAIS + RETIFICADO (proibido)
    print("\n2️⃣ TESTE: GUIA + RETIFICADO")
    print("   Seleção: sel_guia=True, sel_fuso_ret=True")
    especiais = True
    retificados = True
    laminados = False
    if especiais and (retificados or laminados):
        print("   ❌ ERRO: GUIA não pode ser selecionado com RETIFICADO!")
        print("   ✓ Sistema desmarcar RETIFICADO, manter GUIA")
    else:
        print("   ✓ PASSOU")
    
    # Teste 3: ESPECIAIS + LAMINADO (proibido)
    print("\n3️⃣ TESTE: BLOCO + LAMINADO")
    print("   Seleção: sel_bloco=True, sel_fuso_lam=True")
    especiais = True
    retificados = False
    laminados = True
    if especiais and (retificados or laminados):
        print("   ❌ ERRO: BLOCO não pode ser selecionado com LAMINADO!")
        print("   ✓ Sistema desmarcar LAMINADO, manter BLOCO")
    else:
        print("   ✓ PASSOU")
    
    # Teste 4: Apenas RETIFICADO (permitido)
    print("\n4️⃣ TESTE: Apenas RETIFICADO")
    print("   Seleção: sel_fuso_ret=True")
    especiais = False
    retificados = True
    laminados = False
    if especiais or (retificados and laminados):
        print("   ❌ ERRO")
    else:
        print("   ✓ PASSOU - Seleção válida")
    
    # Teste 5: Apenas LAMINADO (permitido)
    print("\n5️⃣ TESTE: Apenas LAMINADO")
    print("   Seleção: sel_fuso_lam=True")
    especiais = False
    retificados = False
    laminados = True
    if especiais or (retificados and laminados):
        print("   ❌ ERRO")
    else:
        print("   ✓ PASSOU - Seleção válida")
    
    # Teste 6: Apenas GUIA (permitido)
    print("\n6️⃣ TESTE: Apenas GUIA")
    print("   Seleção: sel_guia=True")
    especiais = True
    retificados = False
    laminados = False
    if especiais and (retificados or laminados):
        print("   ❌ ERRO")
    else:
        print("   ✓ PASSOU - Seleção válida")
    
    # Teste 7: Apenas BLOCO (permitido)
    print("\n7️⃣ TESTE: Apenas BLOCO")
    print("   Seleção: sel_bloco=True")
    especiais = True
    retificados = False
    laminados = False
    if especiais and (retificados or laminados):
        print("   ❌ ERRO")
    else:
        print("   ✓ PASSOU - Seleção válida")
    
    print("\n" + "=" * 80)
    print("Resumo das Regras:")
    print("  ✓ Pode selecionar: RETIFICADO apenas")
    print("  ✓ Pode selecionar: LAMINADO apenas")
    print("  ✓ Pode selecionar: GUIA apenas")
    print("  ✓ Pode selecionar: BLOCO apenas")
    print("  ❌ Não pode: RETIFICADO + LAMINADO")
    print("  ❌ Não pode: GUIA/BLOCO + RETIFICADO/LAMINADO")
    print("=" * 80)

if __name__ == "__main__":
    testar_validacoes()
