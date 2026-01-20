import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Povos Históricos de Portugal", layout="wide")

# Estilo CSS: Cartão de Cidadão (Preto Total)
st.markdown("""
    <style>
    .cc-card {
        background-color: #000000;
        color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        border: 2px solid #333;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    .cc-title {
        font-size: 0.75rem;
        color: #ff4b4b; /* Um toque de cor no topo */
        font-weight: bold;
        border-bottom: 1px solid #333;
        margin-bottom: 12px;
        letter-spacing: 2px;
    }
    .cc-photo {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 15px;
        border: 1px solid #444;
    }
    .label { color: #888; font-size: 0.7rem; text-transform: uppercase; margin-top: 10px; }
    .value { font-size: 1rem; font-weight: bold; border-bottom: 1px solid #222; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COMPLETA ---
povos = {
    "Lusitanos": {
        "coords": [40.3, -7.5],
        "ferramentas": ["Falcata", "Escudo Caetra", "Arado de Madeira", "Pontas de Lança", "Adagas de Bronze"],
        "animais": [
            {"nome": "Cavalo Lusitano", "uso": "Guerra e Caça", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"},
            {"nome": "Ovelha Bordaleira", "uso": "Produção de Lã", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=400"},
            {"nome": "Cabra da Serra", "uso": "Leite e Queijo", "img": "https://images.unsplash.com/photo-1524024973431-2ad916746881?w=400"}
        ]
    },
    "Celtas": {
        "coords": [41.5, -7.8],
        "ferramentas": ["Machado de Ferro", "Mó de Pedra", "Torques", "Caldeirão", "Tesouras de Tosa"],
        "animais": [
            {"nome": "Gado Barrosão", "uso": "Tração de Carros", "img": "https://images.unsplash.com/photo-1545468843-2796674f1df2?w=400"},
            {"nome": "Porco Bísaro", "uso": "Alimentação Base", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?w=400"},
            {"nome": "Cão de Caça", "uso": "Montaria e Proteção", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"}
        ]
    },
    "Galaicos": {
        "coords": [41.8, -8.4],
        "ferramentas": ["Gládio Castrejo", "Tear", "Hoz de Ferro", "Cerâmica Decorada"],
        "animais": [
            {"nome": "Vaca Cachena", "uso": "Sobrevivência na Serra", "img": "https://images.unsplash.com/photo-1500595046743-cd271d694d30?w=400"},
            {"nome": "Ponei Garrano", "uso": "Transporte de Minério", "img": "https://images.unsplash.com/photo-1598974357851-cb8143c0f243?w=400"}
        ]
    },
    "Conios": {
        "coords": [37.3, -8.0],
        "ferramentas": ["Estela Escrita", "Anzóis", "Redes de Pesca", "Ânforas de Azeite"],
        "animais": [
            {"nome": "Burro do Algarve", "uso": "Carga de Mercadorias", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?w=400"},
            {"nome": "Galinha Pedrês", "uso": "Aves de Quintal", "img": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400"}
        ]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧭 Menu")
    with st.expander("▶ VER POVOS"):
        escolha = st.radio("Selecione:", list(povos.keys()))

dados = povos[escolha]

# --- ECRÃ PRINCIPAL ---
st.title(f"Povo: {escolha}")

col_mapa, col_ferramentas, col_animais = st.columns([1.2, 0.8, 1.2])

with col_mapa:
    st.subheader("📍 Território")
    m = folium.Map(location=dados["coords"], zoom_start=7, tiles="CartoDB dark_matter")
    folium.Marker(location=dados["coords"], tooltip=escolha).add_to(m)
    st_folium(m, width=400, height=450)

with col_ferramentas:
    st.subheader("🛠️ Ferramentas")
    for f in dados["ferramentas"]:
        st.markdown(f"🔳 {f}")

with col_animais:
    st.subheader("🪪 Cartão de Cidadão Animal")
    for animal in dados["animais"]:
        # Se não houver imagem, usa um placeholder cinzento
        img_url = animal.get("img", "https://via.placeholder.com/400x200?text=Sem+Imagem")
        
        st.markdown(f"""
            <div class="cc-card">
                <div class="cc-title">REPUBLICA POVOS ANTIGOS</div>
                <img src="{img_url}" class="cc-photo">
                <div class="label">NOME</div>
                <div class="value">{animal['nome']}</div>
                <div class="label">FUNÇÃO</div>
                <div class="value">{animal['uso']}</div>
            </div>
        """, unsafe_allow_html=True)
