
# Comprendre FastAPI, Uvicorn et Pydantic 🧠

## 1. FastAPI — Le moteur du backend

**FastAPI** est un framework Python moderne et ultra-rapide pour créer des **API Web**.  
Il repose sur deux piliers :
- **Starlette** pour la partie réseau (asynchrone et HTTP).
- **Pydantic** pour la validation et la structuration des données.

### ✅ Points forts
- **Rapide** : proche des performances de Node.js ou Go.
- **Automatique** : documentation Swagger & ReDoc intégrée.
- **Fiable** : validation automatique des données entrantes/sortantes.
- **Asynchrone** : gère plusieurs requêtes simultanément sans blocage.

### ⚙️ Exemple minimal

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bienvenue sur NeuronAI API 🚀"}
```

- `/` → endpoint principal.
- `@app.get()` → déclare une route HTTP (GET).
- `FastAPI()` → crée ton application API.

### 🌐 Documentation intégrée
Une fois ton app lancée avec Uvicorn :
- `http://127.0.0.1:8000/docs` → interface Swagger
- `http://127.0.0.1:8000/redoc` → documentation ReDoc
- `http://127.0.0.1:8000/openapi.json` → schéma OpenAPI

---

## 2. Uvicorn — Le serveur qui fait tourner FastAPI ⚙️

**Uvicorn** est un serveur **ASGI** (*Asynchronous Server Gateway Interface*).  
C’est lui qui écoute les requêtes HTTP et les transmet à FastAPI.

### 🔹 Rôle
- Écouter sur un port (ex: `8000`).
- Recevoir les requêtes HTTP.
- Appeler ton code Python (FastAPI).
- Renvoyer la réponse au navigateur.

### 🔹 Commande typique

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- `app.main` → module Python contenant ton app.
- `app` → instance FastAPI.
- `--reload` → redémarrage auto quand tu modifies le code.

### 🔹 Pourquoi ASGI ?
ASGI est la version moderne de WSGI (Flask, Django).  
Elle permet :
- Le **mode asynchrone (`async/await`)**.
- Le support des **WebSockets**.
- Une **haute performance**.

### 🔹 Schéma général

```
Navigateur → Uvicorn (serveur ASGI) → FastAPI (routes, logique) → Pydantic (validation)
```

---

## 3. Pydantic — Le validateur intelligent 🧩

**Pydantic** est la bibliothèque utilisée par FastAPI pour **valider et structurer les données**.  
Elle repose sur les annotations de type Python (`str`, `int`, `float`, etc.)

### 🔹 Exemple simple

```python
from pydantic import BaseModel

class Utilisateur(BaseModel):
    nom: str
    age: int

u = Utilisateur(nom="Charif", age=30)
print(u)
# ✅ Utilisateur(nom='Charif', age=30)
```

Si on envoie des données invalides :
```python
Utilisateur(nom="Charif", age="trente")
```
➡️ Pydantic renvoie une erreur claire :
```
ValidationError: value is not a valid integer
```

### 🔹 Utilisation dans FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Personne(BaseModel):
    nom: str
    age: int

@app.post("/users")
def creer_user(personne: Personne):
    return {"message": f"Utilisateur {personne.nom} créé"}
```

FastAPI valide automatiquement le corps JSON reçu avant d’appeler ta fonction.  
Si un champ manque ou est invalide, une erreur 422 est renvoyée automatiquement.

---

## 4. Résumé global 🧩

| Élément | Rôle | Exemple |
|----------|------|----------|
| **FastAPI** | Framework pour créer les routes et la logique API | `/questions`, `/assessments` |
| **Uvicorn** | Serveur ASGI qui exécute l’app et gère le trafic HTTP | `uvicorn app.main:app --reload` |
| **Pydantic** | Validation et typage des données | `class AssessmentInput(BaseModel)` |

---

## 5. Schéma visuel

```
Navigateur
   ↓
[ Uvicorn ]
   ↓
[ FastAPI ]
   ↓
[ Pydantic ]
   ↓
Réponse JSON
```

---

## 6. Pour aller plus loin

- 🔗 [Documentation FastAPI](https://fastapi.tiangolo.com/)
- 🔗 [Documentation Pydantic](https://docs.pydantic.dev/)
- 🔗 [Uvicorn sur GitHub](https://github.com/encode/uvicorn)

---

> 🚀 **En résumé :**
> - **FastAPI** = le cerveau (logique API)
> - **Uvicorn** = le moteur (serveur ASGI)
> - **Pydantic** = le gardien des données (validation automatique)
