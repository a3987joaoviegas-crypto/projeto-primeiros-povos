import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Povos Pré-Romanos de Portugal", layout="wide")

# Estilização CSS: Cartão de Cidadão Preto e Branco
st.markdown("""
    <style>
    .cc-card {
        background-color: #000000;
        color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #333;
        font-family: 'Arial', sans-serif;
    }
    .cc-title {
        font-size: 0.7rem;
        color: #888;
        border-bottom: 1px solid #333;
        margin-bottom: 10px;
        padding-bottom: 5px;
        text-transform: uppercase;
    }
    .cc-photo {
        width: 100%;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .label { color: #666; font-size: 0.7rem; }
    .value { font-size: 0.9rem; margin-bottom: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DADOS COMPLETA ---
povos = {
    "Lusitanos": {
        "coords": [40.3, -7.5],
        "ferramentas": ["Falcata (Espada)", "Punhal de Antenas", "Dardo (Soliferrum)", "Escudo Caetra", "Arado de Madeira"],
        "animais": [
            {"nome": "Cavalo Lusitano", "uso": "Guerra e Prestígio", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=300"},
            {"nome": "Ovelha Bordaleira", "uso": "Lã e Alimentação", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=300"},
            {"nome": "Cabra Serrana", "uso": "Leite e Carne", "img": "https://images.unsplash.com/photo-1524024973431-2ad916746881?w=300"}
        ]
    },
    "Celtas (Celtici)": {
        "coords": [38.5, -7.9],
        "ferramentas": ["Machado de Ferro", "Torques de Ouro", "Mó de Pedra Transmontana", "Caldeirão de Bronze"],
        "animais": [
            {"nome": "Gado Alentejano", "uso": "Trabalho Agrícola", "img": "https://images.unsplash.com/photo-1545468843-2796674f1df2?w=300"},
            {"nome": "Porco Alentejano", "uso": "Alimentação (Bolota)", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?w=300"}
        ]
    },
    "Galaicos": {
        "coords": [41.7, -8.5],
        "ferramentas": ["Gládio", "Hoz de Ferro (Colheita)", "Pedra de Funda", "Cerâmica Castreja"],
        "animais": [
            {"nome": "Cão de Castro Laboreiro", "uso": "Guarda de Rebanhos", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=300"},
            {"nome": "Vaca Cachena", "uso": "Tração e Leite", "img": "https://images.unsplash.com/photo-1500595046743-cd271d694d30?w=300"}
        ]
    },
    "Conios": {
        "coords": [37.2, -8.2],
        "ferramentas": ["Escrita Tartéssica (Estelas)", "Anzóis de Cobre", "Ânforas de Vinho", "Redes de Pesca"],
        "animais": [
            {"nome": "Burro de Mirandês", "uso": "Transporte de Carga", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?w=300"},
            {"nome": "Galinha Pedrês", "uso": "Ovos e Carne", "img": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=300"}
        ]
    },
    "Túrdulos Oppidanos": {
        "coords": [39.0, -8.8],
        "ferramentas": ["Espada de Bronze", "Tear Vertical", "Moinho de Rotação", "Fíbula de Anular"],
        "animais": [
            {"nome": "Boi Bravo", "uso": "Simbolismo e Trabalho", "img": "https://images.unsplash.com/photo-1551333330-8049280d8591?w=300"}
        ]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("🗺️ Menu Histórico")
    with st.expander("▶ SELECIONAR POVO"):
        escolha = st.radio("Lista de Povos:", list(povos.keys()))

dados = povos[escolha]

# --- CONTEÚDO ---
st.title(f"Antigos Povos: {escolha}")

col_info, col_ferramentas, col_animais = st.columns([1.5, 0.8, 1.2])

with col_info:
    st.subheader("Localização Estimada")
    m = folium.Map(location=dados["coords"], zoom_start=7, tiles="CartoDB dark_matter")
    folium.Marker(location=dados["coords"], popup=escolha, icon=folium.Icon(color='white')).add_to(m)
    st_folium(m, width=450, height=450)

with col_ferramentas:
    st.subheader("⚒️ Ferramentas")
    for f in dados["ferramentas"]:
        st.write(f"▪️ {f}")

with col_animais:
    st.subheader("🪪 Cartão de Cidadão Animal")
    # Mostrar todos os animais do povo selecionado
    for animal in dados["animais"]:
        st.markdown(f"""
            <div class="cc-card">
                <div class="cc-title">Documento de Identificação Animal</div>
                <img src="{animal['img']}" class="cc-photo">
                <div class="label">NOME COMUM</div>
                <div class="value">{animal['nome']}</div>
                <div class="label">FUNÇÃO NA QUINTA / TRIBO</div>
                <div class="value">{animal['uso']}</div>
                <div class="label">POVO DETENTOR</div>
                <div class="value">{escolha}</div>
            </div>
        """, unsafe_allow_html=True)
