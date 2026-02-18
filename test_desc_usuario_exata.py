"""
Teste com a descrição exata mencionada pelo usuário
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
    
    # 2. EXTRAIR TOLERÂNCIA
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
    # CORREÇÃO: Se tiver palavras de processamento EXPLÍCITAS (RETIFICADO/LAMINADO), trate como FUSO
    # mesmo que a palavra "FUSO" não esteja na descrição
    eh_componente_processado = eh_fuso or eh_castanha or eh_retificado or eh_laminado
    
    if eh_componente_processado:
        # Tipo de componente para escolher a chave correta
        # Se tem CASTANHA explícito, usa CASTANHA; senão usa FUSO
        tipo = 'cast' if eh_castanha else 'fuso'
        
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
        if tem_esferas and eh_conjunto and tolerancia_encontrada and tolerancia_encontrada in [0.023, 0.05]:
            chave_lam = f'sel_{tipo}_lam'
            chave_lam_ad = f'sel_{tipo}_lam_ad'
            resultado[chave_lam_ad if eh_adaptado else chave_lam] = True
            return resultado
        
        # PRIORIDADE 4: Inferir por tolerância
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

# ===== TESTE COM VARIAÇÕES =====
descricoes_teste = [
    "MECÂNICA INDUSTRIAL M.N. LTDA RETIFICADO 0.008",
    "MECÂNICA INDUSTRIAL M.N. LTDA FUSO RETIFICADO 0.008",
    "FUSO MECÂNICA INDUSTRIAL M.N. LTDA RETIFICADO 0.008",
    "MECÂNICA INDUSTRIAL M.N. LTDA 0.008",  # SEM especificação
    "MECÂNICA INDUSTRIAL M.N. LTDA LAMINADO 0.008",
]

print("=" * 100)
print("TESTE COM DESCRIÇÕES DO USUÁRIO - VERSÃO CORRIGIDA")
print("=" * 100)

for desc in descricoes_teste:
    print(f"\n📋 Descrição: {desc}")
    
    # Classificação
    resultado = detectar_classe_precisao(desc)
    
    print(f"   Resultado:")
    classificacoes = {k: v for k, v in resultado.items() if v}
    
    if classificacoes:
        for chave in classificacoes:
            print(f"      ✅ {chave}")
    else:
        print(f"      ⚠️ Nenhuma classificação")

print("\n" + "=" * 100)
