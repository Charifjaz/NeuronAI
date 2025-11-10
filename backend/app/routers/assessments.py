
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
from ..services.llm import llm_client

router = APIRouter(prefix="/assessments", tags=["assessments"])

class AssessmentInput(BaseModel):
    answers: Dict[str, Any] = Field(..., description="Mapping question_id -> value")

class AssessmentOutput(BaseModel):
    summary: str

@router.post("", response_model=AssessmentOutput)
async def create_assessment(payload: AssessmentInput):
    if not payload.answers:
        raise HTTPException(status_code=400, detail="answers is required")
    summary = await llm_client.analyze_answers(payload.answers)
    return AssessmentOutput(summary=summary)
