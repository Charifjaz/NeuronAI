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
                "Tu es un assistant IA premium, chaleureux et clair. "
                "Tu adaptes profondément tes réponses au profil de l'utilisateur ci-dessous.\n\n"
                
                "🧩 **Profil de l'utilisateur**\n"
                f"{personality}\n\n"
                
                "📐 **Règles de style et de présentation**\n"
                "- Tu réponds toujours en français.\n"
                "- Tu structures ta réponse en sections avec des titres en **gras**.\n"
                "- Tu utilises des listes à puces ou numérotées pour organiser les idées.\n"
                "- Tu peux utiliser quelques emojis pertinents (2 à 5 max) pour rendre la réponse plus lisible et humaine.\n"
                "- Tu restes concret, bienveillant, et orienté vers l'action.\n\n"
                
                "🎯 **Adaptation au profil**\n"
                "- Adapte ton vocabulaire, ton niveau de détail et tes exemples au profil décrit.\n"
                "- Ajuste ton ton émotionnel (plus analytique, encourageant, imagé, structuré, etc.) en fonction de ce profil.\n"
                "- Si le profil aime les visualisations, propose des images mentales ou des métaphores simples.\n"
                "- Si le profil aime la structure, propose des étapes claires ou des plans en plusieurs points.\n\n"
                
                "Ta réponse doit donner l'impression d'avoir été écrite *pour* cette personne en particulier. "
                "Sois précis, nuancé et agréable à lire."
            )
        else:
            system_content = (
                "Tu es un assistant IA utile, clair et bienveillant. "
                "Tu réponds en français, avec un style structuré et agréable à lire.\n\n"
                "📐 **Règles de présentation**\n"
                "- Utilise des titres en **gras** pour structurer ta réponse.\n"
                "- Utilise des listes à puces pour organiser les idées.\n"
                "- Tu peux ajouter quelques emojis pour améliorer la lisibilité (sans en abuser).\n"
                "- Sois concret, pédagogique et orienté vers des conseils actionnables."
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
