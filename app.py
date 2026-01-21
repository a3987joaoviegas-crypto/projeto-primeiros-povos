import streamlit as st
import folium
from streamlit_folium import st_folium

# Configuração da Página
st.set_page_config(page_title="Portugal Antigo: Mundovivo", layout="wide")

# Estilo CSS: Cartão de Cidadão Preto e Branco (High Contrast)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .cc-card {
        background-color: #000000;
        color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 25px;
        border: 2px solid #ffffff;
    }
    .cc-title {
        font-size: 0.7rem;
        letter-spacing: 3px;
        color: #888;
        border-bottom: 1px solid #333;
        margin-bottom: 12px;
        text-align: center;
    }
    .img-box {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 8px;
        border: 1px solid #444;
        margin-bottom: 10px;
    }
    .label { color: #888; font-size: 0.65rem; text-transform: uppercase; margin-top: 8px; }
    .value { font-size: 0.95rem; font-weight: bold; font-family: 'Courier New', monospace; }
    .tool-card {
        background: #1a1a1a;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 4px solid #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DADOS GIGANTE ---
# Usando keywords para imagens garantidas do Unsplash
povos = {
    "Lusitanos": {
        "coords": [40.3, -7.5],
        "ferramentas": [
            {"nome": "Falcata (Espada)", "img": "https://source.unsplash.com/400x300/?sword,ancient"},
            {"nome": "Escudo Caetra", "img": "https://source.unsplash.com/400x300/?shield,wood"},
            {"nome": "Arado de Madeira", "img": "https://source.unsplash.com/400x300/?plow,farm"}
        ],
        "animais": [
            {"nome": "Cavalo Lusitano", "desc": "Guerra", "img": "https://source.unsplash.com/400x300/?horse,lusitano"},
            {"nome": "Ovelha", "desc": "Lã", "img": "https://source.unsplash.com/400x300/?sheep"},
            {"nome": "Cabra", "desc": "Leite", "img": "https://source.unsplash.com/400x300/?goat"},
            {"nome": "Porco", "desc": "Alimento", "img": "https://source.unsplash.com/400x300/?pig"}
        ]
    },
    "Celtas": {
        "coords": [39.0, -7.2],
        "ferramentas": [
            {"nome": "Torques de Ouro", "img": "https://source.unsplash.com/400x300/?gold,jewelry"},
            {"nome": "Machado de Ferro", "img": "https://source.unsplash.com/400x300/?axe,iron"},
            {"nome": "Caldeirão", "img": "https://source.unsplash.com/400x300/?cauldron"}
        ],
        "animais": [
            {"nome": "Boi Barrosão", "desc": "Tração", "img": "https://source.unsplash.com/400x300/?ox,bull"},
            {"nome": "Cão Lobo", "desc": "Guarda", "img": "https://source.unsplash.com/400x300/?wolf,dog"}
        ]
    },
    "Galaicos": {
        "coords": [41.7, -8.4],
        "ferramentas": [
            {"nome": "Hoz (Foice)", "img": "https://source.unsplash.com/400x300/?sickle"},
            {"nome": "Moinho Manual", "img": "https://source.unsplash.com/400x300/?stone,mill"}
        ],
        "animais": [
            {"nome": "Vaca Cachena", "desc": "Montanha", "img": "https://source.unsplash.com/400x300/?cow,mountain"},
            {"nome": "Garrano", "desc": "Ponei de Carga", "img": "https://source.unsplash.com/400x300/?pony"}
        ]
    },
    "Conios": {
        "coords": [37.2, -8.1],
        "ferramentas": [
            {"nome": "Estela Escrita", "img": "https://source.unsplash.com/400x300/?hieroglyph,stone"},
            {"nome": "Rede de Pesca", "img": "https://source.unsplash.com/400x300/?fishing,net"}
        ],
        "animais": [
            {"nome": "Burro", "desc": "Transporte Sul", "img": "https://source.unsplash.com/400x300/?donkey"},
            {"nome": "Peixe", "desc": "Aquicultura", "img": "https://source.unsplash.com/400x300/?fish"}
        ]
    },
    "Túrdulos": {
        "coords": [38.8, -8.9],
        "ferramentas": [{"nome": "Ânfora", "img": "https://source.unsplash.com/400x300/?pottery,ancient"}],
        "animais": [{"nome": "Touro", "desc": "Sagrado", "img": "https://source.unsplash.com/400x300/?bull,black"}]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MundoVivo: Povos")
    with st.expander("▶ SELECIONAR POVO"):
        escolha = st.radio("Escolha um povo antigo:", list(povos.keys()))

dados = povos[escolha]

# --- LAYOUT ---
st.title(f"Exploração: {escolha}")

col_map, col_tools, col_animals = st.columns([1.2, 1, 1.2])

with col_map:
    st.subheader("📍 Localização")
    m = folium.Map(location=dados["coords"], zoom_start=7, tiles="CartoDB dark_matter")
    folium.Marker(location=dados["coords"], popup=escolha).add_to(m)
    st_folium(m, width=400, height=400, key="mapa")

with col_tools:
    st.subheader("⚒️ Ferramentas")
    for f in dados["ferramentas"]:
        st.markdown(f"""
            <div class="tool-card">
                <img src="{f['img']}" class="img-box" style="height: 100px;">
                <div class="value">{f['nome']}</div>
            </div>
        """, unsafe_allow_html=True)

with col_animals:
    st.subheader("🪪 Cartões de Cidadão")
    for a in dados["animais"]:
        st.markdown(f"""
            <div class="cc-card">
                <div class="cc-title">REPÚBLICA DOS POVOS ANTIGOS</div>
                <img src="{a['img']}" class="cc-foto img-box">
                <div class="label">NOME DO ANIMAL</div>
                <div class="value">{a['nome']}</div>
                <div class="label">UTILIZAÇÃO</div>
                <div class="value">{a['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

# --- LISTA GERAL DE TODOS OS ANIMAIS (Final da Página) ---
st.divider()
st.subheader("📜 Lista Geral de Todos os Animais das Quintas Antigas")
todos_animais = []
for p in povos.values():
    for a in p["animais"]:
        if a["nome"] not in todos_animais:
            todos_animais.append(a["nome"])

st.write(", ".join(todos_animais))
