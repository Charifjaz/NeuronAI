from enum import Enum
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from sqlalchemy.orm import Session
from sqlalchemy import select

from ..database.db import SessionLocal
from ..database.models import UserProfile
from ..database.db import SessionLocal



from ..services.personality import infer_personality_from_answers
from ..services.profile_store import save_user_profile, get_user_profile, list_user_ids



router = APIRouter(prefix="/profile", tags=["profile"])


# ==============
#  ENUMS FIXES
# ==============

class Q1Option(str, Enum):
    PLAN_TABLEAU = "En faisant un plan ou un tableau"
    IMAGE_METAPHORE = "En trouvant une image ou une métaphore"
    COMPARER_CRITERES = "En comparant des options avec des critères"
    PARLER_POSER_IDEES = "En en parlant pour poser les idées"
    LAISSER_POSER = "En laissant poser et en y revenant plus tard"


class Q2Option(str, Enum):
    BRUME = "Une brume qui se dissipe"
    PUZZLE = "Un puzzle où il manque encore une pièce"
    PORTE = "Une porte à franchir"
    VAGUE = "Une vague d'idées à canaliser"
    CARTE = "Une carte avec plusieurs directions possibles"


class Q3Option(str, Enum):
    RELIRE = "Je relis calmement ce que j'ai déjà posé"
    EXEMPLE_SIMPLE = "Je cherche un exemple ou une version plus simple"
    TABLEAU = "Je mets tout à plat dans un tableau"
    PASSER_AUTRE_CHOSE = "Je passe à autre chose puis j'y reviens"
    REGARD_EXTERIEUR = "Je demande un regard extérieur"


class Q4Option(str, Enum):
    EXPLIQUER_SIMPLE = "Je peux l'expliquer simplement"
    APPLIQUER_TOUT_DE_SUITE = "Je peux l'appliquer tout de suite"
    VISUALISER = "Je le visualise clairement"
    RESUMER_3_POINTS = "Je peux le résumer en 3 points"
    EXEMPLE_CONCRET = "Je peux donner un exemple concret"
    AUTRE = "Autre (préciser)"


class Q5Option(str, Enum):
    ESSENTIEL = "Avoir l'essentiel tout de suite"
    PAS_A_PAS = "Un pas-à-pas avec exemples concrets"
    COMPLET_LOGIQUE = "Une explication complète avec la logique et les détails"
    ANALOGIE = "Une analogie / une image qui parle"
    ADAPTATIF = "Une version qui s'adapte selon ce que tu demandes"


class Q6Option(str, Enum):
    DECORTIQUER = "Décortiquer pour comprendre le fond"
    IMPROVISER = "Improviser et voir ce qui émerge"
    TESTER_AJUSTER = "Tester, observer, ajuster"
    LAISSER_DECLIC = "Laisser venir le déclic"
    CHERCHER_LOGIQUE = "Chercher d'abord la logique sous-jacente"


class Q7Option(str, Enum):
    VISUALISER_CONCRET = "En visualisant comment les choses se passent concrètement"
    ECRIRE_DESSINER = "En écrivant ou dessinant les idées"
    PARLER_EXPLIQUER = "En en parlant pour l'expliquer"
    OBSERVER = "En observant attentivement jusqu'à ce que tout prenne sens"
    CHERCHER_LOGIQUE = "En cherchant la logique qui relie tout"


# ==========================
#  MODELES DE REQUETE/REPONSE
# ==========================

class ProfileRequest(BaseModel):
    user_id: str = Field(
        ...,
        description="Identifiant anonyme de l'utilisateur (ex: uuid généré côté front). "
                    "Le même user_id doit être utilisé pour /profile et /chat."
    )
    Q1: Q1Option = Field(
        ...,
        description=(
            "Q1. Quand tu réfléchis à quelque chose d'important, qu'est-ce qui t'aide le plus à y voir clair ?"
        ),
    )
    Q2: Q2Option = Field(
        ...,
        description=(
            "Q2. Si tu devais représenter ta réflexion du moment, ce serait plutôt…"
        ),
    )
    Q3: Q3Option = Field(
        ...,
        description=(
            "Q3. Quand une idée ou une décision ne te semble pas encore claire, que fais-tu le plus souvent ?"
        ),
    )
    Q4: List[Q4Option] = Field(
        ...,
        description=(
            "Q4. Quand tu comprends quelque chose en profondeur, qu'est-ce qui te le montre ? (plusieurs choix possibles)"
        ),
    )
    Q5: Q5Option = Field(
        ...,
        description=(
            "Q5. Quand on t'explique quelque chose, tu préfères plutôt…"
        ),
    )
    Q6: Q6Option = Field(
        ...,
        description=(
            "Q6. Devant une situation qui demande un peu de réflexion, ton réflexe naturel, c'est plutôt…"
        ),
    )
    Q7: Q7Option = Field(
        ...,
        description=(
            "Q7. Par quel chemin passes-tu spontanément pour apprendre et comprendre ?"
        ),
    )


class ProfileResponse(BaseModel):
    personality: str


# ==========================
#  ENDPOINT PRINCIPAL
# ==========================

def get_db():
    """
    Fournit une session de base de données pour la durée de la requête.
    FastAPI appelle cette fonction, et s'occupe de la fermer après.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=ProfileResponse)
async def create_profile(body: ProfileRequest, db: Session = Depends(get_db)):
    """
    Endpoint profil :
    - Reçoit toujours les mêmes questions Q1..Q7
    - Chaque question a un set d'options fixes (Enum)
    - Renvoie un texte de personnalité à partir de ces réponses
    """
    answers: Dict[str, Any] = {
        "Q1": body.Q1.value,
        "Q2": body.Q2.value,
        "Q3": body.Q3.value,
        "Q4": [opt.value for opt in body.Q4],
        "Q5": body.Q5.value,
        "Q6": body.Q6.value,
        "Q7": body.Q7.value,
    }

    personality = infer_personality_from_answers(answers)

    # On stocke la personnalité pour ce user_id en mémoire
    save_user_profile(body.user_id, personality, db)

    return ProfileResponse(personality=personality)


@router.get(
    "/{user_id}",
    summary="Récupérer le profil de personnalité d'un utilisateur",
)
async def get_profile(
    user_id: str,
    db: Session = Depends(get_db),
):
    if not user_id.strip():
        raise HTTPException(status_code=400, detail="user_id invalide")

    user_profile = get_user_profile(user_id, db=db)

    if user_profile is None:
        raise HTTPException(status_code=404, detail="Profil introuvable pour cet user_id")

    return {
        "user_id": user_profile.user_id,
        "personality": user_profile.personality,
    }


@router.get(
    "/users/list",
    summary="Lister tous les user_id pour lesquels un profil a été créé",
)
async def list_profiles_users(
    db: Session = Depends(get_db),
):
    user_ids = list_user_ids(db=db)
    return {"user_ids": user_ids}