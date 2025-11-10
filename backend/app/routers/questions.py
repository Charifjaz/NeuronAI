
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Literal
# from ..data.questions_data import QUESTIONS  # ✅ import clair

router = APIRouter(prefix="/questions", tags=["questions"])

class Question(BaseModel):
    id: str
    text: str
    scale_min: int = 1
    scale_max: int = 5
    reverse: bool = False

# Exemple de mini-instrument (Big Five simplifié)
QUESTIONS: List[Question] = [
    Question(id="O1", text="J'aime explorer des idées nouvelles."),
    Question(id="C1", text="Je termine ce que je commence."),
    Question(id="E1", text="Je me sens à l'aise en groupe."),
    Question(id="A1", text="J'évite les conflits et fais des compromis."),
    Question(id="N1", text="Je me sens souvent stressé(e)."),
    # Ajoutez vos propres items ici, versionnée côté back.
]


@router.get("", response_model=List[Question])
def list_questions():
    return QUESTIONS
