import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mundovivo: Portugal", layout="wide")

# Inicializar Favoritos
if 'minhas_tribos' not in st.session_state:
    st.session_state.minhas_tribos = []

# CSS Mundovivo Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 15px 0; font-size: 1.2rem; }
    .cc-card { background-color: #111111; color: #ffffff; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; height: 100%; }
    .img-box { width: 100%; height: 140px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; }
    .label { color: #888; font-size: 0.6rem; text-transform: uppercase; margin-top: 5px; }
    .value { font-size: 0.85rem; font-weight: bold; color: #fff; }
    .info-box { background: #111111; padding: 20px; border-radius: 10px; border-top: 4px solid #ffffff; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COMPLETA (7 ÉPOCAS) ---
db = {
    "1. Pré-História": {
        "coord": [38.5, -8.0], "info": "Megalitismo e Caçadores.",
        "ferramentas": [
            {"n": "Biface", "f": "Corte", "img": "https://images.unsplash.com/photo-1510414695470-24970f807365?w=400"},
            {"n": "Arco", "f": "Caça", "img": "https://images.unsplash.com/photo-1511406361295-0a5ff814c0ad?w=400"},
            {"n": "Silex", "f": "Perfurar", "img": "https://images.unsplash.com/photo-1619678595438-66037d4560e2?w=400"},
            {"n": "Vaso", "f": "Cozinha", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?w=400"}
        ],
        "animais": [
            {"n": "Lobo", "f": "Predador", "img": "https://images.unsplash.com/photo-1590424753042-32244f05563c?w=400"},
            {"n": "Cervo", "f": "Alimento", "img": "https://images.unsplash.com/photo-1549194380-f3c6c795af0e?w=400"},
            {"n": "Javali", "f": "Caça", "img": "https://images.unsplash.com/photo-1516248967355-90033c94d13c?w=400"},
            {"n": "Boi", "f": "Força", "img": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400"}
        ]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros da Serra da Estrela.",
        "ferramentas": [
            {"n": "Falcata", "f": "Guerra", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"},
            {"n": "Escudo", "f": "Defesa", "img": "https://images.unsplash.com/photo-1615678815958-5d413b70b653?w=400"},
            {"n": "Lança", "f": "Ataque", "img": "https://images.unsplash.com/photo-1558285511-966956795f55?w=400"},
            {"n": "Tecelagem", "f": "Roupas", "img": "https://images.unsplash.com/photo-1615560113840-06900693f185?w=400"}
        ],
        "animais": [
            {"n": "Cavalo", "f": "Montaria", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"},
            {"n": "Porco", "f": "Carne", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?w=400"},
            {"n": "Ovelha", "f": "Lã", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=400"},
            {"n": "Cão", "f": "Guarda", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"}
        ]
    },
    "3. Conios": {
        "coord": [37.1, -8.2], "info": "Povo da Escrita do Sul.",
        "ferramentas": [
            {"n": "Estela", "f": "Escrita", "img": "https://images.unsplash.com/photo-1515542641795-85ed3b3b4297?w=400"},
            {"n": "Rede", "f": "Pesca", "img": "https://images.unsplash.com/photo-1501703979959-79396f212591?w=400"},
            {"n": "Anzol", "f": "Pesca", "img": "https://images.unsplash.com/photo-1516937941344-00b4e0337589?w=400"},
            {"n": "Ânfora", "f": "Azeite", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?w=400"}
        ],
        "animais": [
            {"n": "Burro", "f": "Carga", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?w=400"},
            {"n": "Cão Água", "f": "Pesca", "img": "https://images.unsplash.com/photo-1598133894008-61f7fdb8cc3a?w=400"},
            {"n": "Galinha", "f": "Ovos", "img": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400"},
            {"n": "Abelha", "f": "Mel", "img": "https://images.unsplash.com/photo-1581404476143-fb31d742929f?w=400"}
        ]
    },
    "4. Romanos": {
        "coord": [38.4, -7.9], "info": "Império e Estradas.",
        "ferramentas": [{"n": "Gladius", "f": "Guerra", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"}, {"n": "Moeda", "f": "Troca", "img": "https://images.unsplash.com/photo-1611085583191-a3b1a6a939db?w=400"}, {"n": "Mosaico", "f": "Arte", "img": "https://images.unsplash.com/photo-1576016770956-debb63d92058?w=400"}, {"n": "Groma", "f": "Medição", "img": "https://images.unsplash.com/photo-1503387762-592dea58ef21?w=400"}],
        "animais": [{"n": "Boi", "f": "Arado", "img": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400"}, {"n": "Mula", "f": "Carga", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?w=400"}, {"n": "Ganso", "f": "Guarda", "img": "https://images.unsplash.com/photo-1542316812-730623661600?w=400"}, {"n": "Cavalo", "f": "Correio", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"}]
    },
    "5. Visigodos": {
        "coord": [38.1, -7.8], "info": "Reinos Germânicos.",
        "ferramentas": [{"n": "Fíbula", "f": "Adorno", "img": "https://images.unsplash.com/photo-1611085583191-a3b1a6a939db?w=400"}, {"n": "Espada", "f": "Guerra", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"}, {"n": "Cruz", "f": "Religião", "img": "https://images.unsplash.com/photo-1544427920-c49ccfb85579?w=400"}, {"n": "Escudo", "f": "Defesa", "img": "https://images.unsplash.com/photo-1615678815958-5d413b70b653?w=400"}],
        "animais": [{"n": "Falcão", "f": "Caça", "img": "https://images.unsplash.com/photo-1506197072618-7ad5df6296df?w=400"}, {"n": "Cavalo", "f": "Montaria", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"}, {"n": "Cão", "f": "Caça", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"}, {"n": "Cabra", "f": "Leite", "img": "https://images.unsplash.com/photo-1524024973431-2ad916746881?w=400"}]
    },
    "6. Árabes": {
        "coord": [37.2, -7.9], "info": "Al-Andalus.",
        "ferramentas": [{"n": "Astrolábio", "f": "Astros", "img": "https://images.unsplash.com/photo-1533134486753-c833f074868f?w=400"}, {"n": "Nora", "f": "Água", "img": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=400"}, {"n": "Azulejo", "f": "Decoração", "img": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=400"}, {"n": "Alaúde", "f": "Música", "img": "https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=400"}],
        "animais": [{"n": "Camelo", "f": "Carga", "img": "https://images.unsplash.com/photo-1551029506-0807df4e2031?w=400"}, {"n": "Cavalo", "f": "Guerra", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"}, {"n": "Pomba", "f": "Mensagem", "img": "https://images.unsplash.com/photo-1501901664534-534a42840673?w=400"}, {"n": "Gato", "f": "Pragas", "img": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400"}]
    },
    "7. Descobrimentos": {
        "coord": [38.7, -9.2], "info": "Mar e Glória.",
        "ferramentas": [{"n": "Bússola", "f": "Rumo", "img": "https://images.unsplash.com/photo-1533630660533-0309e2518f83?w=400"}, {"n": "Caravela", "f": "Mar", "img": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=400"}, {"n": "Mapa", "f": "Terra", "img": "https://images.unsplash.com/photo-1521295121783-8a321d551ad2?w=400"}, {"n": "Telescópio", "f": "Visão", "img": "https://images.unsplash.com/photo-1452723312111-3a7d0db0e024?w=400"}],
        "animais": [{"n": "Papagaio", "f": "Exótico", "img": "https://images.unsplash.com/photo-1552728089-57bdde30fc3a?w=400"}, {"n": "Macaco", "f": "Exótico", "img": "https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=400"}, {"n": "Elefante", "f": "Rei", "img": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=400"}, {"n": "Cão Navio", "f": "Sentinela", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"}]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MENU")
    modo = st.radio("MODO:", ["Explorar", "Linha do Tempo (Slider)", "⭐ Minhas Tribos"])
    if modo == "Explorar":
        item = st.selectbox("POVO:", list(db.keys()))
    elif modo == "Linha do Tempo (Slider)":
        item = st.select_slider("PASSE O TEMPO:", options=list(db.keys()))
    else:
        item = None

# --- LÓGICA ---
if modo == "⭐ Minhas Tribos":
    st.title("Minhas Tribos Favoritas")
    if not st.session_state.minhas_tribos:
        st.warning("Adiciona tribos no modo Explorar!")
    else:
        for t in st.session_state.minhas_tribos:
            st.markdown(f"<div class='info-box'>🛡️ <b>{t}</b></div>", unsafe_allow_html=True)
else:
    dados = db[item]
    st.title(item)
    if st.button(f"➕ Entrar na Tribo {item}"):
        if item not in st.session_state.minhas_tribos:
            st.session_state.minhas_tribos.append(item)
            st.rerun()

    st.markdown(f'<div class="info-box">{dados["info"]}</div>', unsafe_allow_html=True)
    m = folium.Map(location=dados["coord"], zoom_start=7, tiles="CartoDB dark_matter")
    folium.Marker(dados["coord"], icon=folium.Icon(color="red")).add_to(m)
    st_folium(m, width="100%", height=300)

    # Ferramentas
    st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
    cf = st.columns(4)
    for i, f in enumerate(dados["ferramentas"]):
        with cf[i]:
            st.markdown(f'<div class="cc-card"><img src="{f["img"]}" class="img-box"><div class="label">NOME</div><div class="value">{f["n"]}</div><div class="label">FUNÇÃO</div><div class="value">{f["f"]}</div></div>', unsafe_allow_html=True)

    # Animais
    st.markdown("<h3 class='section-title'>🪪 Cartão Animal</h3>", unsafe_allow_html=True)
    ca = st.columns(4)
    for i, a in enumerate(dados["animais"]):
        with ca[i]:
            st.markdown(f'<div class="cc-card"><img src="{a["img"]}" class="img-box"><div class="label">NOME</div><div class="value">{a["n"]}</div><div class="label">PAPEL</div><div class="value">{a["f"]}</div></div>', unsafe_allow_html=True)
