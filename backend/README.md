
# UV Psy Profile App

Une application **Streamlit (IHM)** + **FastAPI (Back)** pour administrer un questionnaire de personnalité,
analyser les réponses avec un modèle LLM (ChatGPT ou équivalent), et afficher un rapport.

## Démarrage rapide

### 1) Backend (FastAPI)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.template .env  # puis éditez les variables
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend (Streamlit)

Dans un autre terminal :
```bash
cd frontend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.template .env  # puis éditez BACKEND_BASE_URL si besoin
streamlit run streamlit_app.py
```

Par défaut, l'IHM consomme l'API exposée sur http://localhost:8000

## Structure

```
uv-psy-profile-app/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/settings.py
│   │   ├── services/llm.py
│   │   └── routers/
│   │       ├── health.py
│   │       ├── questions.py
│   │       └── assessments.py
│   ├── requirements.txt
│   └── .env.template
└── frontend/
    ├── streamlit_app.py
    ├── requirements.txt
    └── .env.template
```

## Notes d'archi

- **Front (Streamlit)** = rendu, navigation, collecte des réponses. Aucune clé LLM côté client.
- **Back (FastAPI)** = logique métier, prompting orchestrator, scoring, appel LLM.
- **Provider-agnostic** : `PROVIDER` peut être `OPENAI` (par défaut) ou autre; `BASE_URL` et `API_KEY` paramétrables.
- **Sécurité** : l'IHM ne manipule pas les clés. Limiter les prompts depuis l'API à un template contrôlé.
- **Évolutions** : ajouter persistance (SQLite/Postgres), auth (JWT), versioning des questionnaires, analytics.
```



## Utilisation avec `uv`

Installation de uv (Linux/macOS) :
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Ensuite :
```bash
cd backend
uv sync              # crée .venv et installe
uv run api           # lance l'API (script défini dans pyproject)
# ou: uv run uvicorn app.main:app --reload --port 8000
```
