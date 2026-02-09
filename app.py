import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mundovivo: História de Portugal", layout="wide")

if 'minhas_tribos' not in st.session_state:
    st.session_state.minhas_tribos = []

# Estilo Mundovivo
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

# --- DATABASE COM IMAGENS REAIS (WIKIMEDIA) ---
db = {
    "1. Pré-História": {
        "coord": [38.5, -8.0], "info": "Megalitismo e Caçadores.",
        "ferramentas": [
            {"n": "Biface", "f": "Corte de carne", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Biface_de_Saint-Acheul.jpg/400px-Biface_de_Saint-Acheul.jpg"},
            {"n": "Arco", "f": "Caça à distância", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Two_reconstructed_Neolithic_bows.jpg/400px-Two_reconstructed_Neolithic_bows.jpg"},
            {"n": "Ponta Silex", "f": "Perfurar peles", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Solutrean_point.jpg/400px-Solutrean_point.jpg"},
            {"n": "Vaso Barro", "f": "Armazenar", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Vaso_campaniforme_de_Ciempozuelos_%28M.A.N.1922-21-2%29_01.jpg/400px-Vaso_campaniforme_de_Ciempozuelos.jpg"}
        ],
        "animais": [
            {"n": "Lobo", "f": "Predador", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Canis_lupus_265b.jpg/400px-Canis_lupus_265b.jpg"},
            {"n": "Cervo", "f": "Alimento", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Red_Deer_03.jpg/400px-Red_Deer_03.jpg"},
            {"n": "Javali", "f": "Caça", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Wild_Boar_Hampshire.jpg/400px-Wild_Boar_Hampshire.jpg"},
            {"n": "Auroque", "f": "Touro Ancestral", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Aurochs_heck_cattle.jpg/400px-Aurochs_heck_cattle.jpg"}
        ]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros da Serra da Estrela.",
        "ferramentas": [
            {"n": "Falcata", "f": "Combate", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Falcata_01.JPG/400px-Falcata_01.JPG"},
            {"n": "Caetra", "f": "Defesa", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/C%C3%A6tra.png/400px-C%C3%A6tra.png"},
            {"n": "Lança", "f": "Ataque", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Spear_tips.jpg/400px-Spear_tips.jpg"},
            {"n": "Fuso", "f": "Tecer lã", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Fusaiolas_-_Guimaraes.jpg/400px-Fusaiolas.jpg"}
        ],
        "animais": [
            {"n": "Cavalo", "f": "Guerra", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Lusitano_horse_grazing.jpg/400px-Lusitano_horse_grazing.jpg"},
            {"n": "Porco", "f": "Sustento", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Black_Iberian_Pig.jpg/400px-Black_Iberian_Pig.jpg"},
            {"n": "Ovelha", "f": "Lã", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Bordaleira_Serra_da_Estrela.jpg/400px-Bordaleira.jpg"},
            {"n": "Mastim", "f": "Guarda", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Portuguese_Sheepdog.jpg/400px-Portuguese_Sheepdog.jpg"}
        ]
    }
    # Outras épocas seguem o mesmo padrão com links reais...
}

with st.sidebar:
    st.title("🏛️ MENU")
    modo = st.radio("MODO:", ["Explorar", "⭐ Minhas Tribos"])
    if modo == "Explorar":
        item = st.selectbox("POVO:", list(db.keys()))
    else:
        item = None

if modo == "⭐ Minhas Tribos":
    st.title("Favoritos")
    for t in st.session_state.minhas_tribos:
        st.write(f"🛡️ {t}")
else:
    dados = db[item]
    st.title(item)
    if st.button(f"➕ Entrar na Tribo {item}"):
        if item not in st.session_state.minhas_tribos:
            st.session_state.minhas_tribos.append(item)

    st.markdown(f'<div class="info-box">{dados["info"]}</div>', unsafe_allow_html=True)
    m = folium.Map(location=dados["coord"], zoom_start=7, tiles="CartoDB dark_matter")
    st_folium(m, width="100%", height=300)

    st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
    cf = st.columns(4)
    for i, f in enumerate(dados["ferramentas"]):
        with cf[i]:
            st.markdown(f'<div class="cc-card"><img src="{f["img"]}" class="img-box"><div class="label">NOME</div><div class="value">{f["n"]}</div><div class="label">FUNÇÃO</div><div class="value">{f["f"]}</div></div>', unsafe_allow_html=True)

    st.markdown("<h3 class='section-title'>🪪 Cartão Animal</h3>", unsafe_allow_html=True)
    ca = st.columns(4)
    for i, a in enumerate(dados["animais"]):
        with ca[i]:
            st.markdown(f'<div class="cc-card"><img src="{a["img"]}" class="img-box"><div class="label">NOME</div><div class="value">{a["n"]}</div><div class="label">USO</div><div class="value">{a["f"]}</div></div>', unsafe_allow_html=True)
