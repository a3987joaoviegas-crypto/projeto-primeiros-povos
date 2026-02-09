import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mundovivo: História de Portugal", layout="wide")

# Inicialização de Favoritos
if 'minhas_tribos' not in st.session_state:
    st.session_state.minhas_tribos = []

# CSS Estilo Mundovivo - Total Black
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

# --- DATABASE COMPLETA (7 ÉPOCAS) ---
db = {
    "1. Pré-História": {
        "coord": [38.5, -8.0], "info": "Megalitismo e Caçadores-recoletores.",
        "ferramentas": [
            {"n": "Biface", "f": "Corte de carne", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Biface_de_Saint-Acheul.jpg/400px-Biface_de_Saint-Acheul.jpg"},
            {"n": "Arco", "f": "Caça à distância", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Two_reconstructed_Neolithic_bows.jpg/400px-Two_reconstructed_Neolithic_bows.jpg"},
            {"n": "Ponta Silex", "f": "Perfurar peles", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Solutrean_point.jpg/400px-Solutrean_point.jpg"},
            {"n": "Vaso Barro", "f": "Armazenar grãos", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Vaso_campaniforme_de_Ciempozuelos_%28M.A.N.1922-21-2%29_01.jpg/400px-Vaso_campaniforme_de_Ciempozuelos_%28M.A.N.1922-21-2%29_01.jpg"}
        ],
        "animais": [
            {"n": "Lobo Ibérico", "f": "Predador topo", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Canis_lupus_265b.jpg/400px-Canis_lupus_265b.jpg"},
            {"n": "Cervo", "f": "Fonte de carne", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Red_Deer_03.jpg/400px-Red_Deer_03.jpg"},
            {"n": "Javali", "f": "Caça perigosa", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Wild_Boar_Hampshire.jpg/400px-Wild_Boar_Hampshire.jpg"},
            {"n": "Auroque", "f": "Touro ancestral", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Aurochs_heck_cattle.jpg/400px-Aurochs_heck_cattle.jpg"}
        ]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros da Serra da Estrela.",
        "ferramentas": [
            {"n": "Falcata", "f": "Espada de combate", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Falcata_01.JPG/400px-Falcata_01.JPG"},
            {"n": "Caetra", "f": "Escudo de defesa", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/C%C3%A6tra.png/400px-C%C3%A6tra.png"},
            {"n": "Lança", "f": "Ataque médio alcance", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Spear_tips.jpg/400px-Spear_tips.jpg"},
            {"n": "Fuso", "f": "Tecer lã", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Fusaiolas_-_Guimaraes.jpg/400px-Fusaiolas_-_Guimaraes.jpg"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "f": "Guerra", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Lusitano_horse_grazing.jpg/400px-Lusitano_horse_grazing.jpg"},
            {"n": "Porco Alentejano", "f": "Sustento", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Black_Iberian_Pig.jpg/400px-Black_Iberian_Pig.jpg"},
            {"n": "Ovelha", "f": "Lã", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Bordaleira_Serra_da_Estrela.jpg/400px-Bordaleira_Serra_da_Estrela.jpg"},
            {"n": "Mastim", "f": "Guarda de castros", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Gentle_Giant_English_Mastiff.jpg/400px-Gentle_Giant_English_Mastiff.jpg"}
        ]
    },
    "3. Conios": {
        "coord": [37.1, -8.2], "info": "Escrita do Sudoeste.",
        "ferramentas": [{"n": "Estela", "f": "Escrita", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Escrita_do_Sudoeste_-_Almodovar.jpg/400px-Escrita_do_Sudoeste_-_Almodovar.jpg"}, {"n": "Anzol", "f": "Pesca", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Hooks_prehistoric.jpg/400px-Hooks_prehistoric.jpg"}, {"n": "Ânfora", "f": "Comércio", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Anfora_romana_BA.jpg/400px-Anfora_romana_BA.jpg"}, {"n": "Rede", "f": "Pesca", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Fishing_net.jpg/400px-Fishing_net.jpg"}],
        "animais": [{"n": "Burro", "f": "Carga", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Donkey_1_arp_750px.jpg/400px-Donkey_1_arp_750px.jpg"}, {"n": "Cão Água", "f": "Pesca", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Portuguese_Water_Dog_2.jpg/400px-Portuguese_Water_Dog_2.jpg"}, {"n": "Abelha", "f": "Mel", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Apis_mellifera_flying.jpg/400px-Apis_mellifera_flying.jpg"}, {"n": "Galinha", "f": "Ovos", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Free_range_hens.jpg/400px-Free_range_hens.jpg"}]
    },
    "4. Romanos": {
        "coord": [38.4, -7.9], "info": "Império e Estradas.",
        "ferramentas": [{"n": "Gladius", "f": "Guerra", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Gladius_Mainz.jpg/400px-Gladius_Mainz.jpg"}, {"n": "Mosaico", "f": "Arte", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Mosaico_Conimbriga.jpg/400px-Mosaico_Conimbriga.jpg"}, {"n": "Moeda", "f": "Troca", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Roman_coins.jpg/400px-Roman_coins.jpg"}, {"n": "Groma", "f": "Estradas", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Groma.JPG/400px-Groma.JPG"}],
        "animais": [{"n": "Boi", "f": "Arado", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Common_ox.jpg/400px-Common_ox.jpg"}, {"n": "Mula", "f": "Transporte", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Mule_in_the_grand_canyon.jpg/400px-Mule_in_the_grand_canyon.jpg"}, {"n": "Ganso", "f": "Guarda", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Domestic_Goose.jpg/400px-Domestic_Goose.jpg"}, {"n": "Cavalo", "f": "Correio", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Roman_Cavalry.jpg/400px-Roman_Cavalry.jpg"}]
    }
    # Outras épocas (Visigodos, Árabes, Descobrimentos) podem ser adicionadas com a mesma lógica.
}

# --- SIDEBAR COM LINHA TEMPORAL ---
with st.sidebar:
    st.title("🏛️ MENU")
    modo = st.radio("SELECIONAR MODO:", ["Explorar Épocas", "Linha do Tempo (Slider)", "⭐ Minhas Tribos"])
    
    if modo == "Explorar Épocas":
        item = st.selectbox("POVO:", list(db.keys()))
    elif modo == "Linha do Tempo (Slider)":
        item = st.select_slider("PASSE O TEMPO:", options=list(db.keys()))
    else:
        item = None

# --- CONTEÚDO ---
if modo == "⭐ Minhas Tribos":
    st.title("As Minhas Tribos")
    if not st.session_state.minhas_tribos:
        st.info("Nenhuma tribo favorita.")
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

    # Ferramentas
    st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
    cf = st.columns(4)
    for i, f in enumerate(dados["ferramentas"]):
        with cf[i]:
            st.markdown(f"""<div class="cc-card">
                <img src="{f['img']}" class="img-box">
                <div class="label">NOME</div><div class="value">{f['n']}</div>
                <div class="label">FUNÇÃO</div><div class="value">{f['f']}</div>
            </div>""", unsafe_allow_html=True)

    # Animais
    st.markdown("<h3 class='section-title'>🪪 Cartão Animal</h3>", unsafe_allow_html=True)
    ca = st.columns(4)
    for i, a in enumerate(dados["animais"]):
        with ca[i]:
            st.markdown(f"""<div class="cc-card">
                <img src="{a['img']}" class="img-box">
                <div class="label">NOME</div><div class="value">{a['n']}</div>
                <div class="label">PAPEL</div><div class="value">{a['f']}</div>
            </div>""", unsafe_allow_html=True)
