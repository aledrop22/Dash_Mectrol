"""
Debug descricao exata
"""
import re

def detectar_tipo_componente(descricao):
    desc_upper = descricao.upper()
    padroes_guias = [r'HG', r'RG', r'EG', r'WER', r'MGN', r'MGW']
    eh_guia = any(padrao in desc_upper for padrao in padroes_guias)
    padroes_fusos = [r'\b[2485]R\b', r'\bR\d+\b', r'\bL\d+\b', r'FUSO']
    eh_fuso = any(re.search(p, desc_upper) if p in [r'\b[2485]R\b', r'\bR\d+\b', r'\bL\d+\b'] else p in desc_upper for p in padroes_fusos)
    eh_bloco = 'BLOCO' in desc_upper or 'PATIM' in desc_upper
    return eh_fuso, eh_guia, eh_bloco

desc = "FUSO DE TESTE RETIFICADO 0.008 MECÂNICA INDUSTRIAL M.N. LTDA"
print(f"Descrição: {desc}")
print()

desc_upper = desc.upper()
print(f"Análise:")
print(f"  Tem 'RETIFICADO': {'RETIFICADO' in desc_upper}")
print(f"  Tem 'LAMINADO': {'LAMINADO' in desc_upper}")
print(f"  Tem 'FUSO': {'FUSO' in desc_upper}")

eh_fuso, eh_guia, eh_bloco = detectar_tipo_componente(desc)
print(f"  Detectado como FUSO: {eh_fuso}")

# Extrair tolerância
match_tol = re.search(r'[-,.]?(0[,/.](0\d{2}|0\d{3}|\d{2}|\d{3}))', desc_upper)
if match_tol:
    tol_str = match_tol.group(1).replace(',', '.')
    tol = float(tol_str)
    print(f"  Tolerância extraída: {tol}")
else:
    print(f"  Tolerância: não encontrada")

print()
print("✓ Com a prioridade RETIFICADO > tolerância, deveria marcar como: FUSO RETIFICADO")
