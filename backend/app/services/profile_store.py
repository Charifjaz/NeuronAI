# app/services/profile_store.py
from typing import Dict, Optional

# Simple stockage en mémoire : user_id -> personality_text
_USER_PROFILES: Dict[str, str] = {}


def save_user_profile(user_id: str, personality: str) -> None:
    """
    Enregistre ou met à jour le profil de personnalité pour un user_id donné.
    """
    _USER_PROFILES[user_id] = personality


def get_user_profile(user_id: str) -> Optional[str]:
    """
    Récupère le profil de personnalité associé à ce user_id, s'il existe.
    """
    return _USER_PROFILES.get(user_id)

def list_user_ids() -> list[str]:
    """
    Renvoie la liste de tous les user_id pour lesquels un profil existe.
    """
    return list(_USER_PROFILES.keys())