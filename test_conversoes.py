#!/usr/bin/env python3
"""Testa a lógica de conversão de medidas entre Centesimal e Milesimal."""

def teste_converter_medida():
    """Testa a lógica de conversão de valores inteiros para decimal."""
    tipo_relogio = "Centesimal"
    
    # Cenário 1: Digitar 25 em Centesimal
    val = 25
    if val >= 1.0:
        divisor = 100.0 if tipo_relogio == "Centesimal" else 1000.0
        val = round(val / divisor, 3)
    print(f"Digitar 25 em Centesimal → {val}")  # Esperado: 0.25
    
    # Cenário 2: Mudar de Centesimal para Milesimal
    tipo_anterior = "Centesimal"
    tipo_novo = "Milesimal"
    fator = 0.1 if "Milesimal" in tipo_novo and "Centesimal" in tipo_anterior else 1.0
    val = 0.25 * fator
    val = round(val, 3)
    print(f"Mudar de Centesimal para Milesimal: 0.25 * 0.1 → {val}")  # Esperado: 0.025
    
    # Cenário 3: Digitar valor decimal diretamente em Milesimal (não convertir)
    val = 0.025
    if val >= 1.0:
        divisor = 1000.0
        val = val / divisor
    print(f"Digitar 0.025 em Milesimal (valor decimal, < 1.0) → {val}")  # Esperado: 0.025 (não muda)
    
    # Cenário 4: Digitar 25 em Milesimal (valor inteiro)
    val = 25
    if val >= 1.0:
        divisor = 1000.0
        val = round(val / divisor, 3)
    print(f"Digitar 25 em Milesimal → {val}")  # Esperado: 0.025
    
    # Cenário 5: Mudar de Milesimal para Centesimal
    tipo_anterior = "Milesimal"
    tipo_novo = "Centesimal"
    fator = 10.0 if "Centesimal" in tipo_novo and "Milesimal" in tipo_anterior else 1.0
    val = 0.025 * fator
    val = round(val, 3)
    print(f"Mudar de Milesimal para Centesimal: 0.025 * 10 → {val}")  # Esperado: 0.25

if __name__ == "__main__":
    teste_converter_medida()
