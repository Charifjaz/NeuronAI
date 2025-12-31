from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.database.models import UserProfile


def save_user_profile(user_id: str, personality: str, db : Session) -> None:
    """
    Crée ou met à jour un profil utilisateur.
    """
    # On cherche si un profil existe déjà pour cet user_id
    stmt = select(UserProfile).where(UserProfile.user_id == user_id)
    result = db.execute(stmt)
    user_profile = result.scalar_one_or_none()

    if user_profile is None:
        # Pas de profil : on en crée un
        user_profile = UserProfile(
            user_id=user_id,
            personality=personality,
        )
        db.add(user_profile)
    else:
        # Profil existe : on le met à jour
        user_profile.personality = personality

    # Validation (commit) des changements en base
    db.commit()


def get_user_profile(user_id: str, db : Session) -> Optional[UserProfile]:
    """
    Récupère le profil de personnalité associé à ce user_id, s'il existe.
    Retourne le texte de personnalité ou None.
    """
    stmt = select(UserProfile).where(UserProfile.user_id == user_id)  # Select l'objet complet
    result = db.execute(stmt)
    user_profile = result.scalar_one_or_none()  # Récupère l'objet UserProfile
    return user_profile  # Retourne l'objet complet

def list_user_ids(db : Session) -> List[str]:
    """
    Renvoie la liste de tous les user_id pour lesquels un profil existe.
    """
    stmt = select(UserProfile.user_id)
    result = db.execute(stmt)
    user_ids = [row[0] for row in result.all()]
    return user_ids
