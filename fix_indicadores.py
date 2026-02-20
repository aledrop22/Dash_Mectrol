import os
import re

with open('app_qualidade.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Procurar usando regex para pegar qualquer caractere antes de "Indicadores"
inicio = re.search(r'elif pagina == ".+ Indicadores":', content)
fim_match = re.search(r'elif pagina == ".+ Pré Carga":', content)

if inicio and fim_match:
    inicio_pos = inicio.start()
    fim_pos = fim_match.start()
    
    novo_bloco = '''elif pagina == "📊 Indicadores":
    st.title("📊 Indicadores da Qualidade")
    st.markdown("Acompanhamento do desempenho diário e mensal da qualidade")
    st.markdown("---")
    
    arquivo_dash = '3.1_DASH_MENSAL_01_26.xlsx'
    
    with st.expander("🔍 Debug", expanded=False):
        st.write(f"Dir: {os.getcwd()}")
        st.write(f"Arquivo existe: {os.path.exists(arquivo_dash)}")
        if not os.path.exists(arquivo_dash):
            arquivos = [f for f in os.listdir('.') if f.endswith('.xlsx')]
            st.write("Excel files:", arquivos)
    
    if not os.path.exists(arquivo_dash):
        st.error(f"Arquivo não encontrado: {arquivo_dash}")
        st.info("Faça upload do arquivo 3.1_DASH_MENSAL_01_26.xlsx")
    else:
        try:
            st.markdown("### 📦 Peças Inspecionadas")
            with st.spinner("Carregando..."):
                df_lanc = pd.read_excel(arquivo_dash, sheet_name='Lançamentos', header=None)
                st.success(f"Carregado: {df_lanc.shape[0]} linhas")
                valores = df_lanc.iloc[298, 2:10].tolist()
                meses = ['Jun/25', 'Jul/25', 'Ago/25', 'Set/25', 'Out/25', 'Nov/25', 'Dez/25', 'Jan/26']
                
                cols = st.columns(4)
                for i in range(4):
                    v = int(valores[i]) if pd.notna(valores[i]) else 0
                    cols[i].metric(f"{meses[i]}", f"{v} peças")
                
                cols2 = st.columns(4)
                for i in range(4):
                    v = int(valores[i+4]) if pd.notna(valores[i+4]) else 0
                    cols2[i].metric(f"{meses[i+4]}", f"{v} peças")
                
                total = sum([int(v) if pd.notna(v) else 0 for v in valores])
                st.markdown("---")
                t1, t2, t3 = st.columns(3)
                t1.metric("Total", f"{total} peças")
                t2.metric("Média Mensal", f"{total//8} peças")
                t3.metric("Período", "8 meses")
                
                st.markdown("#### Evolução Mensal")
                df_g = pd.DataFrame({'Mês': meses, 'Peças': [int(v) if pd.notna(v) else 0 for v in valores]})
                st.bar_chart(df_g.set_index('Mês'))
            
            st.markdown("---")
            st.markdown("### ⚙️ Configuração")
            try:
                df_cfg = pd.read_excel(arquivo_dash, sheet_name='CONFIGURAÇÃO ', header=None)
                st.success(f"Carregado: {df_cfg.shape}")
                st.dataframe(df_cfg.head(30), use_container_width=True)
            except Exception as e:
                st.warning(f"Erro: {e}")
            
            st.markdown("---")
            st.markdown("### 🔧 Indicadores Usinagem")
            try:
                df_usin = pd.read_excel(arquivo_dash, sheet_name='Indicadores Usinagem', header=None)
                st.success(f"Carregado: {df_usin.shape}")
                st.dataframe(df_usin.head(30), use_container_width=True)
            except Exception as e:
                st.warning(f"Erro: {e}")
        except Exception as e:
            st.error(f"Erro ao carregar: {e}")
            st.exception(e)

'''
    content_novo = content[:inicio_pos] + novo_bloco + content[fim_pos:]
    
    with open('app_qualidade.py', 'w', encoding='utf-8') as f:
        f.write(content_novo)
    
    print("✅ Bloco de Indicadores atualizado com sucesso!")
else:
    print(f"❌ Blocos não encontrados")
    print(f"Inicio: {inicio}")
    print(f"Fim: {fim_match}")
