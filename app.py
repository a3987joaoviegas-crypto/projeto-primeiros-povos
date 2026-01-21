import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. Nome da App e Configuração
st.set_page_config(page_title="Primeiros Povos de Portugal", layout="wide")

# Estilo Visual Mundovivo - Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ff4b4b; padding-left: 15px; margin: 30px 0 15px 0; font-size: 1.2rem; font-weight: bold; }
    .cc-card {
        background-color: #111111; color: #ffffff; border: 1px solid #333;
        border-radius: 12px; padding: 15px; text-align: center; height: 100%;
    }
    .cc-header { font-size: 0.5rem; color: #888; border-bottom: 1px solid #222; margin-bottom: 10px; letter-spacing: 2px; }
    .img-real { 
        width: 100%; height: 150px; object-fit: cover; border-radius: 8px; 
        margin-bottom: 10px; border: 1px solid #444; background-color: #222;
    }
    .label { color: #666; font-size: 0.6rem; text-transform: uppercase; margin-top: 10px; }
    .value { font-size: 0.9rem; font-weight: bold; color: #fff; }
    .info-box { background: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE MASSIVA (7 REGIÕES E POVOS) ---
povos_db = {
    "Lusitanos (Centro)": {
        "coords": [40.3, -7.5],
        "historia": "Guerreiros da Serra da Estrela, famosos pela resistência contra Roma sob o comando de Viriato.",
        "ferramentas": [
            {"n": "Falcata", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"},
            {"n": "Caetra (Escudo)", "img": "https://images.unsplash.com/photo-1615678815958-5d413b70b653?w=400"},
            {"n": "Ponta de Lança", "img": "https://images.unsplash.com/photo-1510414695470-24970f807365?w=400"},
            {"n": "Fuso de Tecelagem", "img": "https://images.unsplash.com/photo-1615560113840-06900693f185?w=400"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "uso": "Guerra", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"},
            {"n": "Porco Alentejano", "uso": "Alimento", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?w=400"},
            {"n": "Ovelha Bordaleira", "uso": "Lã", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=400"},
            {"n": "Cão de Fila", "uso": "Guarda", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"}
        ]
    },
    "Celtas e Galaicos (Norte)": {
        "coords": [41.5, -8.3],
        "historia": "Habitantes dos Castros fortificados no topo das montanhas. Mestres da metalurgia do ouro.",
        "ferramentas": [
            {"n": "Torques Ouro", "img": "https://images.unsplash.com/photo-1611085583191-a3b1a6a939db?w=400"},
            {"n": "Machado Ferro", "img": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=400"},
            {"n": "Caldeirão Bronze", "img": "https://images.unsplash.com/photo-1582738411706-bfc8e691d1c2?w=400"},
            {"n": "Mó de Pedra", "img": "https://images.unsplash.com/photo-1603566270543-92f750d03704?w=400"}
        ],
        "animais": [
            {"n": "Vaca Cachena", "uso": "Tração", "img": "https://images.unsplash.com/photo-1545468843-2796674f1df2?w=400"},
            {"n": "Cão de Castro", "uso": "Proteção", "img": "https://images.unsplash.com/photo-1544568100-847a948585b9?w=400"},
            {"n": "Garrano", "uso": "Transporte", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"},
            {"n": "Boi Barrosão", "uso": "Trabalho", "img": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400"}
        ]
    },
    "Conios (Algarve)": {
        "coords": [37.1, -8.2],
        "historia": "O povo mais antigo com escrita própria (Escrita do Sudoeste). Grandes pescadores e comerciantes marítimos.",
        "ferramentas": [
            {"n": "Estela Escrita", "img": "https://images.unsplash.com/photo-1518153925617-3a629474bc9b?w=400"},
            {"n": "Ânfora Barro", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?w=400"},
            {"n": "Rede Pesca", "img": "https://images.unsplash.com/photo-1501703979959-79396f212591?w=400"},
            {"n": "Anzol Bronze", "img": "https://images.unsplash.com/photo-1516937941344-00b4e0337589?w=400"}
        ],
        "animais": [
            {"n": "Burro Algarve", "uso": "Carga", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?w=400"},
            {"n": "Cão de Água", "uso": "Ajuda Pesca", "img": "https://images.unsplash.com/photo-1598133894008-61f7fdb8cc3a?w=400"},
            {"n": "Galinha Pedrês", "uso": "Ovos", "img": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400"},
            {"n": "Abelhas", "uso": "Mel", "img": "https://images.unsplash.com/photo-1581404476143-fb31d742929f?w=400"}
        ]
    },
    "Túrdulos (Alentejo)": {
        "coords": [38.5, -7.9],
        "historia": "Povo proveniente da Tartéssia, famosos pela sua cerâmica e organização urbana avançada.",
        "ferramentas": [{"n": "Cerâmica", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?w=400"}],
        "animais": [{"n": "Lince Ibérico", "uso": "Mítico", "img": "https://images.unsplash.com/photo-1564349683136-77e08bef1ef1?w=400"}]
    },
    "Brácaros (Minho)": {
        "coords": [41.5, -8.4],
        "historia": "Guerreiros do Minho que deram nome a Braga. Resistentes ferozes à conquista romana.",
        "ferramentas": [{"n": "Espada Curta", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"}],
        "animais": [{"n": "Cão de Fila", "uso": "Guerra", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"}]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MENU")
    modo = st.radio("Selecione o Modo:", ["Explorar Regiões", "Evolução Portuguesa"])
    
    if modo == "Evolução Portuguesa":
        selecionado = st.select_slider("Linha do Tempo:", options=list(povos_db.keys()))
        dados = povos_db[selecionado]
    else:
        selecionado = st.selectbox("Escolha a Região/Povo:", list(povos_db.keys()))
        dados = povos_db[selecionado]

# --- CONTEÚDO PRINCIPAL ---
st.title("Primeiros Povos de Portugal")

if modo == "Evolução Portuguesa":
    st.markdown(f"<div class='info-box'><h3>Info Histórica: {selecionado}</h3><p>{dados['historia']}</p></div>", unsafe_allow_html=True)
else:
    st.header(f"Região: {selecionado}")

# Mapa
m = folium.Map(location=[39.5, -8.0], zoom_start=6, tiles="CartoDB dark_matter")
folium.Marker(dados["coords"], icon=folium.Icon(color="red")).add_to(m)
st_folium(m, width="100%", height=350)

# Ferramentas Horizontal
st.markdown("<div class='section-title'>🛠️ Ferramentas da Época</div>", unsafe_allow_html=True)
cols_f = st.columns(4)
for i, f in enumerate(dados["ferramentas"]):
    with cols_f[i % 4]:
        st.markdown(f"""<div class="cc-card">
            <img src="{f['img']}" class="img-real">
            <div class="label">ARTEFACTO</div>
            <div class="value">{f['n']}</div>
        </div>""", unsafe_allow_html=True)

# Animais Horizontal
st.markdown("<div class='section-title'>🪪 Cartão de Cidadão Animal</div>", unsafe_allow_html=True)
cols_a = st.columns(4)
for i, a in enumerate(dados["animais"]):
    with cols_a[i % 4]:
        st.markdown(f"""<div class="cc-card">
            <div class="cc-header">REPÚBLICA POVOS ANTIGOS</div>
            <img src="{a['img']}" class="img-real">
            <div class="label">NOME/RAÇA</div>
            <div class="value">{a['n']}</div>
            <div class="label">FUNÇÃO</div>
            <div class="value">{a['uso']}</div>
        </div>""", unsafe_allow_html=True)
