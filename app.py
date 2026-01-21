import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="MundoVivo: Portugal Ancestral", layout="wide")

# Estilo Visual: Dark Mode, Cartão de Cidadão e Tabelas
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .section-header {
        background: linear-gradient(90deg, #1f1f1f, #000000);
        padding: 10px;
        border-left: 6px solid #ff4b4b;
        margin: 30px 0 15px 0;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .cc-card {
        background-color: #000000;
        color: #ffffff;
        border: 2px solid #333;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .cc-card:hover { border-color: #ff4b4b; }
    .cc-title { font-size: 0.6rem; color: #666; text-align: center; letter-spacing: 2px; }
    .img-box {
        width: 100%;
        height: 140px;
        object-fit: cover;
        border-radius: 6px;
        margin: 10px 0;
        border: 1px solid #222;
    }
    .label { color: #555; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.9rem; font-weight: bold; border-bottom: 1px solid #111; margin-bottom: 8px; }
    .desc-text { font-size: 0.8rem; color: #aaa; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DADOS MASSIVA ---
povos_db = {
    "Lusitanos": {
        "coords": [40.3, -7.5],
        "historia": "Guerreiros da Serra da Estrela, mestres da guerrilha e da pastorícia transumante.",
        "ferramentas": [
            {"n": "Falcata Lusitana", "desc": "Espada curva de gume interior.", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?q=80&w=400"},
            {"n": "Escudo Caetra", "desc": "Escudo redondo e pequeno de couro.", "img": "https://images.unsplash.com/photo-1615678815958-5d413b70b653?q=80&w=400"},
            {"n": "Arado de Madeira", "desc": "Essencial para o cultivo de cereais.", "img": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=400"},
            {"n": "Fuso de Tecelagem", "desc": "Para fiar a lã das ovelhas.", "img": "https://images.unsplash.com/photo-1615560113840-06900693f185?q=80&w=400"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "uso": "Guerra e Caça", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?q=80&w=400"},
            {"n": "Ovelha Bordaleira", "uso": "Lã e Leite", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?q=80&w=400"},
            {"n": "Cão de Fila", "uso": "Proteção de Rebanho", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?q=80&w=400"},
            {"n": "Abelhas", "uso": "Mel e Cera", "img": "https://images.unsplash.com/photo-1581404476143-fb31d742929f?q=80&w=400"}
        ]
    },
    "Celtas (Norte e Alentejo)": {
        "coords": [41.5, -8.0],
        "historia": "Introduziram a metalurgia do ferro e a cultura dos Castros fortificados.",
        "ferramentas": [
            {"n": "Machado de Ferro", "desc": "Ferramenta de corte e combate.", "img": "https://images.unsplash.com/photo-1580910051074-3eb694886505?q=80&w=400"},
            {"n": "Caldeirão de Bronze", "desc": "Uso em banquetes e rituais.", "img": "https://images.unsplash.com/photo-1582738411706-bfc8e691d1c2?q=80&w=400"},
            {"n": "Mó de Pedra", "desc": "Moagem manual de grãos.", "img": "https://images.unsplash.com/photo-1603566270543-92f750d03704?q=80&w=400"},
            {"n": "Torques", "desc": "Colar de ouro, símbolo de status.", "img": "https://images.unsplash.com/photo-1611085583191-a3b1a6a939db?q=80&w=400"}
        ],
        "animais": [
            {"n": "Boi Barrosão", "uso": "Trabalho Pesado", "img": "https://images.unsplash.com/photo-1545468843-2796674f1df2?q=80&w=400"},
            {"n": "Porco Bísaro", "uso": "Alimentação (Enchidos)", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?q=80&w=400"},
            {"n": "Cão Galgo", "uso": "Caça de Lebres", "img": "https://images.unsplash.com/photo-1554692931-90a604297123?q=80&w=400"},
            {"n": "Galinha Pedrês", "uso": "Ovos", "img": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?q=80&w=400"}
        ]
    },
    "Conios (Sul)": {
        "coords": [37.2, -8.1],
        "historia": "O povo mais antigo com escrita própria na Península, influenciado pelos Fenícios.",
        "ferramentas": [
            {"n": "Estela de Escrita", "desc": "Pedra gravada com alfabeto paleo-hispânico.", "img": "https://images.unsplash.com/photo-1518153925617-3a629474bc9b?q=80&w=400"},
            {"n": "Ânfora de Barro", "desc": "Armazenamento de azeite e vinho.", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?q=80&w=400"},
            {"n": "Anzol de Bronze", "desc": "Pesca costeira avançada.", "img": "https://images.unsplash.com/photo-1516937941344-00b4e0337589?q=80&w=400"},
            {"n": "Rede de Linho", "desc": "Pesca de cerco no mar.", "img": "https://images.unsplash.com/photo-1501703979959-79396f212591?q=80&w=400"}
        ],
        "animais": [
            {"n": "Burro do Algarve", "uso": "Carga de Mercadorias", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?q=80&w=400"},
            {"n": "Gado Vacum", "uso": "Carne e Leite", "img": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?q=80&w=400"},
            {"n": "Cão de Água", "uso": "Auxílio na Pesca", "img": "https://images.unsplash.com/photo-1598133894008-61f7fdb8cc3a?q=80&w=400"},
            {"n": "Aves de Capoeira", "uso": "Subsistência", "img": "https://images.unsplash.com/photo-1516467508483-a7212febe31a?q=80&w=400"}
        ]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MundoVivo")
    st.markdown("---")
    with st.expander("▶ EXPLORAR POVOS"):
        selecao = st.radio("", list(povos_db.keys()))

povo = povos_db[selecao]

# --- TOPO: MAPA E INFO ---
st.title(f"Povo Antigo: {selecao}")
st.markdown(f"> {povo['historia']}")

m = folium.Map(location=[39.5, -8.0], zoom_start=6, tiles="CartoDB dark_matter")
folium.Marker(povo["coords"], popup=selecao, icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
st_folium(m, width="100%", height=300)

# --- LISTA HORIZONTAL DE FERRAMENTAS ---
st.markdown("<div class='section-header'>🛠️ Ferramentas e Tecnologia</div>", unsafe_allow_html=True)
cols_f = st.columns(len(povo["ferramentas"]))
for i, f in enumerate(povo["ferramentas"]):
    with cols_f[i]:
        st.markdown(f"""
            <div class="cc-card">
                <img src="{f['img']}" class="img-box">
                <div class="label">OBJETO</div>
                <div class="value">{f['n']}</div>
                <div class="desc-text">{f['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

# --- LISTA HORIZONTAL DE ANIMAIS (CARTÃO DE CIDADÃO) ---
st.markdown("<div class='section-header'>🪪 Animais da Quinta (Cartão de Cidadão)</div>", unsafe_allow_html=True)
cols_a = st.columns(len(povo["animais"]))
for i, a in enumerate(povo["animais"]):
    with cols_a[i]:
        st.markdown(f"""
            <div class="cc-card">
                <div class="cc-title">CARTÃO DE CIDADÃO ANIMAL</div>
                <img src="{a['img']}" class="img-box">
                <div class="label">NOME</div>
                <div class="value">{a['n']}</div>
                <div class="label">FUNÇÃO / UTILIZAÇÃO</div>
                <div class="value">{a['uso']}</div>
            </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption("Dados históricos baseados em achados arqueológicos da Península Ibérica.")
