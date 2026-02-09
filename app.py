import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mundovivo: História de Portugal", layout="wide")

# Inicialização segura do estado
if 'minhas_tribos' not in st.session_state:
    st.session_state.minhas_tribos = []

# CSS Estilo Mundovivo - Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 15px 0; font-size: 1.2rem; }
    .cc-card { background-color: #111111; color: #ffffff; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; height: 100%; transition: 0.3s; }
    .cc-card:hover { border-color: #fff; }
    .img-box { width: 100%; height: 140px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; background-color: #222; }
    .label { color: #888; font-size: 0.6rem; text-transform: uppercase; margin-top: 5px; }
    .value { font-size: 0.85rem; font-weight: bold; color: #fff; line-height: 1.2; }
    .info-box { background: #111111; padding: 20px; border-radius: 10px; border-top: 4px solid #ffffff; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COMPLETA COM 7 ÉPOCAS E FUNÇÕES ---
db = {
    "1. Pré-História": {
        "coord": [38.5, -8.0], "info": "Megalitismo e Caçadores-recoletores.",
        "ferramentas": [
            {"n": "Biface", "f": "Corte e raspagem", "q": "paleolithic,tool"},
            {"n": "Arco", "f": "Caça à distância", "q": "primitive,bow"},
            {"n": "Ponta Silex", "f": "Perfurar peles", "q": "arrowhead"},
            {"n": "Vaso Barro", "f": "Armazenar grãos", "q": "ancient,pottery"}
        ],
        "animais": [
            {"n": "Lobo Ibérico", "f": "Competidor de caça", "q": "wolf"},
            {"n": "Cervo", "f": "Fonte de alimento", "q": "deer"},
            {"n": "Javali", "f": "Caça e rituais", "q": "wild,boar"},
            {"n": "Auroque", "f": "Touro ancestral", "q": "bull"}
        ]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros da Serra da Estrela.",
        "ferramentas": [
            {"n": "Falcata", "f": "Espada de combate", "q": "ancient,sword"},
            {"n": "Caetra", "f": "Escudo de defesa", "q": "round,shield"},
            {"n": "Lança", "f": "Ataque de médio alcance", "q": "spear"},
            {"n": "Fuso", "f": "Fiação de lã", "q": "spinning,tool"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "f": "Montaria de guerra", "q": "horse"},
            {"n": "Porco Alentejano", "f": "Sustento básico", "q": "pig"},
            {"n": "Ovelha", "f": "Produção de lã", "q": "sheep"},
            {"n": "Cão de Fila", "f": "Guarda de castros", "q": "mastiff"}
        ]
    },
    "3. Conios": {
        "coord": [37.1, -8.2], "info": "A enigmática escrita do Sul.",
        "ferramentas": [
            {"n": "Estela", "f": "Inscrição funerária", "q": "monolith"},
            {"n": "Anzol de Bronze", "f": "Pesca costeira", "q": "fish,hook"},
            {"n": "Rede", "f": "Pesca artesanal", "q": "fishing,net"},
            {"n": "Ânfora", "f": "Transporte de vinho", "q": "amphora"}
        ],
        "animais": [
            {"n": "Burro", "f": "Carga e transporte", "q": "donkey"},
            {"n": "Cão de Água", "f": "Auxílio na pesca", "q": "water,dog"},
            {"n": "Galinha", "f": "Alimento doméstico", "q": "chicken"},
            {"n": "Abelha", "f": "Produção de mel", "q": "bee"}
        ]
    },
    "4. Romanos": {
        "coord": [38.4, -7.9], "info": "A civilização das estradas e pontes.",
        "ferramentas": [{"n": "Gladius", "f": "Combate legada", "q": "gladius"}, {"n": "Groma", "f": "Alineação de vias", "q": "surveying"}, {"n": "Mosaico", "f": "Pavimento artístico", "q": "mosaic"}, {"n": "Moeda", "f": "Moeda de troca", "q": "roman,coin"}],
        "animais": [{"n": "Boi", "f": "Arar os campos", "q": "ox"}, {"n": "Mula", "f": "Transporte imperial", "q": "mule"}, {"n": "Ganso", "u": "Sentinela", "q": "goose"}, {"n": "Cavalo", "f": "Cavalaria romana", "q": "roman,horse"}]
    },
    "5. Visigodos": {
        "coord": [38.1, -7.8], "info": "Reinos Bárbaros e Cristandade.",
        "ferramentas": [{"n": "Fíbula", "f": "Adorno e fecho", "q": "brooch"}, {"n": "Espada Longa", "f": "Duelo germânico", "q": "medieval,sword"}, {"n": "Cruz", "f": "Símbolo de fé", "q": "cross"}, {"n": "Escudo", "f": "Proteção em muro", "q": "wood,shield"}],
        "animais": [{"n": "Falcão", "f": "Falcoaria nobre", "q": "falcon"}, {"n": "Cavalo", "f": "Montaria de elite", "q": "stallion"}, {"n": "Ovelha", "f": "Vestuário de pele", "q": "sheep"}, {"n": "Cão", "f": "Caça maior", "q": "hound"}]
    },
    "6. Árabes": {
        "coord": [37.2, -7.9], "info": "Ciência e irrigação no Al-Andalus.",
        "ferramentas": [{"n": "Astrolábio", "f": "Orientação astral", "q": "astrolabe"}, {"n": "Nora", "f": "Regadio agrícola", "q": "waterwheel"}, {"n": "Azulejo", "f": "Decoração geométrica", "q": "arabic,tile"}, {"n": "Alaúde", "f": "Poesia e música", "q": "lute"}],
        "animais": [{"n": "Camelo", "f": "Carga de longa distância", "q": "camel"}, {"n": "Pomba", "f": "Correio aéreo", "q": "pigeon"}, {"n": "Gineto", "f": "Montaria ágil", "q": "horse,arab"}, {"n": "Cabra", "f": "Subsistência", "q": "goat"}]
    },
    "7. Descobrimentos": {
        "coord": [38.7, -9.2], "info": "Navegação e Expansão Mundial.",
        "ferramentas": [{"n": "Bússola", "f": "Rumo no mar", "q": "compass"}, {"n": "Caravela", "f": "Navio de exploração", "q": "caravel"}, {"n": "Quadrante", "f": "Medição de altura", "q": "quadrant"}, {"n": "Mapa", "f": "Traçado do mundo", "q": "old,map"}],
        "animais": [{"n": "Papagaio", "f": "Exótico", "q": "parrot"}, {"n": "Macaco", "f": "Curiosidade", "q": "monkey"}, {"n": "Elefante", "f": "Poder real", "q": "elephant"}, {"n": "Cão Fila", "f": "Proteção de carga", "q": "dog"}]
    }
}

# --- SIDEBAR COM 5 APIS / MOTORES ---
with st.sidebar:
    st.title("🏛️ CONTROLO")
    modo = st.radio("SELECIONAR MODO:", ["Explorar", "Linha do Tempo", "⭐ Minhas Tribos"])
    
    st.markdown("---")
    st.subheader("⚙️ Motores de Imagem (APIs)")
    api_source = st.selectbox("FONTE DE PESQUISA:", ["Unsplash API", "LoremFlickr API", "Picsum API", "Wikimedia Search", "PlaceImg API"])
    
    if modo != "⭐ Minhas Tribos":
        item = st.selectbox("POVO:", list(db.keys())) if modo == "Explorar" else st.select_slider("TEMPO:", options=list(db.keys()))
    else:
        item = None

# --- LÓGICA DE IMAGEM (RODÍZIO DE APIs) ---
def get_img(query, source):
    if source == "Unsplash API": return f"https://source.unsplash.com/featured/400x300?{query}"
    if source == "LoremFlickr API": return f"https://loremflickr.com/400/300/{query}/all"
    if source == "Picsum API": return f"https://picsum.photos/400/300?random={query}"
    if source == "Wikimedia Search": return f"https://commons.wikimedia.org/w/index.php?search={query}&title=Special:Search"
    return f"https://placeimg.com/400/300/{query}"

# --- CONTEÚDO PRINCIPAL ---
if modo == "⭐ Minhas Tribos":
    st.title("As Minhas Tribos Favoritas")
    if not st.session_state.minhas_tribos:
        st.warning("Lista vazia. Entra numa tribo no modo Explorar!")
    else:
        for t in st.session_state.minhas_tribos:
            st.markdown(f"<div class='info-box'>🛡️ Tribo Guardada: <b>{t}</b></div>", unsafe_allow_html=True)
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

    # SECÇÕES COM 4 COLUNAS
    st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
    cf = st.columns(4)
    for i, f in enumerate(dados["ferramentas"]):
        with cf[i]:
            img = get_img(f['q'], api_source)
            st.markdown(f"""<div class="cc-card">
                <img src="{img}" class="img-box">
                <div class="label">NOME</div><div class="value">{f['n']}</div>
                <div class="label">FUNÇÃO</div><div class="value">{f['f']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<h3 class='section-title'>🪪 Cartão Animal</h3>", unsafe_allow_html=True)
    ca = st.columns(4)
    for i, a in enumerate(dados["animais"]):
        with ca[i]:
            img_a = get_img(a['q'], api_source)
            st.markdown(f"""<div class="cc-card">
                <img src="{img_a}" class="img-box">
                <div class="label">NOME</div><div class="value">{a['n']}</div>
                <div class="label">PAPEL</div><div class="value">{a['f']}</div>
            </div>""", unsafe_allow_html=True)
