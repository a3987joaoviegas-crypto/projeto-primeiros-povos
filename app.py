import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="MundoVivo: Evolução de Portugal", layout="wide")

# CSS Estilo Mundovivo - Total Black e Cartão de Cidadão
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 15px 0; }
    .cc-card {
        background-color: #111111; color: #ffffff; border: 1px solid #333;
        border-radius: 12px; padding: 15px; text-align: center; height: 100%;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .cc-header { font-size: 0.5rem; color: #888; border-bottom: 1px solid #222; margin-bottom: 10px; letter-spacing: 2px; }
    .img-real { width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; }
    .label { color: #666; font-size: 0.6rem; text-transform: uppercase; margin-top: 10px; }
    .value { font-size: 0.9rem; font-weight: bold; color: #fff; }
    .timeline-box { background: #1a1a1a; padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE COMPLETA ---
povos_db = {
    "Lusitanos": {
        "coords": [40.3, -7.5],
        "ferramentas": [
            {"n": "Falcata", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"},
            {"n": "Escudo Caetra", "img": "https://images.unsplash.com/photo-1615678815958-5d413b70b653?w=400"},
            {"n": "Arado de Madeira", "img": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=400"},
            {"n": "Ponta de Lança", "img": "https://images.unsplash.com/photo-1558285511-966956795f55?w=400"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "uso": "Guerra", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"},
            {"n": "Porco Alentejano", "uso": "Alimento", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?w=400"},
            {"n": "Ovelha Bordaleira", "uso": "Lã", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=400"},
            {"n": "Cabra Serrana", "uso": "Leite", "img": "https://images.unsplash.com/photo-1524024973431-2ad916746881?w=400"}
        ]
    },
    "Celtas e Galaicos": {
        "coords": [41.5, -8.3],
        "ferramentas": [
            {"n": "Torques de Ouro", "img": "https://images.unsplash.com/photo-1611085583191-a3b1a6a939db?w=400"},
            {"n": "Machado de Ferro", "img": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=400"},
            {"n": "Mó de Pedra", "img": "https://images.unsplash.com/photo-1603566270543-92f750d03704?w=400"},
            {"n": "Caldeirão", "img": "https://images.unsplash.com/photo-1582738411706-bfc8e691d1c2?w=400"}
        ],
        "animais": [
            {"n": "Vaca Cachena", "uso": "Tração", "img": "https://images.unsplash.com/photo-1545468843-2796674f1df2?w=400"},
            {"n": "Cão de Guarda", "uso": "Guarda", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"},
            {"n": "Ponei Garrano", "uso": "Transporte", "img": "https://images.unsplash.com/photo-1598974357851-cb8143c0f243?w=400"},
            {"n": "Boi Barrosão", "uso": "Trabalho", "img": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400"}
        ]
    },
    "Conios": {
        "coords": [37.3, -8.1],
        "ferramentas": [
            {"n": "Estela Escrita", "img": "https://images.unsplash.com/photo-1518153925617-3a629474bc9b?w=400"},
            {"n": "Ânfora", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?w=400"},
            {"n": "Anzol Bronze", "img": "https://images.unsplash.com/photo-1516937941344-00b4e0337589?w=400"},
            {"n": "Rede Pesca", "img": "https://images.unsplash.com/photo-1501703979959-79396f212591?w=400"}
        ],
        "animais": [
            {"n": "Burro", "uso": "Carga", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?w=400"},
            {"n": "Galinha", "uso": "Ovos", "img": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400"},
            {"n": "Cão de Água", "uso": "Pesca", "img": "https://images.unsplash.com/photo-1598133894008-61f7fdb8cc3a?w=400"},
            {"n": "Abelhas", "uso": "Mel", "img": "https://images.unsplash.com/photo-1581404476143-fb31d742929f?w=400"}
        ]
    }
}

# --- LINHA DO TEMPO EVOLUTIVA ---
timeline = {
    "Idade do Ferro": "Surgimento dos Lusitanos e Celtas.",
    "Império Romano": "Romanização da Lusitânia (Estradas e Cidades).",
    "Invasões Bárbaras": "Suevos e Visigodos dominam o território.",
    "Al-Andalus": "Domínio Árabe no Sul de Portugal.",
    "Reino de Portugal": "Independência e Expansão (D. Afonso Henriques).",
    "Portugal Moderno": "A nação tal como a conhecemos hoje."
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ MUNDO VIVO")
    modo = st.radio("Selecione o Modo:", ["Povos Ancestrais", "Evolução Portuguesa"])
    
    if modo == "Povos Ancestrais":
        escolha = st.selectbox("Escolha o Povo:", list(povos_db.keys()))
        povo = povos_db[escolha]
    else:
        etapa = st.select_slider("Viagem no Tempo:", options=list(timeline.keys()))

# --- CONTEÚDO ---
if modo == "Povos Ancestrais":
    st.title(f"Povo: {escolha}")
    m = folium.Map(location=povo["coords"], zoom_start=7, tiles="CartoDB dark_matter")
    folium.Marker(povo["coords"], icon=folium.Icon(color="red")).add_to(m)
    st_folium(m, width="100%", height=300)

    st.markdown("<h3 class='section-title'>🛠️ Ferramentas</h3>", unsafe_allow_html=True)
    cols_f = st.columns(4)
    for i, f in enumerate(povo["ferramentas"]):
        with cols_f[i]:
            st.markdown(f'<div class="cc-card"><img src="{f["img"]}" class="img-real"><div class="label">OBJETO</div><div class="value">{f["n"]}</div></div>', unsafe_allow_html=True)

    st.markdown("<h3 class='section-title'>🪪 Cartão de Cidadão Animal</h3>", unsafe_allow_html=True)
    cols_a = st.columns(4)
    for i, a in enumerate(povo["animais"]):
        with cols_a[i]:
            st.markdown(f'<div class="cc-card"><div class="cc-header">REPÚBLICA POVOS ANTIGOS</div><img src="{a["img"]}" class="img-real"><div class="label">NOME</div><div class="value">{a["n"]}</div><div class="label">USO</div><div class="value">{a["uso"]}</div></div>', unsafe_allow_html=True)

else:
    st.title("⏳ Evolução Portuguesa")
    st.markdown(f'<div class="timeline-box"><h2>{etapa}</h2><p>{timeline[etapa]}</p></div>', unsafe_allow_html=True)
    # Mapa geral de Portugal
    m_pt = folium.Map(location=[39.5, -8.0], zoom_start=6, tiles="CartoDB dark_matter")
    st_folium(m_pt, width="100%", height=500)
