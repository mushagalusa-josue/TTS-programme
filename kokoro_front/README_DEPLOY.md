# Guide de déploiement du frontend

## Configuration de l'URL de l'API

L'URL de l'API est configurable via la variable d'environnement `VITE_API_URL`.

### Pour le développement local
Créez un fichier `.env.local` dans le dossier `kokoro_front` :
```
VITE_API_URL=http://localhost:8000
```

### Pour la production (Vercel/Netlify)
L'URL par défaut est `https://kokoro-tts-api-production-b52e.up.railway.app`. 

Si vous voulez la changer, ajoutez la variable d'environnement dans votre plateforme de déploiement :
- **Vercel** : Settings → Environment Variables → Ajoutez `VITE_API_URL` = `https://kokoro-tts-api-production-b52e.up.railway.app`
- **Netlify** : Site settings → Environment variables → Ajoutez `VITE_API_URL` = `https://kokoro-tts-api-production-b52e.up.railway.app`

## Déploiement

### Vercel
1. Connectez votre dépôt GitHub à Vercel
2. Configurez :
   - Root Directory: `kokoro_front`
   - Build Command: `npm run build`
   - Output Directory: `dist`
3. Ajoutez la variable d'environnement `VITE_API_URL` si nécessaire
4. Déployez !

### Netlify
1. Connectez votre dépôt GitHub à Netlify
2. Configurez :
   - Base directory: `kokoro_front`
   - Build command: `npm run build`
   - Publish directory: `kokoro_front/dist`
3. Ajoutez la variable d'environnement `VITE_API_URL` si nécessaire
4. Déployez !

## Résolution des problèmes

Si vous voyez une erreur `ERR_CONNECTION_REFUSED` sur `127.0.0.1:8000` :
1. Vérifiez que vous avez bien reconstruit le projet : `npm run build`
2. Videz le cache du navigateur (Ctrl+Shift+R ou Cmd+Shift+R)
3. Vérifiez que la variable d'environnement `VITE_API_URL` est bien définie en production

