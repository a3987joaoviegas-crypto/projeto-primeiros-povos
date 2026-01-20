import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuração da página
st.set_page_config(page_title="Povos Antigos de Portugal", layout="wide")

# --- DATABASE SIMULADA ---
# Num projeto real, isto poderia estar num ficheiro CSV ou JSON
povos_data = {
    "Lusitanos": {
        "coords": [40.2, -7.5],
        "descricao": "Ocupavam as terras entre os rios Douro e Tejo. Conhecidos pela resistência aos Romanos.",
        "ferramentas": ["Falcata (Espada)", "Escudos de couro", "Arados de madeira", "Pontas de lança em bronze"],
        "animais": ["Cavalos lusitanos", "Ovelhas", "Cabras", "Porcos"],
        "cor": "green"
    },
    "Celtas": {
        "coords": [41.5, -8.4],
        "descricao": "Presentes sobretudo no Norte e Alentejo. Mestres da metalurgia e da cultura dos castros.",
        "ferramentas": ["Fíbulas de ouro", "Machados de ferro", "Mós manuais", "Torques"],
        "animais": ["Gado vacum", "Cães de caça", "Ovelhas", "Porcos"],
        "cor": "blue"
    },
    "Conios": {
        "coords": [37.2, -8.0],
        "descricao": "Habitavam o Algarve e Baixo Alentejo. Tiveram grande influência da escrita tartéssica.",
        "ferramentas": ["Estelas de pedra escrita", "Ânforas de cerâmica", "Anzóis de pesca"],
        "animais": ["Peixe (aquicultura primitiva)", "Gado", "Aves de capoeira"],
        "cor": "orange"
    }
}

# --- SIDEBAR ---
st.sidebar.title("🏛️ Povos de Portugal")
st.sidebar.markdown("Selecione um povo para detalhar:")
selecao = st.sidebar.selectbox("Povo:", list(povos_data.keys()))

povo = povos_data[selecao]

# Secções da Sidebar baseadas na seleção
st.sidebar.header(f"🛠️ Ferramentas - {selecao}")
for f in povo["ferramentas"]:
    st.sidebar.write(f"- {f}")

st.sidebar.header(f"🐖 Animais de Quinta")
for a in povo["animais"]:
    st.sidebar.write(f"- {a}")

# --- CORPO PRINCIPAL ---
st.title(f"Explorador Histórico: {selecao}")
st.write(povo["descricao"])

# Configuração do Mapa
m = folium.Map(location=[39.5, -8.0], zoom_start=6, tiles="CartoDB positron")

# Adicionar marcadores de todos os povos
for nome, info in povos_data.items():
    icon_color = "red" if nome == selecao else info["cor"]
    folium.Marker(
        location=info["coords"],
        popup=nome,
        tooltip=nome,
        icon=folium.Icon(color=icon_color, icon="info-sign")
    ).add_to(m)

# Exibir o mapa
st_folium(m, width=700, height=500)

st.info("💡 Clique nos marcadores no mapa ou use a barra lateral para navegar.")
