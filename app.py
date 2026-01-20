import streamlit as st
import folium
from streamlit_folium import st_folium

# Configuração da página
st.set_page_config(page_title="Povos Antigos PT", layout="wide")

# Estilização CSS para o Cartão de Cidadão Preto com Letras Brancas
st.markdown("""
    <style>
    .cc-animal-container {
        background-color: #1e1e1e;
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #444;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .cc-header {
        font-size: 0.8rem;
        letter-spacing: 2px;
        color: #888;
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    .cc-foto {
        width: 100%;
        height: 150px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #333;
    }
    .cc-info {
        width: 100%;
        font-family: 'Courier New', Courier, monospace;
    }
    .cc-campo { color: #aaa; font-size: 0.7rem; margin-top: 5px; }
    .cc-valor { font-size: 1rem; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
povos_data = {
    "Lusitanos": {
        "coords": [40.2, -7.5],
        "ferramentas": ["Falcata (Espada Curva)", "Dardo de Arremesso", "Arado de Madeira", "Mó de Pedra"],
        "animais": [
            {
                "nome": "Cavalo Lusitano",
                "funcao": "Montada de Guerra",
                "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"
            },
            {
                "nome": "Ovelha Bordaleira",
                "funcao": "Produção de Lã/Leite",
                "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=400"
            }
        ]
    },
    "Celtas": {
        "coords": [41.5, -8.4],
        "ferramentas": ["Machado de Ferro", "Fíbula em Bronze", "Caldeirão", "Serra de Metal"],
        "animais": [
            {
                "nome": "Cão de Castro Laboreiro",
                "funcao": "Guardião de Gado",
                "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"
            },
            {
                "nome": "Gado Barrosão",
                "funcao": "Trabalho Pesado",
                "img": "https://images.unsplash.com/photo-1545468843-2796674f1df2?w=400"
            }
        ]
    }
}

# --- SIDEBAR COM A SETINHA (EXPANDER) ---
with st.sidebar:
    st.title("🧭 Navegação")
    with st.expander("▶ ESCOLHER POVO"):
        selecao = st.radio("", list(povos_data.keys()))

povo = povos_data[selecao]

# --- LAYOUT PRINCIPAL ---
st.title(f"Povo: {selecao}")

col_mapa, col_ferramentas, col_animais = st.columns([1.5, 1, 1.2])

with col_mapa:
    st.subheader("📍 Localização")
    m = folium.Map(location=povo["coords"], zoom_start=7, tiles="CartoDB dark_matter")
    folium.Marker(location=povo["coords"], tooltip=selecao).add_to(m)
    st_folium(m, width=400, height=400)

with col_ferramentas:
    st.subheader("🛠️ Ferramentas")
    for f in povo["ferramentas"]:
        st.markdown(f"✅ **{f}**")

with col_animais:
    st.subheader("🪪 Cartão de Cidadão Animal")
    for animal in povo["animais"]:
        st.markdown(f"""
            <div class="cc-animal-container">
                <div class="cc-header">República de Portugal Antiga</div>
                <img src="{animal['img']}" class="cc-foto">
                <div class="cc-info">
                    <div class="cc-campo">NOME / NAME</div>
                    <div class="cc-valor">{animal['nome']}</div>
                    <div class="cc-campo">OCUPAÇÃO / OCCUPATION</div>
                    <div class="cc-valor">{animal['funcao']}</div>
                    <div class="cc-campo">POVO / ORIGIN</div>
                    <div class="cc-valor">{selecao}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.divider()
st.info("💡 Este projeto está estruturado para o GitHub. Use o arquivo requirements.txt para o Streamlit Cloud.")
