# Instructions de déploiement

## 🔧 Configuration Backend (Railway)

### Étape 1 : Backend déployé sur Railway

Votre backend est déployé sur Railway : `https://kokoro-tts-api-production-b52e.up.railway.app`

1. Allez dans **Environment** (ou **Settings** → **Environment Variables**)
2. Ajoutez ou modifiez :
   ```
   PORT = 10000
   ```
3. Redéployez le service

**Important** : Render définit automatiquement PORT, mais il est recommandé de l'expliciter à 10000.

## 🔧 Configuration Frontend

### Option A : Déploiement sur Vercel

1. **Connectez votre dépôt** à Vercel
2. **Configurez le projet** :
   - Root Directory: `kokoro_front`
   - Build Command: `npm run build`
   - Output Directory: `dist`
3. **Ajoutez la variable d'environnement** (Settings → Environment Variables) :
   ```
   VITE_API_URL = https://kokoro-tts-api-production-b52e.up.railway.app
   ```
4. **Déployez** !

### Option B : Déploiement sur Netlify

1. **Connectez votre dépôt** à Netlify
2. **Configurez le projet** :
   - Base directory: `kokoro_front`
   - Build command: `npm run build`
   - Publish directory: `kokoro_front/dist`
3. **Ajoutez la variable d'environnement** (Site settings → Environment variables) :
   ```
   VITE_API_URL = https://kokoro-tts-api-production-b52e.up.railway.app
   ```
4. **Déployez** !

### Option C : Test local

1. Créez un fichier `.env.local` dans `kokoro_front/` :
   ```
   VITE_API_URL=http://localhost:8000
   ```
2. Démarrez l'API locale :
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```
3. Démarrez le frontend :
   ```bash
   cd kokoro_front
   npm run dev
   ```

## ✅ Vérification

Après déploiement, testez :
- Backend : `https://kokoro-tts-api-production-b52e.up.railway.app/` → doit retourner un JSON
- Backend health : `https://kokoro-tts-api-production-b52e.up.railway.app/health` → `{"status": "healthy"}`
- Frontend : doit pouvoir envoyer des requêtes à `/tts`

## 🐛 Résolution des problèmes

### Erreur `ERR_CONNECTION_REFUSED` sur `127.0.0.1:8000`

**Cause** : Le frontend n'utilise pas la bonne URL de l'API.

**Solution** :
1. Vérifiez que `VITE_API_URL` est bien définie dans votre plateforme de déploiement
2. Reconstruisez le frontend : `npm run build`
3. Videz le cache du navigateur : `Ctrl + Shift + R`

### Le backend ne démarre pas sur Railway

**Cause** : Le port n'est pas correctement configuré.

**Solution** :
1. Railway définit automatiquement la variable `PORT`
2. Vérifiez les logs de déploiement dans Railway
3. Le Dockerfile utilise `${PORT}`, donc il devrait fonctionner automatiquement

