import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="MundoVivo: Povos Reais de Portugal", layout="wide")

# CSS para Cartão de Cidadão Preto e Imagens Reais
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title {
        color: white;
        border-left: 4px solid #ffffff;
        padding-left: 10px;
        margin-top: 30px;
        font-family: 'Helvetica', sans-serif;
    }
    .cc-card {
        background-color: #111111;
        color: #ffffff;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        text-align: left;
    }
    .cc-header {
        font-size: 0.55rem;
        color: #777;
        text-align: center;
        border-bottom: 1px solid #222;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    .img-real {
        width: 100%;
        height: 150px;
        object-fit: contain;
        background-color: #000;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .label { color: #555; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.85rem; font-weight: bold; margin-bottom: 5px; color: #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COM LINKS DE IMAGENS REAIS ---
povos = {
    "Lusitanos": {
        "coords": [40.3, -7.5],
        "ferramentas": [
            {"n": "Falcata (Espada Real)", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Falcata_de_Almedinilla_%28M.A.N.Inv.2005-59-1%29_01.jpg/800px-Falcata_de_Almedinilla_%28M.A.N.Inv.2005-59-1%29_01.jpg"},
            {"n": "Caetra (Escudo)", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Caetra.png/440px-Caetra.png"},
            {"n": "Arado Antigo", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Alt%C3%A4gyptischer_Maler_um_1200_v._Chr._001.jpg/600px-Alt%C3%A4gyptischer_Maler_um_1200_v._Chr._001.jpg"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "uso": "Guerra", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Lusitano_2.jpg/800px-Lusitano_2.jpg"},
            {"n": "Ovelha Bordaleira", "uso": "Lã Serra Estrela", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Sheep_St_Johns_Island.jpg/800px-Sheep_St_Johns_Island.jpg"}
        ]
    },
    "Celtas / Galaicos": {
        "coords": [41.5, -8.3],
        "ferramentas": [
            {"n": "Torques de Ouro", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Torques_de_Burela.jpg/800px-Torques_de_Burela.jpg"},
            {"n": "Machado de Ferro", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Iron_Axe_Head.JPG/600px-Iron_Axe_Head.JPG"}
        ],
        "animais": [
            {"n": "Vaca Cachena", "uso": "Tração e Leite", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Cachena_cow.jpg/800px-Cachena_cow.jpg"},
            {"n": "Cão Castro Laboreiro", "uso": "Guarda", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Castro_Laboreiro_Dog_C%C3%A3o_de_Castro_Laboreiro.jpg/800px-Castro_Laboreiro_Dog_C%C3%A3o_de_Castro_Laboreiro.jpg"}
        ]
    },
    "Conios (Escrita do Sudoeste)": {
        "coords": [37.3, -8.1],
        "ferramentas": [
            {"n": "Estela de Escrita", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Escrita_do_Sudoeste_Estela_da_Abobada.jpg/400px-Escrita_do_Sudoeste_Estela_da_Abobada.jpg"},
            {"n": "Ânfora de Barro", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Anfora_romana.jpg/400px-Anfora_romana.jpg"}
        ],
        "animais": [
            {"n": "Burro Mirandês", "uso": "Carga", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Burro_Mirand%C3%AAs.jpg/800px-Burro_Mirand%C3%AAs.jpg"}
        ]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MENU")
    with st.expander("▶ ESCOLHER POVO"):
        selecao = st.radio("", list(povos.keys()))

povo = povos[selecao]

# --- LAYOUT SUPERIOR: MAPA ---
st.title(f"Povo: {selecao}")
m = folium.Map(location=[39.5, -8.0], zoom_start=6, tiles="CartoDB dark_matter")
folium.Marker(povo["coords"], popup=selecao).add_to(m)
st_folium(m, width="100%", height=350)

# --- LAYOUT INFERIOR: LISTAS HORIZONTAIS REALISTAS ---

# 1. FERRAMENTAS REAIS
st.markdown("<h3 class='section-title'>⚒️ Ferramentas (Achados Arqueológicos)</h3>", unsafe_allow_html=True)
cols_f = st.columns(4)
for i, f in enumerate(povo["ferramentas"]):
    with cols_f[i % 4]:
        st.markdown(f"""
            <div class="cc-card">
                <img src="{f['img']}" class="img-real">
                <div class="label">ARTEFACTO</div>
                <div class="value">{f['n']}</div>
            </div>
        """, unsafe_allow_html=True)

# 2. ANIMAIS REAIS (CARTÃO DE CIDADÃO)
st.markdown("<h3 class='section-title'>🪪 Cartão de Cidadão Animal (Raças Reais)</h3>", unsafe_allow_html=True)
cols_a = st.columns(4)
for i, a in enumerate(povo["animais"]):
    with cols_a[i % 4]:
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
