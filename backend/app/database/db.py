# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 1) URL de connexion à la base
# Exemple pour PostgreSQL :
# postgresql://<user>:<password>@<host>:<port>/<database>
# DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://neuronai:neuronai@db:5432/neuronai",  # valeur par défaut à modifier apres et mieux comprendre
)

# 2) Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False, future=True)
# - echo=False : ne pas logguer toutes les requêtes SQL (tu peux mettre True en dev)
# - future=True : active la nouvelle API SQLAlchemy 2.x

# 3) Factory de session : chaque requête utilisera une session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)

# 4) Classe de base pour tous nos modèles
Base = declarative_base()
