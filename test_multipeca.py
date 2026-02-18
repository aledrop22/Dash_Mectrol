#!/usr/bin/env python3
"""
Teste funcional para validar o fluxo multi-peça com conversão de relógio.
Simula o comportamente esperado quando alguém muda entre Centesimal e Milesimal.
"""

import sys

def teste_fluxo_multipeca():
    """Simula o fluxo completo de inspeção multi-peça com conversão de relógio."""
    print("=" * 70)
    print("TESTE: Fluxo Multi-Peça com Conversão de Relógio (Centesimal/Milesimal)")
    print("=" * 70)
    
    # Simulando session_state do Streamlit
    session_state = {
        'tipo_relogio_key': 'Centesimal',
        'relogio_anterior': 'Centesimal',
        'peca_atual': 1,
        'emp_e_1': None,
        'bat_e_1': None,
        'bat_d_1': None,
        'emp_d_1': None,
        'emp_e_2': None,
        'bat_e_2': None,
        'bat_d_2': None,
        'emp_d_2': None,
    }
    
    print("\n1. ESTADO INICIAL (Centesimal)")
    print(f"   - Tipo de Relógio: {session_state['tipo_relogio_key']}")
    print(f"   - Peça Atual: {session_state['peca_atual']}")
    
    # Passo 1: Digitar valor em Centesimal
    print("\n2. USUÁRIO DIGITA VALOR EM CENTESIMAL")
    print("   - Entrada: 25")
    valor_digitado = 25
    if valor_digitado >= 1.0:
        divisor = 100.0  # Centesimal
        valor_convertido = round(valor_digitado / divisor, 3)
    session_state['emp_e_1'] = valor_convertido
    print(f"   - Após conversão: {session_state['emp_e_1']} (esperado: 0.25)")
    
    # Passo 2: Usuário digita outro valor
    session_state['bat_e_1'] = 15 / 100.0
    print(f"   - Usuário digita 15 → convertido para: {session_state['bat_e_1']} (esperado: 0.15)")
    
    # Passo 3: Mudar de Centesimal para Milesimal
    print("\n3. USUÁRIO MUDA PARA MILESIMAL")
    print(f"   - Antes: emp_e_1 = {session_state['emp_e_1']}, bat_e_1 = {session_state['bat_e_1']}")
    
    novo = 'Milesimal'
    antigo = session_state['relogio_anterior']
    fator = 0.1 if "Milesimal" in novo and "Centesimal" in antigo else 1.0
    
    # Aplicar conversão
    for k in ['emp_e_1', 'bat_e_1', 'bat_d_1', 'emp_d_1']:
        if session_state.get(k) is not None:
            try:
                val = session_state[k]
                if isinstance(val, (int, float)):
                    session_state[k] = round(val * fator, 3)
            except Exception as e:
                print(f"   ❌ ERRO ao converter {k}: {e}")
                return False
    
    session_state['tipo_relogio_key'] = novo
    session_state['relogio_anterior'] = novo
    
    print(f"   - Depois: emp_e_1 = {session_state['emp_e_1']}, bat_e_1 = {session_state['bat_e_1']}")
    print(f"   - Esperado: emp_e_1 = 0.025, bat_e_1 = 0.015")
    print(f"   - Fator aplicado: {fator}")
    
    # Validar
    if abs(session_state['emp_e_1'] - 0.025) > 0.001:
        print(f"   ❌ ERRO: emp_e_1 deveria ser 0.025, mas é {session_state['emp_e_1']}")
        return False
    if abs(session_state['bat_e_1'] - 0.015) > 0.001:
        print(f"   ❌ ERRO: bat_e_1 deveria ser 0.015, mas é {session_state['bat_e_1']}")
        return False
    
    print("   ✅ Conversão OK")
    
    # Passo 4: Mudança para Peça 2
    print("\n4. USUÁRIO CLICA 'PRÓXIMA PEÇA' - TRANSIÇÃO PARA PEÇA 2")
    session_state['peca_atual'] = 2
    print(f"   - Peça Atual agora: {session_state['peca_atual']}")
    
    # Passo 5: Digitar valor em Milesimal (peça 2)
    print("\n5. USUÁRIO DIGITA VALOR EM MILESIMAL (Peça 2)")
    print("   - Entrada: 25")
    valor_digitado = 25
    if valor_digitado >= 1.0:
        divisor = 1000.0  # Milesimal
        valor_convertido = round(valor_digitado / divisor, 3)
    session_state['emp_e_2'] = valor_convertido
    print(f"   - Após conversão: {session_state['emp_e_2']} (esperado: 0.025)")
    
    # Validar
    if abs(session_state['emp_e_2'] - 0.025) > 0.001:
        print(f"   ❌ ERRO: emp_e_2 deveria ser 0.025, mas é {session_state['emp_e_2']}")
        return False
    
    print("   ✅ Conversão em Milesimal OK")
    
    # Passo 6: Mudar de Milesimal para Centesimal
    print("\n6. USUÁRIO MUDA PARA CENTESIMAL NOVAMENTE")
    print(f"   - Antes: emp_e_2 = {session_state['emp_e_2']}")
    
    novo = 'Centesimal'
    antigo = session_state['relogio_anterior']
    fator = 10.0 if "Centesimal" in novo and "Milesimal" in antigo else 1.0
    
    # Aplicar conversão
    for k in ['emp_e_2', 'bat_e_2', 'bat_d_2', 'emp_d_2']:
        if session_state.get(k) is not None:
            try:
                val = session_state[k]
                if isinstance(val, (int, float)):
                    session_state[k] = round(val * fator, 3)
            except Exception as e:
                print(f"   ❌ ERRO ao converter {k}: {e}")
                return False
    
    session_state['tipo_relogio_key'] = novo
    session_state['relogio_anterior'] = novo
    
    print(f"   - Depois: emp_e_2 = {session_state['emp_e_2']}")
    print(f"   - Esperado: emp_e_2 = 0.25")
    print(f"   - Fator aplicado: {fator}")
    
    # Validar
    if abs(session_state['emp_e_2'] - 0.25) > 0.001:
        print(f"   ❌ ERRO: emp_e_2 deveria ser 0.25, mas é {session_state['emp_e_2']}")
        return False
    
    print("   ✅ Conversão OK")
    
    print("\n" + "=" * 70)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    sucesso = teste_fluxo_multipeca()
    sys.exit(0 if sucesso else 1)
