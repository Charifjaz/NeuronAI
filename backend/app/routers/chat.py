from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from ..services.llm import llm_client
from ..services.profile_store import get_user_profile


router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    user_id: str
    question: str

class ChatResponse(BaseModel):
    answer: str
    personality_used: Optional[str] = None

@router.post(
        "", 
        response_model=ChatResponse,
        summary="Poser une question à l'assistant, qui adapte sa réponse au profil si disponible.",
        )
async def chat_endpoint(body: ChatRequest):
    personality = get_user_profile(body.user_id)
    answer = await llm_client.ask(
        question=body.question,
        personality=personality,
    )
    return ChatResponse(
        answer=answer,
        personality_used=personality
        )
