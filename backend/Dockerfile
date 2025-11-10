# Image officielle uv avec Python inclus
FROM ghcr.io/astral-sh/uv:python3.11-bookworm

WORKDIR /app

# Pour le healthcheck (facultatif mais pratique)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copie d'abord les fichiers de lock pour profiter du cache Docker
COPY pyproject.toml uv.lock ./

# Installe les dépendances dans un venv local (.venv) en mode figé
RUN uv sync --frozen --no-dev

# Puis ton code
COPY app ./app

# Expose l’API
EXPOSE 8000

# Démarre via uv (qui active le venv .venv pour toi)
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
