import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="História de Portugal", layout="wide")

# Inicializar favoritos
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = {}

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

# --- DATABASE COMPLETA (7 ÉPOCAS / 4 ITENS CADA) ---
db = {
    "1. Pré-História": {
        "coord": [38.5, -8.0], "info": "Megalitismo e Caça.",
        "ferramentas": [
            {"n": "Biface Silex", "img": "https://loremflickr.com/400/300/stone,tool/all"},
            {"n": "Arco Caça", "img": "https://loremflickr.com/400/300/bow,primitive/all"},
            {"n": "Vaso Barro", "img": "https://loremflickr.com/400/300/pottery,ancient/all"},
            {"n": "Ponta Lança", "img": "https://loremflickr.com/400/300/spear,stone/all"}
        ],
        "animais": [
            {"n": "Lobo", "u": "Selvagem", "img": "https://loremflickr.com/400/300/wolf/all"},
            {"n": "Cervo", "u": "Alimento", "img": "https://loremflickr.com/400/300/deer/all"},
            {"n": "Javali", "u": "Caça", "img": "https://loremflickr.com/400/300/boar/all"},
            {"n": "Auroque", "u": "Mítico", "img": "https://loremflickr.com/400/300/bull,wild/all"}
        ]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros da Serra.",
        "ferramentas": [
            {"n": "Falcata", "img": "https://loremflickr.com/400/300/sword,ancient/all"},
            {"n": "Caetra", "img": "https://loremflickr.com/400/300/shield,round/all"},
            {"n": "Punhal", "img": "https://loremflickr.com/400/300/dagger/all"},
            {"n": "Fuso", "img": "https://loremflickr.com/400/300/weaving/all"}
        ],
        "animais": [
            {"n": "Cavalo", "u": "Guerra", "img": "https://loremflickr.com/400/300/horse,lusitano/all"},
            {"n": "Porco", "u": "Comida", "img": "https://loremflickr.com/400/300/pig,black/all"},
            {"n": "Ovelha", "u": "Lã", "img": "https://loremflickr.com/400/300/sheep/all"},
            {"n": "Cão Fila", "u": "Guarda", "img": "https://loremflickr.com/400/300/dog,mastiff/all"}
        ]
    },
    "3. Conios": {
        "coord": [37.1, -8.2], "info": "Escrita do Sul.",
        "ferramentas": [
            {"n": "Estela", "img": "https://loremflickr.com/400/300/tablet,stone/all"},
            {"n": "Rede", "img": "https://loremflickr.com/400/300/fishing,net/all"},
            {"n": "Anzol", "img": "https://loremflickr.com/400/300/hook/all"},
            {"n": "Ânfora", "img": "https://loremflickr.com/400/300/vase,clay/all"}
        ],
        "animais": [
            {"n": "Burro", "u": "Carga", "img": "https://loremflickr.com/400/300/donkey/all"},
            {"n": "Cão Água", "u": "Pesca", "img": "https://loremflickr.com/400/300/dog,water/all"},
            {"n": "Galinha", "u": "Ovos", "img": "https://loremflickr.com/400/300/chicken/all"},
            {"n": "Abelha", "u": "Mel", "img": "https://loremflickr.com/400/300/bee/all"}
        ]
    },
    "4. Romanos": {
        "coord": [38.4, -7.9], "info": "Império e Lei.",
        "ferramentas": [
            {"n": "Gladius", "img": "https://loremflickr.com/400/300/sword,roman/all"},
            {"n": "Moeda", "img": "https://loremflickr.com/400/300/coin,gold/all"},
            {"n": "Mosaico", "img": "https://loremflickr.com/400/300/mosaic/all"},
            {"n": "Pilum", "img": "https://loremflickr.com/400/300/spear,roman/all"}
        ],
        "animais": [
            {"n": "Boi", "u": "Arado", "img": "https://loremflickr.com/400/300/ox/all"},
            {"n": "Mula", "u": "Carga", "img": "https://loremflickr.com/400/300/mule/all"},
            {"n": "Ganso", "u": "Vigia", "img": "https://loremflickr.com/400/300/goose/all"},
            {"n": "Cavalo", "u": "Mensageiro", "img": "https://loremflickr.com/400/300/horse,roman/all"}
        ]
    },
    "5. Visigodos": {
        "coord": [38.1, -7.8], "info": "Reinos Bárbaros.",
        "ferramentas": [{"n": "Cruz", "img": "https://loremflickr.com/400/300/cross,gold/all"}, {"n": "Espada", "img": "https://loremflickr.com/400/300/sword,medieval/all"}, {"n": "Fíbula", "img": "https://loremflickr.com/400/300/jewelry,old/all"}, {"n": "Escudo", "img": "https://loremflickr.com/400/300/shield,wood/all"}],
        "animais": [{"n": "Falcão", "u": "Caça", "img": "https://loremflickr.com/400/300/falcon/all"}, {"n": "Cavalo", "u": "Montaria", "img": "https://loremflickr.com/400/300/horse,dark/all"}, {"n": "Ovelha", "u": "Pele", "img": "https://loremflickr.com/400/300/sheep,white/all"}, {"n": "Cão", "u": "Caça", "img": "https://loremflickr.com/400/300/hound/all"}]
    },
    "6. Árabes": {
        "coord": [37.2, -7.9], "info": "Al-Andalus.",
        "ferramentas": [{"n": "Astrolábio", "img": "https://loremflickr.com/400/300/astrolabe/all"}, {"n": "Nora", "img": "https://loremflickr.com/400/300/waterwheel/all"}, {"n": "Azulejo", "img": "https://loremflickr.com/400/300/pattern,tile/all"}, {"n": "Citará", "img": "https://loremflickr.com/400/300/instrument,string/all"}],
        "animais": [{"n": "Camelo", "u": "Carga", "img": "https://loremflickr.com/400/300/camel/all"}, {"n": "Gineto", "u": "Guerra", "img": "https://loremflickr.com/400/300/horse,arabian/all"}, {"n": "Cabra", "u": "Leite", "img": "https://loremflickr.com/400/300/goat/all"}, {"n": "Pomba", "u": "Mensagem", "img": "https://loremflickr.com/400/300/pigeon/all"}]
    },
    "7. Descobrimentos": {
        "coord": [38.7, -9.2], "info": "Mar e Glória.",
        "ferramentas": [{"n": "Bússola", "img": "https://loremflickr.com/400/300/compass/all"}, {"n": "Caravela", "img": "https://loremflickr.com/400/300/ship,old/all"}, {"n": "Astrolábio", "img": "https://loremflickr.com/400/300/navigation/all"}, {"n": "Mapa", "img": "https://loremflickr.com/400/300/map,old/all"}],
        "animais": [{"n": "Papagaio", "u": "Exótico", "img": "https://loremflickr.com/400/300/parrot/all"}, {"n": "Macaco", "u": "Selva", "img": "https://loremflickr.com/400/300/monkey/all"}, {"n": "Elefante", "u": "Rei", "img": "https://loremflickr.com/400/300/elephant/all"}, {"n": "Cão Fila", "u": "Navio", "img": "https://loremflickr.com/400/300/dog,big/all"}]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MENU")
    modo = st.radio("IR PARA:", ["Explorar Épocas", "Linha do Tempo", "⭐ MODO: Minhas Tribos"])
    
    if modo == "Explorar Épocas":
        escolha = st.selectbox("POVO:", list(db.keys()))
    elif modo == "Linha do Tempo":
        escolha = st.select_slider("VIAGEM:", options=list(db.keys()))
    else:
        escolha = None

# --- LÓGICA ---
if modo == "⭐ MODO: Minhas Tribos":
    st.title("As Minhas Tribos Favoritas")
    if not st.session_state.favoritos:
        st.warning("Ainda não tens tribos! Volta a 'Explorar' e clica em 'Entrar na Tribo'.")
    else:
        for t_nome, t_dados in st.session_state.favoritos.items():
            with st.expander(f"🛡️ Membro de: {t_nome}", expanded=True):
                st.write(t_dados["info"])
else:
    dados = db[escolha]
    st.title(escolha)
    if st.button(f"➕ Entrar na Tribo {escolha}"):
        st.session_state.favoritos[escolha] = dados
        st.success("Adicionado aos Favoritos!")

    st.markdown(f'<div class="info-box">{dados["info"]}</div>', unsafe_allow_html=True)
    m = folium.Map(location=dados["coord"], zoom_start=7, tiles="CartoDB dark_matter")
    folium.Marker(dados["coord"], icon=folium.Icon(color="red")).add_to(m)
    st_folium(m, width="100%", height=300)

    # 4 COLUNAS SEMPRE
    st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
    cols_f = st.columns(4)
    for i, f in enumerate(dados["ferramentas"]):
        with cols_f[i]:
            st.markdown(f'<div class="cc-card"><img src="{f["img"]}" class="img-box"><div class="label">OBJETO</div><div class="value">{f["n"]}</div></div>', unsafe_allow_html=True)

    st.markdown("<h3 class='section-title'>🪪 Cartão Animal</h3>", unsafe_allow_html=True)
    cols_a = st.columns(4)
    for i, a in enumerate(dados["animais"]):
        with cols_a[i]:
            st.markdown(f'<div class="cc-card"><img src="{a["img"]}" class="img-box"><div class="label">NOME</div><div class="value">{a["n"]}</div><div class="label">USO</div><div class="value">{a["u"]}</div></div>', unsafe_allow_html=True)
