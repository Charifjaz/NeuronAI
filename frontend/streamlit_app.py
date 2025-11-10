import os
import httpx
import streamlit as st
from dotenv import load_dotenv
from typing import Dict, Any, List

# -------------------------------------------------------------
# Config
# -------------------------------------------------------------
load_dotenv()
DEFAULT_API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Neural Chat Interface",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Futuriste
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d3a 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #e0e7ff !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stChatMessage::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.4), transparent);
        animation: borderShine 3s infinite;
    }
    
    @keyframes borderShine {
        0% {
            left: -100%;
        }
        100% {
            left: 100%;
        }
    }
    
    .stChatMessage:hover {
        border-color: rgba(139, 92, 246, 0.4) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.15);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
        color: #e0e7ff !important;
        font-size: 14px !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(139, 92, 246, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
    }
    
    /* Form */
    .stForm {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        backdrop-filter: blur(10px);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        color: #e0e7ff !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: rgba(139, 92, 246, 0.3) !important;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
    }
    
    /* Status indicators */
    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        border-left: 4px solid #8b5cf6 !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 12px !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(139, 92, 246, 0.2) !important;
    }
    
    /* Labels */
    label {
        color: #c7d2fe !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(10, 14, 39, 0.95) !important;
        border-right: 1px solid rgba(139, 92, 246, 0.2) !important;
    }
    
    /* Caption */
    .stCaption {
        color: #94a3b8 !important;
        font-size: 12px !important;
    }
    
    /* Chat input */
    .stChatInputContainer {
        border-top: 1px solid rgba(139, 92, 246, 0.2) !important;
        background: rgba(255, 255, 255, 0.02) !important;
    }
    
    /* Markdown in expander */
    .streamlit-expanderContent p {
        color: #e0e7ff !important;
    }
    
    /* Success/Warning/Info */
    .stSuccess, .stWarning, .stInfo {
        backdrop-filter: blur(10px);
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Utilities
# -------------------------------------------------------------
def init_state() -> None:
    ss = st.session_state
    ss.setdefault("api_base", DEFAULT_API_BASE)
    ss.setdefault("questions", None)
    ss.setdefault("answers_draft", {})
    ss.setdefault("answers_validated", {})
    ss.setdefault("is_validated", False)
    ss.setdefault("messages", [])
    ss.setdefault("loading_questions_error", None)

@st.cache_data(show_spinner=False)
def fetch_questions(api_base: str) -> List[Dict[str, Any]]:
    """Récupère la liste des questions depuis l'API."""
    try:
        r = httpx.get(f"{api_base.rstrip('/')}/questions", timeout=15.0)
        r.raise_for_status()
        data = r.json()
        if not isinstance(data, list):
            raise ValueError("Le format /questions doit être une liste JSON.")
        for q in data:
            q.setdefault("label", q.get("text", q.get("id", "Question")))
        return data
    except Exception:
        return [
            {"id": "context", "type": "textarea", "label": "Contexte du projet", "placeholder": "Décrivez brièvement…", "default": ""},
            {"id": "objective", "type": "text", "label": "Objectif principal", "placeholder": "Quel est l'objectif ?", "default": ""},
            {"id": "audience", "type": "text", "label": "Public cible", "placeholder": "À qui s'adresse la réponse ?", "default": ""},
        ]

def build_prompt(user_message: str, answers: Dict[str, Any]) -> str:
    profile_lines = []
    for k, v in answers.items():
        val = (str(v).strip() if v is not None else "")
        if val:
            profile_lines.append(f"- {k}: {val}")
    header = "Réponses validées (profil utilisateur):\n" + "\n".join(profile_lines) + "\n\n" if profile_lines else ""
    return (header + f"Question utilisateur: {user_message}").strip()

def call_backend_ask(api_base: str, message: str, answers: Dict[str, Any]) -> str:
    """Appelle le backend /ask avec le message et les réponses validées."""
    payload = {"message": message, "answers": answers}
    try:
        r = httpx.post(f"{api_base.rstrip('/')}/ask", json=payload, timeout=120.0)
        r.raise_for_status()
        data = r.json()
        return data.get("reply", "(Aucune réponse)")
    except Exception as e:
        return f"Erreur d'appel API: {e}"

# -------------------------------------------------------------
# App State init
# -------------------------------------------------------------
init_state()

# -------------------------------------------------------------
# Header
# -------------------------------------------------------------
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1.5rem 0; position: relative;">
    <h1 style="font-size: 3rem; margin: 0; background: linear-gradient(90deg, #8b5cf6, #6366f1, #8b5cf6); 
               background-size: 200% auto; color: transparent; -webkit-background-clip: text; 
               background-clip: text; animation: shine 3s linear infinite;">
        🧠 Neural Chat Interface
    </h1>
    <p style="color: #94a3b8; margin-top: 0.5rem; font-size: 1.1rem; font-weight: 300;">
        Intelligence conversationnelle avec profil contextuel
    </p>
</div>
<style>
    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }
</style>
""", unsafe_allow_html=True)
st.divider()

# -------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.session_state.api_base = st.text_input("🔗 API Base URL", value=st.session_state.api_base)
    
    st.divider()
    
    st.markdown("### 📊 État du système")
    if st.session_state.is_validated:
        st.success("✅ Profil activé", icon="✅")
        st.caption("Le contexte est appliqué à toutes les requêtes")
    else:
        st.warning("⚠️ Profil inactif", icon="⚠️")
        st.caption("Validez votre profil pour activer le chat")

# -------------------------------------------------------------
# Layout (2 colonnes: Chat | Questions)
# -------------------------------------------------------------
col_chat, col_q = st.columns([2, 1], gap="large")

# ===========================
# Colonne de droite: QUESTIONS
# ===========================
with col_q:
    st.markdown("### 🎯 Profil Contextuel")

    # Charger questions (1x)
    if st.session_state.questions is None:
        st.session_state.questions = fetch_questions(st.session_state.api_base)
        for q in st.session_state.questions:
            qid = q.get("id")
            if qid and qid not in st.session_state.answers_draft:
                if q.get("default") is not None:
                    st.session_state.answers_draft[qid] = q["default"]
                elif q.get("type") == "slider":
                    mn, mx = q.get("scale_min", 0), q.get("scale_max", 10)
                    st.session_state.answers_draft[qid] = int((mn + mx) // 2)
                else:
                    st.session_state.answers_draft[qid] = ""

    # Mode édition / lecture selon validation
    if not st.session_state.is_validated:
        with st.form("questions_form"):
            for q in st.session_state.questions:
                qid = q.get("id")
                qtype = q.get("type", "text")
                label = q.get("label", qid)
                placeholder = q.get("placeholder", "")
                key = f"ans_{qid}"

                if qtype == "textarea":
                    st.session_state.answers_draft[qid] = st.text_area(
                        label,
                        value=str(st.session_state.answers_draft.get(qid, "")),
                        placeholder=placeholder,
                        key=key,
                        height=110,
                    )
                elif qtype == "slider":
                    mn = int(q.get("scale_min", 0))
                    mx = int(q.get("scale_max", 10))
                    default_val = int(st.session_state.answers_draft.get(qid, int((mn + mx)//2)))
                    st.session_state.answers_draft[qid] = st.slider(
                        label, min_value=mn, max_value=mx, value=default_val, key=key
                    )
                else:
                    st.session_state.answers_draft[qid] = st.text_input(
                        label,
                        value=str(st.session_state.answers_draft.get(qid, "")),
                        placeholder=placeholder,
                        key=key,
                    )

            submitted = st.form_submit_button("🚀 Activer le profil", use_container_width=True)
            if submitted:
                st.session_state.answers_validated = dict(st.session_state.answers_draft)
                st.session_state.is_validated = True
                try:
                    st.toast("✅ Profil activé avec succès", icon="✅")
                except Exception:
                    pass
                st.rerun()
    else:
        with st.expander("📋 Profil actif", expanded=True):
            for q in st.session_state.questions:
                qid = q.get("id")
                label = q.get("label", qid)
                val = st.session_state.answers_validated.get(qid, "")
                st.markdown(f"**{label}**")
                st.markdown(f"> {val if str(val).strip() else '_(non renseigné)_'}")
                st.markdown("")

        if st.button("✏️ Modifier le profil", use_container_width=True):
            st.session_state.is_validated = False
            try:
                st.toast("✏️ Mode édition activé", icon="✏️")
            except Exception:
                pass
            st.rerun()

        st.divider()
        
        with st.expander("🔍 Aperçu du prompt"):
            st.code(build_prompt("Votre prochain message...", st.session_state.answers_validated), language="markdown")

# ==================
# Colonne de gauche: CHAT
# ==================
with col_chat:
    st.markdown("### 💬 Conversation")

    # Historique
    chat_container = st.container(height=500)
    with chat_container:
        for m in st.session_state.messages:
            with st.chat_message(m["role"], avatar="🧑" if m["role"] == "user" else "🤖"):
                st.write(m["content"])

    # Saisie (désactivée si non validé)
    prompt_disabled = not st.session_state.is_validated
    user_input = st.chat_input("💭 Écrivez votre message...", disabled=prompt_disabled)

    if user_input is not None and not prompt_disabled:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with chat_container:
            with st.chat_message("user", avatar="🧑"):
                st.write(user_input)

            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("⚡ Traitement en cours..."):
                    reply = call_backend_ask(
                        st.session_state.api_base,
                        message=user_input,
                        answers=st.session_state.answers_validated,
                    )
                    st.write(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if prompt_disabled:
        st.info("👉 Activez votre profil dans le panneau de droite pour démarrer la conversation", icon="ℹ️")

# -------------------------------------------------------------
# Footer
# -------------------------------------------------------------
st.divider()
st.caption("🔒 Session en mémoire · Aucune donnée persistée · Alimenté par l'API backend")