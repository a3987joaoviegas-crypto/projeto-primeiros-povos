import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Primeiros Povos de Portugal", layout="wide")

# Inicializar favoritos no estado da sessão
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []

# Estilo Visual Mundovivo - Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 10px 0; font-size: 1.2rem; }
    .cc-card { background-color: #111111; color: #ffffff; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; height: 100%; }
    .img-box { width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; }
    .label { color: #666; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.85rem; font-weight: bold; color: #fff; }
    .info-box { background: #111111; padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; border-top: 4px solid #ffffff; }
    /* Botão Entrar na Tribo */
    .stButton>button { background-color: #222; color: white; border: 1px solid #444; width: 100%; border-radius: 5px; font-size: 0.7rem; }
    .stButton>button:hover { border-color: #fff; background-color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COMPLETA ---
db = {
    "1. Pré-História": {
        "coord": [38.5, -8.0], "info": "Megalitismo e Caçadores.",
        "ferramentas": [{"n": "Biface", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Biface_de_Saint-Acheul.jpg/400px-Biface_de_Saint-Acheul.jpg"}],
        "animais": [{"n": "Lobo", "u": "Selvagem", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Canis_lupus_265b.jpg/400px-Canis_lupus_265b.jpg"}]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros da Serra da Estrela.",
        "ferramentas": [{"n": "Falcata", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Falcata_01.JPG/400px-Falcata_01.JPG"}],
        "animais": [{"n": "Cavalo", "u": "Guerra", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Lusitano_horse_grazing.jpg/400px-Lusitano_horse_grazing.jpg"}]
    },
    "3. Conios": {
        "coord": [37.1, -8.2], "info": "Povo da escrita do Sul.",
        "ferramentas": [{"n": "Estela", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Escrita_do_Sudoeste_-_Almodovar.jpg/400px-Escrita_do_Sudoeste_-_Almodovar.jpg"}],
        "animais": [{"n": "Burro", "u": "Carga", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Donkey_1_arp_750px.jpg/400px-Donkey_1_arp_750px.jpg"}]
    },
    "4. Romanos": {
        "coord": [38.4, -7.9], "info": "Civilização e Estradas.",
        "ferramentas": [{"n": "Gladius", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Gladius_Mainz.jpg/400px-Gladius_Mainz.jpg"}],
        "animais": [{"n": "Boi", "u": "Arado", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Common_ox.jpg/400px-Common_ox.jpg"}]
    },
    "5. Visigodos": {
        "coord": [38.1, -7.8], "info": "Reinos Germânicos.",
        "ferramentas": [{"n": "Fíbula", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Fibule_wisigothique.jpg/400px-Fibule_wisigothique.jpg"}],
        "animais": [{"n": "Falcão", "u": "Caça", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Falco_peregrinus_-_01.jpg/400px-Falco_peregrinus_-_01.jpg"}]
    },
    "6. Árabes": {
        "coord": [37.2, -7.9], "info": "Al-Andalus e Ciência.",
        "ferramentas": [{"n": "Astrolábio", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Astrolabe-Persian-18C.jpg/400px-Astrolabe-Persian-18C.jpg"}],
        "animais": [{"n": "Camelo", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/07._Camel_Profile%2C_Near_Silverton%2C_NSW%2C_07.07.2007.jpg/400px-07._Camel_Profile%2C_Near_Silverton%2C_NSW%2C_07.07.2007.jpg"}]
    },
    "7. Descobrimentos": {
        "coord": [38.7, -9.2], "info": "Expansão Marítima.",
        "ferramentas": [{"n": "Bússola", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Compass_Card_fixed.jpg/400px-Compass_Card_fixed.jpg"}],
        "animais": [{"n": "Papagaio", "u": "Exótico", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Macaw_Ara_ararauna_and_Ara_macao.jpg/400px-Macaw_Ara_ararauna_and_Ara_macao.jpg"}]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🇵🇹 HISTÓRIA")
    
    # Secção Minhas Tribos (Favoritos)
    st.markdown("### ⭐ Minhas Tribos")
    if not st.session_state.favoritos:
        st.write("Nenhuma tribo favorita.")
    else:
        for fav in st.session_state.favoritos:
            st.write(f"- {fav}")
    
    st.markdown("---")
    modo = st.radio("MODO:", ["Seleção Direta", "Evolução (Slider)"])
    if modo == "Seleção Direta":
        item = st.selectbox("ESCOLHA:", list(db.keys()))
    else:
        item = st.select_slider("VIAGEM NO TEMPO:", options=list(db.keys()))

dados = db[item]

# --- CONTEÚDO ---
st.title(f"{item}")

# Botão Entrar na Tribo
if st.button(f"➕ Entrar na Tribo {item}"):
    if item not in st.session_state.favoritos:
        st.session_state.favoritos.append(item)
        st.success(f"{item} adicionada aos favoritos!")

st.markdown(f'<div class="info-box"><b>Resumo:</b> {dados["info"]}</div>', unsafe_allow_html=True)

# Mapa
m = folium.Map(location=dados["coord"], zoom_start=7, tiles="CartoDB dark_matter")
folium.Marker(dados["coord"], icon=folium.Icon(color="red")).add_to(m)
st_folium(m, width="100%", height=300)

# Ferramentas e Animais
st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
cols_f = st.columns(len(dados["ferramentas"]))
for i, f in enumerate(dados["ferramentas"]):
    with cols_f[i]:
        st.markdown(f'<div class="cc-card"><img src="{f["img"]}" class="img-box"><div class="label">ARTEFACTO</div><div class="value">{f["n"]}</div></div>', unsafe_allow_html=True)

st.markdown("<h3 class='section-title'>🪪 Cartão Animal</h3>", unsafe_allow_html=True)
cols_a = st.columns(len(dados["animais"]))
for i, a in enumerate(dados["animais"]):
    with cols_a[i]:
        st.markdown(f'<div class="cc-card"><img src="{a["img"]}" class="img-box"><div class="label">NOME</div><div class="value">{a["n"]}</div></div>', unsafe_allow_html=True)
