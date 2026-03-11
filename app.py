import streamlit as st
import anthropic
import json

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Churrinha Agent",
    page_icon="🎮",
    layout="centered"
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Bebas+Neue&display=swap');
html, body, [class*="css"] { font-family: 'Space Mono', monospace; background-color: #080810; color: #ffffff; }
.stApp { background-color: #080810; }
h1 { font-family: 'Bebas Neue', sans-serif !important; font-size: 2.4rem !important; background: linear-gradient(90deg, #39ff14, #00ffcc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 3px; }
h2, h3 { color: #39ff14 !important; font-family: 'Space Mono', monospace !important; }
.stButton>button { background: linear-gradient(135deg, #39ff14, #00e6b0) !important; color: #000 !important; font-weight: 700 !important; border: none !important; border-radius: 10px !important; padding: 12px 28px !important; font-family: 'Space Mono', monospace !important; width: 100% !important; font-size: 15px !important; }
.stTextArea>div>div>textarea { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 10px !important; color: #fff !important; font-family: 'Space Mono', monospace !important; }
.stSelectbox>div>div { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 10px !important; color: #fff !important; }
.card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px 20px; margin-bottom: 14px; }
.card-green { background: rgba(57,255,20,0.06); border: 1px solid rgba(57,255,20,0.2); border-radius: 12px; padding: 18px 20px; margin-bottom: 14px; }
.card-red { background: rgba(255,51,102,0.06); border: 1px solid rgba(255,51,102,0.2); border-radius: 12px; padding: 18px 20px; margin-bottom: 14px; }
.card-orange { background: rgba(255,153,0,0.06); border: 1px solid rgba(255,153,0,0.2); border-radius: 12px; padding: 18px 20px; margin-bottom: 14px; }
.score-high { background:#ff3366; color:#000; padding:3px 12px; border-radius:20px; font-weight:900; font-size:13px; }
.score-mid { background:#ff9900; color:#000; padding:3px 12px; border-radius:20px; font-weight:900; font-size:13px; }
.score-low { background:#39ff14; color:#000; padding:3px 12px; border-radius:20px; font-weight:900; font-size:13px; }
.tag { background:rgba(57,255,20,0.1); color:#39ff14; padding:2px 10px; border-radius:4px; font-size:12px; margin-right:6px; }
.label { color:rgba(255,255,255,0.4); font-size:11px; letter-spacing:1px; margin-bottom:6px; }
.divider { border-top: 1px solid rgba(255,255,255,0.06); margin: 28px 0; }
</style>
""", unsafe_allow_html=True)

# ── API Setup ─────────────────────────────────────────────────────────────────
def get_client():
    try:
        return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    except:
        return None

client = get_client()

def call_claude(system_prompt, user_prompt):
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return msg.content[0].text

def parse_json(raw, bracket="["):
    clean = raw.replace("```json","").replace("```","").strip()
    end_b = "]" if bracket == "[" else "}"
    return json.loads(clean[clean.find(bracket):clean.rfind(end_b)+1])

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<h1>CHURRINHA AGENT</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:rgba(255,255,255,0.35);font-size:12px;letter-spacing:1px;margin-top:-16px;'>TikTok Gaming · Content AI · @churrinha</p>", unsafe_allow_html=True)
st.markdown("---")

if not client:
    st.error("🔑 Adicione ANTHROPIC_API_KEY nos secrets do Streamlit.")
    st.stop()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📡  Radar de Tendências", "📝  Gerador de Roteiro"])

# ── TAB 1 ─────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("### 🔍 O que está bombando agora?")
    st.markdown("<p style='color:rgba(255,255,255,0.5);font-size:13px;'>Analisa o cenário atual dos games e identifica os tópicos com maior potencial no TikTok BR.</p>", unsafe_allow_html=True)

    genero = st.selectbox("Filtrar por gênero:", ["Qualquer","FPS","RPG","Battle Royale","MOBA","Indie","Mobile","Esports","Retro / Clássicos","Nintendo / SNES / N64","Sega / Mega Drive","Arcade","Survival / Crafting","Simulação","Terror / Horror","Hack and Slash","Plataforma","Luta / Fighting","Corrida / Racing","Puzzle / Casual","Mundo Aberto / Open World","MMO / Online"])

    if st.button("🔍 BUSCAR TENDÊNCIAS AGORA"):
        with st.spinner("Analisando o que está bombando no mundo dos games..."):
            try:
                raw = call_claude(
                    "Você é um analista de tendências de games para TikTok brasileiro. Retorne SOMENTE JSON válido, sem markdown.",
                    f"""Identifique 5 tópicos de games com maior potencial no TikTok Brasil agora.
Gênero: {genero if genero != 'Qualquer' else 'todos'}.
Considere: lançamentos, patches polêmicos, memes, torneios, trailers, dramas da comunidade.

JSON exato:
[{{"title":"titulo curto","reason":"por que está em alta e funciona no TikTok BR (2 frases)","score":9,"tags":["tag1","tag2","tag3"]}}]
Score 1-10 = potencial de engajamento. Use jogos e eventos reais e atuais."""
                )
                st.session_state["trends"] = parse_json(raw, "[")
                st.session_state["selected_trend"] = None
                st.session_state["roteiro"] = None
            except Exception as e:
                st.error(f"Erro: {e}")

    if st.session_state.get("trends"):
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown(f"<p class='label'>{len(st.session_state['trends'])} TENDÊNCIAS — clique para gerar roteiro</p>", unsafe_allow_html=True)
        for i, t in enumerate(st.session_state["trends"]):
            sc = t.get("score",5)
            sc_class = "score-high" if sc>=9 else "score-mid" if sc>=7 else "score-low"
            tags_html = " ".join([f"<span class='tag'>#{x}</span>" for x in t.get("tags",[])])
            st.markdown(f"""
            <div class='card'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div style='flex:1;'>
                        <div style='font-weight:700;font-size:15px;margin-bottom:6px;'>{t['title']}</div>
                        <div style='color:rgba(255,255,255,0.5);font-size:13px;line-height:1.6;'>{t['reason']}</div>
                    </div>
                    <span class='{sc_class}' style='margin-left:14px;white-space:nowrap;'>{sc}/10</span>
                </div>
                <div style='margin-top:10px;'>{tags_html}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"✍️ Gerar roteiro para este tópico", key=f"t{i}"):
                st.session_state["selected_trend"] = t
                st.session_state["roteiro"] = None
                st.rerun()

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<p class='label'>OU INSIRA UM TÓPICO MANUALMENTE</p>", unsafe_allow_html=True)
    custom = st.text_area("Descreva o tópico:", placeholder="Ex: patch de nerf no Valorant deixou o jogo horrível...", height=80)
    if st.button("✍️ GERAR ROTEIRO COM TÓPICO MANUAL") and custom:
        st.session_state["selected_trend"] = {"title": custom, "reason": ""}
        st.session_state["roteiro"] = None
        st.rerun()

# ── TAB 2 ─────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### 📝 Roteiro para TikTok")
    selected = st.session_state.get("selected_trend")

    if not selected:
        st.info("💡 Vá para **📡 Radar**, busque tendências e clique em **Gerar roteiro**.")
    else:
        st.markdown(f"<div class='card-green'><p class='label'>TÓPICO SELECIONADO</p><b>{selected['title']}</b></div>", unsafe_allow_html=True)

        if not st.session_state.get("roteiro"):
            if st.button("✍️ GERAR ROTEIRO AGORA"):
                with st.spinner("Criando roteiro no estilo @churrinha..."):
                    try:
                        raw = call_claude(
                            "Você é roteirista de TikTok gaming para @churrinha. Estilo: humor + gameplay, linguagem brasileira gamer, energia alta. Retorne SOMENTE JSON válido.",
                            f"""Roteiro de TikTok sobre: "{selected['title']}"
Contexto: {selected.get('reason','')}

JSON exato:
{{"titulo":"titulo impactante","hook":"frase impossível de ignorar nos 3 primeiros segundos","desenvolvimento":["ponto 1","ponto 2","ponto 3","ponto 4 surpresa"],"cta":"call to action final","descricao":"legenda com emojis para TikTok","hashtags":["gaming","tiktokgaming","games","gamer","gamerbr","fyp","viral","br"],"duracao_segundos":45}}"""
                        )
                        st.session_state["roteiro"] = parse_json(raw, "{")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro: {e}")

    if st.session_state.get("roteiro"):
        r = st.session_state["roteiro"]
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        st.markdown(f"""<div class='card-red'>
            <p class='label'>🎬 TÍTULO DO VÍDEO</p>
            <b style='font-size:16px;'>{r.get('titulo','')}</b>
            <p style='color:rgba(255,255,255,0.4);font-size:12px;margin-top:8px;margin-bottom:0;'>⏱ Duração ideal: ~{r.get('duracao_segundos',45)}s</p>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class='card-green'>
            <p class='label'>⚡ HOOK — PRIMEIROS 3 SEGUNDOS</p>
            <i style='font-size:15px;line-height:1.6;'>"{r.get('hook','')}"</i>
        </div>""", unsafe_allow_html=True)

        dev = r.get("desenvolvimento", [])
        dev_html = "".join([f"<div style='display:flex;gap:12px;margin-bottom:10px;'><div style='width:22px;height:22px;border-radius:50%;background:rgba(57,255,20,0.15);border:1px solid rgba(57,255,20,0.3);color:#39ff14;font-size:11px;display:flex;align-items:center;justify-content:center;flex-shrink:0;'>{i+1}</div><div style='color:rgba(255,255,255,0.8);font-size:14px;line-height:1.6;'>{item}</div></div>" for i,item in enumerate(dev)])
        st.markdown(f"<div class='card'><p class='label'>📋 DESENVOLVIMENTO</p>{dev_html}</div>", unsafe_allow_html=True)

        st.markdown(f"""<div class='card-orange'>
            <p class='label'>🎯 CALL TO ACTION FINAL</p>
            <span style='font-size:14px;'>{r.get('cta','')}</span>
        </div>""", unsafe_allow_html=True)

        hashtags = " ".join([f"#{h}" if not h.startswith("#") else h for h in r.get("hashtags",[])])
        legenda = f"{r.get('descricao','')}\n\n{hashtags}"
        tags_html = " ".join([f"<span class='tag'>{h if h.startswith('#') else '#'+h}</span>" for h in r.get("hashtags",[])])
        st.markdown(f"<div class='card'><p class='label'>📱 LEGENDA + HASHTAGS</p><p style='color:rgba(255,255,255,0.7);font-size:13px;line-height:1.7;margin-bottom:12px;'>{r.get('descricao','')}</p><div>{tags_html}</div></div>", unsafe_allow_html=True)

        st.text_area("📋 Copiar legenda:", value=legenda, height=110, key="leg")
        st.text_area("📋 Copiar roteiro completo:", value=f"TÍTULO: {r.get('titulo','')}\nDURAÇÃO: ~{r.get('duracao_segundos',45)}s\n\nHOOK:\n\"{r.get('hook','')}\"\n\nDESENVOLVIMENTO:\n"+"\n".join([f"{i+1}. {x}" for i,x in enumerate(dev)])+f"\n\nCTA:\n{r.get('cta','')}\n\n---\nLEGENDA:\n{legenda}", height=220, key="rot")

        if st.button("🔄 Gerar novo roteiro"):
            st.session_state["roteiro"] = None
            st.session_state["selected_trend"] = None
            st.rerun()
