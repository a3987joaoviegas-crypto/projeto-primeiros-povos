import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="História de Portugal", layout="wide")

# 1. CORREÇÃO DO ERRO DOS FAVORITOS (Inicialização Segura)
if 'minhas_tribos' not in st.session_state:
    st.session_state.minhas_tribos = []

# Estilo Mundovivo Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 10px 0; font-size: 1.2rem; }
    .cc-card { background-color: #111111; color: #ffffff; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; height: 100%; }
    .img-box { width: 100%; height: 140px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; }
    .label { color: #888; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.85rem; font-weight: bold; color: #fff; }
    .info-box { background: #111111; padding: 20px; border-radius: 10px; border-top: 4px solid #ffffff; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COMPLETA (7 ÉPOCAS) ---
db = {
    "1. Pré-História": {"coord": [38.5, -8.0], "info": "Megalitismo e Caça.", "ids": [10, 11, 12, 13, 14, 15, 16, 17]},
    "2. Lusitanos": {"coord": [40.3, -7.5], "info": "Guerreiros da Serra da Estrela.", "ids": [20, 21, 22, 23, 24, 25, 26, 27]},
    "3. Conios": {"coord": [37.1, -8.2], "info": "Povo da escrita do Sul (Algarve).", "ids": [30, 31, 32, 33, 34, 35, 36, 37]},
    "4. Romanos": {"coord": [38.4, -7.9], "info": "A Lusitânia e as Cidades.", "ids": [40, 41, 42, 43, 44, 45, 46, 47]},
    "5. Visigodos": {"coord": [38.1, -7.8], "info": "Reinos Germânicos e Cristandade.", "ids": [50, 51, 52, 53, 54, 55, 56, 57]},
    "6. Árabes": {"coord": [37.2, -7.9], "info": "Al-Andalus e Ciência.", "ids": [60, 61, 62, 63, 64, 65, 66, 67]},
    "7. Descobrimentos": {"coord": [38.7, -9.2], "info": "Expansão Marítima Portuguesa.", "ids": [70, 71, 72, 73, 74, 75, 76, 77]}
}

# Nomes para preencher os itens
ferramentas_nomes = ["Lâmina", "Escudo", "Lança", "Vaso"]
animais_nomes = ["Lobo", "Cavalo", "Boi", "Águia"]

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MENU HISTÓRICO")
    modo = st.radio("IR PARA:", ["Explorar", "Linha do Tempo", "⭐ Minhas Tribos"])
    
    if modo == "Explorar":
        escolha = st.selectbox("POVO:", list(db.keys()))
    elif modo == "Linha do Tempo":
        escolha = st.select_slider("VIAGEM:", options=list(db.keys()))
    else:
        escolha = None

# --- LÓGICA DE EXIBIÇÃO ---
if modo == "⭐ Minhas Tribos":
    st.title("As Minhas Tribos Favoritas")
    if not st.session_state.minhas_tribos:
        st.warning("Ainda não tens tribos! Vai a 'Explorar' e clica em 'Entrar na Tribo'.")
    else:
        for tribo in st.session_state.minhas_tribos:
            st.markdown(f"<div class='info-box'>🛡️ Membro Honorário de: <b>{tribo}</b></div>", unsafe_allow_html=True)
else:
    # Exibição Normal
    dados = db[escolha]
    st.title(escolha)
    
    # Botão Entrar na Tribo (Favoritos)
    if st.button(f"➕ Entrar na Tribo {escolha}"):
        if escolha not in st.session_state.minhas_tribos:
            st.session_state.minhas_tribos.append(escolha)
            st.toast(f"Bem-vindo à tribo {escolha}!")

    st.markdown(f'<div class="info-box">{dados["info"]}</div>', unsafe_allow_html=True)
    
    # Mapa
    m = folium.Map(location=dados["coord"], zoom_start=7, tiles="CartoDB dark_matter")
    folium.Marker(dados["coord"], icon=folium.Icon(color="white")).add_to(m)
    st_folium(m, width="100%", height=300)

    # Ferramentas (4 Colunas)
    st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
    cols_f = st.columns(4)
    for i in range(4):
        with cols_f[i]:
            img_url = f"https://picsum.photos/id/{dados['ids'][i]}/400/300"
            st.markdown(f"""<div class='cc-card'>
                <img src='{img_url}' class='img-box'>
                <div class='label'>OBJETO</div>
                <div class='value'>{ferramentas_nomes[i]}</div>
            </div>""", unsafe_allow_html=True)

    # Animais (4 Colunas)
    st.markdown("<h3 class='section-title'>🪪 Cartão Animal</h3>", unsafe_allow_html=True)
    cols_a = st.columns(4)
    for i in range(4):
        with cols_a[i]:
            img_url_a = f"https://picsum.photos/id/{dados['ids'][i+4]}/400/300"
            st.markdown(f"""<div class='cc-card'>
                <img src='{img_url_a}' class='img-box'>
                <div class='label'>NOME</div>
                <div class='value'>{animais_nomes[i]}</div>
            </div>""", unsafe_allow_html=True)
