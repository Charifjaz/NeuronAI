# 🧠 Neural Chat Interface - React

Application React moderne remplaçant l'interface Streamlit pour une expérience conversationnelle avec profil contextuel.

## ✨ Fonctionnalités

- 💬 **Chat Interface** : Interface de conversation fluide et réactive
- 🎯 **Profil Contextuel** : Gestion de questionnaires dynamiques
- 🎨 **Design Futuriste** : Style moderne avec animations et effets visuels
- 🔄 **API Integration** : Communication avec le backend via REST API
- 📱 **Responsive** : Optimisé pour tous les écrans

## 📁 Structure du Projet

```
neural-chat-interface/
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx    # Interface de chat
│   │   ├── ProfilePanel.jsx     # Panneau de profil
│   │   ├── Message.jsx          # Composant message
│   │   └── Header.jsx           # En-tête
│   ├── services/
│   │   └── api.js               # Services API
│   ├── styles/
│   │   └── App.css              # Styles globaux
│   ├── App.jsx                  # Composant principal
│   └── main.jsx                 # Point d'entrée
├── index.html
├── vite.config.js
└── package.json
```

## 🚀 Installation

### Prérequis

- Node.js 18+ et npm/yarn
- Backend API fonctionnel (port 8000 par défaut)

### Étapes

1. **Créer la structure du projet**

```bash
# Créer le dossier du projet
mkdir neural-chat-interface
cd neural-chat-interface

# Créer la structure des dossiers
mkdir -p src/components src/services src/styles
```

2. **Copier les fichiers**

Copiez tous les fichiers fournis dans les dossiers appropriés :

```
- App.jsx → src/
- main.jsx → src/
- Header.jsx → src/components/
- ChatInterface.jsx → src/components/
- ProfilePanel.jsx → src/components/
- Message.jsx → src/components/
- api.js → src/services/
- App.css → src/styles/
- index.html → racine du projet
- package.json → racine du projet
- vite.config.js → racine du projet
```

3. **Installer les dépendances**

```bash
npm install
```

4. **Configuration de l'API**

Créez un fichier `.env` à la racine :

```bash
cp .env.example .env
```

Modifiez `.env` si nécessaire :

```env
VITE_API_BASE_URL=http://localhost:8000
```

5. **Lancer l'application**

```bash
# Mode développement
npm run dev

# Build production
npm run build

# Prévisualiser le build
npm run preview
```

L'application sera accessible sur `http://localhost:3000`

## 🔧 Configuration

### Variables d'environnement

- `VITE_API_BASE_URL` : URL de base de votre API backend (défaut : `http://localhost:8000`)

### API Endpoints requis

Votre backend doit exposer les endpoints suivants :

#### GET `/questions`

Retourne la liste des questions du profil utilisateur.

**Réponse :**
```json
[
  {
    "id": "context",
    "type": "textarea",
    "label": "Contexte du projet",
    "placeholder": "Décrivez brièvement...",
    "default": ""
  },
  {
    "id": "priority",
    "type": "slider",
    "label": "Niveau de priorité",
    "scale_min": 0,
    "scale_max": 10,
    "default": 5
  }
]
```

**Types de questions supportés :**
- `text` : Champ texte simple
- `textarea` : Zone de texte multiligne
- `slider` : Curseur numérique (avec `scale_min` et `scale_max`)

#### POST `/ask`

Envoie un message avec le contexte utilisateur.

**Requête :**
```json
{
  "message": "Votre message ici",
  "answers": {
    "context": "Développement d'une app mobile",
    "priority": 8
  }
}
```

**Réponse :**
```json
{
  "reply": "Réponse de l'assistant..."
}
```

## 🎨 Personnalisation

### Styles

Le fichier `src/styles/App.css` contient tous les styles. Vous pouvez personnaliser :

- **Couleurs** : Modifier les gradients et couleurs primaires
- **Animations** : Ajuster les durées et effets
- **Layout** : Changer les proportions des colonnes (`.layout-grid`)

### Composants

Chaque composant est indépendant et peut être modifié :

- **ChatInterface** : Logique du chat et affichage des messages
- **ProfilePanel** : Gestion du formulaire de profil
- **Message** : Apparence des messages
- **Header** : En-tête et configuration

## 📊 Différences avec Streamlit

| Aspect | Streamlit | React |
|--------|-----------|-------|
| **Performance** | Rechargement complet | Mise à jour réactive |
| **Personnalisation** | Limitée | Totale |
| **Déploiement** | Serveur Python requis | Build statique |
| **Scalabilité** | Moyenne | Excellente |
| **Expérience utilisateur** | Basique | Moderne et fluide |

## 🐛 Dépannage

### Le chat ne charge pas

- Vérifiez que le backend est démarré sur le bon port
- Contrôlez la console browser (F12) pour les erreurs réseau
- Vérifiez la variable `VITE_API_BASE_URL` dans `.env`

### Les styles ne s'appliquent pas

- Assurez-vous que `App.css` est bien importé dans `App.jsx`
- Vérifiez que la police Inter est chargée (connexion internet requise)
- Videz le cache du navigateur

### Erreurs CORS

Si vous avez des erreurs CORS, configurez votre backend pour accepter les requêtes depuis `http://localhost:3000` :

```python
# Exemple FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🚢 Déploiement

### Build Production

```bash
npm run build
```

Le dossier `dist/` contiendra les fichiers statiques prêts pour le déploiement.

### Déploiement sur Vercel

```bash
npm install -g vercel
vercel
```

### Déploiement sur Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Déploiement sur serveur statique

Copiez le contenu du dossier `dist/` sur votre serveur web (Nginx, Apache, etc.).

## 📝 License

MIT

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📧 Support

Pour toute question ou problème, ouvrez une issue sur le repository.

---

**Profitez de votre nouvelle interface Neural Chat ! 🎉**
