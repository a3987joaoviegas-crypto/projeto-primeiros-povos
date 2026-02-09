import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="História de Portugal", layout="wide")

# Inicializar favoritos de forma segura
if 'minhas_tribos' not in st.session_state:
    st.session_state.minhas_tribos = []

# Estilo Visual Mundovivo - Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 15px 0; font-size: 1.2rem; }
    .cc-card { background-color: #111111; color: #ffffff; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; height: 100%; }
    .img-box { width: 100%; height: 140px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; }
    .label { color: #666; font-size: 0.6rem; text-transform: uppercase; margin-top: 5px; }
    .value { font-size: 0.85rem; font-weight: bold; color: #fff; }
    .info-box { background: #111111; padding: 20px; border-radius: 10px; border-top: 4px solid #ffffff; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE REAL COM FUNÇÕES E 7 ÉPOCAS ---
db = {
    "1. Pré-História": {
        "coord": [38.5, -8.0], "info": "Época das pedras e caça primitiva.",
        "ferramentas": [
            {"n": "Biface", "f": "Corte de carne", "img": "https://loremflickr.com/400/300/stone,axe/all"},
            {"n": "Arco", "f": "Caça à distância", "img": "https://loremflickr.com/400/300/bow,hunting/all"},
            {"n": "Ponta Silex", "f": "Perfurar peles", "img": "https://loremflickr.com/400/300/arrowhead/all"},
            {"n": "Raspador", "f": "Limpar peles", "img": "https://loremflickr.com/400/300/scraper,tool/all"}
        ],
        "animais": [
            {"n": "Lobo", "f": "Predador topo", "img": "https://loremflickr.com/400/300/wolf/all"},
            {"n": "Cervo", "f": "Fonte de carne", "img": "https://loremflickr.com/400/300/deer/all"},
            {"n": "Javali", "f": "Caça perigosa", "img": "https://loremflickr.com/400/300/wildboar/all"},
            {"n": "Auroque", "f": "Touro selvagem", "img": "https://loremflickr.com/400/300/bull/all"}
        ]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros montanheses liderados por Viriato.",
        "ferramentas": [
            {"n": "Falcata", "f": "Combate corpo a corpo", "img": "https://loremflickr.com/400/300/sword/all"},
            {"n": "Caetra", "f": "Defesa ágil", "img": "https://loremflickr.com/400/300/shield/all"},
            {"n": "Lança", "f": "Ataque médio alcance", "img": "https://loremflickr.com/400/300/spear/all"},
            {"n": "Fuso", "f": "Fiar lã de ovelha", "img": "https://loremflickr.com/400/300/spinning,tool/all"}
        ],
        "animais": [
            {"n": "Cavalo", "f": "Montaria de guerra", "img": "https://loremflickr.com/400/300/horse/all"},
            {"n": "Porco", "f": "Sustento base", "img": "https://loremflickr.com/400/300/pig/all"},
            {"n": "Ovelha", "f": "Produção de lã", "img": "https://loremflickr.com/400/300/sheep/all"},
            {"n": "Cão Fila", "f": "Guarda de gado", "img": "https://loremflickr.com/400/300/mastiff/all"}
        ]
    },
    "3. Conios": {
        "coord": [37.1, -8.2], "info": "Primeira escrita da Península no Sul.",
        "ferramentas": [
            {"n": "Estela", "f": "Gravar leis/nomes", "img": "https://loremflickr.com/400/300/stone,writing/all"},
            {"n": "Anzol", "f": "Pesca costeira", "img": "https://loremflickr.com/400/300/fishhook/all"},
            {"n": "Rede", "f": "Pesca em massa", "img": "https://loremflickr.com/400/300/fishingnet/all"},
            {"n": "Ânfora", "f": "Guardar azeite", "img": "https://loremflickr.com/400/300/clay,pot/all"}
        ],
        "animais": [
            {"n": "Burro", "f": "Transporte de carga", "img": "https://loremflickr.com/400/300/donkey/all"},
            {"n": "Cão Água", "f": "Ajuda aos pescadores", "img": "https://loremflickr.com/400/300/waterdog/all"},
            {"n": "Galinha", "f": "Ovos e carne", "img": "https://loremflickr.com/400/300/chicken/all"},
            {"n": "Abelha", "f": "Mel e cera", "img": "https://loremflickr.com/400/300/bee/all"}
        ]
    },
    "4. Romanos": {
        "coord": [38.4, -7.9], "info": "Império, Estradas e Direito.",
        "ferramentas": [
            {"n": "Gladius", "f": "Espada legada", "img": "https://loremflickr.com/400/300/gladius/all"},
            {"n": "Groma", "f": "Medir estradas", "img": "https://loremflickr.com/400/300/surveying/all"},
            {"n": "Mosaico", "f": "Decoração de vilas", "img": "https://loremflickr.com/400/300/mosaic/all"},
            {"n": "Moeda", "f": "Comércio imperial", "img": "https://loremflickr.com/400/300/coin/all"}
        ],
        "animais": [
            {"n": "Boi", "f": "Puxar o arado", "img": "https://loremflickr.com/400/300/oxen/all"},
            {"n": "Mula", "f": "Carga pesada", "img": "https://loremflickr.com/400/300/mule/all"},
            {"n": "Ganso", "f": "Vigilância", "img": "https://loremflickr.com/400/300/goose/all"},
            {"n": "Cavalo", "f": "Correio rápido", "img": "https://loremflickr.com/400/300/riding,horse/all"}
        ]
    },
    "5. Visigodos": {
        "coord": [38.1, -7.8], "info": "Sucessores germânicos dos Romanos.",
        "ferramentas": [{"n": "Fíbula", "f": "Prender mantos", "img": "https://loremflickr.com/400/300/brooch/all"}, {"n": "Espada", "f": "Combate", "img": "https://loremflickr.com/400/300/medieval,sword/all"}, {"n": "Cruz", "f": "Símbolo religioso", "img": "https://loremflickr.com/400/300/cross/all"}, {"n": "Escudo", "f": "Defesa", "img": "https://loremflickr.com/400/300/shield,wood/all"}],
        "animais": [{"n": "Falcão", "f": "Caça desportiva", "img": "https://loremflickr.com/400/300/falcon/all"}, {"n": "Cavalo", "f": "Montaria nobre", "img": "https://loremflickr.com/400/300/horse/all"}, {"n": "Cão", "f": "Caça em matilha", "img": "https://loremflickr.com/400/300/hound/all"}, {"n": "Cabra", "f": "Leite e queijo", "img": "https://loremflickr.com/400/300/goat/all"}]
    },
    "6. Árabes": {
        "coord": [37.2, -7.9], "info": "Mestres da agricultura e ciência.",
        "ferramentas": [{"n": "Astrolábio", "f": "Navegação", "img": "https://loremflickr.com/400/300/astrolabe/all"}, {"n": "Nora", "f": "Elevação de água", "img": "https://loremflickr.com/400/300/waterwheel/all"}, {"n": "Enxada", "f": "Cuidar da horta", "img": "https://loremflickr.com/400/300/hoe/all"}, {"n": "Azulejo", "f": "Revestimento", "img": "https://loremflickr.com/400/300/tile/all"}],
        "animais": [{"n": "Camelo", "f": "Carga no deserto", "img": "https://loremflickr.com/400/300/camel/all"}, {"n": "Gineto", "f": "Guerra rápida", "img": "https://loremflickr.com/400/300/arabian,horse/all"}, {"n": "Pomba", "f": "Mensagens", "img": "https://loremflickr.com/400/300/pigeon/all"}, {"n": "Gato", "f": "Controlo de pragas", "img": "https://loremflickr.com/400/300/cat/all"}]
    },
    "7. Descobrimentos": {
        "coord": [38.7, -9.2], "info": "A era dos oceanos e caravelas.",
        "ferramentas": [{"n": "Bússola", "f": "Orientação", "img": "https://loremflickr.com/400/300/compass/all"}, {"n": "Caravela", "f": "Navio de exploração", "img": "https://loremflickr.com/400/300/ship/all"}, {"n": "Astrolábio", "f": "Latitude", "img": "https://loremflickr.com/400/300/navigation/all"}, {"n": "Mapa", "f": "Cartografia", "img": "https://loremflickr.com/400/300/map/all"}],
        "animais": [{"n": "Papagaio", "f": "Mascote exótica", "img": "https://loremflickr.com/400/300/parrot/all"}, {"n": "Macaco", "f": "Curiosidade", "img": "https://loremflickr.com/400/300/monkey/all"}, {"n": "Elefante", "f": "Presente real", "img": "https://loremflickr.com/400/300/elephant/all"}, {"n": "Cão Navio", "f": "Sentinela bordo", "img": "https://loremflickr.com/400/300/dog/all"}]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MENU")
    modo = st.radio("SELECIONAR MODO:", ["Explorar", "Linha do Tempo", "⭐ Minhas Tribos"])
    if modo == "Explorar":
        item = st.selectbox("POVO:", list(db.keys()))
    elif modo == "Linha do Tempo":
        item = st.select_slider("TEMPO:", options=list(db.keys()))
    else:
        item = None

# --- CONTEÚDO ---
if modo == "⭐ Minhas Tribos":
    st.title("As Minhas Tribos Favoritas")
    if not st.session_state.minhas_tribos:
        st.warning("Não tens tribos favoritas! Vai a 'Explorar' e clica em 'Entrar na Tribo'.")
    else:
        for t in st.session_state.minhas_tribos:
            st.markdown(f"<div class='info-box'>🛡️ És membro da tribo: <b>{t}</b></div>", unsafe_allow_html=True)
else:
    dados = db[item]
    st.title(item)
    if st.button(f"➕ Entrar na Tribo {item}"):
        if item not in st.session_state.minhas_tribos:
            st.session_state.minhas_tribos.append(item)
            st.success(f"Entraste na tribo {item}!")

    st.markdown(f'<div class="info-box">{dados["info"]}</div>', unsafe_allow_html=True)
    m = folium.Map(location=dados["coord"], zoom_start=7, tiles="CartoDB dark_matter")
    folium.Marker(dados["coord"], icon=folium.Icon(color="red")).add_to(m)
    st_folium(m, width="100%", height=300)

    # SECÇÕES COM 4 COLUNAS E FUNÇÕES
    st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
    cf = st.columns(4)
    for i, f in enumerate(dados["ferramentas"]):
        with cf[i]:
            st.markdown(f"""<div class="cc-card">
                <img src="{f['img']}" class="img-box">
                <div class="label">NOME</div><div class="value">{f['n']}</div>
                <div class="label">FUNÇÃO</div><div class="value">{f['f']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<h3 class='section-title'>🪪 Cartão Animal</h3>", unsafe_allow_html=True)
    ca = st.columns(4)
    for i, a in enumerate(dados["animais"]):
        with ca[i]:
            st.markdown(f"""<div class="cc-card">
                <img src="{a['img']}" class="img-box">
                <div class="label">NOME</div><div class="value">{a['n']}</div>
                <div class="label">PAPEL</div><div class="value">{a['f']}</div>
            </div>""", unsafe_allow_html=True)
