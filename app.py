import streamlit as st
import google.generativeai as genai
import json
import re

# ── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Churrinha Agent",
    page_icon="🎮",
    layout="centered"
)

# ── Styles ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Bebas+Neue&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Mono', monospace;
    background-color: #080810;
    color: #ffffff;
}
.stApp { background-color: #080810; }

h1 { 
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 2.4rem !important;
    background: linear-gradient(90deg, #39ff14, #00ffcc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 3px;
}
h2, h3 { color: #39ff14 !important; font-family: 'Space Mono', monospace !important; }

.stButton>button {
    background: linear-gradient(135deg, #39ff14, #00e6b0) !important;
    color: #000 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-family: 'Space Mono', monospace !important;
    width: 100% !important;
    font-size: 15px !important;
}
.stButton>button:hover { box-shadow: 0 0 25px rgba(57,255,20,0.4) !important; }

.stTextArea>div>div>textarea, .stTextInput>div>div>input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'Space Mono', monospace !important;
}
.stSelectbox>div>div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #fff !important;
}
.stRadio>div { gap: 10px; }
.stRadio>div>label { color: #39ff14 !important; }

.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.card-green {
    background: rgba(57,255,20,0.06);
    border: 1px solid rgba(57,255,20,0.2);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.card-red {
    background: rgba(255,51,102,0.06);
    border: 1px solid rgba(255,51,102,0.2);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.card-orange {
    background: rgba(255,153,0,0.06);
    border: 1px solid rgba(255,153,0,0.2);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.score-high { background:#ff3366; color:#000; padding:3px 12px; border-radius:20px; font-weight:900; font-size:13px; }
.score-mid  { background:#ff9900; color:#000; padding:3px 12px; border-radius:20px; font-weight:900; font-size:13px; }
.score-low  { background:#39ff14; color:#000; padding:3px 12px; border-radius:20px; font-weight:900; font-size:13px; }
.tag { background:rgba(57,255,20,0.1); color:#39ff14; padding:2px 10px; border-radius:4px; font-size:12px; margin-right:6px; }
.label { color:rgba(255,255,255,0.4); font-size:11px; letter-spacing:1px; margin-bottom:6px; }
.divider { border-top: 1px solid rgba(255,255,255,0.06); margin: 28px 0; }
</style>
""", unsafe_allow_html=True)

# ── API Setup ─────────────────────────────────────────────────────────────────
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        return None

api_key = get_api_key()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<h1>CHURRINHA AGENT</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:rgba(255,255,255,0.35); font-size:12px; letter-spacing:1px; margin-top:-16px;'>TikTok Gaming · Content AI · @churrinha</p>", unsafe_allow_html=True)
st.markdown("---")

# ── API Key check ─────────────────────────────────────────────────────────────
if not api_key:
    st.error("🔑 API Key não configurada. Adicione GEMINI_API_KEY nos secrets do Streamlit.")
    st.info("Vá em Settings → Secrets e adicione: GEMINI_API_KEY = 'sua_chave_aqui'")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📡  Radar de Tendências", "📝  Gerador de Roteiro"])

# ════════════════════════════════════════════════════════════
# TAB 1 — RADAR
# ════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 🔍 O que está bombando agora?")
    st.markdown("<p style='color:rgba(255,255,255,0.5); font-size:13px;'>Busca em tempo real os tópicos de games com maior potencial de engajamento no TikTok brasileiro.</p>", unsafe_allow_html=True)

    genero = st.selectbox(
        "Filtrar por gênero:",
        ["Qualquer", "FPS", "RPG", "Battle Royale", "MOBA", "Indie", "Mobile", "Esports"]
    )

    if st.button("🔍 BUSCAR TENDÊNCIAS AGORA"):
        with st.spinner("Varrendo Reddit, Steam, YouTube Gaming, X..."):
            prompt = f"""Você é um analista de tendências de games para TikTok brasileiro.
Pesquise o que está em alta NO MUNDO DOS GAMES AGORA: lançamentos, patches, polêmicas, virais, memes, torneios, trailers.
Filtre por gênero: {genero if genero != 'Qualquer' else 'todos os gêneros'}.
Foco em conteúdo com alto potencial para TikTok Brasil.

Retorne SOMENTE um JSON válido, sem markdown, sem texto extra.
Formato exato:
[
  {{
    "title": "Nome do tópico",
    "reason": "Por que está em alta e por que funciona no TikTok (2 frases)",
    "score": 9,
    "tags": ["tag1", "tag2", "tag3"]
  }}
]
Máximo 5 tendências. Score 1-10 representa potencial de engajamento."""

            try:
                response = model.generate_content(prompt)
                raw = response.text
                clean = raw.replace("```json", "").replace("```", "").strip()
                start = clean.find("[")
                end = clean.rfind("]") + 1
                trends = json.loads(clean[start:end])
                st.session_state["trends"] = trends
                st.session_state["selected_trend"] = None
            except Exception as e:
                st.error(f"Erro ao buscar tendências: {e}")

    # Mostrar tendências
    if "trends" in st.session_state and st.session_state["trends"]:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown(f"<p class='label'>{len(st.session_state['trends'])} TENDÊNCIAS ENCONTRADAS</p>", unsafe_allow_html=True)

        for i, trend in enumerate(st.session_state["trends"]):
            score = trend.get("score", 5)
            score_class = "score-high" if score >= 9 else "score-mid" if score >= 7 else "score-low"
            tags_html = " ".join([f"<span class='tag'>#{t}</span>" for t in trend.get("tags", [])])

            st.markdown(f"""
            <div class='card' style='cursor:pointer;'>
                <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                    <div style='flex:1;'>
                        <div style='font-weight:700; font-size:15px; margin-bottom:6px;'>{trend['title']}</div>
                        <div style='color:rgba(255,255,255,0.5); font-size:13px; line-height:1.6;'>{trend['reason']}</div>
                    </div>
                    <span class='{score_class}' style='margin-left:14px;'>{score}/10</span>
                </div>
                <div style='margin-top:10px;'>{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"✍️ Gerar roteiro → {trend['title'][:40]}...", key=f"trend_{i}"):
                st.session_state["selected_trend"] = trend
                st.session_state["active_tab"] = "roteiro"
                st.rerun()

    # Tópico manual
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<p class='label'>OU INSIRA UM TÓPICO MANUALMENTE</p>", unsafe_allow_html=True)
    custom = st.text_area("Descreva o tópico:", placeholder="Ex: patch de nerf no Valorant deixou o jogo horrível...", height=80)
    if st.button("✍️ GERAR ROTEIRO COM TÓPICO MANUAL") and custom:
        st.session_state["selected_trend"] = {"title": custom, "reason": ""}
        st.rerun()

# ════════════════════════════════════════════════════════════
# TAB 2 — ROTEIRO
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 📝 Roteiro para TikTok")

    selected = st.session_state.get("selected_trend")

    if not selected:
        st.info("💡 Vá para **📡 Radar**, busque tendências e clique em **Gerar roteiro** em uma delas.")
    else:
        st.markdown(f"<div class='card-green'><p class='label'>TÓPICO SELECIONADO</p><b>{selected['title']}</b></div>", unsafe_allow_html=True)

        if st.button("✍️ GERAR ROTEIRO AGORA"):
            with st.spinner("Criando roteiro no estilo @churrinha..."):
                prompt = f"""Você é um roteirista especialista em TikTok de games para o criador @churrinha.
Estilo do criador: humor + gameplay, direto, linguagem brasileira gamer, irreverente.
Tópico: "{selected['title']}"
Contexto: {selected.get('reason', '')}

Retorne SOMENTE um JSON válido, sem markdown, sem texto extra:
{{
  "titulo": "Título chamativo do vídeo",
  "hook": "Frase de abertura dos primeiros 3 segundos - deve ser impossível de ignorar, use humor ou provocação forte",
  "desenvolvimento": [
    "Ponto 1 do vídeo",
    "Ponto 2 do vídeo",
    "Ponto 3 do vídeo",
    "Ponto 4 do vídeo"
  ],
  "cta": "Call to action final para engajar o público",
  "descricao": "Legenda completa com emojis para colar no TikTok",
  "hashtags": ["gaming", "tiktokgaming", "games", "gamer", "br", "fyp", "viral", "gamerbr"],
  "duracao_segundos": 45
}}"""

                try:
                    response = model.generate_content(prompt)
                    raw = response.text
                    clean = raw.replace("```json", "").replace("```", "").strip()
                    start = clean.find("{")
                    end = clean.rfind("}") + 1
                    roteiro = json.loads(clean[start:end])
                    st.session_state["roteiro"] = roteiro
                except Exception as e:
                    st.error(f"Erro ao gerar roteiro: {e}")

    # Mostrar roteiro
    if "roteiro" in st.session_state and st.session_state.get("roteiro"):
        r = st.session_state["roteiro"]
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # Título
        st.markdown(f"""
        <div class='card-red'>
            <p class='label'>🎬 TÍTULO DO VÍDEO</p>
            <b style='font-size:16px;'>{r.get('titulo','')}</b>
            <p style='color:rgba(255,255,255,0.4); font-size:12px; margin-top:8px; margin-bottom:0;'>⏱ Duração ideal: ~{r.get('duracao_segundos', 45)}s</p>
        </div>
        """, unsafe_allow_html=True)

        # Hook
        st.markdown(f"""
        <div class='card-green'>
            <p class='label'>⚡ HOOK — PRIMEIROS 3 SEGUNDOS</p>
            <i style='font-size:15px; line-height:1.6;'>"{r.get('hook','')}"</i>
        </div>
        """, unsafe_allow_html=True)

        # Desenvolvimento
        dev = r.get("desenvolvimento", [])
        dev_html = "".join([f"<div style='display:flex;gap:12px;margin-bottom:10px;align-items:flex-start;'><div style='width:22px;height:22px;border-radius:50%;background:rgba(57,255,20,0.15);border:1px solid rgba(57,255,20,0.3);color:#39ff14;font-size:11px;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;'>{i+1}</div><div style='color:rgba(255,255,255,0.8);font-size:14px;line-height:1.6;'>{item}</div></div>" for i, item in enumerate(dev)])
        st.markdown(f"""
        <div class='card'>
            <p class='label'>📋 DESENVOLVIMENTO</p>
            {dev_html}
        </div>
        """, unsafe_allow_html=True)

        # CTA
        st.markdown(f"""
        <div class='card-orange'>
            <p class='label'>🎯 CALL TO ACTION FINAL</p>
            <span style='font-size:14px;line-height:1.6;'>{r.get('cta','')}</span>
        </div>
        """, unsafe_allow_html=True)

        # Descrição + Hashtags
        hashtags = " ".join([f"#{h}" if not h.startswith("#") else h for h in r.get("hashtags", [])])
        legenda_completa = f"{r.get('descricao','')}\n\n{hashtags}"
        st.markdown(f"""
        <div class='card'>
            <p class='label'>📱 LEGENDA + HASHTAGS</p>
            <p style='color:rgba(255,255,255,0.7);font-size:13px;line-height:1.7;'>{r.get('descricao','')}</p>
            <p style='color:#39ff14;font-size:12px;'>{hashtags}</p>
        </div>
        """, unsafe_allow_html=True)

        st.text_area("📋 Copiar legenda completa:", value=legenda_completa, height=120)

        roteiro_texto = f"""TÍTULO: {r.get('titulo','')}

HOOK (primeiros 3s):
"{r.get('hook','')}"

DESENVOLVIMENTO:
{chr(10).join([f"{i+1}. {item}" for i, item in enumerate(dev)])}

CTA FINAL:
{r.get('cta','')}

---
LEGENDA:
{legenda_completa}"""

        st.text_area("📋 Copiar roteiro completo:", value=roteiro_texto, height=200)

        if st.button("🔄 Gerar novo roteiro"):
            st.session_state["roteiro"] = None
            st.session_state["selected_trend"] = None
            st.rerun()
