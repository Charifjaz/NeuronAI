from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..services.llm import llm_client
from ..services.profile_store import get_user_profile
from ..database.db import SessionLocal

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    user_id: str
    question: str

class ChatResponse(BaseModel):
    answer: str
    personality_used: Optional[str] = None


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


@router.post(
    "", 
    response_model=ChatResponse,
    summary="Poser une question à l'assistant, qui adapte sa réponse au profil si disponible.",
)
async def chat_endpoint(body: ChatRequest, db: Session = Depends(get_db)):
    user_profile = get_user_profile(body.user_id, db)
    personality = user_profile.personality if user_profile else None
    
    answer = await llm_client.ask(
        question=body.question,
        personality=personality,
    )
    return ChatResponse(
        answer=answer,
        personality_used=personality
    )