# 🚀 Guide de déploiement sur Vercel

## Prérequis
- Un compte Vercel (gratuit) : [vercel.com](https://vercel.com)
- Votre backend déployé sur Railway (URL nécessaire)

## 📋 Étapes de déploiement

### 1. Préparer le projet

Assurez-vous que votre projet est prêt :
```bash
cd kokoro_front
npm install
npm run build  # Vérifier que le build fonctionne
```

### 2. Déployer sur Vercel

#### Option A : Via l'interface Vercel (Recommandé)

1. **Connecter votre repository**
   - Allez sur [vercel.com](https://vercel.com)
   - Cliquez sur "Add New..." → "Project"
   - Importez votre repository GitHub/GitLab/Bitbucket

2. **Configurer le projet**
   - **Root Directory** : `kokoro_front`
   - **Framework Preset** : Vite (détecté automatiquement)
   - **Build Command** : `npm run build` (déjà dans vercel.json)
   - **Output Directory** : `dist` (déjà dans vercel.json)

3. **Ajouter la variable d'environnement**
   - Dans "Environment Variables", ajoutez :
     - **Name** : `VITE_API_URL`
     - **Value** : `https://votre-url-railway.up.railway.app`
     - Cochez les environnements : Production, Preview, Development

4. **Déployer**
   - Cliquez sur "Deploy"
   - Attendez la fin du déploiement (2-3 minutes)

#### Option B : Via la CLI Vercel

```bash
# Installer Vercel CLI
npm i -g vercel

# Se connecter
vercel login

# Déployer (depuis le dossier kokoro_front)
cd kokoro_front
vercel

# Ajouter la variable d'environnement
vercel env add VITE_API_URL
# Entrez votre URL Railway quand demandé

# Redéployer avec la variable
vercel --prod
```

### 3. Vérifier le déploiement

1. Vercel vous donnera une URL comme : `https://votre-projet.vercel.app`
2. Ouvrez cette URL dans votre navigateur
3. Testez la génération de TTS
4. Ouvrez la console du navigateur (F12) pour vérifier que l'URL API est correcte

## 🔧 Configuration des variables d'environnement

### Variables nécessaires

| Variable | Description | Exemple |
|----------|-------------|---------|
| `VITE_API_URL` | URL de votre backend Railway | `https://tts-backend-production-1234.up.railway.app` |

### Comment modifier après déploiement

1. Allez sur Vercel → Votre projet → Settings → Environment Variables
2. Modifiez `VITE_API_URL` avec la nouvelle valeur
3. Redéployez (Vercel le fait automatiquement ou cliquez sur "Redeploy")

## 🐛 Dépannage

### Le frontend ne peut pas se connecter au backend

1. **Vérifier l'URL API** :
   - Ouvrez la console du navigateur (F12)
   - Regardez les logs : `🔗 API URL utilisée: ...`
   - Vérifiez que c'est bien l'URL Railway

2. **Vérifier CORS** :
   - Assurez-vous que l'URL Vercel est dans la liste CORS du backend
   - Vérifiez dans `api.py` que votre domaine Vercel est autorisé

3. **Vérifier les variables d'environnement** :
   - Vercel → Settings → Environment Variables
   - Vérifiez que `VITE_API_URL` est bien définie
   - **Important** : Les variables Vite doivent commencer par `VITE_`

### Le build échoue

1. Vérifiez les logs de build sur Vercel
2. Testez localement : `npm run build`
3. Vérifiez que toutes les dépendances sont dans `package.json`

## 📝 Notes importantes

- **Variables d'environnement** : Vercel doit redéployer pour prendre en compte les nouvelles variables
- **Build automatique** : Vercel redéploie automatiquement à chaque push sur votre branche principale
- **Preview deployments** : Chaque pull request crée un déploiement de prévisualisation

## 🔗 Liens utiles

- [Documentation Vercel](https://vercel.com/docs)
- [Vite + Vercel](https://vercel.com/docs/frameworks/vite)
- [Variables d'environnement Vercel](https://vercel.com/docs/environment-variables)

