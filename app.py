import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. Configuração e Nome da App
st.set_page_config(page_title="Primeiros Povos de Portugal", layout="wide")

# Estilo Visual Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 15px 0; }
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
    .info-box { background: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 5px solid #ffffff; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COMPLETA (TODOS OS POVOS) ---
povos_db = {
    "Lusitanos": {
        "coords": [40.3, -7.5],
        "historia": "Habitantes das montanhas entre o Douro e o Tejo. Famosos pela resistência a Roma liderada por Viriato.",
        "ferramentas": [
            {"n": "Falcata", "img": "https://source.unsplash.com/400x300/?sword,ancient"},
            {"n": "Escudo Caetra", "img": "https://source.unsplash.com/400x300/?shield,warrior"},
            {"n": "Arado Madeira", "img": "https://source.unsplash.com/400x300/?plough,farm"},
            {"n": "Ponta de Lança", "img": "https://source.unsplash.com/400x300/?spear,iron"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "uso": "Guerra", "img": "https://source.unsplash.com/400x300/?horse,stallion"},
            {"n": "Porco Alentejano", "uso": "Alimento", "img": "https://source.unsplash.com/400x300/?pig,farm"},
            {"n": "Ovelha Bordaleira", "uso": "Lã", "img": "https://source.unsplash.com/400x300/?sheep,wool"},
            {"n": "Lobo Ibérico", "uso": "Mítico", "img": "https://source.unsplash.com/400x300/?wolf,forest"}
        ]
    },
    "Celtas e Galaicos": {
        "coords": [41.5, -8.3],
        "historia": "Povos do Noroeste com cultura de Castros. Grandes metalúrgicos do ouro e do ferro.",
        "ferramentas": [
            {"n": "Torques de Ouro", "img": "https://source.unsplash.com/400x300/?gold,jewelry"},
            {"n": "Machado Ferro", "img": "https://source.unsplash.com/400x300/?axe,tool"},
            {"n": "Caldeirão", "img": "https://source.unsplash.com/400x300/?cauldron,bronze"},
            {"n": "Mó de Pedra", "img": "https://source.unsplash.com/400x300/?stone,ancient"}
        ],
        "animais": [
            {"n": "Vaca Cachena", "uso": "Tração", "img": "https://source.unsplash.com/400x300/?cow,mountain"},
            {"n": "Cão de Castro", "uso": "Guarda", "img": "https://source.unsplash.com/400x300/?dog,guardian"},
            {"n": "Boi Barrosão", "uso": "Trabalho", "img": "https://source.unsplash.com/400x300/?ox,field"},
            {"n": "Garrano", "uso": "Transporte", "img": "https://source.unsplash.com/400x300/?pony,wild"}
        ]
    },
    "Conios": {
        "coords": [37.3, -8.1],
        "historia": "Povo do Sul (Algarve/Baixo Alentejo). Criadores da Escrita do Sudoeste, a mais antiga da península.",
        "ferramentas": [
            {"n": "Estela Escrita", "img": "https://source.unsplash.com/400x300/?tablet,inscription"},
            {"n": "Ânfora", "img": "https://source.unsplash.com/400x300/?pottery,ancient"},
            {"n": "Rede Pesca", "img": "https://source.unsplash.com/400x300/?fishing,net"},
            {"n": "Anzol Bronze", "img": "https://source.unsplash.com/400x300/?hook,bronze"}
        ],
        "animais": [
            {"n": "Burro Mirandês", "uso": "Carga", "img": "https://source.unsplash.com/400x300/?donkey,animal"},
            {"n": "Cão de Água", "uso": "Pesca", "img": "https://source.unsplash.com/400x300/?dog,water"},
            {"n": "Galinha Pedrês", "uso": "Ovos", "img": "https://source.unsplash.com/400x300/?chicken,hen"},
            {"n": "Abelhas", "uso": "Mel", "img": "https://source.unsplash.com/400x300/?bees,honey"}
        ]
    },
    "Túrdulos": {
        "coords": [38.2, -7.5],
        "historia": "Povo proveniente da Tartéssia, ocuparam o Vale do Guadiana e o litoral alentejano.",
        "ferramentas": [{"n": "Cerâmica", "img": "https://source.unsplash.com/400x300/?clay,pot"}],
        "animais": [{"n": "Lince Ibérico", "uso": "Caça", "img": "https://source.unsplash.com/400x300/?lynx,cat"}]
    },
    "Brácaros": {
        "coords": [41.5, -8.4],
        "historia": "Povo de Bracara Augusta (Braga), conhecidos pela sua forte resistência e tradição guerreira.",
        "ferramentas": [{"n": "Espada Curta", "img": "https://source.unsplash.com/400x300/?dagger,ancient"}],
        "animais": [{"n": "Cão de Fila", "uso": "Guerra", "img": "https://source.unsplash.com/400x300/?mastiff,dog"}]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MENU PRINCIPAL")
    modo = st.radio("Selecione o Modo:", ["Povos Ancestrais", "Evolução Portuguesa"])
    
    if modo == "Evolução Portuguesa":
        etapa = st.select_slider("Linha do Tempo:", options=list(povos_db.keys()))
        dados = povos_db[etapa]
    else:
        escolha = st.selectbox("Escolha o Povo:", list(povos_db.keys()))
        dados = povos_db[escolha]

# --- CONTEÚDO ---
st.title("Primeiros Povos de Portugal")

if modo == "Evolução Portuguesa":
    st.markdown(f"<div class='info-box'><h3>História de {etapa}</h3><p>{dados['historia']}</p></div>", unsafe_allow_html=True)
else:
    st.header(f"Explorando: {escolha}")

# Mapa
m = folium.Map(location=dados["coords"], zoom_start=7, tiles="CartoDB dark_matter")
folium.Marker(dados["coords"], icon=folium.Icon(color="red")).add_to(m)
st_folium(m, width="100%", height=300)

# Listas Horizontais
st.markdown("<h3 class='section-title'>🛠️ Ferramentas e Tecnologia</h3>", unsafe_allow_html=True)
cols_f = st.columns(len(dados["ferramentas"]))
for i, f in enumerate(dados["ferramentas"]):
    with cols_f[i]:
        st.markdown(f'<div class="cc-card"><img src="{f["img"]}" class="img-real"><div class="label">ARTEFACTO</div><div class="value">{f["n"]}</div></div>', unsafe_allow_html=True)

st.markdown("<h3 class='section-title'>🪪 Cartão de Cidadão Animal</h3>", unsafe_allow_html=True)
cols_a = st.columns(len(dados["animais"]))
for i, a in enumerate(dados["animais"]):
    with cols_a[i]:
        st.markdown(f'<div class="cc-card"><div class="cc-header">REPÚBLICA POVOS ANTIGOS</div><img src="{a["img"]}" class="img-real"><div class="label">NOME</div><div class="value">{a["n"]}</div><div class="label">USO</div><div class="value">{a["uso"]}</div></div>', unsafe_allow_html=True)
