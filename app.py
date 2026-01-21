import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="MundoVivo: Povos de Portugal", layout="wide")

# CSS Estilo Mundovivo - Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title {
        color: white;
        border-left: 4px solid #ffffff;
        padding-left: 15px;
        margin: 30px 0 15px 0;
    }
    .cc-card {
        background-color: #111111;
        color: #ffffff;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        height: 100%;
    }
    .cc-header {
        font-size: 0.5rem;
        color: #888;
        border-bottom: 1px solid #222;
        margin-bottom: 10px;
        letter-spacing: 2px;
    }
    .img-real {
        width: 100%;
        height: 150px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #444;
    }
    .label { color: #666; font-size: 0.6rem; text-transform: uppercase; margin-top: 10px; }
    .value { font-size: 0.9rem; font-weight: bold; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COMPLETA COM IMAGENS TESTADAS ---
povos = {
    "Lusitanos": {
        "coords": [40.3, -7.5],
        "ferramentas": [
            {"n": "Falcata (Espada)", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"},
            {"n": "Escudo Caetra", "img": "https://images.unsplash.com/photo-1615678815958-5d413b70b653?w=400"},
            {"n": "Ponta de Lança", "img": "https://images.unsplash.com/photo-1510414695470-24970f807365?w=400"},
            {"n": "Arado de Madeira", "img": "https://images.unsplash.com/photo-1594391829624-dfc392bbbc24?w=400"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "uso": "Guerra", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"},
            {"n": "Ovelha Bordaleira", "uso": "Lã", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=400"},
            {"n": "Cabra Serrana", "uso": "Leite", "img": "https://images.unsplash.com/photo-1524024973431-2ad916746881?w=400"},
            {"n": "Porco Alentejano", "uso": "Alimento", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?w=400"}
        ]
    },
    "Celtas e Galaicos": {
        "coords": [41.5, -8.3],
        "ferramentas": [
            {"n": "Torques de Ouro", "img": "https://images.unsplash.com/photo-1611085583191-a3b1a6a939db?w=400"},
            {"n": "Machado de Ferro", "img": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=400"},
            {"n": "Caldeirão", "img": "https://images.unsplash.com/photo-1582738411706-bfc8e691d1c2?w=400"},
            {"n": "Mó de Pedra", "img": "https://images.unsplash.com/photo-1603566270543-92f750d03704?w=400"}
        ],
        "animais": [
            {"n": "Vaca Cachena", "uso": "Tração", "img": "https://images.unsplash.com/photo-1545468843-2796674f1df2?w=400"},
            {"n": "Cão de Guarda", "uso": "Guarda", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"},
            {"n": "Boi Barrosão", "uso": "Trabalho", "img": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400"},
            {"n": "Ponei Garrano", "uso": "Transporte", "img": "https://images.unsplash.com/photo-1598974357851-cb8143c0f243?w=400"}
        ]
    },
    "Conios (Sul)": {
        "coords": [37.3, -8.1],
        "ferramentas": [
            {"n": "Estela Escrita", "img": "https://images.unsplash.com/photo-1518153925617-3a629474bc9b?w=400"},
            {"n": "Ânfora de Barro", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?w=400"},
            {"n": "Anzol Bronze", "img": "https://images.unsplash.com/photo-1516937941344-00b4e0337589?w=400"},
            {"n": "Rede de Pesca", "img": "https://images.unsplash.com/photo-1501703979959-79396f212591?w=400"}
        ],
        "animais": [
            {"n": "Burro Mirandês", "uso": "Carga", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?w=400"},
            {"n": "Galinha Pedrês", "uso": "Ovos", "img": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400"},
            {"n": "Cão de Água", "uso": "Pesca", "img": "https://images.unsplash.com/photo-1598133894008-61f7fdb8cc3a?w=400"},
            {"n": "Abelhas", "uso": "Mel", "img": "https://images.unsplash.com/photo-1581404476143-fb31d742929f?w=400"}
        ]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MundoVivo")
    with st.expander("▶ SELECIONAR POVO"):
        selecao = st.radio("", list(povos.keys()))

povo = povos[selecao]

# --- MAPA ---
st.title(f"Exploração: {selecao}")
m = folium.Map(location=[39.5, -8.0], zoom_start=6, tiles="CartoDB dark_matter")
folium.Marker(povo["coords"], icon=folium.Icon(color="red")).add_to(m)
st_folium(m, width="100%", height=300)

# --- LISTAS HORIZONTAIS ---

st.markdown("<h3 class='section-title'>🛠️ Ferramentas</h3>", unsafe_allow_html=True)
cols_f = st.columns(len(povo["ferramentas"]))
for i, f in enumerate(povo["ferramentas"]):
    with cols_f[i]:
        st.markdown(f"""
            <div class="cc-card">
                <img src="{f['img']}" class="img-real">
                <div class="label">ARTEFACTO</div>
                <div class="value">{f['n']}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<h3 class='section-title'>🪪 Cartão de Cidadão Animal</h3>", unsafe_allow_html=True)
cols_a = st.columns(len(povo["animais"]))
for i, a in enumerate(povo["animais"]):
    with cols_a[i]:
        st.markdown(f"""
            <div class="cc-card">
                <div class="cc-header">REPÚBLICA POVOS ANTIGOS</div>
                <img src="{a['img']}" class="img-real">
                <div class="label">NOME / RAÇA</div>
                <div class="value">{a['n']}</div>
                <div class="label">UTILIZAÇÃO</div>
                <div class="value">{a['uso']}</div>
            </div>
        """, unsafe_allow_html=True)
