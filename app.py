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
    .img-box { width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; }
    .label { color: #666; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.85rem; font-weight: bold; color: #fff; }
    .info-box { background: #111111; padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; border-top: 4px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE INTEGRADA (POVOS E EVOLUÇÃO) ---
db = {
    "Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros da Serra da Estrela.",
        "ferramentas": [{"n": "Falcata", "p": "sword"}, {"n": "Escudo", "p": "shield"}, {"n": "Lança", "p": "spear"}, {"n": "Arado", "p": "farm"}],
        "animais": [{"n": "Cavalo", "u": "Guerra", "p": "horse"}, {"n": "Porco", "u": "Alimento", "p": "pig"}, {"n": "Ovelha", "u": "Lã", "p": "sheep"}, {"n": "Cão", "u": "Guarda", "p": "dog"}]
    },
    "Celtas": {
        "coord": [41.5, -8.3], "info": "Mestres da metalurgia e dos Castros.",
        "ferramentas": [{"n": "Torques", "p": "gold"}, {"n": "Machado", "p": "axe"}, {"n": "Caldeirão", "p": "pot"}, {"n": "Mó", "p": "stone"}],
        "animais": [{"n": "Vaca Cachena", "u": "Tração", "p": "cow"}, {"n": "Boi", "u": "Trabalho", "p": "ox"}, {"n": "Ponei", "u": "Transporte", "p": "pony"}, {"n": "Cão Castro", "u": "Guarda", "p": "dog"}]
    },
    "Conios": {
        "coord": [37.1, -8.2], "info": "Criadores da escrita do sudoeste.",
        "ferramentas": [{"n": "Estela", "p": "stone"}, {"n": "Ânfora", "p": "clay"}, {"n": "Anzol", "p": "hook"}, {"n": "Rede", "p": "net"}],
        "animais": [{"n": "Burro", "u": "Carga", "p": "donkey"}, {"n": "Cão Água", "u": "Pesca", "p": "dog"}, {"n": "Galinha", "u": "Ovos", "p": "chicken"}, {"n": "Abelhas", "u": "Mel", "p": "bee"}]
    },
    "Romanos": {
        "coord": [38.4, -7.9], "info": "Império que trouxe estradas e o latim.",
        "ferramentas": [{"n": "Gladius", "p": "sword"}, {"n": "Pilum", "p": "spear"}, {"n": "Toga", "p": "fabric"}, {"n": "Moeda", "p": "coin"}],
        "animais": [{"n": "Mula", "u": "Carga", "p": "mule"}, {"n": "Ganso", "u": "Alarme", "p": "goose"}, {"n": "Cavalo", "u": "Correio", "p": "horse"}, {"n": "Boi", "u": "Arado", "p": "ox"}]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MENU")
    modo = st.radio("MODO:", ["Povos Ancestrais", "Evolução Portuguesa"])
    
    if modo == "Povos Ancestrais":
        item = st.selectbox("ESCOLHA O POVO:", list(db.keys()))
    else:
        item = st.select_slider("VIAGEM NO TEMPO:", options=list(db.keys()))
    
dados = db[item]

# --- CONTEÚDO ---
st.title(f"{modo}: {item}")

st.markdown(f'<div class="info-box"><h3>Contexto Histórico</h3><p>{dados["info"]}</p></div>', unsafe_allow_html=True)

# Mapa
m = folium.Map(location=dados["coord"], zoom_start=7, tiles="CartoDB dark_matter")
folium.Marker(dados["coord"], icon=folium.Icon(color="red")).add_to(m)
st_folium(m, width="100%", height=300)

# Ferramentas
st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
cols_f = st.columns(4)
for i, f in enumerate(dados["ferramentas"]):
    with cols_f[i]:
        img_url = f"https://loremflickr.com/400/300/{f['p']},ancient"
        st.markdown(f'<div class="cc-card"><img src="{img_url}" class="img-box"><div class="label">ARTEFACTO</div><div class="value">{f["n"]}</div></div>', unsafe_allow_html=True)

# Animais
st.markdown("<h3 class='section-title'>🪪 Cartão Animal</h3>", unsafe_allow_html=True)
cols_a = st.columns(4)
for i, a in enumerate(dados["animais"]):
    with cols_a[i]:
        img_url = f"https://loremflickr.com/400/300/{a['p']},animal"
        st.markdown(f'<div class="cc-card"><img src="{img_url}" class="img-box"><div class="label">NOME</div><div class="value">{a["n"]}</div><div class="label">USO</div><div class="value">{a["u"]}</div></div>', unsafe_allow_html=True)
