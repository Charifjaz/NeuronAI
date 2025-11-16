#!/bin/bash

# Script de migration Streamlit → React
# Neural Chat Interface

echo "🚀 Migration de Streamlit vers React"
echo "===================================="
echo ""

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé"
    echo "   Installez Node.js depuis https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"
echo "✅ npm version: $(npm -v)"
echo ""

# Créer la structure
echo "📁 Création de la structure du projet..."
mkdir -p src/components src/services src/styles

# Vérifier que les fichiers sont présents
echo "🔍 Vérification des fichiers..."
files=(
    "package.json"
    "vite.config.js"
    "index.html"
    "src/main.jsx"
    "src/App.jsx"
    "src/styles/App.css"
    "src/services/api.js"
    "src/components/Header.jsx"
    "src/components/ChatInterface.jsx"
    "src/components/ProfilePanel.jsx"
    "src/components/Message.jsx"
)

missing_files=0
for file in "${files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "   ❌ Manquant: $file"
        missing_files=$((missing_files + 1))
    fi
done

if [ $missing_files -gt 0 ]; then
    echo ""
    echo "⚠️  $missing_files fichier(s) manquant(s)"
    echo "   Assurez-vous d'avoir copié tous les fichiers dans les bons dossiers"
    exit 1
fi

echo "✅ Tous les fichiers sont présents"
echo ""

# Créer .env
if [ ! -f ".env" ]; then
    echo "📝 Création du fichier .env..."
    cat > .env << EOF
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
EOF
    echo "✅ Fichier .env créé"
else
    echo "ℹ️  Fichier .env déjà existant"
fi
echo ""

# Installation des dépendances
echo "📦 Installation des dépendances..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dépendances installées avec succès"
else
    echo "❌ Erreur lors de l'installation des dépendances"
    exit 1
fi
echo ""

# Résumé
echo "✨ Migration terminée avec succès !"
echo ""
echo "📋 Prochaines étapes :"
echo "   1. Vérifiez la configuration dans .env"
echo "   2. Assurez-vous que votre backend est démarré sur le port 8000"
echo "   3. Lancez l'application avec: npm run dev"
echo ""
echo "🚀 Pour démarrer maintenant :"
echo "   npm run dev"
echo ""
