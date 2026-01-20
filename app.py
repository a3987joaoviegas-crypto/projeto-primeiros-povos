import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuração da página
st.set_page_config(page_title="Povos de Portugal", layout="wide")

# Estilo CSS para o "Cartão de Cidadão" dos animais e design
st.markdown("""
    <style>
    .cc-animal {
        border: 2px solid #2e4a62;
        border-radius: 10px;
        padding: 15px;
        background-color: #f0f2f6;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .cc-header {
        color: #2e4a62;
        font-weight: bold;
        border-bottom: 1px solid #2e4a62;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
povos_data = {
    "Lusitanos": {
        "coords": [40.2, -7.5],
        "descricao": "Guerreiros e pastores da zona central de Portugal.",
        "ferramentas": ["Falcata (Espada)", "Escudo Caetra", "Arado de Madeira"],
        "animais": [
            {"nome": "Cavalo Lusitano", "origem": "Serra da Estrela", "funcao": "Guerra/Transporte"},
            {"nome": "Ovelha Bordaleira", "origem": "Vales do Mondego", "funcao": "Lã e Leite"}
        ]
    },
    "Celtas": {
        "coords": [41.5, -8.4],
        "descricao": "Mestres da metalurgia do ferro e construtores de Castros.",
        "ferramentas": ["Fíbula de Bronze", "Machado de Ferro", "Mó de Pedra"],
        "animais": [
            {"nome": "Gado Barrosão", "origem": "Minho/Gerês", "funcao": "Trabalho Agrícola"},
            {"nome": "Cão de Castro Laboreiro", "origem": "Planalto de Castro", "funcao": "Guarda de Rebanho"}
        ]
    }
}

# --- SIDEBAR COM SETINHA (EXPANDER) ---
st.sidebar.title("🏛️ Navegação")

with st.sidebar.expander("▶ Ver Povos de Portugal"):
    escolha_povo = st.radio("Selecione um povo para explorar:", list(povos_data.keys()))

povo = povos_data[escolha_povo]

# --- CORPO PRINCIPAL ---
st.title(f"Explorador Histórico: {escolha_povo}")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 Localização e História")
    m = folium.Map(location=[39.5, -8.0], zoom_start=6, tiles="CartoDB positron")
    folium.Marker(location=povo["coords"], popup=escolha_povo, icon=folium.Icon(color="red")).add_to(m)
    st_folium(m, width=700, height=400)
    st.write(povo["descricao"])

with col2:
    # SECÇÃO DE FERRAMENTAS
    st.subheader("🛠️ Ferramentas")
    for f in povo["ferramentas"]:
        st.info(f)

    # SECÇÃO DE ANIMAIS (CARTÃO DE CIDADÃO)
    st.subheader("🐖 Animais (CC)")
    for animal in povo["animais"]:
        st.markdown(f"""
            <div class="cc-animal">
                <div class="cc-header">CARTÃO DE CIDADÃO ANIMAL</div>
                <b>Nome:</b> {animal['nome']}<br>
                <b>Natural de:</b> {animal['origem']}<br>
                <b>Ocupação:</b> {animal['funcao']}
            </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption("Código disponível no GitHub | Desenvolvido com Streamlit")
