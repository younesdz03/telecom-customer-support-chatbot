from pathlib import Path
import sys
import time
import base64

ROOT_DIR = Path(__file__).resolve().parents[1]
LOGO_PATH = ROOT_DIR / "app" / "assets" / "logo.png"

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
from app.main import ask


st.set_page_config(
    page_title="Assistant Algérie Télécom",
    page_icon="💬",
    layout="wide"
)


def image_to_base64(path: Path) -> str:
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# =========================
# STYLE
# =========================
st.markdown(
    """
    <style>
        :root {
            --at-blue: #2458A6;
            --at-blue-dark: #173B75;
            --at-green: #00A859;
            --at-bg: #F3F7FC;
            --at-text: #1F2937;
            --at-muted: #64748B;
            --at-border: #DDE7F2;
        }

        .stApp {
            background: var(--at-bg);
            color: var(--at-text);
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        .block-container {
            max-width: 1120px;
            padding-top: 1.4rem;
            padding-bottom: 7rem;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2458A6 0%, #1D4D95 100%);
            border-right: 1px solid rgba(255,255,255,0.15);
        }

        section[data-testid="stSidebar"] * {
            color: white;
        }

        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0.8rem;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding-top: 0.8rem;
        }

        .sidebar-logo-card {
            background: white;
            border-radius: 18px;
            padding: 16px 14px;
            margin: 0 0 20px 0;
            box-shadow: 0 10px 28px rgba(0,0,0,0.16);
            border: 1px solid rgba(255,255,255,0.4);
            text-align: center;
        }

        .sidebar-logo-card img {
            width: 155px;
            max-width: 100%;
            height: auto;
            object-fit: contain;
            display: block;
            margin: 0 auto 10px auto;
        }

        .sidebar-brand-name {
            color: #2458A6 !important;
            font-weight: 800;
            font-size: 1.02rem;
            letter-spacing: 0.02em;
            line-height: 1.2;
            margin: 0;
        }

        .sidebar-brand-line {
            width: 36px;
            height: 3px;
            margin: 10px auto;
            border-radius: 2px;
            background: linear-gradient(90deg, var(--at-green), var(--at-blue));
        }

        .sidebar-brand-role {
            color: #64748B !important;
            font-size: 0.78rem;
            font-weight: 650;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin: 0;
        }

        .sidebar-card {
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 16px;
            padding: 15px 16px;
            margin-bottom: 14px;
        }

        .sidebar-title {
            font-size: 1rem;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .sidebar-text {
            font-size: 0.9rem;
            line-height: 1.55;
            color: #ECF6FF;
        }

        /* Buttons */
        .stButton > button {
            background: var(--at-green);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            padding: 0.58rem 1rem;
            box-shadow: 0 6px 14px rgba(0,168,89,0.25);
        }

        .stButton > button:hover {
            background: #008F4C;
            color: white;
            border: none;
        }

        /* Header professionnel */
        .main-header {
            position: relative;
            background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
            border-radius: 24px;
            border: 1px solid #dbe7f3;
            box-shadow: 0 14px 36px rgba(36, 88, 166, 0.12);
            overflow: hidden;
            margin-bottom: 28px;
        }

        .main-header::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 9px;
            height: 100%;
            background: linear-gradient(180deg, var(--at-green), var(--at-blue));
        }

        .main-header-content {
            padding: 34px 42px 36px 46px;
        }

        .main-kicker {
            display: inline-block;
            background: rgba(0, 168, 89, 0.10);
            color: var(--at-green);
            border: 1px solid rgba(0, 168, 89, 0.18);
            border-radius: 999px;
            padding: 6px 14px;
            font-weight: 800;
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 14px;
        }

        .main-title {
            color: var(--at-blue);
            font-size: 2.25rem;
            line-height: 1.18;
            font-weight: 900;
            margin-bottom: 12px;
        }

        .header-line {
            width: 70px;
            height: 4px;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--at-green), var(--at-blue));
            margin-bottom: 16px;
        }

        .main-subtitle {
            color: #475569;
            font-size: 1rem;
            line-height: 1.7;
            max-width: 920px;
        }

        .green-text {
            color: var(--at-green);
            font-weight: 800;
        }

        /* Questions rapides */
        .section-title {
            color: #0F172A;
            font-size: 1.35rem;
            font-weight: 800;
            margin: 6px 0 14px 0;
        }

        /* Messages */
        div[data-testid="stChatMessage"] {
            padding: 0.2rem 0;
        }

        div[data-testid="stChatMessageContent"] {
            background: white;
            color: var(--at-text);
            border: 1px solid var(--at-border);
            border-radius: 18px;
            padding: 1rem 1.15rem;
            box-shadow: 0 8px 22px rgba(15,23,42,0.06);
            line-height: 1.65;
        }

        /* Sources */
        .source-box {
            background: #F8FBFF;
            border: 1px solid var(--at-border);
            border-left: 5px solid var(--at-green);
            border-radius: 14px;
            padding: 12px 14px;
            margin-top: 6px;
        }

        .source-item {
            color: #1F2937;
            font-size: 0.94rem;
            margin-bottom: 8px;
        }

        /* Chat input */
        div[data-testid="stChatInput"] {
            max-width: 980px;
            margin: auto;
        }

        .footer-note {
            text-align: center;
            color: var(--at-muted);
            font-size: 0.85rem;
            margin-top: 28px;
        }

        hr {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.22);
            margin: 1.4rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    if LOGO_PATH.exists():
        logo_base64 = image_to_base64(LOGO_PATH)

        st.markdown(
            f"""
            <div class="sidebar-logo-card">
                <img src="data:image/png;base64,{logo_base64}" alt="Logo Algérie Télécom">
                <p class="sidebar-brand-name">Algérie Télécom</p>
                <div class="sidebar-brand-line"></div>
                <p class="sidebar-brand-role">Assistant client</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("Logo introuvable : app/assets/logo.png")

    if st.button("Vider l'historique", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Exemples de questions</div>
            <div class="sidebar-text">
                • J’ai une panne d’internet<br>
                • Mon internet est lent<br>
                • Le voyant LOS est rouge<br>
                • Comment contacter le support ?<br>
                • Quelle est la différence entre ADSL et fibre ?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Système</div>
            <div class="sidebar-text">
                RAG local<br>
                FAISS + Ollama + Phi-3
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# HEADER
# =========================
st.markdown(
    """
    <div class="main-header">
        <div class="main-header-content">
            <div class="main-kicker">Algérie Télécom</div>
            <div class="main-title">Assistant virtuel </div>
            <div class="header-line"></div>
            <div class="main-subtitle">
                Posez vos questions sur les offres, les services, les pannes internet,
                le Wi-Fi, le modem et la fibre. L’assistant s’appuie sur une approche
                <span class="green-text">RAG locale</span> afin de fournir des réponses
                contextualisées à partir d’une base de connaissance dédiée.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# SESSION
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# QUESTIONS RAPIDES
# =========================
st.markdown('<div class="section-title">Questions rapides</div>', unsafe_allow_html=True)

quick_question = None
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("Panne internet", use_container_width=True):
        quick_question = "J’ai une panne d’internet"

with col2:
    if st.button("Débit lent", use_container_width=True):
        quick_question = "Mon internet est lent"

with col3:
    if st.button("Problème Wi-Fi", use_container_width=True):
        quick_question = "Mon Wi-Fi ne fonctionne pas"

with col4:
    if st.button("Voyant LOS rouge", use_container_width=True):
        quick_question = "Le voyant LOS est rouge"

with col5:
    if st.button("Offres internet", use_container_width=True):
        quick_question = "Quelles sont les offres internet disponibles ?"


# =========================
# AFFICHAGE HISTORIQUE
# =========================
for msg in st.session_state.messages:
        st.markdown(msg["content"])

        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("Sources utilisées"):
                st.markdown('<div class="source-box">', unsafe_allow_html=True)

                displayed_titles = set()

                for src in msg["sources"]:
                    title = (src.get("title") or "Source sans titre").strip()
                    source = (src.get("source") or "").strip()

                    key = f"{title}-{source}"

                    if key not in displayed_titles:
                        displayed_titles.add(key)
                        st.markdown(
                            f"""
                            <div class="source-item">
                                • <b>{title}</b><br>
                                <small>Source : {source}</small>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                st.markdown("</div>", unsafe_allow_html=True)


# =========================
# INPUT
# =========================
typed_question = st.chat_input("Écrivez votre question ici...")
question = typed_question or quick_question


# =========================
# TRAITEMENT
# =========================
if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Recherche dans la base de connaissance..."):
            start_time = time.time()

            try:
                answer, results, context = ask(question)

                response_time = round(time.time() - start_time, 2)

                if results:
                    avg_score = round(
                        sum(src.get("score", 0) for src in results) / len(results),
                        3
                    )
                else:
                    avg_score = 0

                print("\n========== MÉTRIQUES ==========")
                print(f"Question : {question}")
                print(f"Temps de réponse : {response_time} s")
                print(f"Documents récupérés : {len(results)}")
                print(f"Score moyen RAG : {avg_score}")
                print("===============================\n")

                st.markdown(answer)

                if results:
                    with st.expander("Sources utilisées"):
                        st.markdown('<div class="source-box">', unsafe_allow_html=True)

                        displayed_titles = set()

                        for src in results:
                            title = (src.get("title") or "Source sans titre").strip()
                            source = (src.get("source") or "").strip()

                            key = f"{title}-{source}"

                            if key not in displayed_titles:
                                displayed_titles.add(key)
                                st.markdown(
                                    f"""
                                    <div class="source-item">
                                        • <b>{title}</b><br>
                                        <small>Source : {source}</small>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                        st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                answer = f"Une erreur est survenue : {e}"
                results = []
                context = ""

                print("\n========== ERREUR ==========")
                print(answer)
                print("============================\n")

                st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": results,
        "context": context
    })


# =========================
# FOOTER
# =========================
st.markdown(
    '<div class="footer-note">Algérie Télécom Assistant • RAG local • Ollama + Phi-3</div>',
    unsafe_allow_html=True
)