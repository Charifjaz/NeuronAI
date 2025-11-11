
# ⚙️ NeuronAI - Gestion des variables d’environnement

Ce document explique comment **les variables d’environnement** sont gérées dans le backend du projet **NeuronAI**, et comment fonctionnent les fichiers `.env.template` et `core/settings.py`.

---

## 🧠 1. Objectif des variables d’environnement

Les variables d’environnement servent à **configurer ton application sans modifier le code**.  
Elles permettent de stocker des informations comme :
- les clés API (OpenAI, HuggingFace, etc.),
- les URL d’accès à des services externes,
- les paramètres de debug,
- les secrets.

> ✅ Cela rend ton code plus sûr, portable et maintenable.

---

## 🗂️ 2. Fichiers impliqués

```
backend/
├── .env.template     ← modèle de configuration
├── .env              ← fichier réel (non commité)
└── app/core/settings.py  ← code Python qui charge ces variables
```

---

## 🧩 3. `.env.template` — le modèle de configuration

C’est un **fichier d’exemple** qui indique quelles variables doivent être définies.  
Il ne contient **aucune donnée sensible**.

### Exemple :
```env
# .env.template
PROVIDER=OPENAI
PROVIDER_BASE_URL=https://api.openai.com/v1
PROVIDER_API_KEY=sk-...
DEBUG=true
```

### 🎯 Rôle :
- Sert de **documentation** pour les développeurs.
- Permet de savoir quelles variables sont nécessaires.
- Peut être versionné sans danger (commit dans Git).

### 💡 Utilisation :
Avant de démarrer le projet, chaque développeur fait :
```bash
cp .env.template .env
```
Puis il remplit **les vraies valeurs** dans `.env` :
```env
# .env (local)
PROVIDER=OPENAI
PROVIDER_BASE_URL=https://api.openai.com/v1
PROVIDER_API_KEY=sk-real-key-123456
DEBUG=true
```

> ⚠️ Le fichier `.env` **ne doit jamais être commité** (ajouté dans `.gitignore`).

---

## 🧠 4. `core/settings.py` — le cerveau de la configuration

Ce module Python utilise **Pydantic Settings** pour :
1. Lire les valeurs du fichier `.env` (ou des variables système),
2. Les convertir dans les bons types (`bool`, `int`, `str`, etc.),
3. Fournir un accès simple et sûr dans tout ton code.

### Exemple :
```python
# app/core/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "NeuronAI"
    DEBUG: bool = True
    PROVIDER: str = "OPENAI"
    PROVIDER_BASE_URL: str
    PROVIDER_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

### 🔍 Ce que fait ce code :
- Il lit automatiquement `.env` (grâce à la config Pydantic).
- Il valide chaque variable selon son type.
- Il applique des valeurs par défaut si certaines variables manquent.
- Il expose un objet global `settings` utilisable partout.

---

## 🧰 5. Exemple d’utilisation dans le backend

### Dans `services/llm.py` :
```python
from ..core.settings import settings

print(settings.PROVIDER_BASE_URL)
# → https://api.openai.com/v1
```

Tu peux aussi conditionner le comportement :
```python
if settings.DEBUG:
    print("Mode développement activé")
```

---

## 🔒 6. Pourquoi séparer `.env.template` et `settings.py` ?

| Élément | Rôle | Contenu | Partage |
|----------|------|----------|----------|
| `.env.template` | Modèle des variables | Noms de variables, valeurs d’exemple | ✅ Oui (dans Git) |
| `.env` | Configuration réelle | Clés et secrets réels | ❌ Non (privé) |
| `core/settings.py` | Lecture et validation | Code Python (structure et types) | ✅ Oui (dans Git) |

---

## 🔁 7. Schéma du flux complet

```
                (exemple partagé)
                ┌───────────────────────────────┐
                │         .env.template          │
                └───────────────────────────────┘
                               │
                               │ (copie et remplissage)
                               ▼
                ┌───────────────────────────────┐
                │             .env              │
                │  (valeurs réelles + clés API) │
                └───────────────────────────────┘
                               │
                               │ (lu par Pydantic)
                               ▼
                ┌───────────────────────────────┐
                │     core/settings.py          │
                │ → crée l’objet `settings`     │
                └───────────────────────────────┘
                               │
                               │ (importé dans ton code)
                               ▼
                ┌───────────────────────────────┐
                │    services/llm.py, routers   │
                │    utilisent `settings`       │
                └───────────────────────────────┘
```

---

## 🧠 8. Bonnes pratiques

1. ✅ Toujours garder `.env.template` à jour quand tu ajoutes une variable.
2. ❌ Ne jamais commiter `.env` (ajoute-le dans `.gitignore`).
3. ✅ Donne des **valeurs par défaut sûres** dans `settings.py`.
4. ✅ Utilise `settings.DEBUG` pour différencier les environnements (dev/prod).
5. ✅ Centralise toutes les configs dans `core/settings.py` (pas de `os.getenv()` éparpillés).

---

## 🧩 9. Exemple concret d’évolution

Tu veux ajouter une variable pour contrôler le modèle IA :

### Étape 1 — Ajouter dans `.env.template` :
```env
MODEL_NAME=gpt-4o-mini
```

### Étape 2 — Définir dans `.env` :
```env
MODEL_NAME=gpt-4o-mini
```

### Étape 3 — Ajouter dans `core/settings.py` :
```python
class Settings(BaseSettings):
    MODEL_NAME: str = "gpt-4o-mini"
```

### Étape 4 — Utiliser dans ton service :
```python
from ..core.settings import settings

print(f"Modèle IA utilisé : {settings.MODEL_NAME}")
```

---

## 🚀 10. En résumé

| Étape | Action | Fichier concerné |
|--------|---------|------------------|
| 1️⃣ | Définir les variables nécessaires | `.env.template` |
| 2️⃣ | Remplir les valeurs réelles | `.env` |
| 3️⃣ | Lire et valider dans Python | `core/settings.py` |
| 4️⃣ | Utiliser les valeurs dans ton code | `services`, `routers`, etc. |

> 💬 **En clair :**
> - `.env.template` = ce qu’il faut configurer.  
> - `.env` = tes vraies données locales.  
> - `settings.py` = la couche qui relie les deux et valide tout.

---

> 🧠 **Astuce pro :**  
> Si tu déploies ton app sur un serveur (Docker, Cloud), tu peux **ne pas utiliser `.env`** du tout et simplement définir les variables d’environnement directement dans le système — `settings.py` les détectera automatiquement !
