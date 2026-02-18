"""
Teste para validar o novo sistema de classificação de componentes
"""
import re

def detectar_tipo_componente(descricao):
    """Detecta se é FUSO, GUIA ou BLOCO baseado em padrões específicos."""
    desc_upper = descricao.upper()
    
    # GUIAS: Iniciais HG, RG, EG, WER, MGN, MGW (buscar em toda a descrição)
    padroes_guias = [r'HG', r'RG', r'EG', r'WER', r'MGN', r'MGW']
    eh_guia = any(padrao in desc_upper for padrao in padroes_guias)
    
    # FUSOS: Iniciais com R ou L, seguidas de números OU palavra "FUSO" na descrição
    padroes_fusos = [r'\b[2485]R\b', r'\bR\d+\b', r'\bL\d+\b', r'FUSO']
    eh_fuso = any(re.search(p, desc_upper) if p in [r'\b[2485]R\b', r'\bR\d+\b', r'\bL\d+\b'] else p in desc_upper for p in padroes_fusos)
    
    # BLOCO: Palavras-chave específicas
    eh_bloco = 'BLOCO' in desc_upper or 'PATIM' in desc_upper
    
    return eh_fuso, eh_guia, eh_bloco

def detectar_classe_precisao(descricao):
    """Detecta classe de precisão (tolerância) na descrição e retorna classificação automática."""
    desc_upper = descricao.upper()
    
    # 1. DETECTAR TIPO DE COMPONENTE
    eh_fuso, eh_guia, eh_bloco = detectar_tipo_componente(descricao)
    
    # 2. EXTRAIR TOLERÂNCIA (0,025 ou 0.025 ou 0,05 ou 0.05, etc)
    match_tolerancia = re.search(r'[-,.]?(0[,/.](0\d{2}|0\d{3}|\d{2}|\d{3}))', desc_upper)
    tolerancia_encontrada = None
    
    if match_tolerancia:
        tol_str = match_tolerancia.group(1).replace(',', '.').replace('/', '.')
        try:
            tolerancia_encontrada = float(tol_str)
        except:
            pass
    
    # 3. VERIFICAR CARACTERÍSTICAS DE PROCESSAMENTO
    tem_mop = 'MOP' in desc_upper
    tem_esferas = 'ESFERAS' in desc_upper
    eh_conjunto = 'CONJUNTO' in desc_upper
    eh_retificado = 'RETIFICADO' in desc_upper
    eh_laminado = 'LAMINADO' in desc_upper
    eh_adaptado = 'ADAPTADO' in desc_upper
    eh_castanha = 'CASTANHA' in desc_upper or 'ADAPTADA' in desc_upper
    
    # 4. INICIALIZAR RESULTADO
    resultado = {
        'sel_fuso_ret': False,
        'sel_fuso_ret_ad': False,
        'sel_cast_ret': False,
        'sel_cast_ret_ad': False,
        'sel_fuso_lam': False,
        'sel_fuso_lam_ad': False,
        'sel_cast_lam': False,
        'sel_cast_lam_ad': False,
        'sel_guia': False,
        'sel_bloco': False,
    }
    
    # 5. CLASSIFICAR COMPONENTES ESPECIAIS
    if eh_guia:
        resultado['sel_guia'] = True
        return resultado
    
    if eh_bloco:
        resultado['sel_bloco'] = True
        return resultado
    
    # 6. CLASSIFICAR FUSOS E CASTANHAS
    if eh_fuso or eh_castanha:
        # Tipo de componente para escolher a chave correta
        tipo = 'fuso' if eh_fuso else 'cast'
        
        # PRIORIDADE 1: Palavras explícitas RETIFICADO ou LAMINADO têm prioridade MÁXIMA
        if eh_retificado and not eh_laminado:
            chave_ret = f'sel_{tipo}_ret'
            chave_ret_ad = f'sel_{tipo}_ret_ad'
            resultado[chave_ret_ad if eh_adaptado else chave_ret] = True
            return resultado
        
        if eh_laminado and not eh_retificado:
            chave_lam = f'sel_{tipo}_lam'
            chave_lam_ad = f'sel_{tipo}_lam_ad'
            resultado[chave_lam_ad if eh_adaptado else chave_lam] = True
            return resultado
        
        # PRIORIDADE 2: MOP → RETIFICADO
        if tem_mop:
            chave_ret = f'sel_{tipo}_ret'
            chave_ret_ad = f'sel_{tipo}_ret_ad'
            resultado[chave_ret_ad if eh_adaptado else chave_ret] = True
            return resultado
        
        # PRIORIDADE 3: LAMINADO DE PRECISÃO
        # (ESFERAS + CONJUNTO + tolerância baixa (0.023 ou 0.05))
        if tem_esferas and eh_conjunto and tolerancia_encontrada and tolerancia_encontrada in [0.023, 0.05]:
            chave_lam = f'sel_{tipo}_lam'
            chave_lam_ad = f'sel_{tipo}_lam_ad'
            resultado[chave_lam_ad if eh_adaptado else chave_lam] = True
            return resultado
        
        # PRIORIDADE 4: Inferir por tolerância
        # Tolerâncias baixas (<= 0.023) indicam RETIFICADO
        # Tolerâncias altas (>= 0.05) indicam LAMINADO
        if tolerancia_encontrada:
            if tolerancia_encontrada <= 0.023:
                chave_ret = f'sel_{tipo}_ret'
                chave_ret_ad = f'sel_{tipo}_ret_ad'
                resultado[chave_ret_ad if eh_adaptado else chave_ret] = True
            elif tolerancia_encontrada >= 0.05:
                chave_lam = f'sel_{tipo}_lam'
                chave_lam_ad = f'sel_{tipo}_lam_ad'
                resultado[chave_lam_ad if eh_adaptado else chave_lam] = True
            return resultado
    
    return resultado

# ============ TESTES ============

if __name__ == "__main__":
    print("=" * 80)
    print("TESTANDO NOVO SISTEMA DE CLASSIFICAÇÃO")
    print("=" * 80)
    
    # Teste 1: FUSO com tolerância baixa (deve ser RETIFICADO)
    desc1 = "R25-5-437-530-0,008"
    print(f"\n1. {desc1}")
    res1 = detectar_classe_precisao(desc1)
    print(f"   Resultado: {res1}")
    print(f"   ✓ ESPERADO: sel_fuso_ret=True" if res1['sel_fuso_ret'] else f"   ✗ ERRO!")
    
    # Teste 2: FUSO com castanha (deve ser RETIFICADO com castanha)
    desc2 = "R50-10-K8-FSC-1550-1885-0,05"
    print(f"\n2. {desc2}")
    res2 = detectar_classe_precisao(desc2)
    print(f"   Resultado: {res2}")
    print(f"   ✓ ESPERADO: detecta como fuso + castanha" if res2['sel_fuso_lam'] else f"   Tipo: {res2}")
    
    # Teste 3: GUIA (deve ser GUIA)
    desc3 = "HG20CA LINEAR"
    print(f"\n3. {desc3}")
    res3 = detectar_classe_precisao(desc3)
    print(f"   Resultado: {res3}")
    print(f"   ✓ ESPERADO: sel_guia=True" if res3['sel_guia'] else f"   ✗ ERRO!")
    
    # Teste 4: BLOCO (deve ser BLOCO)
    desc4 = "BLOCO CALIBRADO"
    print(f"\n4. {desc4}")
    res4 = detectar_classe_precisao(desc4)
    print(f"   Resultado: {res4}")
    print(f"   ✓ ESPERADO: sel_bloco=True" if res4['sel_bloco'] else f"   ✗ ERRO!")
    
    # Teste 5: FUSO com MOP (deve ser RETIFICADO)
    desc5 = "R40 FUSO MOP 0,023"
    print(f"\n5. {desc5}")
    res5 = detectar_classe_precisao(desc5)
    print(f"   Resultado: {res5}")
    print(f"   ✓ ESPERADO: sel_fuso_ret=True (MOP prioridade)" if res5['sel_fuso_ret'] else f"   ✗ ERRO!")
    
    # Teste 6: FUSO com ESFERAS + CONJUNTO (deve ser LAMINADO)
    desc6 = "R32 FUSO DE ESFERAS CONJUNTO 0,05"
    print(f"\n6. {desc6}")
    res6 = detectar_classe_precisao(desc6)
    print(f"   Resultado: {res6}")
    print(f"   ✓ ESPERADO: sel_fuso_lam=True" if res6['sel_fuso_lam'] else f"   ✗ ERRO!")
    
    # Teste 7: RG20 GUIA
    desc7 = "RG20 - GUIA LINEAR"
    print(f"\n7. {desc7}")
    res7 = detectar_classe_precisao(desc7)
    print(f"   Resultado: {res7}")
    print(f"   ✓ ESPERADO: sel_guia=True" if res7['sel_guia'] else f"   ✗ ERRO!")
    
    # Teste 8: MGN12 GUIA
    desc8 = "MGN12H LINEAR GUIDE"
    print(f"\n8. {desc8}")
    res8 = detectar_classe_precisao(desc8)
    print(f"   Resultado: {res8}")
    print(f"   ✓ ESPERADO: sel_guia=True" if res8['sel_guia'] else f"   ✗ ERRO!")
    
    # Teste 9: CASTANHA com tolerância alta
    desc9 = "CASTANHA 0,05"
    print(f"\n9. {desc9}")
    res9 = detectar_classe_precisao(desc9)
    print(f"   Resultado: {res9}")
    print(f"   ✓ ESPERADO: sel_cast_lam=True" if res9['sel_cast_lam'] else f"   ✗ ERRO!")
    
    # Teste 10: FUSO sem castanha (R##-) - permitido
    desc10 = "R25-5-437-530-0,05"
    print(f"\n10. {desc10}")
    print(f"   Padrão: R##- encontrado: ", bool(re.search(r'\bR\d+-', desc10)))
    print(f"   ✓ Fuso SEM castanha permitido" if re.search(r'\bR\d+-', desc10) else f"   Requer castanha")
    
    # Teste CRÍTICO: FUSO RETIFICADO com tolerância 0.05 (problema citado)
    desc11 = "R50 FUSO RETIFICADO 0,05"
    print(f"\n11. {desc11}")
    res11 = detectar_classe_precisao(desc11)
    print(f"   Resultado: {res11}")
    print(f"   ✓ ESPERADO: sel_fuso_ret=True (RETIFICADO tem prioridade)" if res11['sel_fuso_ret'] else f"   ✗ ERRO! Está marcando como: {res11}")
    
    # Teste CRÍTICO 2: FUSO RETIFICADO com tolerância 0.05 (variação)
    desc12 = "FUSO RETIFICADO R40-0,05"
    print(f"\n12. {desc12}")
    res12 = detectar_classe_precisao(desc12)
    print(f"   Resultado: {res12}")
    print(f"   ✓ ESPERADO: sel_fuso_ret=True (RETIFICADO tem prioridade)" if res12['sel_fuso_ret'] else f"   ✗ ERRO! Está marcando como: {res12}")
    
    print("\n" + "=" * 80)
    print("TESTES CONCLUÍDOS")
    print("=" * 80)
