
# 🌐 Comprendre les méthodes HTTP : GET vs POST

Ce document t’explique la différence entre **GET** et **POST**, leurs rôles dans une API web, et leur utilisation concrète dans **FastAPI**.  
Il inclut des schémas pour bien visualiser le flux entre le client (Streamlit, navigateur, Postman) et ton backend.

---

## 🧠 1. Le contexte : le protocole HTTP

Les APIs (comme celle de **NeuronAI**) fonctionnent avec le protocole **HTTP**, utilisé partout sur le Web.  
Chaque requête envoyée à ton backend contient :
- une **méthode** (GET, POST, PUT, DELETE...),
- une **URL** (ex: `/questions`),
- parfois un **corps (body)** avec des données JSON.

Ces méthodes indiquent **ce que le client veut faire** : lire, créer, modifier, supprimer, etc.

---

## ⚙️ 2. La méthode GET — Lire ou récupérer des données

### 🔹 Objectif
> Récupérer des informations sans modifier l’état du serveur.

### 🧩 Exemple concret (dans NeuronAI)
- Endpoint : `/questions`
- Action : le front Streamlit veut afficher la liste des questions.
- Méthode : `GET`

### 📦 Exemple FastAPI
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/questions")
def get_questions():
    return [
        {"id": "O1", "text": "J'aime explorer des idées nouvelles."},
        {"id": "C1", "text": "Je planifie mes tâches avec rigueur."}
    ]
```

### 🔍 Caractéristiques
| Élément | Description |
|----------|--------------|
| Type d’opération | Lecture |
| Corps de requête | Aucun |
| Paramètres | Passés dans l’URL (query params) |
| Effet sur le serveur | Aucun |
| Cachable | ✅ Oui |
| Idempotente | ✅ Oui (répéter la requête ne change rien) |

### 🧭 Schéma de fonctionnement

```
┌──────────────┐          GET /questions
│   Client     │ ───────────────────────────────▶ │   Serveur FastAPI   │
│ (Streamlit)  │                                   │   (backend)        │
└──────────────┘ ◀─────────────────────────────── │                     │
                     Liste de questions (JSON)
```

---

## 🧠 3. La méthode POST — Envoyer ou créer des données

### 🔹 Objectif
> Envoyer des données au serveur pour qu’il les traite ou crée quelque chose.

### 🧩 Exemple concret (dans NeuronAI)
- Endpoint : `/assessments`
- Action : le front Streamlit envoie les réponses du questionnaire.
- Méthode : `POST`

### 📦 Exemple FastAPI
```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AssessmentInput(BaseModel):
    answers: dict

@router.post("/assessments")
def analyze(assessment: AssessmentInput):
    summary = "Profil créatif et curieux."
    return {"summary": summary}
```

### 🔍 Caractéristiques
| Élément | Description |
|----------|--------------|
| Type d’opération | Création / soumission |
| Corps de requête | Oui (JSON, FormData, etc.) |
| Effet sur le serveur | Oui (modifie l’état ou crée une ressource) |
| Cachable | ❌ Non |
| Idempotente | ❌ Non (chaque appel peut produire un résultat différent) |

### 🧭 Schéma de fonctionnement

```
┌──────────────┐        POST /assessments
│   Client     │ ───────────────────────────────▶ │   Serveur FastAPI   │
│ (Streamlit)  │                                   │   (backend)        │
│              │   answers = {...} (JSON body)     │                    │
└──────────────┘ ◀─────────────────────────────── │                     │
                     Résumé du profil (JSON)
```

---

## 🧩 4. Comparatif GET vs POST

| Critère | **GET** | **POST** |
|----------|----------|----------|
| Objectif | Lire des données | Envoyer ou créer des données |
| Données envoyées | Dans l’URL | Dans le corps (body) |
| Modifie le serveur ? | ❌ Non | ✅ Oui |
| Peut être mis en cache ? | ✅ Oui | ❌ Non |
| Idempotent ? | ✅ Oui | ❌ Non |
| Exemple NeuronAI | `/questions` | `/assessments` |

---

## 🚀 5. Utilisation dans FastAPI (exemples réels du backend NeuronAI)

### 📄 `/health` — GET
```python
@router.get("/health")
def health():
    return {"status": "ok"}
```
➡️ Vérifie que le backend tourne.

---

### 📄 `/questions` — GET
```python
@router.get("/questions")
def get_questions():
    return questions_list
```
➡️ Récupère le questionnaire.

---

### 📄 `/assessments` — POST
```python
@router.post("/assessments")
async def create_assessment(payload: AssessmentInput):
    summary = await llm_client.analyze_answers(payload.answers)
    return {"summary": summary}
```
➡️ Reçoit les réponses du front, appelle le modèle IA, renvoie le profil.

---

## 🧱 6. Schéma global d’interaction

```
               ┌────────────────────────────┐
               │       FRONT (Streamlit)    │
               └──────────────┬─────────────┘
                              │
                              │
                ┌─────────────┴──────────────┐
                │       BACKEND (FastAPI)    │
                └─────────────┬──────────────┘
                              │
                              │
             ┌────────────────┴────────────────┐
             │          Service LLM            │
             └─────────────────────────────────┘
```

### Exemple de flux complet :

1️⃣ `GET /questions` → le front récupère les questions.  
2️⃣ L’utilisateur remplit le questionnaire.  
3️⃣ `POST /assessments` → le front envoie les réponses.  
4️⃣ Le backend appelle le modèle IA → calcule le profil.  
5️⃣ Réponse JSON : résumé de personnalité.

---

## 🧭 7. Bonnes pratiques

✅ **Toujours utiliser GET pour la lecture seule.**  
✅ **Toujours utiliser POST pour les créations, calculs ou traitements.**  
✅ **Éviter de transmettre des données sensibles dans les URL (GET).**  
✅ **Documenter les endpoints dans `/docs` (Swagger auto-généré).**  
✅ **Utiliser Pydantic pour valider le corps des requêtes POST.**

---

## 💬 8. En résumé

| Cas d’usage | Méthode | Exemple |
|--------------|----------|----------|
| Lire la santé du backend | GET | `/health` |
| Récupérer les questions | GET | `/questions` |
| Soumettre des réponses | POST | `/assessments` |

---

## 🧠 9. À retenir

> - **GET = lecture (rien ne change)**  
> - **POST = action (quelque chose change)**  
> - Ces deux méthodes sont la base de la communication entre ton **frontend (Streamlit)** et ton **backend (FastAPI)**.

---

📘 **Ressources complémentaires :**
- [Documentation FastAPI - Request Methods](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#methods)
- [MDN Web Docs - HTTP Methods](https://developer.mozilla.org/fr/docs/Web/HTTP/Methods)
