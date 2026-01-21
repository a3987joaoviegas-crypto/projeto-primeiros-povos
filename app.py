import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. Configuração de Nome e Layout
st.set_page_config(page_title="Primeiros Povos de Portugal", layout="wide")

# Estilo Visual Mundovivo - Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 15px 0; font-size: 1.3rem; }
    .cc-card {
        background-color: #111111; color: #ffffff; border: 1px solid #333;
        border-radius: 12px; padding: 15px; text-align: center; height: 100%;
    }
    .cc-header { font-size: 0.5rem; color: #888; border-bottom: 1px solid #222; margin-bottom: 10px; letter-spacing: 2px; }
    .img-real { 
        width: 100%; height: 160px; object-fit: cover; border-radius: 8px; 
        margin-bottom: 10px; border: 1px solid #444; background-color: #222;
    }
    .label { color: #666; font-size: 0.6rem; text-transform: uppercase; margin-top: 10px; }
    .value { font-size: 0.9rem; font-weight: bold; color: #fff; }
    .info-box { 
        background: #111111; padding: 20px; border-radius: 10px; 
        border: 1px solid #333; border-top: 4px solid #ffffff; margin-bottom: 20px; 
    }
    .epoch-detail { color: #aaa; font-size: 0.85rem; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATA AMPLIADA ---
povos_db = {
    "Lusitanos (Centro-Interior)": {
        "coords": [40.3, -7.5],
        "epoca_info": {
            "Sociedade": "Tribos independentes lideradas por chefes guerreiros.",
            "Habitação": "Casas de pedra retangulares ou circulares no topo de montes.",
            "Economia": "Pastoreio, caça e metalurgia de bronze e ouro."
        },
        "historia": "Guerreiros montanheses conhecidos pela resistência feroz liderada por Viriato.",
        "ferramentas": [
            {"n": "Falcata (Espada)", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"},
            {"n": "Escudo Caetra", "img": "https://images.unsplash.com/photo-1615678815958-5d413b70b653?w=400"},
            {"n": "Ponta de Lança", "img": "https://images.unsplash.com/photo-1510414695470-24970f807365?w=400"},
            {"n": "Tecelagem Manual", "img": "https://images.unsplash.com/photo-1615560113840-06900693f185?w=400"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "uso": "Guerra", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"},
            {"n": "Porco Alentejano", "uso": "Pastoreio", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?w=400"},
            {"n": "Ovelha Bordaleira", "uso": "Lã e Leite", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=400"},
            {"n": "Cão de Fila", "uso": "Guarda", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"}
        ]
    },
    "Celtas e Galaicos (Norte)": {
        "coords": [41.5, -8.3],
        "epoca_info": {
            "Sociedade": "Cultura castreja com clãs familiares organizados.",
            "Habitação": "Castros: aldeias fortificadas com casas circulares de pedra.",
            "Economia": "Agricultura de cereais e mineração avançada de ouro."
        },
        "historia": "Mestres da metalurgia e habitantes de fortalezas naturais conhecidas como Castros.",
        "ferramentas": [
            {"n": "Torques (Joia)", "img": "https://images.unsplash.com/photo-1611085583191-a3b1a6a939db?w=400"},
            {"n": "Machado de Ferro", "img": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=400"},
            {"n": "Mó de Pedra", "img": "https://images.unsplash.com/photo-1603566270543-92f750d03704?w=400"},
            {"n": "Caldeirão", "img": "https://images.unsplash.com/photo-1582738411706-bfc8e691d1c2?w=400"}
        ],
        "animais": [
            {"n": "Vaca Cachena", "uso": "Tração", "img": "https://images.unsplash.com/photo-1545468843-2796674f1df2?w=400"},
            {"n": "Boi Barrosão", "uso": "Trabalho Agrícola", "img": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400"},
            {"n": "Cão de Castro", "uso": "Proteção Gado", "img": "https://images.unsplash.com/photo-1544568100-847a948585b9?w=400"},
            {"n": "Garrano", "uso": "Transporte", "img": "https://images.unsplash.com/photo-1598974357851-cb8143c0f243?w=400"}
        ]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🗺️ EXPLORAÇÃO")
    modo = st.radio("Selecione o Modo:", ["Regiões", "Evolução Histórica"])
    selecionado = st.selectbox("Escolha o Povo/Época:", list(povos_db.keys()))
    dados = povos_db[selecionado]

# --- CONTEÚDO ---
st.title("Primeiros Povos de Portugal")

# Informações Detalhadas da Época
st.markdown(f"""
<div class='info-box'>
    <h3>Época: {selecionado}</h3>
    <p><b>Resumo:</b> {dados['historia']}</p>
    <hr style='border: 0.1px solid #333'>
    <div class='epoch-detail'>
        <b>🏠 Habitação:</b> {dados['epoca_info']['Habitação']}<br>
        <b>🤝 Sociedade:</b> {dados['epoca_info']['Sociedade']}<br>
        <b>💰 Economia:</b> {dados['epoca_info']['Economia']}
    </div>
</div>
""", unsafe_allow_html=True)

# Mapa
m = folium.Map(location=[39.5, -8.0], zoom_start=6, tiles="CartoDB dark_matter")
folium.Marker(dados["coords"], icon=folium.Icon(color="white")).add_to(m)
st_folium(m, width="100%", height=350)

# Listas Horizontais (Imagens Reais)
st.markdown("<div class='section-title'>⚒️ Tecnologia e Artefactos</div>", unsafe_allow_html=True)
cols_f = st.columns(4)
for i, f in enumerate(dados["ferramentas"]):
    with cols_f[i % 4]:
        st.markdown(f'<div class="cc-card"><img src="{f["img"]}" class="img-real"><div class="label">OBJETO</div><div class="value">{f["n"]}</div></div>', unsafe_allow_html=True)

st.markdown("<div class='section-title'>🪪 Cartão de Cidadão Animal</div>", unsafe_allow_html=True)
cols_a = st.columns(4)
for i, a in enumerate(dados["animais"]):
    with cols_a[i % 4]:
        st.markdown(f"""<div class="cc-card">
            <div class="cc-header">DOC. IDENTIFICAÇÃO ANCESTRAL</div>
            <img src="{a['img']}" class="img-real">
            <div class="label">ESPÉCIE/RAÇA</div>
            <div class="value">{a['n']}</div>
            <div class="label">FUNÇÃO NA ÉPOCA</div>
            <div class="value">{a['uso']}</div>
        </div>""", unsafe_allow_html=True)
