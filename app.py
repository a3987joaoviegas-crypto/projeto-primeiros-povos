import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="MundoVivo: Portugal Ancestral", layout="wide")

# Estilo CSS Total Black e Cartão de Cidadão
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title {
        color: white;
        border-left: 4px solid #ffffff;
        padding-left: 10px;
        margin: 30px 0 15px 0;
    }
    .cc-card {
        background-color: #111111;
        color: #ffffff;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .cc-header {
        font-size: 0.5rem;
        color: #666;
        text-align: center;
        border-bottom: 1px solid #222;
        margin-bottom: 10px;
        letter-spacing: 2px;
    }
    .img-box {
        width: 100%;
        height: 160px;
        object-fit: cover;
        border-radius: 5px;
        margin-bottom: 10px;
        border: 1px solid #222;
        background-color: #222; /* Placeholder caso a imagem falhe */
    }
    .label { color: #555; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.85rem; font-weight: bold; margin-bottom: 5px; color: #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COM LINKS ESTÁVEIS ---
povos = {
    "Lusitanos": {
        "coords": [40.3, -7.5],
        "ferramentas": [
            {"n": "Falcata (Espada)", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Falcata_de_Almedinilla_%28M.A.N.Inv.2005-59-1%29_01.jpg/800px-Falcata.jpg"},
            {"n": "Escudo Caetra", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Caetra.png/440px-Caetra.png"},
            {"n": "Ponta de Lança", "img": "https://images.unsplash.com/photo-1558285511-966956795f55?w=400"},
            {"n": "Arado Madeira", "img": "https://images.unsplash.com/photo-1594391829624-dfc392bbbc24?w=400"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "uso": "Guerra", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"},
            {"n": "Ovelha Bordaleira", "uso": "Lã", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=400"},
            {"n": "Cabra Serrana", "uso": "Leite", "img": "https://images.unsplash.com/photo-1524024973431-2ad916746881?w=400"},
            {"n": "Porco Alentejano", "uso": "Alimento", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Porco_Alentejano.JPG/800px-Porco.jpg"}
        ]
    },
    "Celtas e Galaicos": {
        "coords": [41.5, -8.3],
        "ferramentas": [
            {"n": "Torques Ouro", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Torques_de_Burela.jpg/800px-Torques.jpg"},
            {"n": "Machado Ferro", "img": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=400"},
            {"n": "Caldeirão", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Battersea_Cauldron.jpg/800px-Cauldron.jpg"},
            {"n": "Mó de Pedra", "img": "https://images.unsplash.com/photo-1603566270543-92f750d03704?w=400"}
        ],
        "animais": [
            {"n": "Vaca Cachena", "uso": "Tração", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Cachena_cow.jpg/800px-Cachena.jpg"},
            {"n": "Cão de Guarda", "uso": "Guarda", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"},
            {"n": "Boi Barrosão", "uso": "Trabalho", "img": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400"},
            {"n": "Ponei Garrano", "uso": "Transporte", "img": "https://images.unsplash.com/photo-1598974357851-cb8143c0f243?w=400"}
        ]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("MundoVivo")
    with st.expander("▶ SELECIONAR POVO"):
        selecao = st.radio("", list(povos.keys()))

povo = povos[selecao]

# --- MAPA ---
st.title(f"Povo: {selecao}")
m = folium.Map(location=[39.5, -8.0], zoom_start=6, tiles="CartoDB dark_matter")
folium.Marker(povo["coords"], popup=selecao).add_to(m)
st_folium(m, width="100%", height=300)

# --- LISTAS HORIZONTAIS ---

st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
cols_f = st.columns(4)
for i, f in enumerate(povo["ferramentas"]):
    with cols_f[i]:
        st.markdown(f"""
            <div class="cc-card">
                <img src="{f['img']}" class="img-box" onerror="this.style.display='none'">
                <div class="label">ARTEFACTO</div>
                <div class="value">{f['n']}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<h3 class='section-title'>🪪 Cartão de Cidadão Animal</h3>", unsafe_allow_html=True)
cols_a = st.columns(4)
for i, a in enumerate(povo["animais"]):
    with cols_a[i]:
        st.markdown(f"""
            <div class="cc-card">
                <div class="cc-header">REPÚBLICA POVOS ANTIGOS</div>
                <img src="{a['img']}" class="img-box" onerror="this.style.display='none'">
                <div class="label">ESPÉCIE</div>
                <div class="value">{a['n']}</div>
                <div class="label">FUNÇÃO</div>
                <div class="value">{a['uso']}</div>
            </div>
        """, unsafe_allow_html=True)
