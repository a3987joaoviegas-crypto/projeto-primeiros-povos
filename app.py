import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Primeiros Povos de Portugal", layout="wide")

# Inicializar favoritos no estado da sessão
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []

# Estilo Visual Mundovivo - Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 10px 0; font-size: 1.2rem; }
    .cc-card { background-color: #111111; color: #ffffff; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; height: 100%; }
    .img-box { width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; }
    .label { color: #666; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.85rem; font-weight: bold; color: #fff; }
    .info-box { background: #111111; padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; border-top: 4px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COMPLETA (4 ITENS POR CATEGORIA) ---
db = {
    "1. Pré-História": {
        "coord": [38.5, -8.0], "info": "Megalitismo e Caçadores-recoletores.",
        "ferramentas": [
            {"n": "Biface", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Biface_de_Saint-Acheul.jpg/400px-Biface_de_Saint-Acheul.jpg"},
            {"n": "Arco", "img": "https://images.unsplash.com/photo-1511406361295-0a5ff814c0ad?w=400"},
            {"n": "Ponta Silex", "img": "https://images.unsplash.com/photo-1619678595438-66037d4560e2?w=400"},
            {"n": "Vaso Barro", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?w=400"}
        ],
        "animais": [
            {"n": "Lobo", "u": "Selvagem", "img": "https://images.unsplash.com/photo-1590424753042-32244f05563c?w=400"},
            {"n": "Cervo", "u": "Alimento", "img": "https://images.unsplash.com/photo-1549194380-f3c6c795af0e?w=400"},
            {"n": "Javali", "u": "Caça", "img": "https://images.unsplash.com/photo-1516248967355-90033c94d13c?w=400"},
            {"n": "Auroque", "u": "Mítico", "img": "https://images.unsplash.com/photo-1551029506-0807df4e2031?w=400"}
        ]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros da Serra da Estrela (Idade do Ferro).",
        "ferramentas": [
            {"n": "Falcata", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Falcata_01.JPG/400px-Falcata_01.JPG"},
            {"n": "Caetra", "img": "https://images.unsplash.com/photo-1615678815958-5d413b70b653?w=400"},
            {"n": "Lança", "img": "https://images.unsplash.com/photo-1558285511-966956795f55?w=400"},
            {"n": "Fuso", "img": "https://images.unsplash.com/photo-1615560113840-06900693f185?w=400"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "u": "Guerra", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"},
            {"n": "Porco", "u": "Alimento", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?w=400"},
            {"n": "Ovelha", "u": "Lã", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=400"},
            {"n": "Cão Fila", "u": "Guarda", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"}
        ]
    },
    "3. Conios": {
        "coord": [37.1, -8.2], "info": "Povo misterioso do Sul com escrita própria.",
        "ferramentas": [
            {"n": "Estela", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Escrita_do_Sudoeste_-_Almodovar.jpg/400px-Escrita_do_Sudoeste_-_Almodovar.jpg"},
            {"n": "Rede Pesca", "img": "https://images.unsplash.com/photo-1501703979959-79396f212591?w=400"},
            {"n": "Anzol", "img": "https://images.unsplash.com/photo-1516937941344-00b4e0337589?w=400"},
            {"n": "Ânfora", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?w=400"}
        ],
        "animais": [
            {"n": "Burro", "u": "Carga", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?w=400"},
            {"n": "Cão d'Água", "u": "Pesca", "img": "https://images.unsplash.com/photo-1598133894008-61f7fdb8cc3a?w=400"},
            {"n": "Galinha", "u": "Ovos", "img": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400"},
            {"n": "Abelha", "u": "Mel", "img": "https://images.unsplash.com/photo-1581404476143-fb31d742929f?w=400"}
        ]
    }
    # Adicionar Romanos, Visigodos, Árabes e Descobrimentos seguindo o mesmo padrão...
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🇵🇹 HISTÓRIA")
    
    st.markdown("### ⭐ Minhas Tribos")
    if not st.session_state.favoritos:
        st.info("Lista vazia.")
    else:
        for fav in st.session_state.favoritos:
            st.write(f"🛡️ {fav}")
    
    st.markdown("---")
    modo = st.radio("MODO:", ["Seleção Direta", "Evolução (Slider)"])
    item = st.selectbox("ESCOLHA:", list(db.keys())) if modo == "Seleção Direta" else st.select_slider("VIAGEM NO TEMPO:", options=list(db.keys()))

dados = db[item]

# --- CONTEÚDO ---
st.title(f"{item}")

if st.button(f"➕ Entrar na Tribo {item}"):
    if item not in st.session_state.favoritos:
        st.session_state.favoritos.append(item)
        st.rerun()

st.markdown(f'<div class="info-box"><b>Resumo:</b> {dados["info"]}</div>', unsafe_allow_html=True)

# Mapa
m = folium.Map(location=dados["coord"], zoom_start=7, tiles="CartoDB dark_matter")
folium.Marker(dados["coord"], icon=folium.Icon(color="red")).add_to(m)
st_folium(m, width="100%", height=300)

# Listas Horizontais (Tudo em 4 colunas)
st.markdown("<h3 class='section-title'>⚒️ Ferramentas</h3>", unsafe_allow_html=True)
cols_f = st.columns(4)
for i, f in enumerate(dados["ferramentas"]):
    with cols_f[i]:
        st.markdown(f'<div class="cc-card"><img src="{f["img"]}" class="img-box"><div class="label">ARTEFACTO</div><div class="value">{f["n"]}</div></div>', unsafe_allow_html=True)

st.markdown("<h3 class='section-title'>🪪 Cartão Animal</h3>", unsafe_allow_html=True)
cols_a = st.columns(4)
for i, a in enumerate(dados["animais"]):
    with cols_a[i]:
        st.markdown(f'<div class="cc-card"><img src="{a["img"]}" class="img-box"><div class="label">NOME</div><div class="value">{a["n"]}</div><div class="label">USO</div><div class="value">{a["u"]}</div></div>', unsafe_allow_html=True)
