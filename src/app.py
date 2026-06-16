import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from datetime import date

st.set_page_config(
    page_title="CopaPulse AI",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .stRadio > div { flex-direction: row; gap: 1rem; }
    div[data-testid="stMetricValue"] { font-size: 1.4rem; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_agent():
    from agent import CopaPulseAgent
    return CopaPulseAgent()


@st.cache_data
def get_teams():
    from data_loader import get_all_team_names
    return get_all_team_names()


@st.cache_data
def get_today_games():
    from data_loader import buscar_jogos_por_data, jogos_para_texto
    jogos = buscar_jogos_por_data(date.today())
    return jogos_para_texto(jogos), len(jogos)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚽ CopaPulse AI")
    st.caption("Agente inteligente · Copa 2026")
    st.divider()

    mode = st.radio(
        "Modo de resposta",
        ["Torcedor", "Conteúdo", "Empresa"],
        help=(
            "**Torcedor:** linguagem simples\n\n"
            "**Conteúdo:** posts e boletins prontos\n\n"
            "**Empresa:** ações comerciais e comunicados"
        ),
    )

    st.divider()
    st.caption(f"Data atual: {date.today().strftime('%d/%m/%Y')}")
    st.caption("LLM: Groq · LLaMA 3.3 70B")
    st.caption("Base: Copa do Mundo 2026")

# ── Header ────────────────────────────────────────────────────────────────────
st.title("⚽ CopaPulse AI")

mode_colors = {"Torcedor": "🟢", "Conteúdo": "🔵", "Empresa": "🟠"}
st.caption(f"{mode_colors[mode]} Modo **{mode}** · Copa do Mundo 2026")

# ── Métricas rápidas ──────────────────────────────────────────────────────────
jogos_hoje_txt, n_jogos_hoje = get_today_games()
col1, col2, col3 = st.columns(3)
col1.metric("Jogos hoje", n_jogos_hoje)
col2.metric("Grupos", 12)
col3.metric("Seleções", 48)

st.divider()

# ── Botões rápidos ────────────────────────────────────────────────────────────
st.subheader("Acesso rápido")
c1, c2, c3, c4 = st.columns(4)

quick_query = None
with c1:
    if st.button("📋 Resumo da rodada", use_container_width=True):
        quick_query = "Faça um resumo completo dos resultados mais recentes da Copa, destacando os destaques e surpresas."
with c2:
    if st.button("📅 Jogos de hoje", use_container_width=True):
        quick_query = "Quais são os jogos de hoje na Copa do Mundo 2026? Liste com horários e estádios."
with c3:
    if st.button("🇧🇷 Situação do Brasil", use_container_width=True):
        quick_query = "Qual é a situação atual do Brasil na Copa? Explique o grupo, pontos, resultados e próximos jogos."
with c4:
    if st.button("📱 Gerar posts", use_container_width=True):
        quick_query = "Gere 3 posts prontos para Instagram sobre os jogos mais recentes da Copa do Mundo 2026."

st.divider()

# ── Campo de pergunta ─────────────────────────────────────────────────────────
with st.form("query_form", clear_on_submit=False):
    query = st.text_area(
        "Faça sua pergunta sobre a Copa 2026:",
        placeholder=(
            "Ex: Quais seleções estão liderando os grupos?\n"
            "Ex: Crie um comunicado interno sobre o jogo do Brasil.\n"
            "Ex: Gere um boletim para WhatsApp com os resultados do dia."
        ),
        height=110,
    )
    submitted = st.form_submit_button("Consultar ⚽", type="primary", use_container_width=True)

# ── Processar consulta ────────────────────────────────────────────────────────
final_query = quick_query or (query.strip() if submitted else None)

if final_query:
    try:
        agent = get_agent()
    except ValueError as e:
        st.error(f"Erro de configuração: {e}")
        st.info("Crie um arquivo `.env` na raiz do projeto com sua `GROQ_API_KEY`.")
        st.stop()

    with st.spinner(f"Consultando base e gerando resposta ({mode})..."):
        response = agent.respond(query=final_query, mode=mode)

    st.subheader("Resposta")
    st.markdown(response)

    with st.expander("Ver contexto consultado pela IA"):
        st.text(agent.get_last_context())

elif not submitted and not quick_query:
    # Estado inicial — mostra jogos de hoje
    if n_jogos_hoje > 0:
        st.subheader(f"Jogos de hoje — {date.today().strftime('%d/%m/%Y')}")
        st.text(jogos_hoje_txt)
    else:
        st.info("Nenhum jogo agendado para hoje. Use os botões rápidos ou faça uma pergunta.")
