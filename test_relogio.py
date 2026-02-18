"""
Teste para validar conversão de relógio Centesimal <-> Milesimal
"""

def testar_conversao_relogio():
    """Simular a conversão de relógio"""
    
    # Simulando o session_state
    class MockSessionState:
        def __init__(self):
            self.tipo_relogio_key = "Centesimal"
            self.relogio_anterior = "Centesimal"
            self.peca_atual = 1
            self.emp_e = "0.12"  # Valor em string como vem do text_input
            self.bat_e = "0.08"
            self.bat_d = ""
            self.emp_d = ""
    
    mock_state = MockSessionState()
    
    print("=" * 80)
    print("TESTE DE CONVERSÃO DE RELÓGIO")
    print("=" * 80)
    
    # Estado inicial
    print(f"\n📍 ESTADO INICIAL (Centesimal):")
    print(f"   emp_e: {mock_state.emp_e}")
    print(f"   bat_e: {mock_state.bat_e}")
    print(f"   bat_d: {mock_state.bat_d}")
    print(f"   emp_d: {mock_state.emp_d}")
    
    # Mudança para Milesimal
    print(f"\n🔄 Alterando para Milesimal...")
    novo = "Milesimal"
    antigo = mock_state.relogio_anterior
    
    # Calcula fator
    fator = 0.1 if "Milesimal" in novo and "Centesimal" in antigo else 10.0 if "Centesimal" in novo and "Milesimal" in antigo else 1.0
    print(f"   Fator de conversão: {fator}")
    
    if fator != 1.0:
        # Converter valores
        for k in ['emp_e', 'bat_e', 'bat_d', 'emp_d']:
            val = getattr(mock_state, k)
            if val is not None and val != "":
                try:
                    if isinstance(val, str):
                        num_val = float(val)
                    else:
                        num_val = float(val)
                    convertido = round(num_val * fator, 3)
                    novo_valor = str(convertido) if isinstance(val, str) else convertido
                    setattr(mock_state, k, novo_valor)
                    print(f"   ✓ {k}: {val} × {fator} = {novo_valor}")
                except Exception as e:
                    print(f"   ✗ {k}: Erro - {e}")
    
    mock_state.relogio_anterior = novo
    mock_state.tipo_relogio_key = novo
    
    print(f"\n📍 APÓS CONVERSÃO (Milesimal):")
    print(f"   emp_e: {mock_state.emp_e}")
    print(f"   bat_e: {mock_state.bat_e}")
    print(f"   bat_d: {mock_state.bat_d}")
    print(f"   emp_d: {mock_state.emp_d}")
    
    # Validar tolerância
    print(f"\n✓ Tolerância em Milesimal: 0.05 (5%)")
    print(f"  - emp_e = {mock_state.emp_e}: {'❌ FORA' if float(mock_state.emp_e) > 0.05 else '✅ OK'}")
    print(f"  - bat_e = {mock_state.bat_e}: {'❌ FORA' if float(mock_state.bat_e) > 0.05 else '✅ OK'}")
    
    # Converter de volta para Centesimal
    print(f"\n🔄 Alterando de volta para Centesimal...")
    novo = "Centesimal"
    antigo = mock_state.relogio_anterior
    
    fator = 0.1 if "Milesimal" in novo and "Centesimal" in antigo else 10.0 if "Centesimal" in novo and "Milesimal" in antigo else 1.0
    print(f"   Fator de conversão: {fator}")
    
    if fator != 1.0:
        for k in ['emp_e', 'bat_e', 'bat_d', 'emp_d']:
            val = getattr(mock_state, k)
            if val is not None and val != "":
                try:
                    if isinstance(val, str):
                        num_val = float(val)
                    else:
                        num_val = float(val)
                    convertido = round(num_val * fator, 3)
                    novo_valor = str(convertido) if isinstance(val, str) else convertido
                    setattr(mock_state, k, novo_valor)
                    print(f"   ✓ {k}: {val} × {fator} = {novo_valor}")
                except Exception as e:
                    print(f"   ✗ {k}: Erro - {e}")
    
    mock_state.relogio_anterior = novo
    mock_state.tipo_relogio_key = novo
    
    print(f"\n📍 APÓS CONVERSÃO (Centesimal novamente):")
    print(f"   emp_e: {mock_state.emp_e}")
    print(f"   bat_e: {mock_state.bat_e}")
    print(f"   bat_d: {mock_state.bat_d}")
    print(f"   emp_d: {mock_state.emp_d}")
    
    print("\n" + "=" * 80)
    print("✓ TESTE CONCLUÍDO")
    print("=" * 80)

if __name__ == "__main__":
    testar_conversao_relogio()
