import streamlit as st
import folium
from streamlit_folium import st_folium
import random

st.set_page_config(page_title="Primeiros Povos de Portugal", layout="wide")

# Estilo Visual Mundovivo - Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 15px 0; font-size: 1.2rem; }
    .cc-card { background-color: #111111; color: #ffffff; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; height: 100%; }
    .img-box { width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; }
    .label { color: #666; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.85rem; font-weight: bold; color: #fff; }
    .info-box { background: #111111; padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; border-top: 4px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COMPLETA COM 7 ÉPOCAS ---
db = {
    "1. Pré-História": {
        "coord": [38.5, -8.0], "info": "Megalitismo e Caçadores.",
        "ferramentas": [{"n": "Biface", "q": "prehistoric-stone"}, {"n": "Arco", "q": "bow-arrow"}, {"n": "Ponta Silex", "q": "arrowhead"}, {"n": "Vaso Barro", "q": "pottery"}],
        "animais": [{"n": "Lobo", "u": "Selvagem", "q": "wolf"}, {"n": "Auroque", "u": "Caça", "q": "bull"}, {"n": "Cervo", "u": "Alimento", "q": "deer"}, {"n": "Javali", "u": "Caça", "q": "wild-boar"}]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros da Serra da Estrela.",
        "ferramentas": [{"n": "Falcata", "q": "ancient-sword"}, {"n": "Caetra", "q": "shield"}, {"n": "Lança", "q": "spear"}, {"n": "Fuso", "q": "wool"}],
        "animais": [{"n": "Cavalo", "u": "Guerra", "q": "horse"}, {"n": "Porco", "u": "Alimento", "q": "pig"}, {"n": "Ovelha", "u": "Lã", "q": "sheep"}, {"n": "Cão Fila", "u": "Guarda", "q": "big-dog"}]
    },
    "3. Conios": {
        "coord": [37.1, -8.2], "info": "Povo da escrita do Sul.",
        "ferramentas": [{"n": "Estela", "q": "monument"}, {"n": "Anzol", "q": "fishing-hook"}, {"n": "Rede", "q": "fishing-net"}, {"n": "Ânfora", "q": "amphora"}],
        "animais": [{"n": "Burro", "u": "Carga", "q": "donkey"}, {"n": "Cão Água", "u": "Pesca", "q": "water-dog"}, {"n": "Galinha", "u": "Ovos", "q": "chicken"}, {"n": "Abelha", "u": "Mel", "q": "bee"}]
    },
    "4. Romanos": {
        "coord": [38.4, -7.9], "info": "Civilização e Estradas.",
        "ferramentas": [{"n": "Gladius", "q": "roman-sword"}, {"n": "Moeda", "q": "roman-coin"}, {"n": "Estilo", "q": "ancient-writing"}, {"n": "Groma", "q": "engineering"}],
        "animais": [{"n": "Mula", "u": "Transporte", "q": "mule"}, {"n": "Boi", "u": "Arado", "q": "ox"}, {"n": "Ganso", "u": "Guarda", "q": "goose"}, {"n": "Cavalo", "u": "Correio", "q": "horse-riding"}]
    },
    "5. Visigodos": {
        "coord": [38.1, -7.8], "info": "Reinos Germânicos.",
        "ferramentas": [{"n": "Fíbula", "q": "jewelry-ancient"}, {"n": "Espada Longa", "q": "medieval-sword"}, {"n": "Cruz", "q": "ancient-cross"}, {"n": "Escudo", "q": "warrior-shield"}],
        "animais": [{"n": "Falcão", "u": "Caça", "q": "falcon"}, {"n": "Cavalo", "u": "Nobreza", "q": "stallion"}, {"n": "Cão", "u": "Caça", "q": "hound-dog"}, {"n": "Ovelha", "u": "Pele", "q": "sheep-wool"}]
    },
    "6. Árabes": {
        "coord": [37.2, -7.9], "info": "Al-Andalus e Ciência.",
        "ferramentas": [{"n": "Nora", "q": "water-well"}, {"n": "Astrolábio", "q": "astrolabe"}, {"n": "Azulejo", "q": "tile-pattern"}, {"n": "Alaúde", "q": "lute"}],
        "animais": [{"n": "Camelo", "u": "Raro", "q": "camel"}, {"n": "Pomba", "u": "Mensagem", "q": "pigeon"}, {"n": "Gineto", "u": "Montaria", "q": "horse-arabian"}, {"n": "Cabra", "u": "Leite", "q": "goat"}]
    },
    "7. Descobrimentos": {
        "coord": [38.7, -9.2], "info": "Expansão Marítima.",
        "ferramentas": [{"n": "Bússola", "q": "compass-old"}, {"n": "Quadrante", "q": "navigation-tool"}, {"n": "Caravela", "q": "sailing-ship"}, {"n": "Mapa", "q": "ancient-map"}],
        "animais": [{"n": "Papagaio", "u": "Exótico", "q": "parrot"}, {"n": "Macaco", "u": "Curiosidade", "q": "monkey"}, {"n": "Elefante", "u": "Presente", "q": "elephant"}, {"n": "Cão Fila", "u": "Navio", "q": "mastiff"}]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🇵🇹 HISTÓRIA")
    modo = st.radio("MODO:", ["Seleção Direta", "Evolução (Slider)"])
    if modo == "Seleção Direta":
        item = st.selectbox("ESCOLHA:", list(db.keys()))
    else:
        item = st.select_slider("VIAGEM NO TEMPO:", options=list(db.keys()))

dados = db[item]

# --- CONTEÚDO ---
st.title(f"{item}")
st.markdown(f'<div class="info-box"><b>Resumo:</b> {dados["info"]}</div>', unsafe_allow_html=True)

# Mapa
m = folium.Map(location=dados["coord"], zoom_start=7, tiles="CartoDB dark_matter")
folium.Marker(dados["coord"], icon=folium.Icon(color="red")).add_to(m)
st_folium(m, width="100%", height=300)

# Ferramentas
st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
cols_f = st.columns(4)
for i, f in enumerate(dados["ferramentas"]):
    with cols_f[i]:
        # URL com semente aleatória para evitar cache/bloqueio
        img_url = f"https://images.unsplash.com/photo-1?auto=format&fit=crop&w=400&q=80&sig={random.randint(1,1000)}&keyword={f['q']}"
        st.markdown(f'<div class="cc-card"><img src="https://images.unsplash.com/featured/?{f["q"]}" class="img-box"><div class="label">ARTEFACTO</div><div class="value">{f["n"]}</div></div>', unsafe_allow_html=True)

# Animais
st.markdown("<h3 class='section-title'>🪪 Cartão Animal</h3>", unsafe_allow_html=True)
cols_a = st.columns(4)
for i, a in enumerate(dados["animais"]):
    with cols_a[i]:
        st.markdown(f'<div class="cc-card"><img src="https://images.unsplash.com/featured/?{a["q"]}" class="img-box"><div class="label">NOME</div><div class="value">{a["n"]}</div><div class="label">USO</div><div class="value">{a["u"]}</div></div>', unsafe_allow_html=True)
