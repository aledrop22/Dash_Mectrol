import streamlit as st
import pandas as pd
from datetime import date, datetime
import os
import re
import math
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font

st.set_page_config(page_title="Controle Qualidade", layout="wide")

# --- GERENCIAMENTO DE PASTAS E DATA (DINÂMICO) ---
hoje = date.today()
mes_ano_atual = hoje.strftime("%m-%y") # Ex: 02-26

# Nomes das Pastas
PASTA_RNC = f"RNC {mes_ano_atual}"
PASTA_DB = "BANCO_DADOS_MENSAIS"
PASTA_CRONOGRAMA = f"CRONOGRAMA {mes_ano_atual}"

# Garante que as pastas existam
for pasta in [PASTA_RNC, PASTA_DB, PASTA_CRONOGRAMA]:
    if not os.path.exists(pasta):
        os.makedirs(pasta)

# --- ARQUIVOS ---
ARQUIVO_CRONOGRAMA = os.path.join(PASTA_CRONOGRAMA, '1_CRONOGRAMA_QUALIDADE.xlsx')
NOME_DB_MES = f"Banco_Dados_Qualidade_{mes_ano_atual}.xlsx"
ARQUIVO_HISTORICO = os.path.join(PASTA_DB, NOME_DB_MES)
ARQUIVO_MODELO_RNC = 'USAR MODELO RNC.xlsx' 

# --- INICIALIZAÇÃO DE VARIÁVEIS DE SESSÃO ---
if 'relogio_anterior' not in st.session_state:
    st.session_state.relogio_anterior = "Centesimal"

for k in ['emp_e', 'bat_e', 'bat_d', 'emp_d']:
    if k not in st.session_state:
        st.session_state[k] = None

# --- LISTAS PADRÃO ---
LISTA_MAQUINAS = ["", "CNC-01", "CNC-30", "GL-01", "GL-02", "FRESA-01", "FRESA-02", "TORNO -01", "TORNO -02", "TORNO -03"]
LISTA_TORNEIROS = ["", "Everton", "Alex", "Pedro", "Leandro", "Vitor", "Vinicius", "Rodrigo", "Marcos", "Luiz", "Lucas"]

# --- CSS ---
st.markdown("""
    <style>
    .main .block-container { padding-top: 1rem !important; }
    .stMarkdown, .stSelectbox label, .stTextInput label, .stNumberInput label, .stDateInput label, .stTextArea label, .stRadio label { font-size: 18px !important; }
    .stSelectbox div[data-baseweb="select"], input { font-size: 16px !important; }
    div.stButton > button:first-child { background-color: #28a745; color: white; font-size: 24px; height: 3.5em; width: 100%; }
    .tolerancia-alert { background-color: #fff3cd; color: #856404; padding: 15px; border-left: 6px solid #ffc107; border-radius: 5px; margin: 10px 0; }
    .isento-alert { background-color: #d1ecf1; color: #0c5460; padding: 15px; border-left: 6px solid #17a2b8; border-radius: 5px; margin: 10px 0; }
    .classificacao-card { background-color: #e8f4f8; padding: 15px; border-left: 6px solid #17a2b8; border-radius: 5px; margin-bottom: 15px; }
    .classificacao-texto { font-size: 20px; font-weight: bold; color: #0c5460; }
    .reprov-section { background-color: #fff5f5; padding: 20px; border-radius: 10px; border: 2px solid #dc3545; margin-top: 10px; margin-bottom: 20px;}
    .reprov-title { color: #dc3545; font-weight: bold; font-size: 22px; margin-bottom: 15px; border-bottom: 1px solid #dc3545; padding-bottom: 5px; }
    .card-falha { background-color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6; height: 100%; }
    .card-header { font-weight: bold; font-size: 18px; margin-bottom: 10px; color: #333; border-bottom: 2px solid #eee; padding-bottom: 5px; }
    .card-sobra { background-color: #e2e3e5; padding: 15px; border-radius: 8px; border: 1px solid #d6d8db; margin-top: 15px; margin-bottom: 15px; }
    .card-sobra-header { font-weight: bold; color: #383d41; margin-bottom: 10px; font-size: 18px; }
    section[data-testid="stSidebar"] .block-container { padding-top: 1rem; }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÕES ---

def ajustar_casas_relogio():
    novo = st.session_state.tipo_relogio_key
    antigo = st.session_state.get('relogio_anterior', "Centesimal")
    if "Milesimal" in novo and "Centesimal" in antigo: fator = 0.1
    elif "Centesimal" in novo and "Milesimal" in antigo: fator = 10.0
    else: fator = 1.0
    if fator != 1.0:
        for k in ['emp_e', 'bat_e', 'bat_d', 'emp_d']:
            if st.session_state.get(k) is not None:
                st.session_state[k] = round(st.session_state[k] * fator, 3)
    st.session_state.relogio_anterior = novo

def converter_medida(key_name):
    if key_name in st.session_state and st.session_state[key_name] is not None:
        valor_atual = st.session_state[key_name]
        tipo = st.session_state.get("tipo_relogio_key", "Centesimal")
        if valor_atual >= 1.0:
            if "Milesimal" in tipo: st.session_state[key_name] = valor_atual / 1000.0
            else: st.session_state[key_name] = valor_atual / 100.0

def formatar_hora_automatica():
    if "hora_entrada_key" in st.session_state:
        valor = st.session_state.hora_entrada_key
        limpo = ''.join(filter(str.isdigit, str(valor)))
        if len(limpo) in [1, 2]: 
            try:
                h = int(limpo)
                if 0 <= h <= 23:
                    periodo = "Manhã" if h < 12 else "Tarde" if h < 18 else "Noite"
                    st.session_state.hora_entrada_key = f"{h:02d}:00 - {periodo}"
            except: pass
        elif len(limpo) == 3: limpo = "0" + limpo
        if len(limpo) == 4:
            try:
                h = int(limpo[:2]); m = int(limpo[2:])
                if 0 <= h <= 23 and 0 <= m <= 59:
                    periodo = "Manhã" if h < 12 else "Tarde" if h < 18 else "Noite"
                    st.session_state.hora_entrada_key = f"{h:02d}:{m:02d} - {periodo}"
            except: pass

def definir_prioridade(transportadora):
    transp = str(transportadora).upper()
    if "MIGUEL" in transp: return "1_ALTA"
    elif "BIGTRANS" in transp: return "2_MEDIA"
    elif "ALFA" in transp or "RODONAVES" in transp: return "3_BAIXA"
    else: return "4_OUTRAS"

def arredondar_sobra_10(valor):
    try:
        if isinstance(valor, str): valor = float(valor.replace(',', '.'))
        return int(valor // 10) * 10
    except: return 0

def extrair_medidas_peca(descricao):
    try:
        match = re.search(r'-([\d.,]+)-([\d.,]+)-', descricao)
        if match:
            raw_usin = match.group(1).replace('.', '').replace(',', '.')
            return arredondar_sobra_10(float(raw_usin))
        return 0
    except: return 0

def verificar_isencao_tamanho(descricao):
    try:
        desc_upper = descricao.upper()
        if "FUSO" not in desc_upper: return False, False
        match_diam = re.search(r'R(\d+)', desc_upper)
        diametro = int(match_diam.group(1)) if match_diam else 0
        match_len = re.search(r'-([\d.,]+)-0[,.]0', desc_upper)
        comprimento = float(match_len.group(1).replace('.', '').replace(',', '.')) if match_len else 0.0
        if diametro in [63, 80, 100] and comprimento > 2400: return True, True
        return True, False
    except: return False, False

def tratar_valor_numerico_string(valor):
    try:
        s = str(valor)
        return s[:-2] if s.endswith('.0') else s
    except: return str(valor)

def gerar_nome_arquivo_rnc(pedido, cliente, item):
    try:
        pedido_limpo = tratar_valor_numerico_string(pedido)
        item_limpo = tratar_valor_numerico_string(item)
        cliente_curto = str(cliente).strip().split(' ')[0]
        nome_limpo = f"RNC - {pedido_limpo} - {cliente_curto} - {item_limpo}.xlsx"
        nome_limpo = re.sub(r'[\\/*?:"<>|]', "", nome_limpo)
        return os.path.join(PASTA_RNC, nome_limpo)
    except: return "RNC_GERADA.xlsx"

# --- PREENCHIMENTO DO MODELO RNC ---
def preencher_modelo_rnc_existente(dados_rnc, nome_saida):
    try:
        if not os.path.exists(ARQUIVO_MODELO_RNC):
            st.error(f"⚠️ O modelo '{ARQUIVO_MODELO_RNC}' não foi encontrado na pasta do script!")
            return False

        wb = load_workbook(ARQUIVO_MODELO_RNC)
        ws = wb.active

        # --- AJUSTE DE ALTURA DA LINHA 6 ---
        ws.row_dimensions[6].height = 21

        # Mapeamento
        mapa = {
            "Data:": date.today().strftime("%d/%m/%Y"),
            "OP": tratar_valor_numerico_string(dados_rnc['OP']),
            "Item": dados_rnc['Descricao'],
            "Quantidade na OP": dados_rnc['Qtd_Total'],
            "Quantidade de Falha": dados_rnc['Qtd_Reprovada'],
            "PV": tratar_valor_numerico_string(dados_rnc.get('Pedido', '')),
            "Cliente": dados_rnc['Cliente'],
            "Máquina": dados_rnc['Maquina'],
            "Operador": dados_rnc['Operador'],
            "Descrição do ocorrido": dados_rnc['Descricao_Ocorrido'],
            "Observação do colaborador": dados_rnc['Obs_Colaborador'],
            "Possível causa": dados_rnc['Obs_Inspetor'],
            "Medida Sobra (se houver)": f"{dados_rnc['Sobra1']} mm" if dados_rnc['Sobra1'] else "",
            "Responsável": dados_rnc['Inspetor'] # AGORA USA O NOME DO INSPETOR
        }

        # Checkboxes
        tipo = dados_rnc['Tipo_Refugo']
        analise = dados_rnc.get('Analise', False)
        
        campos_para_marcar = []
        if tipo == "RETRABALHO": campos_para_marcar.append("RETRABALHO")
        if "MORTE" in tipo: campos_para_marcar.append("REFUGO")
        if "SOBRA" in tipo: campos_para_marcar.append("SOBRA")
        if analise: campos_para_marcar.append("ANALISE")

        def get_master_cell(sheet, row, col):
            for merged_range in sheet.merged_cells.ranges:
                if (row >= merged_range.min_row and row <= merged_range.max_row and
                    col >= merged_range.min_col and col <= merged_range.max_col):
                    return sheet.cell(merged_range.min_row, merged_range.min_col)
            return sheet.cell(row, col)

        for row in ws.iter_rows(min_row=1, max_row=60, min_col=1, max_col=10):
            for cell in row:
                if cell.value:
                    val_str = str(cell.value).strip()
                    
                    # 1. Texto
                    for chave, valor in mapa.items():
                        if val_str.startswith(chave):
                            target = get_master_cell(ws, cell.row, cell.column + 1)
                            target.value = valor
                            
                            # Alinhamento Padrão
                            alinhamento = Alignment(wrap_text=True, vertical='center')
                            
                            # --- AJUSTE DE ALINHAMENTO DO RESPONSÁVEL ---
                            if chave == "Responsável":
                                alinhamento = Alignment(horizontal='center', vertical='center', wrap_text=True)
                            
                            target.alignment = alinhamento
                    
                    # 2. Checkboxes (X)
                    if val_str in ["RETRABALHO", "REFUGO", "SOBRA", "ANALISE"]:
                        target = get_master_cell(ws, cell.row, cell.column + 1)
                        target.value = "" 
                        
                        if val_str in campos_para_marcar:
                            target.value = "X"
                            target.font = Font(bold=True, size=12, name='Arial')
                            target.alignment = Alignment(horizontal='center', vertical='center')

        wb.save(nome_saida)
        return True

    except Exception as e:
        st.error(f"Erro ao preencher o modelo Excel: {e}")
        return False

# --- CARREGA DADOS (LENDO DA PASTA 'CRONOGRAMA DO MES') ---
@st.cache_data(ttl=600) 
def carregar_dados():
    try:
        if not os.path.exists(ARQUIVO_CRONOGRAMA): return None
        df = pd.read_excel(ARQUIVO_CRONOGRAMA, engine='openpyxl')
        df = df.fillna("")
        df['Atividade PCP'] = df['Atividade PCP'].astype(str).str.upper().str.strip()
        df['Cliente'] = df['Cliente'].astype(str).str.strip()
        df = df[df['OP'] != ""]
        df['Previsão'] = pd.to_datetime(df['Previsão'], errors='coerce')
        df['Prioridade_Logistica'] = df['Transportadora'].apply(definir_prioridade)
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel (Verifique se está na pasta '{PASTA_CRONOGRAMA}'): {e}")
        return pd.DataFrame()

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("### ⚙️ Painel de Controle")
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")
    inspetor_selecionado = st.selectbox("👷 Quem é você?", ["", "Alexandre", "Pedro", "Lilian", "Ygor"])
    st.markdown("---")
    ver_todas_datas = st.checkbox("Ver Todas as Datas", value=False)
    data_filtro = st.date_input("Selecione o Dia:", date.today(), format="DD/MM/YYYY") if not ver_todas_datas else None
    st.markdown("---")
    filtro_prioridade = []
    if st.checkbox("🔴 1º Alta", value=True): filtro_prioridade.append("1_ALTA")
    if st.checkbox("🟡 2º Média", value=True): filtro_prioridade.append("2_MEDIA")
    if st.checkbox("🟢 3º Baixa", value=True): filtro_prioridade.append("3_BAIXA")
    if st.checkbox("⚪ Outras", value=True): filtro_prioridade.append("4_OUTRAS")
    st.markdown("---")
    LISTA_ATIVIDADES = ["U - USINAGEM", "I - Industrialização", "H - Indust/Usin", "P - Producao", "S - Separacao"]
    filtro_atividade = [ativ for ativ in LISTA_ATIVIDADES if st.checkbox(ativ, value=("USINAGEM" in ativ))]

# --- APP ---
df = carregar_dados()
st.title("📱 Apontamento de Qualidade")

if df is None: st.error(f"🚨 Arquivo '{ARQUIVO_CRONOGRAMA}' não encontrado! Coloque-o na pasta '{PASTA_CRONOGRAMA}'.")
elif df.empty: st.warning("Arquivo vazio.")
else:
    df_filtrado_data = df.copy()
    if not ver_todas_datas and data_filtro:
        df_filtrado_data = df[df['Previsão'].dt.date == data_filtro]
        if df_filtrado_data.empty: st.info(f"📅 Nenhuma produção agendada para **{data_filtro.strftime('%d/%m/%Y')}**.")

    if not df_filtrado_data.empty:
        df_final = df_filtrado_data[
            (df_filtrado_data['Atividade PCP'].isin(filtro_atividade)) & 
            (df_filtrado_data['Prioridade_Logistica'].isin(filtro_prioridade))
        ]
        
        if df_final.empty:
             st.markdown("<h3 style='text-align: center; color: gray;'>🚫 Sem OPs com os filtros atuais</h3>", unsafe_allow_html=True)
        else:
            lista_clientes = sorted(df_final['Cliente'].unique())
            cliente_selecionado = st.selectbox("1️⃣ Selecione o Cliente:", lista_clientes)
            st.markdown("<br>", unsafe_allow_html=True)
            
            df_cliente = df_final[df_final['Cliente'] == cliente_selecionado]
            df_cliente['Rotulo_OP'] = df_cliente['OP'].astype(str) + " - " + df_cliente['Descrição do Item'].astype(str)
            op_rotulo = st.selectbox("2️⃣ Selecione a Peça/OP:", sorted(df_cliente['Rotulo_OP'].unique()))
            
            op_escolhida_num = op_rotulo.split(" - ")[0]
            dados_op = df_cliente[df_cliente['OP'].astype(str) == op_escolhida_num].iloc[0]

            valor_padrao_qtd = 1
            qtd_visual = "N/D"
            for col in dados_op.index:
                if "QTD" in col.upper() or "QUANT" in col.upper():
                    try:
                        raw_val = str(dados_op[col]).strip().replace(',', '.')
                        if raw_val and float(raw_val) > 0: valor_padrao_qtd = int(float(raw_val))
                        qtd_visual = str(valor_padrao_qtd)
                        break
                    except: continue

            col_info1, col_info2, col_info3 = st.columns([2, 1.5, 1])
            with col_info1: st.info(f"📦 **Peça:**\n{dados_op.get('Descrição do Item', '')}\n\n🔢 **Qtd Prevista:** {qtd_visual}")
            with col_info2:
                prio = dados_op['Prioridade_Logistica']
                txt_t = f"🚚 **Transp:** {dados_op.get('Transportadora', 'Não informada')}"
                if prio == "1_ALTA": st.error(f"🔴 **PRIORIDADE ALTA**\n\n{txt_t}")
                elif prio == "2_MEDIA": st.warning(f"🟡 **PRIORIDADE MÉDIA**\n\n{txt_t}")
                else: st.info(f"⚪ **NORMAL**\n\n{txt_t}")
            with col_info3:
                data_prev = dados_op.get('Previsão', '')
                if isinstance(data_prev, (pd.Timestamp, datetime)): data_prev = data_prev.strftime('%d/%m/%Y')
                st.info(f"📅 **Previsão:**\n{data_prev}")

            desc_upper = dados_op.get('Descrição do Item', '').upper()
            padrao_fuso_ret = False; padrao_fuso_lam = False; padrao_fuso_lam_prec = False 
            padrao_guia = False; padrao_bloco = False
            
            if "GUIA" in desc_upper or "TRILHO" in desc_upper: padrao_guia = True
            elif "BLOCO" in desc_upper or "PATIM" in desc_upper: padrao_bloco = True
            else:
                tem_mop = "(MOP)" in desc_upper
                if "0,023" in desc_upper and not tem_mop: padrao_fuso_lam_prec = True
                elif "0,05" in desc_upper: padrao_fuso_lam = True
                elif tem_mop or any(x in desc_upper for x in ["0,008", "0,012", "0,018"]): padrao_fuso_ret = True
            
            tem_adaptado = "ADAPTADO" in desc_upper
            medida_sobra_padrao = extrair_medidas_peca(desc_upper)
            eh_fuso_peca, isento_por_tamanho = verificar_isencao_tamanho(desc_upper)

            st.markdown("---")
            st.subheader("📝 Dados da Inspeção")
            
            c_time1, c_time2, c_time3, c_time4 = st.columns(4)
            with c_time1: data_producao = st.date_input("Data Produção (Hoje)", date.today(), format="DD/MM/YYYY")
            with c_time2: data_chegada = st.date_input("Data Chegada (Anterior)", value=None, format="DD/MM/YYYY")
            with c_time3: st.text_input("Hora Entrada (Ex: 7, 13 ou 1530)", max_chars=20, placeholder="HH:MM", key="hora_entrada_key", on_change=formatar_hora_automatica)
            with c_time4: st.text_input("Líder Responsável", value="Pedro Miguel", disabled=True)

            st.markdown("---")
            c_geral1, c_geral2 = st.columns(2)
            with c_geral1: qtd_pecas = st.number_input("Qtd Produzida (Total)*", min_value=1, step=1, value=valor_padrao_qtd)
            with c_geral2: cod_castanha = st.text_input("Código Castanha*", placeholder="Ex: SF043V3008")

            st.markdown("---")
            if isento_por_tamanho:
                st.markdown(f"""<div class='isento-alert'><h3>📏 NÃO PRECISA REALIZAR INSPEÇÃO POR CONTA DO TAMANHO</h3>Esta peça excede os limites de medição na mesa (>2400mm e >R63).</div>""", unsafe_allow_html=True)
            
            c_med_tit, c_med_rad = st.columns([1, 2])
            with c_med_tit: st.markdown("#### Medições Técnicas")
            with c_med_rad:
                tipo_relogio = st.radio("Instrumento de Medição:", ["Centesimal", "Milesimal"], horizontal=True, key="tipo_relogio_key", on_change=ajustar_casas_relogio)

            if "Milesimal" in tipo_relogio: formato_medida = "%.3f"; passo_medida = 0.001; limite_tolerancia = 0.050
            else: formato_medida = "%.2f"; passo_medida = 0.01; limite_tolerancia = 0.50

            col_tec_esq, col_tec_meio, col_tec_dir = st.columns([1, 0.1, 1])
            with col_tec_esq:
                st.markdown("##### ⬅️ Lado ESQUERDO")
                st.number_input("Empenamento ESQ (mm)*", value=st.session_state.emp_e, placeholder="Insira...", step=passo_medida, format=formato_medida, key="emp_e", on_change=converter_medida, args=("emp_e",))
                st.number_input("Batimento ESQ (mm)*", value=st.session_state.bat_e, placeholder="Insira...", step=passo_medida, format=formato_medida, key="bat_e", on_change=converter_medida, args=("bat_e",))
            with col_tec_dir:
                st.markdown("##### ➡️ Lado DIREITO")
                st.number_input("Batimento DIR (mm)*", value=st.session_state.bat_d, placeholder="Insira...", step=passo_medida, format=formato_medida, key="bat_d", on_change=converter_medida, args=("bat_d",))
                st.number_input("Empenamento DIR (mm)*", value=st.session_state.emp_d, placeholder="Insira...", step=passo_medida, format=formato_medida, key="emp_d", on_change=converter_medida, args=("emp_d",))

            vals = [st.session_state.emp_e, st.session_state.bat_e, st.session_state.bat_d, st.session_state.emp_d]
            vals_limpos = [v if v is not None else 0.0 for v in vals]
            max_medido = max(vals_limpos) if vals_limpos else 0.0
            
            autorizacao_lider = False 
            if max_medido > limite_tolerancia:
                st.markdown(f"""<div class='tolerancia-alert'><h3>⚠️ ATENÇÃO: MEDIDA FORA DA TOLERÂNCIA!</h3>Necessário autorização do Líder.</div>""", unsafe_allow_html=True)
                autorizacao_lider = st.checkbox("☑️ Líder AUTORIZOU a liberação?")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📊 Classificação do Produto")
            st.markdown(f"""<div class='classificacao-card'><div class='classificacao-texto'>🔩 Peça: {dados_op.get('Descrição do Item', '')}<br>🔢 Qtd: {qtd_pecas}</div></div>""", unsafe_allow_html=True)
            
            cc1, cc2, cc3, cc4 = st.columns(4)
            with cc1:
                sel_fuso_ret = st.checkbox("Fuso Retificado", value=(padrao_fuso_ret and not tem_adaptado))
                sel_fuso_ret_adpt = st.checkbox("Fuso Ret. Adaptado", value=(padrao_fuso_ret and tem_adaptado))
            with cc2:
                sel_cast_ret_adpt = st.checkbox("Castanha Ret. Adaptada")
                sel_fuso_lam_prec = st.checkbox("Fuso Laminado PRECISÃO", value=(padrao_fuso_lam_prec and not tem_adaptado))
            with cc3:
                sel_fuso_lam = st.checkbox("Fuso Laminado", value=(padrao_fuso_lam and not tem_adaptado))
                sel_fuso_lam_adpt = st.checkbox("Fuso Lam. Adaptado", value=(padrao_fuso_lam and tem_adaptado))
                sel_cast_lam_adpt = st.checkbox("Castanha Lam. Adaptada")
            with cc4:
                sel_guia = st.checkbox("Guia", value=padrao_guia)
                sel_bloco = st.checkbox("Bloco", value=padrao_bloco)
            
            st.markdown("---")

            # --- CONTROLE DE REFUGO ---
            st.markdown("##### ⚠️ Controle de Refugo")
            qtd_reprovada = st.number_input("Qtd Reprovada", min_value=0, step=1, value=0)
            
            onde_falha_keys = ["Usinagem", "Inspeção", "Desenho", "Programação CNC", "Produção", "Gerar op", "PCP"]
            motivo_falha_keys = ["Medida não conforme", "Usinagem não conforme"]
            detalhe_falha_keys = ["Acabamento Ruim", "Concentricidade", "Craterizada", "Estética", "Rebarba", "Faltou Chaveta", "Desenho Errado"]
            motivos = {k: False for k in onde_falha_keys + motivo_falha_keys + detalhe_falha_keys}
            
            tipo_refugo = None; maquina_refugo = ""; operador_refugo = ""; obs_inspetor = ""; obs_colaborador = ""; sobra_medida1 = 0
            em_analise = False

            if qtd_reprovada > 0:
                st.markdown("<div class='reprov-section'><div class='reprov-title'>🔴 PRODUTOS DE REFUGO</div>", unsafe_allow_html=True)
                
                c_tipo, c_maq, c_ope = st.columns([2, 1, 1])
                with c_tipo:
                    st.markdown("**Tipo:**")
                    tipo_refugo = st.radio("Tipo", ["RETRABALHO", "MORTE COM SOBRA", "MORTE SEM SOBRA"], horizontal=True, label_visibility="collapsed")
                    em_analise = st.checkbox("Em Análise (Não Finalizado)")
                with c_maq: maquina_refugo = st.selectbox("Máquina:", LISTA_MAQUINAS)
                with c_ope: operador_refugo = st.selectbox("Torneiro:", LISTA_TORNEIROS)
                
                if tipo_refugo in ["MORTE COM SOBRA", "MORTE SEM SOBRA"]:
                    st.markdown(f"""<div class='card-sobra'><div class='card-sobra-header'>📏 Comprimento da Sobra (Rosca Útil)?</div><small>Valor sugerido: Primeiro número da descrição arredondado.</small></div>""", unsafe_allow_html=True)
                    sobra_medida1 = st.number_input("Informe a medida (mm):", value=medida_sobra_padrao, step=10)

                st.markdown("<br>", unsafe_allow_html=True)
                col_card1, col_card2, col_card3 = st.columns(3)
                with col_card1:
                    st.markdown("""<div class='card-falha'><div class='card-header'>1. Onde houve a falha</div>""", unsafe_allow_html=True)
                    for k in onde_falha_keys:
                        txt = "Instr. Corte Errado" if k == "Gerar op" else k
                        motivos[k] = st.checkbox(txt)
                    st.markdown("</div>", unsafe_allow_html=True)
                with col_card2:
                    st.markdown("""<div class='card-falha'><div class='card-header'>2. Motivo da falha</div>""", unsafe_allow_html=True)
                    for k in motivo_falha_keys:
                        txt = "Usinagem ñ conforme" if k == "Usinagem não conforme" else k
                        motivos[k] = st.checkbox(txt)
                    st.markdown("</div>", unsafe_allow_html=True)
                with col_card3:
                    st.markdown("""<div class='card-falha'><div class='card-header'>3. Detalhe da falha</div>""", unsafe_allow_html=True)
                    for k in detalhe_falha_keys: motivos[k] = st.checkbox(k)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**📝 Detalhes do Ocorrido:**")
                obs_inspetor = st.text_area("O que o Inspetor encontrou (Avaria):", placeholder="Descreva tecnicamente...")
                obs_colaborador = st.text_area("Observação do Colaborador (Causa):", placeholder="Justificativa do operador...")
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("✅ SALVAR NO HISTÓRICO"):
                erros = []
                if not inspetor_selecionado: erros.append("⚠️ Selecione o INSPETOR!")
                if not cod_castanha: erros.append("⚠️ Preencha o CÓDIGO DA CASTANHA!")
                if max_medido > limite_tolerancia and not autorizacao_lider: erros.append(f"⛔ BLOQUEADO: Medidas fora da tolerância!")
                if eh_fuso_peca and not isento_por_tamanho:
                    if not any(v and v > 0 for v in vals_limpos): erros.append("⚠️ Fuso requer inspeção!")

                any_motivo = any(motivos.values())
                if qtd_reprovada > 0:
                    if not tipo_refugo: erros.append("⚠️ Selecione o TIPO DE REFUGO.")
                    if not any_motivo: erros.append("⚠️ Marque o MOTIVO.")
                    if not maquina_refugo: erros.append("⚠️ Selecione a MÁQUINA.")
                    if not operador_refugo: erros.append("⚠️ Selecione o TORNEIRO.")

                classif_ret = (sel_fuso_ret or sel_fuso_ret_adpt or sel_cast_ret_adpt)
                classif_lam = (sel_fuso_lam or sel_fuso_lam_adpt or sel_cast_lam_adpt or sel_fuso_lam_prec)
                classif_guia_bloco = (sel_guia or sel_bloco)
                if classif_ret and classif_lam: erros.append("⛔ Erro: Retificado + Laminado")
                if (classif_ret or classif_lam) and classif_guia_bloco: erros.append("⛔ Erro: Fuso + Guia/Bloco")
                if not (classif_ret or classif_lam or classif_guia_bloco): erros.append("⚠️ Selecione uma Classificação.")

                if erros:
                    for erro in erros: st.error(erro)
                else:
                    qtd_aprovada = max(0, qtd_pecas - qtd_reprovada)
                    hora_final = st.session_state.get("hora_entrada_key", "")
                    obs_final_excel = f"AVARIA: {obs_inspetor} | CAUSA: {obs_colaborador}" if qtd_reprovada > 0 else ""
                    
                    nova_linha = {
                        'Data Registro': date.today().strftime("%d/%m/%Y"), 
                        'Hora Saída': datetime.now().strftime("%H:%M"),
                        'Inspetor': inspetor_selecionado,
                        'Inspetor Responsável': "Pedro Miguel",
                        'Data Chegada': data_chegada.strftime("%d/%m/%Y") if data_chegada else "",
                        'Hora Entrada': hora_final,
                        'Data Produção': data_producao.strftime("%d/%m/%Y"), 
                        'OP': op_escolhida_num,
                        'Cliente': dados_op.get('Cliente', ''), 
                        'Descrição': dados_op.get('Descrição do Item', ''),
                        'Transportadora': dados_op.get('Transportadora', ''), 
                        'Pedido': dados_op.get('Pedido', ''),
                        'Codigo': dados_op.get('Código Item', ''),
                        'Qtd Total': qtd_pecas,
                        'Peças produzidas': qtd_pecas,
                        'Aprovado': qtd_aprovada,
                        'Reprovado': qtd_reprovada,
                        'Tipo Refugo': tipo_refugo if qtd_reprovada > 0 else '',
                        'Sobra Medida 1': sobra_medida1,
                        'Sobra Medida 2': '', 
                        'Maquina': maquina_refugo,
                        'Operador': operador_refugo,
                        'Cód. Castanha': cod_castanha, 
                        'Bat. Esq': st.session_state.bat_e if st.session_state.bat_e else 0.0, 
                        'Bat. Dir': st.session_state.bat_d if st.session_state.bat_d else 0.0,
                        'Emp. Esq': st.session_state.emp_e if st.session_state.emp_e else 0.0, 
                        'Emp. Dir': st.session_state.emp_d if st.session_state.emp_d else 0.0, 
                        'Obs': obs_final_excel, 
                        'Status': 'Finalizado',
                        'Aprovação Especial': "Liberado Fora Tol." if autorizacao_lider else "",
                        'Fuso Retificado': qtd_pecas if sel_fuso_ret else '',
                        'Fuso Retificado Adaptado': qtd_pecas if sel_fuso_ret_adpt else '',
                        'Castanha Retificada Adaptada': qtd_pecas if sel_cast_ret_adpt else '',
                        'Fuso Laminado': qtd_pecas if sel_fuso_lam else '',
                        'Fuso Laminado PRECISÃO': qtd_pecas if sel_fuso_lam_prec else '',
                        'Fuso Laminado Adaptado': qtd_pecas if sel_fuso_lam_adpt else '',
                        'Castanha Laminada Adaptada': qtd_pecas if sel_cast_lam_adpt else '',
                        'Guia': qtd_pecas if sel_guia else '',
                        'Bloco': qtd_pecas if sel_bloco else '',
                        'Usinagem': 'X' if motivos.get("Usinagem") else '',
                        'Inspeção': 'X' if motivos.get("Inspeção") else '',
                        'Desenho': 'X' if motivos.get("Desenho") else '',
                        'Programação CNC': 'X' if motivos.get("Programação CNC") else '',
                        'Produção': 'X' if motivos.get("Produção") else '',
                        'Gerar op': 'X' if motivos.get("Gerar op") else '',
                        'PCP': 'X' if motivos.get("PCP") else '',
                        'Medida não conforme': 'X' if motivos.get("Medida não conforme") else '',
                        'Usinagem não conforme': 'X' if motivos.get("Usinagem não conforme") else '',
                        'Acabamento Ruim': 'X' if motivos.get("Acabamento Ruim") else '',
                        'Concentricidade': 'X' if motivos.get("Concentricidade") else '',
                        'Craterizada': 'X' if motivos.get("Craterizada") else '',
                        'Estética': 'X' if motivos.get("Estética") else '',
                        'Rebarba': 'X' if motivos.get("Rebarba") else '',
                        'Faltou Chaveta': 'X' if motivos.get("Faltou Chaveta") else '',
                        'Desenho Errado': 'X' if motivos.get("Desenho Errado") else ''
                    }
                    
                    df_novo = pd.DataFrame([nova_linha])
                    
                    rnc_gerado = False
                    nome_rnc = ""
                    if qtd_reprovada > 0:
                        nome_rnc = gerar_nome_arquivo_rnc(dados_op.get('Pedido', ''), dados_op.get('Cliente', ''), dados_op.get('Código Item', ''))
                        
                        onde_str = ", ".join([k for k in onde_falha_keys if motivos.get(k)])
                        motivo_str = ", ".join([k for k in motivo_falha_keys if motivos.get(k)])
                        detalhe_str = ", ".join([k for k in detalhe_falha_keys if motivos.get(k)])
                        
                        desc_completa = []
                        if onde_str: desc_completa.append(f"Onde: {onde_str}")
                        if motivo_str: desc_completa.append(f"Motivo: {motivo_str}")
                        if detalhe_str: desc_completa.append(f"Detalhe: {detalhe_str}")
                        
                        dados_rnc_pack = {
                            'OP': op_escolhida_num,
                            'Cliente': dados_op.get('Cliente', ''),
                            'Descricao': dados_op.get('Descrição do Item', ''),
                            'Qtd_Total': qtd_pecas,
                            'Qtd_Reprovada': qtd_reprovada,
                            'Pedido': dados_op.get('Pedido', ''),
                            'Maquina': maquina_refugo,
                            'Operador': operador_refugo,
                            'Tipo_Refugo': tipo_refugo,
                            'Analise': em_analise,
                            'Descricao_Ocorrido': " | ".join(desc_completa),
                            'Obs_Inspetor': obs_inspetor,
                            'Obs_Colaborador': obs_colaborador,
                            'Sobra1': sobra_medida1,
                            'Inspetor': inspetor_selecionado
                        }
                        
                        rnc_gerado = preencher_modelo_rnc_existente(dados_rnc_pack, nome_rnc)

                    try:
                        if not os.path.exists(ARQUIVO_HISTORICO): df_novo.to_excel(ARQUIVO_HISTORICO, index=False)
                        else:
                            df_ex = pd.read_excel(ARQUIVO_HISTORICO)
                            pd.concat([df_ex, df_novo], ignore_index=True).to_excel(ARQUIVO_HISTORICO, index=False)
                        
                        msg = f"Sucesso! OP {op_escolhida_num} salva."
                        if rnc_gerado: msg += f" 📄 RNC gerada: '{nome_rnc}' (Usando Modelo)."
                        st.success(msg)
                    except PermissionError: st.error("⚠️ Feche o arquivo Excel antes de salvar!")
                    except Exception as e: st.error(f"Erro técnico: {e}")