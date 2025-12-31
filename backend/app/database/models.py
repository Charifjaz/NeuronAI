# app/models.py
from sqlalchemy import Column, String, Text
from app.database.db import Base

class UserProfile(Base):
    """
    Représente la table user_profiles en base.
    Chaque ligne = le profil d'un utilisateur.
    """
    __tablename__ = "user_profiles"

    # user_id sera la clé primaire (PK)
    user_id = Column(String, primary_key=True, index=True)

    # personality : le texte de personnalité que tu stockais dans ton dict
    personality = Column(Text, nullable=False)


# Remarque :
# ce qu'on vient de définit est equivalent de :
# CREATE TABLE user_profiles (
#     user_id VARCHAR PRIMARY KEY,
#     personality TEXT NOT NULL
# );
