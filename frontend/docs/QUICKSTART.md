# ⚡ Quick Start - Neural Chat Interface

Guide ultra-rapide pour lancer votre application React en 5 minutes !

## 🎯 Prérequis

- ✅ Node.js 18+ installé ([télécharger](https://nodejs.org/))
- ✅ Backend API fonctionnel sur le port 8000
- ✅ Tous les fichiers React copiés dans un dossier

## 🚀 Installation Express (3 commandes)

### Linux / macOS

```bash
# 1. Aller dans le dossier du projet
cd neural-chat-interface

# 2. Installer les dépendances
npm install

# 3. Lancer l'application
npm run dev
```

### Windows

```powershell
# 1. Aller dans le dossier du projet
cd neural-chat-interface

# 2. Installer les dépendances
npm install

# 3. Lancer l'application
npm run dev
```

**C'est tout !** 🎉

L'application s'ouvrira automatiquement sur `http://localhost:3000`

## 📋 Checklist Pre-Launch

Avant de lancer, vérifiez :

1. **Backend démarré ?**
   ```bash
   curl http://localhost:8000/questions
   ```
   Devrait retourner un JSON

2. **Fichier .env créé ?**
   ```bash
   cp .env.example .env
   ```
   Vérifiez que `VITE_API_BASE_URL=http://localhost:8000`

3. **Dépendances installées ?**
   ```bash
   ls node_modules
   ```
   Le dossier doit exister et contenir des fichiers

## 🔧 Configuration Minimale

Si votre backend n'est **pas** sur `localhost:8000`, créez/éditez `.env` :

```env
VITE_API_BASE_URL=http://votre-backend:8000
```

Puis relancez :
```bash
npm run dev
```

## 🐛 Problèmes Courants

### ❌ "Cannot find module"
**Solution :** 
```bash
rm -rf node_modules package-lock.json
npm install
```

### ❌ Erreur CORS
**Solution :** Ajoutez dans votre backend (Python/FastAPI) :
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

### ❌ Port 3000 déjà utilisé
**Solution :** Modifiez `vite.config.js` :
```javascript
export default defineConfig({
  server: {
    port: 3001  // Changez le port ici
  }
});
```

## ✅ Vérification Rapide

Après le lancement, vérifiez :

1. **Interface visible** → OK ✅
2. **Questions chargées** dans le panneau de droite → OK ✅
3. **Validation du profil** fonctionne → OK ✅
4. **Envoi de message** fonctionne → OK ✅
5. **Réception de réponse** fonctionne → OK ✅

Si tout est OK, **félicitations !** 🎉

## 🎨 Première Personnalisation (Optionnel)

Changez le titre dans `src/components/Header.jsx` :

```jsx
<h1 className="header-title">
    🧠 MON APPLICATION
</h1>
```

Sauvegardez, la page se recharge automatiquement !

## 📚 Aller Plus Loin

- **Documentation complète** → `README.md`
- **Guide de migration** → `MIGRATION_GUIDE.md`
- **Structure du projet** → `STRUCTURE.md`

## 💡 Commandes Utiles

```bash
# Mode développement (hot reload)
npm run dev

# Build pour production
npm run build

# Prévisualiser le build
npm run preview

# Tester l'API backend
node test-api.js

# Voir les logs détaillés
npm run dev -- --debug
```

## 🎯 Prochaine Étape

Maintenant que ça fonctionne :

1. **Personnalisez** les couleurs dans `src/styles/App.css`
2. **Ajoutez** des fonctionnalités dans les composants
3. **Déployez** avec Vercel ou Netlify

---

**Temps total : ~5 minutes** ⏱️

**Besoin d'aide ?** Consultez `README.md` ou `MIGRATION_GUIDE.md`

**Bon développement !** 🚀
