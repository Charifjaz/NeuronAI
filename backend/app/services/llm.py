
from __future__ import annotations
from typing import List, Dict, Any
import httpx
# from . import typing as _t  # optional placeholder for future types
from ..core.settings import settings

SYSTEM_PROMPT = (
    "Tu es un assistant psychométrique prudent. "
    "Tu aides à synthétiser un profil de personnalité à partir d'un questionnaire. "
    "Tu évites tout diagnostic médical. "
    "Tu synthétises en sections: Forces, Points d'attention, Style de résolution de problèmes, "
    "Conseils pratiques personnalisés."
)

class LLMClient:
    def __init__(self, base_url: str, api_key: str, provider: str = "OPENAI"):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.provider = provider.upper()

    async def chat(self, messages: List[Dict[str, str]], model: str = "gpt-4o-mini", temperature: float = 0.3) -> str:
        headers = {}
        url = ""
        payload: Dict[str, Any] = {}
        if self.provider == "OPENAI":
            url = f"{self.base_url}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": model,
                "temperature": temperature,
                "messages": messages,
            }
        else:
            # Fallback generic OpenAI-compatible
            url = f"{self.base_url}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": model,
                "temperature": temperature,
                "messages": messages,
            }

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            # OpenAI-compatible schema
            return data["choices"][0]["message"]["content"]

    async def analyze_answers(self, answers: Dict[str, Any]) -> str:
        # Minimal orchestrator: build a compact prompt with derived features
        # Example: simple Likert aggregation (Big Five lite). Replace with your instrument.
        traits = {
            "ouverture": 0.0,
            "conscienciosite": 0.0,
            "extraversion": 0.0,
            "agreabilite": 0.0,
            "nevrosisme": 0.0,
        }
        # naive aggregation
        for qid, val in answers.items():
            try:
                v = float(val)
            except Exception:
                v = 0.0
            # toy mapping by prefix
            if str(qid).startswith("O"):
                traits["ouverture"] += v
            elif str(qid).startswith("C"):
                traits["conscienciosite"] += v
            elif str(qid).startswith("E"):
                traits["extraversion"] += v
            elif str(qid).startswith("A"):
                traits["agreabilite"] += v
            elif str(qid).startswith("N"):
                traits["nevrosisme"] += v

        user_summary = "\n".join([f"- {k}: {round(v,2)}" for k,v in traits.items()])

        user_prompt = (
            f"Voici un résumé chiffré (0-5 par item, plus haut = plus marqué) :\n{user_summary}\n\n"
            "Rédige un profil concis (<= 250 mots) structuré en 4 sections avec des puces. "
            "Utilise un ton positif, concret, et actionnable. "
            "N'ajoute pas d'avertissements médicaux."
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
        return await self.chat(messages)

llm_client = LLMClient(
    base_url=settings.PROVIDER_BASE_URL,
    api_key=settings.PROVIDER_API_KEY,
    provider=settings.PROVIDER,
)
