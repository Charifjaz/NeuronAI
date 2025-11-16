# 📁 Structure Complète du Projet React

## Vue d'ensemble

Cette structure remplace complètement votre application Streamlit avec une architecture React moderne et organisée.

```
neural-chat-interface/
│
├── 📄 index.html                    # Point d'entrée HTML
├── 📄 package.json                  # Dépendances et scripts
├── 📄 vite.config.js               # Configuration Vite
├── 📄 .env.example                 # Exemple de configuration
├── 📄 .env                         # Configuration (à créer)
├── 📄 .gitignore                   # Fichiers à ignorer par Git
├── 📄 README.md                    # Documentation principale
├── 📄 MIGRATION_GUIDE.md          # Guide de migration
├── 📄 test-api.js                  # Tests API
├── 📄 migrate.sh                   # Script migration (Linux/Mac)
├── 📄 start.ps1                    # Script démarrage (Windows)
│
├── 📂 src/                         # Code source
│   │
│   ├── 📄 main.jsx                 # Point d'entrée React
│   ├── 📄 App.jsx                  # Composant racine
│   │
│   ├── 📂 components/              # Composants React
│   │   ├── 📄 Header.jsx           # En-tête avec config
│   │   ├── 📄 ChatInterface.jsx    # Interface de chat
│   │   ├── 📄 ProfilePanel.jsx     # Panneau profil/questions
│   │   └── 📄 Message.jsx          # Composant message individuel
│   │
│   ├── 📂 services/                # Logique métier
│   │   └── 📄 api.js               # Appels API backend
│   │
│   └── 📂 styles/                  # Styles
│       └── 📄 App.css              # Styles globaux futuristes
│
├── 📂 dist/                        # Build production (généré)
└── 📂 node_modules/                # Dépendances (généré)
```

## 📋 Description Détaillée des Fichiers

### 🌐 Racine du Projet

#### `index.html`
Point d'entrée de l'application. Charge le JavaScript React.
```html
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <title>Neural Chat Interface</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

#### `package.json`
Définit les dépendances et scripts npm.
- **Scripts disponibles:**
  - `npm run dev` → Mode développement
  - `npm run build` → Build production
  - `npm run preview` → Prévisualiser le build

#### `vite.config.js`
Configuration du bundler Vite.
- Port : 3000
- Auto-ouverture du navigateur

#### `.env` (à créer)
Variables d'environnement.
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 📦 Dossier `src/`

#### `main.jsx`
Bootstrap de l'application React. Monte le composant `App` dans le DOM.

#### `App.jsx` ⭐ PRINCIPAL
Composant racine qui:
- Gère l'état global (messages, profil, validation)
- Charge les questions depuis l'API
- Coordonne les sous-composants
- Gère la logique d'envoi de messages

**État géré:**
```jsx
const [apiBase, setApiBase] = useState('...');
const [questions, setQuestions] = useState(null);
const [answersDraft, setAnswersDraft] = useState({});
const [answersValidated, setAnswersValidated] = useState({});
const [isValidated, setIsValidated] = useState(false);
const [messages, setMessages] = useState([]);
const [isLoading, setIsLoading] = useState(false);
```

### 🧩 Dossier `src/components/`

#### `Header.jsx`
En-tête de l'application avec:
- Titre et sous-titre animés
- Bouton de configuration (⚙️)
- Panel de configuration (URL API, statut)

**Props:**
- `apiBase`: URL de l'API
- `setApiBase`: Fonction pour modifier l'URL
- `isValidated`: Statut du profil

#### `ChatInterface.jsx`
Interface de conversation principale:
- Zone de messages scrollable
- Indicateur de frappe (typing indicator)
- Champ de saisie avec textarea auto-resize
- Bouton d'envoi
- Auto-scroll vers le bas

**Props:**
- `messages`: Array des messages
- `isValidated`: Si le chat est actif
- `isLoading`: Si une réponse est en cours
- `onSendMessage`: Callback pour envoyer un message

#### `ProfilePanel.jsx`
Panneau de gestion du profil utilisateur:
- Affichage des questions dynamiques
- Formulaire d'édition
- Vue validée (read-only)
- Aperçu du prompt
- Gestion des types de questions (text, textarea, slider)

**Props:**
- `questions`: Array des questions
- `answersDraft`: Réponses en brouillon
- `answersValidated`: Réponses validées
- `isValidated`: Mode (édition/lecture)
- `onAnswerChange`: Callback modification
- `onValidateProfile`: Callback validation
- `onEditProfile`: Callback édition

#### `Message.jsx`
Composant simple pour afficher un message:
- Avatar (🧑 ou 🤖)
- Contenu du message
- Style différent user/assistant

**Props:**
- `role`: 'user' ou 'assistant'
- `content`: Texte du message

### 🔧 Dossier `src/services/`

#### `api.js`
Service pour les appels API:

**Fonctions:**
```javascript
// Récupère les questions
fetchQuestions(apiBase) → Promise<Array>

// Envoie un message avec contexte
sendMessage(apiBase, message, answers) → Promise<string>

// Construit le prompt avec profil
buildPrompt(userMessage, answers) → string
```

### 🎨 Dossier `src/styles/`

#### `App.css`
Styles complets de l'application:
- Design futuriste violet/bleu
- Animations et transitions
- Layout responsive
- Effets visuels (glow, shine)
- Dark theme
- Police Inter

**Sections principales:**
1. Global styles
2. Header
3. Main layout
4. Chat interface
5. Profile panel
6. Buttons
7. Utilities
8. Footer
9. Responsive

## 🔄 Flux de Données

```
┌─────────────────────────────────────────────┐
│              App.jsx (État Global)          │
│  ┌──────────────────────────────────────┐  │
│  │ • apiBase                             │  │
│  │ • questions ←─────────┐              │  │
│  │ • answersDraft        │              │  │
│  │ • answersValidated    │              │  │
│  │ • isValidated         │              │  │
│  │ • messages            │              │  │
│  └──────────────────────┼───────────────┘  │
│                          │                   │
│         ┌────────────────┴─────────┐        │
│         │                          │        │
│    ┌────▼────┐               ┌────▼────┐   │
│    │ Header  │               │  Chat   │   │
│    └─────────┘               └────┬────┘   │
│                                   │        │
│                              ┌────▼────┐   │
│                              │ Message │   │
│                              └─────────┘   │
│                                            │
│                              ┌─────────┐   │
│                              │ Profile │   │
│                              │  Panel  │   │
│                              └─────────┘   │
└─────────────────────────────────────────────┘
                    │
                    ▼
           ┌────────────────┐
           │   api.js       │
           │  • fetchQuestions│
           │  • sendMessage  │
           └────────┬────────┘
                    │
                    ▼
           ┌────────────────┐
           │  Backend API   │
           │ • GET /questions│
           │ • POST /ask     │
           └────────────────┘
```

## 📊 Comparaison avec Streamlit

| Fichier React | Équivalent Streamlit |
|---------------|---------------------|
| `App.jsx` | Script principal `.py` |
| `ChatInterface.jsx` | `st.chat_message()` |
| `ProfilePanel.jsx` | `st.form()` + widgets |
| `api.js` | `httpx.post()` / `requests` |
| `App.css` | `st.markdown("<style>")` |
| `useState()` | `st.session_state` |

## 🚀 Commandes Utiles

```bash
# Installation
npm install

# Développement
npm run dev

# Build production
npm run build

# Test de l'API
node test-api.js

# Migration (Linux/Mac)
chmod +x migrate.sh
./migrate.sh

# Migration (Windows)
powershell -ExecutionPolicy Bypass -File start.ps1
```

## 🔍 Points d'Attention

### État Partagé
Contrairement à Streamlit où tout est automatiquement rechargé, React nécessite une gestion explicite de l'état avec `useState()`.

### Effets de Bord
Utilisez `useEffect()` pour les chargements initiaux et les synchronisations:
```jsx
useEffect(() => {
    loadQuestions();
}, [apiBase]); // Se déclenche quand apiBase change
```

### Rendu Conditionnel
```jsx
{isValidated ? (
    <ChatInterface />
) : (
    <p>Activez votre profil</p>
)}
```

### Immutabilité
Toujours créer de nouveaux objets/arrays:
```jsx
// ❌ Mauvais
state.push(newItem);

// ✅ Bon
setState([...state, newItem]);
```

## 🎯 Prochaines Étapes

1. **Copier tous les fichiers** dans votre structure
2. **Installer les dépendances** avec `npm install`
3. **Configurer `.env`** avec votre URL d'API
4. **Tester l'API** avec `node test-api.js`
5. **Lancer en dev** avec `npm run dev`
6. **Personnaliser** les styles et composants

---

**Vous avez maintenant une structure React complète et professionnelle !** 🎉
