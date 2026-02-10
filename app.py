import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mundovivo: Portugal", layout="wide")

# Inicializar Favoritos
if 'minhas_tribos' not in st.session_state:
    st.session_state.minhas_tribos = []

# Estilo Mundovivo
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 10px 0; font-size: 1.2rem; }
    .cc-card { background-color: #111111; color: #ffffff; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; height: 100%; }
    .img-box { width: 100%; height: 140px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; }
    .label { color: #888; font-size: 0.6rem; text-transform: uppercase; margin-top: 5px; }
    .value { font-size: 0.85rem; font-weight: bold; color: #fff; }
    .info-box { background: #111111; padding: 20px; border-radius: 10px; border-top: 4px solid #ffffff; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COM PALAVRAS-CHAVE PARA API ---
db = {
    "1. Pré-História": {
        "coord": [38.5, -8.0], "info": "Megalitismo e Caçadores.",
        "ferramentas": [
            {"n": "Biface", "f": "Corte de carne", "kw": "stone-tool"},
            {"n": "Arco", "f": "Caça", "kw": "bow-arrow"},
            {"n": "Silex", "f": "Perfurar", "kw": "flint-stone"},
            {"n": "Vaso", "f": "Cozinha", "kw": "prehistoric-pottery"}
        ],
        "animais": [
            {"n": "Lobo", "f": "Predador", "kw": "wolf"},
            {"n": "Cervo", "f": "Alimento", "kw": "deer"},
            {"n": "Javali", "f": "Caça", "kw": "wild-boar"},
            {"n": "Boi", "f": "Força", "kw": "ox"}
        ]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros da Serra da Estrela.",
        "ferramentas": [
            {"n": "Falcata", "f": "Guerra", "kw": "ancient-sword"},
            {"n": "Escudo", "f": "Defesa", "kw": "round-shield"},
            {"n": "Lança", "f": "Ataque", "kw": "spear"},
            {"n": "Fuso", "f": "Roupas", "kw": "weaving-loom"}
        ],
        "animais": [
            {"n": "Cavalo", "f": "Montaria", "kw": "iberian-horse"},
            {"n": "Porco", "f": "Carne", "kw": "iberian-pig"},
            {"n": "Ovelha", "f": "Lã", "kw": "sheep"},
            {"n": "Mastim", "f": "Guarda", "kw": "mastiff-dog"}
        ]
    },
    "3. Conios": {
        "coord": [37.1, -8.2], "info": "Povo da Escrita do Sul.",
        "ferramentas": [
            {"n": "Estela", "f": "Escrita", "kw": "ancient-stone-inscription"},
            {"n": "Rede", "f": "Pesca", "kw": "fishing-net"},
            {"n": "Anzol", "f": "Pesca", "kw": "fish-hook"},
            {"n": "Ânfora", "f": "Azeite", "kw": "amphora"}
        ],
        "animais": [
            {"n": "Burro", "f": "Carga", "kw": "donkey"},
            {"n": "Cão Água", "f": "Pesca", "kw": "water-dog"},
            {"n": "Galinha", "f": "Ovos", "kw": "chicken"},
            {"n": "Abelha", "f": "Mel", "kw": "bee"}
        ]
    },
    "4. Romanos": {
        "coord": [38.4, -7.9], "info": "Império e Estradas.",
        "ferramentas": [
            {"n": "Gladius", "f": "Guerra", "kw": "roman-sword"},
            {"n": "Moeda", "f": "Troca", "kw": "roman-coin"},
            {"n": "Mosaico", "f": "Arte", "kw": "roman-mosaic"},
            {"n": "Groma", "f": "Medição", "kw": "ancient-engineering"}
        ],
        "animais": [
            {"n": "Boi", "f": "Arado", "kw": "oxen"},
            {"n": "Mula", "f": "Carga", "kw": "mule"},
            {"n": "Ganso", "f": "Guarda", "kw": "goose"},
            {"n": "Cavalo", "f": "Correio", "kw": "roman-cavalry"}
        ]
    },
    "5. Visigodos": {
        "coord": [38.1, -7.8], "info": "Reinos Germânicos.",
        "ferramentas": [
            {"n": "Fíbula", "f": "Adorno", "kw": "visigoth-jewelry"},
            {"n": "Espada", "f": "Guerra", "kw": "medieval-sword"},
            {"n": "Cruz", "f": "Religião", "kw": "visigoth-cross"},
            {"n": "Escudo", "f": "Defesa", "kw": "wooden-shield"}
        ],
        "animais": [
            {"n": "Falcão", "f": "Caça", "kw": "falcon"},
            {"n": "Cavalo", "f": "Montaria", "kw": "knight-horse"},
            {"n": "Cão", "f": "Caça", "kw": "hunting-dog"},
            {"n": "Cabra", "f": "Leite", "kw": "goat"}
        ]
    },
    "6. Árabes": {
        "coord": [37.2, -7.9], "info": "Al-Andalus e Ciência.",
        "ferramentas": [
            {"n": "Astrolábio", "f": "Astros", "kw": "astrolabe"},
            {"n": "Nora", "f": "Água", "kw": "water-wheel"},
            {"n": "Azulejo", "f": "Decoração", "kw": "arabic-tile"},
            {"n": "Alaúde", "f": "Música", "kw": "lute-instrument"}
        ],
        "animais": [
            {"n": "Camelo", "f": "Carga", "kw": "camel"},
            {"n": "Cavalo", "f": "Guerra", "kw": "arabian-horse"},
            {"n": "Pomba", "f": "Mensagem", "kw": "pigeon"},
            {"n": "Gato", "f": "Pragas", "kw": "cat"}
        ]
    },
    "7. Descobrimentos": {
        "coord": [38.7, -9.2], "info": "Mar e Glória Mundial.",
        "ferramentas": [
            {"n": "Bússola", "f": "Rumo", "kw": "maritime-compass"},
            {"n": "Caravela", "f": "Mar", "kw": "old-sailing-ship"},
            {"n": "Mapa", "f": "Terra", "kw": "old-map"},
            {"n": "Astrolábio", "f": "Estrelas", "kw": "navigation-tool"}
        ],
        "animais": [
            {"n": "Papagaio", "f": "Exótico", "kw": "parrot"},
            {"n": "Macaco", "f": "Exótico", "kw": "monkey"},
            {"n": "Elefante", "f": "Rei", "kw": "elephant"},
            {"n": "Cão Navio", "f": "Sentinela", "kw": "big-dog"}
        ]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MENU")
    modo = st.radio("MODO:", ["Explorar Épocas", "Linha do Tempo (Slider)", "⭐ Minhas Tribos"])
    if modo == "Explorar Épocas":
        item = st.selectbox("POVO:", list(db.keys()))
    elif modo == "Linha do Tempo (Slider)":
        item = st.select_slider("PASSE O TEMPO:", options=list(db.keys()))
    else:
        item = None

# --- LÓGICA ---
if modo == "⭐ Minhas Tribos":
    st.title("As Minhas Tribos Favoritas")
    if not st.session_state.minhas_tribos:
        st.warning("Ainda não és membro de nenhuma tribo.")
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

    # SECÇÃO FERRAMENTAS (4 COLUNAS)
    st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
    cf = st.columns(4)
    for i, f in enumerate(dados["ferramentas"]):
        with cf[i]:
            # API DINÂMICA DO UNSPLASH POR KEYWORD
            img_url = f"https://source.unsplash.com/featured/400x300?{f['kw']}"
            st.markdown(f"""<div class="cc-card">
                <img src="{img_url}" class="img-box">
                <div class="label">NOME</div><div class="value">{f['n']}</div>
                <div class="label">FUNÇÃO</div><div class="value">{f['f']}</div>
            </div>""", unsafe_allow_html=
