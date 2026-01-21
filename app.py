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
    }
    .cc-header { font-size: 0.5rem; color: #888; border-bottom: 1px solid #222; margin-bottom: 10px; letter-spacing: 2px; }
    .img-real { width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; background-color: #222; }
    .label { color: #666; font-size: 0.6rem; text-transform: uppercase; margin-top: 10px; }
    .value { font-size: 0.9rem; font-weight: bold; color: #fff; }
    .info-box { background: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 5px solid #ffffff; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE DE POVOS E IMAGENS ---
povos_db = {
    "Lusitanos": {
        "coords": [40.3, -7.5],
        "historia": "Guerreiros independentes que habitavam as montanhas. Mestres da tática de guerrilha contra os Romanos.",
        "ferramentas": [
            {"n": "Falcata", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"},
            {"n": "Escudo Caetra", "img": "https://images.unsplash.com/photo-1615678815958-5d413b70b653?w=400"},
            {"n": "Arado de Madeira", "img": "https://images.unsplash.com/photo-1594391829624-dfc392bbbc24?w=400"},
            {"n": "Lança de Bronze", "img": "https://images.unsplash.com/photo-1510414695470-24970f807365?w=400"}
        ],
        "animais": [
            {"n": "Cavalo Lusitano", "uso": "Guerra", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"},
            {"n": "Porco Alentejano", "uso": "Alimento", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?w=400"},
            {"n": "Ovelha Bordaleira", "uso": "Lã", "img": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=400"},
            {"n": "Cão de Fila", "uso": "Guarda", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"}
        ]
    },
    "Celtas e Galaicos": {
        "coords": [41.5, -8.3],
        "historia": "Povos do Norte conhecidos pela cultura dos Castros e pelo domínio avançado do ferro e do ouro.",
        "ferramentas": [
            {"n": "Torques de Ouro", "img": "https://images.unsplash.com/photo-1611085583191-a3b1a6a939db?w=400"},
            {"n": "Machado de Ferro", "img": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=400"},
            {"n": "Caldeirão Bronze", "img": "https://images.unsplash.com/photo-1582738411706-bfc8e691d1c2?w=400"},
            {"n": "Mó de Pedra", "img": "https://images.unsplash.com/photo-1603566270543-92f750d03704?w=400"}
        ],
        "animais": [
            {"n": "Vaca Cachena", "uso": "Tração", "img": "https://images.unsplash.com/photo-1545468843-2796674f1df2?w=400"},
            {"n": "Cão de Castro", "uso": "Guarda", "img": "https://images.unsplash.com/photo-1554692931-90a604297123?w=400"},
            {"n": "Boi Barrosão", "uso": "Trabalho", "img": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400"},
            {"n": "Garrano", "uso": "Transporte", "img": "https://images.unsplash.com/photo-1598974357851-cb8143c0f243?w=400"}
        ]
    },
    "Romanos": {
        "coords": [38.5, -7.9],
        "historia": "O Império que unificou a Península. Trouxeram o latim, o direito, e transformaram a agricultura com grandes villas.",
        "ferramentas": [{"n": "Gladius", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"}, {"n": "Ânfora", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?w=400"}],
        "animais": [{"n": "Burro", "uso": "Carga", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?w=400"}, {"n": "Gado Vacum", "uso": "Alimento", "img": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400"}]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ primeiros povos")
    modo = st.radio("Selecione o Modo:", ["Povos Ancestrais", "Evolução Portuguesa"])
    
    if modo == "Evolução Portuguesa":
        etapa = st.select_slider("Linha do Tempo:", options=list(povos_db.keys()))
        dados = povos_db[etapa]

# --- CONTEÚDO PRINCIPAL ---
if modo == "Povos Ancestrais":
    povo_nome = st.selectbox("Escolha o Povo:", list(povos_db.keys()))
    dados = povos_db[povo_nome]
    st.title(f"Povo: {povo_nome}")
else:
    st.title(f"⏳ Evolução: {etapa}")
    st.markdown(f"<div class='info-box'><h3>Informação Histórica</h3><p>{dados['historia']}</p></div>", unsafe_allow_html=True)

# Mapa comum a ambos os modos
m = folium.Map(location=dados["coords"], zoom_start=7, tiles="CartoDB dark_matter")
folium.Marker(dados["coords"], icon=folium.Icon(color="red")).add_to(m)
st_folium(m, width="100%", height=300)

# Listas Horizontais (Animais e Ferramentas)
st.markdown("<h3 class='section-title'>🛠️ Ferramentas</h3>", unsafe_allow_html=True)
cols_f = st.columns(len(dados["ferramentas"]))
for i, f in enumerate(dados["ferramentas"]):
    with cols_f[i]:
        st.markdown(f'<div class="cc-card"><img src="{f["img"]}" class="img-real"><div class="label">ARTEFACTO</div><div class="value">{f["n"]}</div></div>', unsafe_allow_html=True)

st.markdown("<h3 class='section-title'>🪪 Cartão de Cidadão Animal</h3>", unsafe_allow_html=True)
cols_a = st.columns(len(dados["animais"]))
for i, a in enumerate(dados["animais"]):
    with cols_a[i]:
        st.markdown(f'<div class="cc-card"><div class="cc-header">REPÚBLICA POVOS ANTIGOS</div><img src="{a["img"]}" class="img-real"><div class="label">NOME</div><div class="value">{a["n"]}</div><div class="label">USO</div><div class="value">{a["uso"]}</div></div>', unsafe_allow_html=True)
