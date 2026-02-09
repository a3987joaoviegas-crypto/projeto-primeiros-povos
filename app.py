import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Primeiros Povos de Portugal", layout="wide")

# Estilo Visual Mundovivo - Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 10px 0; font-size: 1.2rem; }
    .cc-card { background-color: #111111; color: #ffffff; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; height: 100%; }
    .img-box { width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; background-color: #222; }
    .label { color: #666; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.85rem; font-weight: bold; color: #fff; }
    .info-box { background: #111111; padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; border-top: 4px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COMPLETA COM 7 ÉPOCAS ---
db = {
    "1. Pré-História": {
        "coord": [38.5, -8.0], "info": "Megalitismo e Caçadores.",
        "ferramentas": [{"n": "Biface", "p": "stone,tool"}, {"n": "Arco", "p": "bow"}, {"n": "Ponta Silex", "p": "arrow"}, {"n": "Vaso Barro", "p": "pottery"}],
        "animais": [{"n": "Lobo", "u": "Selvagem", "p": "wolf"}, {"n": "Auroque", "u": "Caça", "p": "bull"}, {"n": "Cervo", "u": "Alimento", "p": "deer"}, {"n": "Javali", "u": "Caça", "p": "boar"}]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros da Serra da Estrela.",
        "ferramentas": [{"n": "Falcata", "p": "sword"}, {"n": "Caetra", "p": "shield"}, {"n": "Lança", "p": "spear"}, {"n": "Fuso", "p": "wool"}],
        "animais": [{"n": "Cavalo", "u": "Guerra", "p": "horse"}, {"n": "Porco", "u": "Alimento", "p": "pig"}, {"n": "Ovelha", "u": "Lã", "p": "sheep"}, {"n": "Cão Fila", "u": "Guarda", "p": "dog"}]
    },
    "3. Conios": {
        "coord": [37.1, -8.2], "info": "Povo da escrita do Sul.",
        "ferramentas": [{"n": "Estela", "p": "tablet"}, {"n": "Anzol", "p": "hook"}, {"n": "Rede", "p": "net"}, {"n": "Ânfora", "p": "clay"}],
        "animais": [{"n": "Burro", "u": "Carga", "p": "donkey"}, {"n": "Cão Água", "u": "Pesca", "p": "dog"}, {"n": "Galinha", "u": "Ovos", "p": "chicken"}, {"n": "Abelha", "u": "Mel", "p": "bee"}]
    },
    "4. Romanos": {
        "coord": [38.4, -7.9], "info": "Civilização e Estradas.",
        "ferramentas": [{"n": "Gladius", "p": "sword"}, {"n": "Moeda", "p": "coin"}, {"n": "Estilo", "p": "pen"}, {"n": "Groma", "p": "map"}],
        "animais": [{"n": "Mula", "u": "Transporte", "p": "mule"}, {"n": "Boi", "u": "Arado", "p": "ox"}, {"n": "Ganso", "u": "Guarda", "p": "goose"}, {"n": "Cavalo", "u": "Correio", "p": "horse"}]
    },
    "5. Visigodos": {
        "coord": [38.1, -7.8], "info": "Reinos Germânicos.",
        "ferramentas": [{"n": "Fíbula", "p": "jewelry"}, {"n": "Espada Longa", "p": "sword"}, {"n": "Cruz", "p": "cross"}, {"n": "Escudo", "p": "shield"}],
        "animais": [{"n": "Falcão", "u": "Caça", "p": "hawk"}, {"n": "Cavalo", "u": "Nobreza", "p": "horse"}, {"n": "Cão", "u": "Caça", "p": "hound"}, {"n": "Ovelha", "u": "Pele", "p": "sheep"}]
    },
    "6. Árabes": {
        "coord": [37.2, -7.9], "info": "Al-Andalus e Ciência.",
        "ferramentas": [{"n": "Nora", "p": "water"}, {"n": "Astrolábio", "p": "star"}, {"n": "Azulejo", "p": "tile"}, {"n": "Alaúde", "p": "music"}],
        "animais": [{"n": "Camelo", "u": "Raro", "p": "camel"}, {"n": "Pomba", "u": "Mensagem", "p": "pigeon"}, {"n": "Gineto", "u": "Montaria", "p": "horse"}, {"n": "Cabra", "u": "Leite", "p": "goat"}]
    },
    "7. Descobrimentos": {
        "coord": [38.7, -9.2], "info": "Expansão Marítima.",
        "ferramentas": [{"n": "Bússola", "p": "compass"}, {"n": "Quadrante", "p": "navigation"}, {"n": "Caravela", "p": "ship"}, {"n": "Mapa", "p": "map"}],
        "animais": [{"n": "Papagaio", "u": "Exótico", "p": "parrot"}, {"n": "Macaco", "u": "Curiosidade", "p": "monkey"}, {"n": "Elefante", "u": "Presente", "p": "elephant"}, {"n": "Cão Fila", "u": "Navio", "p": "dog"}]
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
        img_url = f"https://placeimg.com/400/300/{f['p']}" # Fallback estável
        # Usando Placehold.jp para garantir que NUNCA fica vazio
        final_img = f"https://placehold.jp/24/333333/ffffff/400x300.png?text={f['n']}"
        st.markdown(f'<div class="cc-card"><img src="{final_img}" class="img-box"><div class="label">ARTEFACTO</div><div class="value">{f["n"]}</div></div>', unsafe_allow_html=True)

# Animais
st.markdown("<h3 class='section-title'>🪪 Cartão Animal</h3>", unsafe_allow_html=True)
cols_a = st.columns(4)
for i, a in enumerate(dados["animais"]):
    with cols_a[i]:
        final_img_a = f"https://placehold.jp/24/222222/ffffff/400x300.png?text={a['n']}"
        st.markdown(f'<div class="cc-card"><img src="{final_img_a}" class="img-box"><div class="label">NOME</div><div class="value">{a["n"]}</div><div class="label">USO</div><div class="value">{a["u"]}</div></div>', unsafe_allow_html=True)
