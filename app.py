import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Primeiros Povos de Portugal", layout="wide")

# Inicializar favoritos
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = {}

# Estilo Visual Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 10px 0; font-size: 1.2rem; }
    .cc-card { background-color: #111111; color: #ffffff; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; height: 100%; }
    .img-box { width: 100%; height: 140px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; background-color: #222; }
    .label { color: #888; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.85rem; font-weight: bold; color: #fff; }
    .info-box { background: #111111; padding: 20px; border-radius: 10px; border-top: 4px solid #ffffff; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE GIGANTE ---
db = {
    "1. Pré-História": {
        "coord": [38.5, -8.0], "info": "Megalitismo e Caçadores.",
        "ferramentas": [
            {"n": "Biface", "img": "https://images.unsplash.com/photo-1619678595438-66037d4560e2?w=400"},
            {"n": "Arco de Madeira", "img": "https://images.unsplash.com/photo-1511406361295-0a5ff814c0ad?w=400"},
            {"n": "Ponta de Silex", "img": "https://images.unsplash.com/photo-1510414695470-24970f807365?w=400"},
            {"n": "Vaso de Argila", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?w=400"}
        ],
        "animais": [
            {"n": "Lobo Ibérico", "u": "Selvagem", "img": "https://images.unsplash.com/photo-1590424753042-32244f05563c?w=400"},
            {"n": "Cervo", "u": "Caça", "img": "https://images.unsplash.com/photo-1549194380-f3c6c795af0e?w=400"},
            {"n": "Javali", "u": "Alimento", "img": "https://images.unsplash.com/photo-1516248967355-90033c94d13c?w=400"},
            {"n": "Auroque", "u": "Mítico", "img": "https://images.unsplash.com/photo-1551029506-0807df4e2031?w=400"}
        ]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5], "info": "Guerreiros da Serra da Estrela.",
        "ferramentas": [
            {"n": "Falcata", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"},
            {"n": "Escudo Caetra", "img": "https://images.unsplash.com/photo-1615678815958-5d413b70b653?w=400"},
            {"n": "Lança de Bronze", "img": "https://images.unsplash.com/photo-1558285511-966956795f55?w=400"},
            {"n": "Fuso de Tecelagem", "img": "https://images.unsplash.com/photo-1615560113840-06900693f185?w=400"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "u": "Guerra", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"},
            {"n": "Porco Alentejano", "u": "Alimento", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?w=400"},
            {"n": "Ovelha Bordaleira", "u": "Lã", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=400"},
            {"n": "Mastim", "u": "Guarda", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"}
        ]
    },
    "3. Romanos": {
        "coord": [38.4, -7.9], "info": "O Império em Portugal.",
        "ferramentas": [
            {"n": "Gladius", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"},
            {"n": "Arado Romano", "img": "https://images.unsplash.com/photo-1594391829624-dfc392bbbc24?w=400"},
            {"n": "Ânfora de Vinho", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?w=400"},
            {"n": "Moeda de Ouro", "img": "https://images.unsplash.com/photo-1611085583191-a3b1a6a939db?w=400"}
        ],
        "animais": [
            {"n": "Boi de Carga", "u": "Trabalho", "img": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400"},
            {"n": "Mula", "u": "Transporte", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?w=400"},
            {"n": "Ganso", "u": "Alerta", "img": "https://images.unsplash.com/photo-1542316812-730623661600?w=400"},
            {"n": "Cão de Caça", "u": "Lazer", "img": "https://images.unsplash.com/photo-1554692931-90a604297123?w=400"}
        ]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MENU")
    modo = st.radio("MODO ATUAL:", ["Explorar Épocas", "Evolução (Slider)", "⭐ Minhas Tribos"])
    
    if modo == "Explorar Épocas":
        escolha = st.selectbox("QUAL POVO:", list(db.keys()))
    elif modo == "Evolução (Slider)":
        escolha = st.select_slider("PASSE O TEMPO:", options=list(db.keys()))
    else:
        escolha = None

# --- LÓGICA DE EXIBIÇÃO ---
if modo == "⭐ Minhas Tribos":
    st.title("As Minhas Tribos Favoritas")
    if not st.session_state.favoritos:
        st.warning("Ainda não entraste em nenhuma tribo! Volta ao modo Explorar e clica no botão.")
    else:
        for t_nome, t_dados in st.session_state.favoritos.items():
            with st.expander(f"🛡️ Membro da Tribo: {t_nome}", expanded=True):
                st.write(t_dados["info"])
                c1, c2 = st.columns(2)
                with c1: st.write(f"Ferramentas: {len(t_dados['ferramentas'])}")
                with c2: st.write(f"Animais: {len(t_dados['animais'])}")
else:
    dados = db[escolha]
    st.title(escolha)
    
    # Botão Entrar na Tribo
    if st.button(f"➕ Entrar na Tribo {escolha}"):
        st.session_state.favoritos[escolha] = dados
        st.success(f"Agora és oficialmente parte da tribo {escolha}!")

    st.markdown(f'<div class="info-box"><b>Contexto:</b> {dados["info"]}</div>', unsafe_allow_html=True)

    # Mapa
    m = folium.Map(location=dados["coord"], zoom_start=7, tiles="CartoDB dark_matter")
    folium.Marker(dados["coord"], icon=folium.Icon(color="red")).add_to(m)
    st_folium(m, width="100%", height=300)

    # Listas Horizontais (4 Colunas)
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
