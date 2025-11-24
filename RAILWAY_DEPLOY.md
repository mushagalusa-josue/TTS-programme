# Guide de déploiement sur Railway.app

## 🚀 Étapes de déploiement

### 1. Créer un compte Railway
- Allez sur [railway.app](https://railway.app)
- Créez un compte (connexion GitHub recommandée)

### 2. Créer un nouveau projet
- Cliquez sur "New Project"
- Sélectionnez "Deploy from GitHub repo"
- Choisissez votre dépôt `tetosp`

### 3. Configuration automatique
Railway détectera automatiquement :
- ✅ Le Dockerfile
- ✅ Le fichier `railway.json` (configuration)
- ✅ Les variables d'environnement nécessaires

### 4. Variables d'environnement (optionnel)
Railway définit automatiquement `PORT`, mais vous pouvez ajouter :
- `PYTHON_CMD=python` (déjà dans le code par défaut)

### 5. Déploiement
- Railway déploiera automatiquement après le push
- Le build peut prendre 10-15 minutes (installation des dépendances)
- Une fois déployé, Railway vous donnera une URL comme `https://your-app.up.railway.app`

## 🔧 Différences avec Render

### Avantages de Railway :
- ✅ Plus tolérant avec les processus longs
- ✅ Pas de redémarrage automatique après inactivité
- ✅ Meilleure gestion des ressources
- ✅ Variables d'environnement plus flexibles

### Configuration :
- Railway utilise `PORT` automatiquement (généralement un port aléatoire)
- Le Dockerfile est déjà configuré pour Railway
- Pas besoin de `railway.json` si vous utilisez Dockerfile

## 📝 Mise à jour du frontend

Après le déploiement sur Railway, mettez à jour l'URL dans le frontend :

1. Dans Vercel/Netlify, ajoutez la variable d'environnement :
   ```
   VITE_API_URL=https://your-app.up.railway.app
   ```

2. Ou modifiez directement dans `kokoro_front/src/App.jsx` :
   ```javascript
   const API_URL = import.meta.env.VITE_API_URL || 'https://your-app.up.railway.app';
   ```

3. Reconstruisez et redéployez le frontend

## ✅ Vérification

Après le déploiement, testez :
- `https://your-app.up.railway.app/` → doit retourner un JSON
- `https://your-app.up.railway.app/health` → doit retourner `{"status": "healthy"}`
- `https://your-app.up.railway.app/test-kokoro` → teste kokoro

## 🐛 Résolution des problèmes

### Le service ne démarre pas
- Vérifiez les logs dans Railway Dashboard
- Assurez-vous que le port est bien bindé sur `0.0.0.0`

### Erreur CORS
- Vérifiez que l'URL Railway est dans la liste des origines autorisées dans `api.py`
- Ajoutez votre domaine Railway dans la liste `origins`

### Timeout
- Railway est plus tolérant, mais si le problème persiste, vérifiez les logs
- La première génération peut prendre plusieurs minutes (téléchargement des modèles)

