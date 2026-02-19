# Dashboard de Qualidade Mectrol

Sistema de gestão de qualidade para inspeção de peças e controle de não-conformidades (RNC).

## 🚀 Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com GitHub
3. Configure:
   - **Repository:** `aledrop22/Dash_Mectrol`
   - **Branch:** `main`
   - **Main file:** `app_qualidade.py`
4. Clique em "Deploy"

## 📋 Funcionalidades

- ✅ Gestão de inspeção de qualidade
- ✅ Controle de RNC (Relatório de Não Conformidade)
- ✅ Classificação automática de peças
- ✅ Sistema multi-peça
- ✅ Validação visual com avisos piscantes
- ✅ Exportação para Excel (CONFORME/NAO CONFORME)
- ✅ Análise de refugo com 4 quadrantes

## 🛠️ Tecnologias

- Python 3.x
- Streamlit
- Pandas
- OpenPyXL

## 📦 Instalação Local

```bash
pip install -r requirements.txt
streamlit run app_qualidade.py
```

## 📁 Estrutura de Pastas

```
BANCO_DADOS_MENSAIS/   # Banco de dados Excel
CRONOGRAMA 02-26/      # Cronogramas mensais
RNC 02-26/             # Relatórios de não conformidade
```
