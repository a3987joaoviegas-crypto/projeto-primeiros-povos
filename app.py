import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Primeiros Povos de Portugal", layout="wide")

# Estilo Visual Total Black
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .section-title { color: white; border-left: 4px solid #ffffff; padding-left: 15px; margin: 30px 0 10px 0; font-size: 1.2rem; }
    .info-box { background: #111111; padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; }
    .cc-card { background-color: #111111; color: #ffffff; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; height: 100%; }
    .img-real { width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; border: 1px solid #444; }
    .label { color: #666; font-size: 0.6rem; text-transform: uppercase; }
    .value { font-size: 0.85rem; font-weight: bold; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE DE TODAS AS ÉPOCAS ---
historia_pt = {
    "1. Pré-História": {
        "coord": [38.5, -8.0],
        "info": "Época dos grandes monumentos de pedra (Megalitismo).",
        "detalhe": "Habitantes: Povos Recoletores. Habitação: Grutas e abrigos. Economia: Caça.",
        "ferramentas": [{"n": "Machado de Pedra", "img": "https://images.unsplash.com/photo-1510414695470-24970f807365?w=400"}],
        "animais": [{"n": "Lobo", "uso": "Selvagem", "img": "https://images.unsplash.com/photo-1590424753042-32244f05563c?w=400"}]
    },
    "2. Lusitanos": {
        "coord": [40.3, -7.5],
        "info": "Guerreiros da Idade do Ferro liderados por Viriato.",
        "detalhe": "Habitação: Castros fortificados. Sociedade: Guerreira e independente.",
        "ferramentas": [{"n": "Falcata", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"}],
        "animais": [{"n": "Porco Alentejano", "uso": "Alimento", "img": "https://images.unsplash.com/photo-1594145070112-7096e79201f9?w=400"}]
    },
    "3. Romanos": {
        "coord": [38.4, -7.9],
        "info": "Fundação da Província da Lusitânia.",
        "detalhe": "Construção de estradas, pontes e cidades como Évora e Conimbriga.",
        "ferramentas": [{"n": "Ânfora", "img": "https://images.unsplash.com/photo-1578507065211-1c4e99a5fd24?w=400"}],
        "animais": [{"n": "Boi", "uso": "Arado", "img": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400"}]
    },
    "4. Visigodos": {
        "coord": [38.1, -7.8],
        "info": "Reinos Germânicos que sucederam aos Romanos.",
        "detalhe": "Época de transição e cristianização profunda da península.",
        "ferramentas": [{"n": "Coroa Votiva", "img": "https://images.unsplash.com/photo-1611085583191-a3b1a6a939db?w=400"}],
        "animais": [{"n": "Cavalo", "uso": "Transporte", "img": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400"}]
    },
    "5. Árabes (Al-Andalus)": {
        "coord": [37.1, -7.9],
        "info": "Influência islâmica no Sul (Algarve e Alentejo).",
        "detalhe": "Novas técnicas de rega, pomares e avanços na ciência e poesia.",
        "ferramentas": [{"n": "Astrolábio", "img": "https://images.unsplash.com/photo-1603566270543-92f750d03704?w=400"}],
        "animais": [{"n": "Burro", "uso": "Carga", "img": "https://images.unsplash.com/photo-1534145557161-469b768e987c?w=400"}]
    },
    "6. Fundação do Reino": {
        "coord": [41.4, -8.2],
        "info": "Afonso Henriques proclama a independência (1143).",
        "detalhe": "Reconquista cristã e nascimento de Portugal em Guimarães.",
        "ferramentas": [{"n": "Espada Real", "img": "https://images.unsplash.com/photo-1590256153835-bd3c4014292c?w=400"}],
        "animais": [{"n": "Cão de Guarda", "uso": "Castelo", "img": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400"}]
    },
    "7. Descobrimentos": {
        "coord": [38.7, -9.2],
        "info": "A expansão marítima portuguesa pelo mundo.",
        "detalhe": "Invenção da Caravela e mapeamento dos oceanos.",
        "ferramentas": [{"n": "Bússola", "img": "https://images.unsplash.com/photo-1516937941344-00b4e0337589?w=400"}],
        "animais": [{"n": "Papagaio", "uso": "Exótico", "img": "https://images.unsplash.com/photo-1552728089-57bdde30fc3e?w=400"}]
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🇵🇹 HISTÓRIA DE PORTUGAL")
    epoca = st.select_slider("PASSE A ÉPOCA AQUI:", options=list(historia_pt.keys()))
    dados = historia_pt[epoca]

# --- CONTEÚDO PRINCIPAL ---
st.title(f"Época: {epoca}")

st.markdown(f"""
<div class="info-box">
    <h3>{dados['info']}</h3>
    <p>{dados['detalhe']}</p>
</div>
""", unsafe_allow_html=True)

# Mapa
m = folium.Map(location=dados["coord"], zoom_start=7, tiles="CartoDB dark_matter")
folium.Marker(dados["coord"], icon=folium.Icon(color="red")).add_to(m)
st_folium(m, width="100%", height=300)

# Listas Horizontais
st.markdown("<h3 class='section-title'>⚒️ Ferramentas da Época</h3>", unsafe_allow_html=True)
cols_f = st.columns(4)
for i, f in enumerate(dados["ferramentas"]):
    with cols_f[i]:
        st.markdown(f'<div class="cc-card"><img src="{f["img"]}" class="img-real"><div class="label">ARTEFACTO</div><div class="value">{f["n"]}</div></div>', unsafe_allow_html=True)

st.markdown("<h3 class='section-title'>🪪 Animais e Vida</h3>", unsafe_allow_html=True)
cols_a = st.columns(4)
for i, a in enumerate(dados["animais"]):
    with cols_a[i]:
        st.markdown(f'<div class="cc-card"><img src="{a["img"]}" class="img-real"><div class="label">NOME</div><div class="value">{a["n"]}</div><div class="label">USO</div><div class="value">{a["uso"]}</div></div>', unsafe_allow_html=True)
