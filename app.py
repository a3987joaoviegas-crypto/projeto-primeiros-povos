import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="MundoVivo: Povos de Portugal", layout="wide")

# Estilo CSS para o Cartão de Cidadão Preto e Listas Horizontais
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .section-title {
        color: white;
        border-left: 5px solid #ff4b4b;
        padding-left: 10px;
        margin: 20px 0;
    }
    .cc-card {
        background-color: #000000;
        color: #ffffff;
        border: 2px solid #ffffff;
        border-radius: 10px;
        padding: 15px;
        min-width: 200px;
        margin-bottom: 10px;
    }
    .cc-title { font-size: 0.6rem; color: #888; text-align: center; border-bottom: 1px solid #333; margin-bottom: 10px; }
    .img-fluid {
        width: 100%;
        height: 120px;
        object-fit: cover;
        border-radius: 5px;
        margin-bottom: 8px;
    }
    .label { color: #888; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.85rem; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DADOS COMPLETA ---
povos_data = {
    "Lusitanos": {
        "coords": [40.3, -7.5],
        "ferramentas": [
            {"n": "Falcata", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"},
            {"n": "Escudo Caetra", "img": "https://images.unsplash.com/photo-1547631100-305f609e900c?w=400"},
            {"n": "Arado", "img": "https://images.unsplash.com/photo-1594391829624-dfc392bbbc24?w=400"}
        ],
        "animais": [
            {"n": "Cavalo", "uso": "Guerra", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"},
            {"n": "Ovelha", "uso": "Lã", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=400"},
            {"n": "Cabra", "uso": "Leite", "img": "https://images.unsplash.com/photo-1524024973431-2ad916746881?w=400"}
        ]
    },
    "Celtas": {
        "coords": [41.5, -8.0],
        "ferramentas": [
            {"n": "Machado", "img": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=400"},
            {"n": "Caldeirão", "img": "https://images.unsplash.com/photo-1582738411706-bfc8e691d1c2?w=400"}
        ],
        "animais": [
            {"n": "Boi", "uso": "Arado", "img": "https://images.unsplash.com/photo-1545468843-2796674f1df2?w=400"},
            {"n": "Porco", "uso": "Alimento", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?w=400"}
        ]
    },
    "Conios": {
        "coords": [37.2, -8.1],
        "ferramentas": [
            {"n": "Anzol", "img": "https://images.unsplash.com/photo-1516937941344-00b4e0337589?w=400"},
            {"n": "Estela", "img": "https://images.unsplash.com/photo-1518153925617-3a629474bc9b?w=400"}
        ],
        "animais": [
            {"n": "Burro", "uso": "Carga", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?w=400"},
            {"n": "Galinha", "uso": "Ovos", "img": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400"}
        ]
    }
}

# --- SIDEBAR COM SETA ---
with st.sidebar:
    st.title("MundoVivo PT")
    with st.expander("▶ ESCOLHER POVO"):
        selecao = st.radio("", list(povos_data.keys()))

povo = povos_data[selecao]

# --- LAYOUT SUPERIOR: MAPA ---
st.title(f"Povo: {selecao}")
m = folium.Map(location=[39.5, -8.0], zoom_start=6, tiles="CartoDB dark_matter")
folium.Marker(povo["coords"], popup=selecao, icon=folium.Icon(color='red')).add_to(m)
st_folium(m, width="100%", height=350)

st.divider()

# --- LAYOUT INFERIOR: LISTAS HORIZONTAIS ---

# 1. FERRAMENTAS
st.markdown("<h2 class='section-title'>🛠️ Ferramentas Usadas</h2>", unsafe_allow_html=True)
cols_f = st.columns(len(povo["ferramentas"]))
for i, f in enumerate(povo["ferramentas"]):
    with cols_f[i]:
        st.markdown(f"""
            <div class="cc-card">
                <img src="{f['img']}" class="img-fluid">
                <div class="label">FERRAMENTA</div>
                <div class="value">{f['n']}</div>
            </div>
        """, unsafe_allow_html=True)

# 2. ANIMAIS (CARTÃO DE CIDADÃO)
st.markdown("<h2 class='section-title'>🪪 Animais da Quinta (Cartão de Cidadão)</h2>", unsafe_allow_html=True)
cols_a = st.columns(len(povo["animais"]))
for i, a in enumerate(povo["animais"]):
    with cols_a[i]:
        st.markdown(f"""
            <div class="cc-card">
                <div class="cc-title">REPÚBLICA POVOS ANTIGOS</div>
                <img src="{a['img']}" class="img-fluid">
                <div class="label">NOME</div>
                <div class="value">{a['n']}</div>
                <div class="label">FUNÇÃO</div>
                <div class="value">{a['uso']}</div>
            </div>
        """, unsafe_allow_html=True)
