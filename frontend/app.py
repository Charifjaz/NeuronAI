import streamlit as st
import requests
import uuid
import os
from typing import Optional, List, Dict

# ============================================
# CONFIGURATION
# ============================================

# Get API URL from environment variable (Docker) or use default (local dev)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# ============================================
# API FUNCTIONS
# ============================================

def get_user_profile(user_id: str) -> Optional[Dict]:
    """Retrieve user profile from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/profile/{user_id}", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Erreur lors de la récupération du profil: {e}")
        return None


def create_profile(user_id: str, answers: Dict) -> Optional[str]:
    """Create a new user profile"""
    try:
        payload = {
            "user_id": user_id,
            **answers
        }
        response = requests.post(f"{API_BASE_URL}/profile", json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["personality"]
        else:
            st.error(f"Erreur API: {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de la création du profil: {e}")
        return None


def send_chat_message(user_id: str, question: str) -> Optional[Dict]:
    """Send a chat message to the API"""
    try:
        payload = {
            "user_id": user_id,
            "question": question
        }
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API: {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de l'envoi du message: {e}")
        return None


def list_users() -> List[str]:
    """List all user IDs"""
    try:
        response = requests.get(f"{API_BASE_URL}/profile/users/list", timeout=10)
        if response.status_code == 200:
            return response.json().get("user_ids", [])
        return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des utilisateurs: {e}")
        return []


def check_backend_health() -> bool:
    """Check if backend is reachable"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


# ============================================
# PERSONALITY QUIZ QUESTIONS
# ============================================

QUESTIONS = {
    "Q1": {
        "question": "Quand tu réfléchis à quelque chose d'important, qu'est-ce qui t'aide le plus à y voir clair ?",
        "options": [
            "En faisant un plan ou un tableau",
            "En trouvant une image ou une métaphore",
            "En comparant des options avec des critères",
            "En en parlant pour poser les idées",
            "En laissant poser et en y revenant plus tard"
        ]
    },
    "Q2": {
        "question": "Si tu devais représenter ta réflexion du moment, ce serait plutôt…",
        "options": [
            "Une brume qui se dissipe",
            "Un puzzle où il manque encore une pièce",
            "Une porte à franchir",
            "Une vague d'idées à canaliser",
            "Une carte avec plusieurs directions possibles"
        ]
    },
    "Q3": {
        "question": "Quand une idée ou une décision ne te semble pas encore claire, que fais-tu le plus souvent ?",
        "options": [
            "Je relis calmement ce que j'ai déjà posé",
            "Je cherche un exemple ou une version plus simple",
            "Je mets tout à plat dans un tableau",
            "Je passe à autre chose puis j'y reviens",
            "Je demande un regard extérieur"
        ]
    },
    "Q4": {
        "question": "Quand tu comprends quelque chose en profondeur, qu'est-ce qui te le montre ? (plusieurs choix possibles)",
        "options": [
            "Je peux l'expliquer simplement",
            "Je peux l'appliquer tout de suite",
            "Je le visualise clairement",
            "Je peux le résumer en 3 points",
            "Je peux donner un exemple concret",
            "Autre (préciser)"
        ],
        "multiple": True
    },
    "Q5": {
        "question": "Quand on t'explique quelque chose, tu préfères plutôt…",
        "options": [
            "Avoir l'essentiel tout de suite",
            "Un pas-à-pas avec exemples concrets",
            "Une explication complète avec la logique et les détails",
            "Une analogie / une image qui parle",
            "Une version qui s'adapte selon ce que tu demandes"
        ]
    },
    "Q6": {
        "question": "Devant une situation qui demande un peu de réflexion, ton réflexe naturel, c'est plutôt…",
        "options": [
            "Décortiquer pour comprendre le fond",
            "Improviser et voir ce qui émerge",
            "Tester, observer, ajuster",
            "Laisser venir le déclic",
            "Chercher d'abord la logique sous-jacente"
        ]
    },
    "Q7": {
        "question": "Par quel chemin passes-tu spontanément pour apprendre et comprendre ?",
        "options": [
            "En visualisant comment les choses se passent concrètement",
            "En écrivant ou dessinant les idées",
            "En en parlant pour l'expliquer",
            "En observant attentivement jusqu'à ce que tout prenne sens",
            "En cherchant la logique qui relie tout"
        ]
    }
}

# ============================================
# STREAMLIT UI
# ============================================

def init_session_state():
    """Initialize session state variables"""
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "personality" not in st.session_state:
        st.session_state.personality = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}


def user_selection_page():
    """User selection/creation page"""
    st.title("🎭 Assistant Personnalisé")
    st.markdown("---")
    
    # Check backend health
    if not check_backend_health():
        st.error("⚠️ Le backend n'est pas accessible. Vérifiez que l'API FastAPI est démarrée.")
        st.info(f"URL du backend: {API_BASE_URL}")
        return
    
    st.subheader("👤 Sélection de profil")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Utilisateur existant")
        users = list_users()
        
        if users:
            selected_user = st.selectbox(
                "Choisir un profil",
                [""] + users,
                key="user_select"
            )
            
            if st.button("Charger ce profil", disabled=not selected_user):
                profile = get_user_profile(selected_user)
                if profile:
                    st.session_state.user_id = selected_user
                    st.session_state.personality = profile["personality"]
                    st.success(f"✅ Profil chargé: {selected_user}")
                    st.rerun()
        else:
            st.info("Aucun utilisateur existant")
    
    with col2:
        st.markdown("### Nouveau profil")
        new_user_name = st.text_input("Nom du profil", key="new_user_name")
        
        if st.button("Créer un nouveau profil", disabled=not new_user_name):
            new_user_id = f"{new_user_name}_{str(uuid.uuid4())[:8]}"
            st.session_state.user_id = new_user_id
            st.session_state.personality = None
            st.success(f"✅ Nouveau profil créé: {new_user_id}")
            st.rerun()


def personality_quiz_page():
    """Personality quiz page"""
    st.title("📋 Questionnaire de personnalité")
    st.markdown("Répondez aux questions suivantes pour personnaliser votre expérience.")
    st.markdown("---")
    
    answers = {}
    
    for q_id, q_data in QUESTIONS.items():
        st.markdown(f"### {q_data['question']}")
        
        if q_data.get("multiple", False):
            selected = st.multiselect(
                "Sélectionnez une ou plusieurs réponses",
                q_data["options"],
                key=f"quiz_{q_id}"
            )
            if selected:
                answers[q_id] = selected
        else:
            selected = st.radio(
                "Choisissez votre réponse",
                q_data["options"],
                key=f"quiz_{q_id}",
                index=None
            )
            if selected:
                answers[q_id] = selected
        
        st.markdown("---")
    
    # Check if all questions are answered
    all_answered = len(answers) == len(QUESTIONS)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📤 Soumettre", disabled=not all_answered, use_container_width=True):
            with st.spinner("Création de votre profil..."):
                personality = create_profile(st.session_state.user_id, answers)
                if personality:
                    st.session_state.personality = personality
                    st.success("✅ Profil de personnalité créé avec succès!")
                    st.rerun()
    
    if not all_answered:
        st.info(f"⏳ Veuillez répondre à toutes les questions ({len(answers)}/{len(QUESTIONS)})")


def chat_page():
    """Main chat interface"""
    st.title("💬 Chat avec l'Assistant")
    
    # Sidebar with user info
    with st.sidebar:
        st.markdown("### 👤 Profil actuel")
        st.info(f"**ID:** {st.session_state.user_id}")
        
        if st.session_state.personality:
            with st.expander("🎭 Votre personnalité", expanded=False):
                st.markdown(st.session_state.personality)
        
        st.markdown("---")
        st.markdown("### ⚙️ Actions")
        
        if st.button("🔄 Refaire le quiz", use_container_width=True):
            st.session_state.personality = None
            st.rerun()
        
        if st.button("👤 Changer de profil", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.personality = None
            st.session_state.chat_history = []
            st.rerun()
        
        if st.button("🗑️ Effacer l'historique", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown("---")
        st.caption(f"🔗 Backend: {API_BASE_URL}")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Posez votre question..."):
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Réflexion en cours..."):
                response = send_chat_message(st.session_state.user_id, prompt)
                
                if response:
                    answer = response["answer"]
                    st.markdown(answer)
                    
                    # Add assistant message to history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })
                else:
                    st.error("Erreur lors de la communication avec l'API")


# ============================================
# MAIN APP
# ============================================

def main():
    st.set_page_config(
        page_title="Assistant Personnalisé",
        page_icon="🎭",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stButton > button {
            width: 100%;
        }
        .stRadio > div {
            padding: 10px 0;
        }
        .stChatMessage {
            padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    init_session_state()
    
    # Navigation logic
    if st.session_state.user_id is None:
        user_selection_page()
    elif st.session_state.personality is None:
        personality_quiz_page()
    else:
        chat_page()


if __name__ == "__main__":
    main()