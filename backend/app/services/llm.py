from __future__ import annotations
from typing import Dict, Any, Optional
import httpx
from ..core.settings import settings


class LLMClient:
    def __init__(self, base_url: str, api_key: str):
        # Exemple : base_url = "https://api.openai.com/v1"
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        if not self.api_key:
            raise RuntimeError("PROVIDER_API_KEY / OPENAI_API_KEY is missing or empty")

    async def ask(self, question: str, personality: Optional[str] = None) -> str:
        """
        Tu lui passes une question (string) et éventuellement une description de personnalité,
        il te renvoie une réponse construite en tenant compte de cette personnalité.
        """
        url = f"{self.base_url}/chat/completions"

        # 1️⃣ Construire un system prompt qui intègre la personnalité
        if personality:
            system_content = (
                "Tu es un assistant IA spécialisé dans l'adaptation de tes réponses selon le profil psychologique de l'utilisateur. "
                "Tu DOIS IMPÉRATIVEMENT respecter et incarner la personnalité décrite ci-dessous dans CHAQUE aspect de ta réponse.\n\n"
                
                "PROFIL DE PERSONNALITÉ DE L'UTILISATEUR :\n"
                f"{personality}\n\n"
                
                "INSTRUCTIONS STRICTES :\n"
                "1. ADAPTE ton vocabulaire, ton niveau de détail et ta structure de réponse selon ce profil\n"
                "2. UTILISE des exemples, métaphores et références qui résonnent avec cette personnalité\n"
                "3. AJUSTE ton ton émotionnel (chaleureux, analytique, direct, encourageant...) selon le profil\n"
                "4. STRUCTURE tes réponses selon les préférences cognitives du profil (concret vs abstrait, visuel vs verbal, etc.)\n"
                "5. ANTICIPE les besoins implicites liés à cette personnalité\n\n"
                
                "Ta réponse doit donner l'impression d'avoir été écrite PAR quelqu'un partageant cette personnalité "
                "ou POUR quelqu'un avec cette personnalité. Sois authentique, cohérent et bienveillant."
            )        
        else:
            system_content = (
                "Tu es un assistant IA utile. "
                "Tu réponds en français, de manière claire, concrète et bienveillante."
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: Dict[str, Any] = {
            "model": "gpt-4o-mini",  # adapte si besoin
            "temperature": 0.5,
            "messages": [
                {
                    "role": "system",
                    "content": system_content,
                },
                {
                    "role": "user",
                    "content": (
                        "Question de l'utilisateur : "
                        f"{question}"
                    ),
                },
            ],
        }

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]


llm_client = LLMClient(
    base_url=settings.PROVIDER_BASE_URL,
    api_key=settings.PROVIDER_API_KEY,
)
