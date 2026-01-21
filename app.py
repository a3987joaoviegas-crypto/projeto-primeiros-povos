import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="MundoVivo: Povos de Portugal", layout="wide")

# Estilo Visual Total Black e Cartão de Cidadão
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title {
        color: white;
        border-left: 4px solid #ffffff;
        padding-left: 10px;
        margin: 30px 0 15px 0;
        font-family: sans-serif;
    }
    .cc-card {
        background-color: #111111;
        color: #ffffff;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .cc-header {
        font-size: 0.5rem;
        color: #666;
        text-align: center;
        border-bottom: 1px solid #222;
        margin-bottom: 10px;
        letter-spacing: 2px;
    }
    .img-real {
        width: 100%;
        height: 140px;
        object-fit: cover;
        border-radius: 5px;
        margin-bottom: 10px;
        border: 1px solid #222;
    }
    .label { color: #555; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.85rem; font-weight: bold; margin-bottom: 5px; color: #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DADOS COMPLETA COM IMAGENS REAIS ---
povos = {
    "Lusitanos": {
        "coords": [40.3, -7.5],
        "ferramentas": [
            {"n": "Falcata (Espada)", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Falcata_de_Almedinilla_%28M.A.N.Inv.2005-59-1%29_01.jpg/800px-falcata.jpg"},
            {"n": "Escudo Caetra", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Caetra.png/440px-Caetra.png"},
            {"n": "Ponta de Lança", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Ponta_de_lan%C3%A7a_de_bronze.jpg/640px-lança.jpg"},
            {"n": "Arado de Madeira", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Ancient_plough_wood.jpg/640px-plough.jpg"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "uso": "Guerra", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Lusitano_2.jpg/800px-Lusitano_2.jpg"},
            {"n": "Ovelha Bordaleira", "uso": "Lã", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Sheep_in_Portugal.jpg/640px-sheep.jpg"},
            {"n": "Cabra Serrana", "uso": "Leite", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Goat_in_the_mountains.jpg/640px-goat.jpg"},
            {"n": "Porco Alentejano", "uso": "Alimento", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Porco_Alentejano.JPG/640px-porco.jpg"}
        ]
    },
    "Celtas e Galaicos": {
        "coords": [41.5, -8.3],
        "ferramentas": [
            {"n": "Torques de Ouro", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Torques_de_Burela.jpg/800px-Torques.jpg"},
            {"n": "Machado de Ferro", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Iron_Axe_Head.JPG/640px-axe.jpg"},
            {"n": "Caldeirão Bronze", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Battersea_Cauldron.jpg/640px-cauldron.jpg"},
            {"n": "Mó de Pedra", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Quern_stone.jpg/640px-stone.jpg"}
        ],
        "animais": [
            {"n": "Vaca Cachena", "uso": "Tração", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Cachena_cow.jpg/800px-Cachena_cow.jpg"},
            {"n": "Cão Castro Laboreiro", "uso": "Guarda", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Castro_Laboreiro_Dog.jpg/800px-Castro.jpg"},
            {"n": "Boi Barrosão", "uso": "Trabalho", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Barros%C3%A3_Ox.jpg/640px-ox.jpg"},
            {"n": "Garrano (Ponei)", "uso": "Transporte", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Garrano_horse.jpg/640px-garrano.jpg"}
        ]
    },
    "Conios e Sudoeste": {
        "coords": [37.3, -8.1],
        "ferramentas": [
            {"n": "Estela de Escrita", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Escrita_do_Sudoeste_Estela_da_Abobada.jpg/400px-Estela.jpg"},
            {"n": "Ânfora Cerâmica", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Anfora_romana.jpg/400px-Anfora.jpg"},
            {"n": "Anzóis Antigos", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Fish_hooks_bronze.jpg/640px-hooks.jpg"},
            {"n": "Tear Manual", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Loom_weights.jpg/640px-loom.jpg"}
        ],
        "animais": [
            {"n": "Burro Mirandês", "uso": "Carga", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Burro_Mirand%C3%AAs.jpg/800px-Burro.jpg"},
            {"n": "Galinha Pedrês", "uso": "Ovos", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Pedr%C3%AAs_Portuguesa.jpg/640px-hen.jpg"},
            {"n": "Cão de Água", "uso": "Pesca", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Portuguese_Water_Dog_2.jpg/640px-pwd.jpg"},
            {"n": "Abelhas", "uso": "Mel", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Apis_mellifera_Western_honey_bee.jpg/640px-bee.jpg"}
        ]
    }
}

# --- SIDEBAR COM SETA ---
with st.sidebar:
    st.title("MundoVivo PT")
    with st.expander("▶ ESCOLHER POVO"):
        selecao = st.radio("", list(povos.keys()))

povo = povos[selecao]

# --- TOPO: MAPA ---
st.title(f"Povo: {selecao}")
m = folium.Map(location=[39.5, -8.0], zoom_start=6, tiles="CartoDB dark_matter")
folium.Marker(povo["coords"], popup=selecao).add_to(m)
st_folium(m, width="100%", height=350)

# --- BAIXO: LISTAS HORIZONTAIS ---

# 1. FERRAMENTAS
st.markdown("<h3 class='section-title'>⚒️ Ferramentas Reais</h3>", unsafe_allow_html=True)
cols_f = st.columns(4)
for i, f in enumerate(povo["ferramentas"]):
    with cols_f[i]:
        st.markdown(f"""
            <div class="cc-card">
                <img src="{f['img']}" class="img-real">
                <div class="label">ARTEFACTO</div>
                <div class="value">{f['n']}</div>
            </div>
        """, unsafe_allow_html=True)

# 2. ANIMAIS (CARTÃO DE CIDADÃO)
st.markdown("<h3 class='section-title'>🪪 Cartão de Cidadão Animal (Todos)</h3>", unsafe_allow_html=True)
cols_a = st.columns(4)
for i, a in enumerate(povo["animais"]):
    with cols_a[i]:
        st.markdown(f"""
            <div class="cc-card">
                <div class="cc-header">REPÚBLICA POVOS ANTIGOS</div>
                <img src="{a['img']}" class="img-real">
                <div class="label">ESPÉCIE/RAÇA</div>
                <div class="value">{a['n']}</div>
                <div class="label">OCUPAÇÃO</div>
                <div class="value">{a['uso']}</div>
            </div>
        """, unsafe_allow_html=True)
