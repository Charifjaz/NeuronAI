
# 🧠 NeuronAI - Architecture Backend (FastAPI)

Ce document explique en détail **l’architecture du backend** du projet **NeuronAI**, son organisation, et le rôle de chaque fichier et dossier.  
L’objectif est de permettre à tout développeur (ou toi-même plus tard) de comprendre clairement le fonctionnement interne du backend.

---

## 1. 📁 Arborescence du backend

```
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── settings.py
│   │   └── __init__.py
│   ├── services/
│   │   ├── llm.py
│   │   └── __init__.py
│   ├── routers/
│   │   ├── health.py
│   │   ├── questions.py
│   │   ├── assessments.py
│   │   └── __init__.py
│   └── __init__.py
├── .env.template
├── pyproject.toml
└── README.md
```

---

## 2. 🚀 app/main.py

Le **point d’entrée** de ton application FastAPI.  
C’est ici que l’application est créée, configurée, et que les différents routeurs sont inclus.

### ✨ Rôle :
- Créer l’objet `FastAPI()`.
- Ajouter le middleware **CORS** (pour permettre les appels depuis Streamlit).
- Inclure les routeurs (`health`, `questions`, `assessments`).

### 🧩 Exemple simplifié :
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import health, questions, assessments

app = FastAPI(title="NeuronAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(questions.router)
app.include_router(assessments.router)
```

### ✅ Intérêt :
Centraliser la **configuration** et le **routing global**.  
C’est le fichier que tu lances avec Uvicorn :
```bash
uv run -- python -m uvicorn app.main:app --reload --port 8000
```

---

## 3. ⚙️ app/core/settings.py

Contient toute la **configuration** de l’application (nom, mode debug, clés API, URL du modèle LLM, etc.).  
Utilise **Pydantic Settings** pour charger les variables d’environnement depuis `.env`.

### 🧩 Exemple :
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "NeuronAI API"
    DEBUG: bool = True
    PROVIDER: str = "OPENAI"
    PROVIDER_BASE_URL: str = "https://api.openai.com/v1"
    PROVIDER_API_KEY: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

### ✅ Intérêt :
- Centralise toutes les configurations sensibles.
- Facilite le changement d’environnement (local, staging, prod).
- Empêche les secrets d’être commités (grâce au `.env`).

---

## 4. 🔧 app/services/llm.py

C’est la **logique métier principale** : l’analyse des réponses et la communication avec le modèle de langage (LLM).

### 🧩 Structure :
```python
class LLMClient:
    def __init__(self, base_url, api_key, provider="OPENAI"):
        self.base_url = base_url
        self.api_key = api_key
        self.provider = provider

    async def chat(self, messages, model="gpt-4o-mini", temperature=0.3):
        # Appel à l’API du modèle
        ...

    async def analyze_answers(self, answers):
        # Calcule les traits, construit le prompt et appelle le modèle
        ...
```

### ✅ Intérêt :
- Isole toute la logique liée à l’intelligence artificielle.  
- Permet de changer de modèle (OpenAI → Mistral → interne) sans toucher aux routes.  
- Simplifie les tests unitaires (tu peux mocker `analyze_answers`).

---

## 5. 🌐 app/routers/

Les **routeurs** sont les fichiers qui définissent les **endpoints de l’API**.  
Chaque fichier correspond à un “domaine fonctionnel”.

### 📄 health.py
```python
@router.get("/health")
def health():
    return {"status": "ok"}
```
➡️ Vérifie que le backend tourne correctement.

### 📄 questions.py
```python
@router.get("/questions")
def list_questions():
    return [
        {"id": "O1", "text": "J'aime explorer des idées nouvelles.", "scale_min": 1, "scale_max": 5},
        ...
    ]
```
➡️ Sert le questionnaire au front.  
> Permet d’avoir une seule source de vérité.

### 📄 assessments.py
```python
@router.post("/assessments")
async def create_assessment(payload: AssessmentInput):
    summary = await llm_client.analyze_answers(payload.answers)
    return {"summary": summary}
```
➡️ Endpoint principal : reçoit les réponses, déclenche l’analyse IA et renvoie le profil synthétique.

### ✅ Intérêt global :
- Structure le code en “blocs métier” indépendants.
- Facilite la maintenance et les tests.
- Permet d’ajouter facilement de nouveaux domaines (ex: `auth.py`, `admin.py`).

---

## 6. ⚙️ .env.template

Un modèle de fichier `.env` que tu dupliques en `.env`.

### Exemple :
```env
PROVIDER=OPENAI
PROVIDER_BASE_URL=https://api.openai.com/v1
PROVIDER_API_KEY=sk-...
DEBUG=true
```

### ✅ Intérêt :
- Ne jamais exposer les secrets dans le code.
- Permet de configurer facilement différents environnements.

---

## 7. 📦 pyproject.toml

Définit les dépendances et la configuration du projet (pour `uv`).

### Exemple :
```toml
[project]
name = "neuronai-backend"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi==0.115.0",
    "uvicorn==0.30.6",
    "pydantic==2.9.2",
    "pydantic-settings==2.5.2",
    "python-dotenv==1.0.1",
    "httpx==0.27.2",
]
```

### ✅ Intérêt :
- Liste claire des dépendances.
- Installation rapide : `uv sync`
- Reproductibilité entre développeurs.

---

## 8. 🔄 Flux de traitement complet

```
1️⃣ Le front (Streamlit ou Postman) envoie un POST /assessments
   {
     "answers": {"O1": 4, "C1": 5, "E1": 3, "A1": 4, "N1": 2}
   }

2️⃣ FastAPI reçoit la requête → router `assessments.py`
3️⃣ Pydantic valide la structure → modèle AssessmentInput
4️⃣ llm_client.analyze_answers() calcule les traits et génère un prompt
5️⃣ Appel HTTP à l’API LLM (ex: OpenAI)
6️⃣ LLM renvoie un résumé (texte structuré)
7️⃣ FastAPI le renvoie au front sous forme JSON
```

---

## 9. 🧩 Pourquoi cette architecture est robuste

| Couche | Rôle | Avantage |
|--------|------|-----------|
| **Routers** | Endpoints (HTTP) | Code clair, facilement testable |
| **Services** | Logique métier / appels externes | Réutilisable, testable indépendamment |
| **Core** | Config & settings | Centralisation, sécurité |
| **.env** | Variables d’environnement | Sécurité, flexibilité |
| **Uvicorn** | Serveur ASGI | Performance et asynchronicité |

---

## 10. 🔮 Évolutions futures possibles

1. **Persistance (BDD)**  
   Ajouter `services/db.py` avec SQLAlchemy ou SQLite pour stocker :
   - Les réponses des utilisateurs
   - Les profils générés
   - Les historiques d’appels LLM

2. **Authentification / Autorisation**  
   - Nouveau fichier `routers/auth.py`
   - JWT Tokens ou API Keys

3. **Versioning des questionnaires**  
   - Gérer plusieurs versions des questions et mappages de traits

4. **Observabilité**  
   - Ajouter un middleware de logs
   - Mesurer le temps de réponse et le coût LLM

---

## 11. 🧠 Bonnes pratiques générales

- Toujours valider les entrées avec **Pydantic**.
- Ne jamais exposer les clés API dans le code.
- Utiliser des **routers modulaires** plutôt qu’un gros fichier unique.
- Ajouter un **middleware de logs** pour tracer les requêtes.
- Tester chaque service indépendamment.

---

## 12. 🧭 Commandes de base

```bash
# Démarrer le serveur
cd backend
uv sync
uv run -- python -m uvicorn app.main:app --reload --port 8000

# Vérifier la santé
curl http://127.0.0.1:8000/health

# Consulter la doc API
http://127.0.0.1:8000/docs
```

---

> 🚀 **Résumé final :**
> - **FastAPI** : le framework qui structure ton API.
> - **Uvicorn** : le serveur qui la fait tourner.
> - **Pydantic** : le garde-fou des données.
> - **Routers / Services / Core** : la colonne vertébrale de ton backend.
> - **NeuronAI Backend** est déjà prêt pour évoluer vers une plateforme IA modulaire et maintenable.
