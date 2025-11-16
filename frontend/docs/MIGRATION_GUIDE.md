# 🔄 Guide de Migration : Streamlit → React

## Vue d'ensemble

Ce guide vous accompagne dans la migration de votre application Streamlit vers React, en conservant toutes les fonctionnalités tout en gagnant en performance et flexibilité.

## 📊 Comparaison

### Avant (Streamlit)
```python
import streamlit as st
st.set_page_config(...)
st.markdown("# Title")
if st.button("Click"):
    # Action
```

### Après (React)
```jsx
import { useState } from 'react';
function App() {
    const [state, setState] = useState();
    return <button onClick={handleClick}>Click</button>
}
```

## 🎯 Étapes de Migration

### 1️⃣ Préparation

**a) Arrêtez votre application Streamlit**
```bash
# Ctrl+C dans le terminal où Streamlit tourne
```

**b) Sauvegardez votre configuration**
- Notez l'URL de votre API backend
- Sauvegardez vos fichiers `.env` ou `config.py`

### 2️⃣ Installation React

**a) Créez le nouveau dossier**
```bash
cd votre-projet
mkdir frontend-react
cd frontend-react
```

**b) Copiez tous les fichiers fournis**

Structure cible :
```
frontend-react/
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx
│   │   ├── ProfilePanel.jsx
│   │   ├── Message.jsx
│   │   └── Header.jsx
│   ├── services/
│   │   └── api.js
│   ├── styles/
│   │   └── App.css
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── package.json
├── vite.config.js
├── .env.example
├── .gitignore
└── README.md
```

**c) Installez les dépendances**
```bash
npm install
```

### 3️⃣ Configuration

**a) Créez votre fichier .env**
```bash
cp .env.example .env
```

**b) Éditez .env**
```env
VITE_API_BASE_URL=http://localhost:8000
```

> ⚠️ Remplacez par l'URL de votre backend si différente

### 4️⃣ Adaptation du Backend

Votre backend doit exposer les mêmes endpoints que ceux utilisés par Streamlit :

**Streamlit faisait :**
```python
# Route /questions
@app.get("/questions")
def get_questions():
    return [...]

# Route /ask
@app.post("/ask")
def ask(data: dict):
    message = data["message"]
    answers = data["answers"]
    return {"reply": "..."}
```

**Vérifiez que ces routes existent** et qu'elles retournent le bon format JSON.

### 5️⃣ Test

**a) Lancez votre backend**
```bash
# Dans le terminal du backend
python main.py
# ou
uvicorn main:app --reload
```

**b) Lancez React**
```bash
# Dans le terminal frontend
npm run dev
```

**c) Ouvrez votre navigateur**
```
http://localhost:3000
```

### 6️⃣ Vérifications

✅ **Checklist :**

- [ ] L'interface se charge correctement
- [ ] Les questions du profil s'affichent
- [ ] Le formulaire de profil fonctionne
- [ ] La validation du profil active le chat
- [ ] Les messages s'envoient et reçoivent des réponses
- [ ] Le design futuriste s'affiche correctement
- [ ] Aucune erreur dans la console (F12)

## 🔧 Résolution de Problèmes

### Problème : Erreur CORS

**Symptôme :** Messages d'erreur dans la console mentionnant CORS

**Solution :** Ajoutez les headers CORS dans votre backend

**FastAPI :**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Flask :**
```python
from flask_cors import CORS

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
```

### Problème : Les questions ne se chargent pas

**Vérifications :**

1. Backend démarré ?
```bash
curl http://localhost:8000/questions
```

2. Format JSON correct ?
```json
[
  {
    "id": "context",
    "type": "textarea",
    "label": "Contexte",
    "placeholder": "...",
    "default": ""
  }
]
```

3. Console browser (F12) → Onglet Network

### Problème : Styles cassés

**Vérifications :**

1. `App.css` est dans `src/styles/` ?
2. Import présent dans `App.jsx` ?
```jsx
import './styles/App.css';
```

3. Police Google Fonts charge ? (nécessite Internet)

### Problème : Build échoue

**Solution :**
```bash
# Nettoyez et réinstallez
rm -rf node_modules package-lock.json
npm install
```

## 📦 Migration des Données

### Sessions Streamlit → React

**Streamlit :**
```python
st.session_state["messages"] = []
```

**React :**
```jsx
const [messages, setMessages] = useState([]);
```

Les données de session Streamlit **ne sont pas transférables**. C'est normal - React utilise son propre système de state.

### Historique des Conversations

Si vous voulez conserver l'historique :

1. **Exportez depuis Streamlit** (avant migration)
```python
import json
with open('history.json', 'w') as f:
    json.dump(st.session_state.messages, f)
```

2. **Importez dans React**
```jsx
useEffect(() => {
    fetch('/history.json')
        .then(r => r.json())
        .then(data => setMessages(data));
}, []);
```

## 🚀 Déploiement

### Option 1 : Vercel (Recommandé)

```bash
npm install -g vercel
vercel login
vercel
```

### Option 2 : Netlify

```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod
```

### Option 3 : Serveur traditionnel

```bash
npm run build
# Copiez le dossier dist/ sur votre serveur
scp -r dist/* user@server:/var/www/html/
```

## 🎨 Personnalisation Post-Migration

### Changer les Couleurs

Éditez `src/styles/App.css` :

```css
/* Couleur principale */
background: linear-gradient(135deg, #VOTRE_COULEUR1, #VOTRE_COULEUR2);

/* Couleur des boutons */
.btn-primary {
    background: linear-gradient(135deg, #VOTRE_COULEUR1, #VOTRE_COULEUR2);
}
```

### Ajouter un Logo

Dans `src/components/Header.jsx` :

```jsx
<h1 className="header-title">
    <img src="/logo.png" alt="Logo" style={{height: '48px'}} />
    Neural Chat Interface
</h1>
```

### Modifier le Layout

Dans `src/styles/App.css`, changez la grille :

```css
.layout-grid {
    /* 2fr 1fr = 2/3 pour le chat, 1/3 pour le profil */
    grid-template-columns: 2fr 1fr;
    
    /* Changez en 1fr 1fr pour 50/50 */
    grid-template-columns: 1fr 1fr;
}
```

## 📈 Avantages de React vs Streamlit

| Critère | Streamlit | React |
|---------|-----------|-------|
| **Vitesse** | ⭐⭐ (rechargement complet) | ⭐⭐⭐⭐⭐ (mise à jour réactive) |
| **Personnalisation** | ⭐⭐ (limitée) | ⭐⭐⭐⭐⭐ (totale) |
| **Déploiement** | ⭐⭐⭐ (nécessite serveur Python) | ⭐⭐⭐⭐⭐ (fichiers statiques) |
| **Coût hébergement** | ⭐⭐ (serveur actif requis) | ⭐⭐⭐⭐⭐ (CDN gratuit possible) |
| **Scalabilité** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Offline** | ❌ | ✅ (avec service worker) |

## 🎓 Ressources d'Apprentissage

Si vous souhaitez personnaliser davantage :

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)

## ✅ Checklist Finale

Avant de fermer Streamlit définitivement :

- [ ] ✅ Application React fonctionne en dev
- [ ] ✅ Application React fonctionne en production
- [ ] ✅ Backend compatible avec les nouveaux appels
- [ ] ✅ Tests effectués sur différents navigateurs
- [ ] ✅ Tests sur mobile
- [ ] ✅ Documentation mise à jour
- [ ] ✅ Équipe formée sur la nouvelle stack
- [ ] ✅ Backup de l'ancienne version Streamlit

## 🎉 Félicitations !

Vous avez migré avec succès de Streamlit vers React ! 

Votre application est maintenant :
- ⚡ Plus rapide
- 🎨 Plus personnalisable
- 📱 Plus moderne
- 💰 Moins coûteuse à héberger
- 🚀 Prête à scaler

---

**Besoin d'aide ?** Consultez le README.md ou ouvrez une issue sur le repository.
