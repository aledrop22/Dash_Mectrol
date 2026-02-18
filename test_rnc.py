from app_qualidade import _campos_para_rnc


def run_tests():
    print("""\nTESTE DE CAMINHOS DE CAIXA RNC"""
          )

    # caso vazio
    d = {'Tipo_Refugo': '', 'Analise': False}
    print("1️⃣ Nenhum campo verdadeiro ->", _campos_para_rnc(d))

    # somente retrabalho
    d = {'Tipo_Refugo': 'RETRABALHO', 'Analise': False}
    print("2️⃣ Apenas retrabalho ->", _campos_para_rnc(d))

    # todos os flags
    d = {
        'Tipo_Refugo': 'RETRABALHO',
        'Analise': True,
        'Motivo_Usinagem': True,
        'Motivo_Medida': True,
        'Motivo_Outros': True,
    }
    campos = _campos_para_rnc(d)
    print("3️⃣ Todos os motivos + analise ->", campos)

    # refugo com sobra
    d = {'Tipo_Refugo': 'MORTE COM SOBRA', 'Analise': False}
    campos = _campos_para_rnc(d)
    print("4️⃣ Morto com sobra ->", campos)

    # simulando o trecho que constrói o pacote para RNC, garantindo
    # que as flags de motivo estão presentes
    motivos = {'Usinagem': True, 'Medida': False, 'Outros': True}
    pack = {
        'Tipo_Refugo': 'RETRABALHO',
        'Analise': False,
        'Obs_Inspetor': 'foo',
        'Obs_Colaborador': 'bar',
        'Sobra1': 0,
        'Inspetor': 'João',
        'Motivo_Usinagem': motivos['Usinagem'],
        'Motivo_Medida': motivos['Medida'],
        'Motivo_Outros': motivos['Outros'],
    }
    print("5️⃣ Pack simulado ->", pack)

    print("\n(Fim dos testes)\n")


if __name__ == "__main__":
    run_tests()
