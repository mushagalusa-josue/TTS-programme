# 🚨 Problème de mémoire sur Railway Free Tier

## Problème identifié

Le processus kokoro est tué avec `SIGKILL (-9)` par Railway car il dépasse les limites de mémoire du plan gratuit.

```
ERROR:root:kokoro subprocess failed with return code -9
ERROR:root:Command '['python', '-m', 'kokoro', ...]' died with <Signals.SIGKILL: 9>.
```

## Cause

- **Railway Free Tier** : Limite de mémoire très stricte (~512MB-1GB)
- **Kokoro + PyTorch** : Nécessite beaucoup de mémoire pour charger les modèles (~2-4GB)
- Le processus est tué avant même de pouvoir générer l'audio

## Solutions appliquées

### 1. Variables d'environnement pour limiter la mémoire PyTorch

Ajoutées dans le `Dockerfile` :
```dockerfile
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
```

### 2. Gestion d'erreur améliorée

Le code détecte maintenant les SIGKILL et affiche un message explicite.

## Solutions recommandées

### Option 1 : Passer à Railway Pro (Recommandé) ⭐

**Railway Pro** offre :
- Plus de mémoire (2GB+)
- Meilleures performances
- Pas de limitations strictes

**Prix** : ~$5-20/mois selon l'utilisation

### Option 2 : Utiliser une autre plateforme

#### Fly.io
- **Free tier** : 3 VMs partagées, 256MB RAM par VM
- **Hobby** : $5/mois, 256MB RAM par VM
- Meilleur pour les applications légères

#### Render.com
- **Free tier** : 512MB RAM, mais tue les processus inactifs
- **Starter** : $7/mois, 512MB RAM
- Limite de 750 heures/mois sur le free tier

#### Google Cloud Run
- **Free tier** : 2 millions de requêtes/mois
- **Payant** : $0.00002400 par GB-seconde
- Plus flexible, mais configuration plus complexe

#### AWS Lambda + ECS
- **Free tier** : 1 million de requêtes/mois
- **Payant** : Pay-as-you-go
- Complexe à configurer

### Option 3 : Optimiser davantage (Difficile)

- Utiliser un modèle TTS plus léger
- Précharger les modèles au démarrage (risque de SIGKILL au démarrage)
- Utiliser un cache de modèles partagé
- Limiter la taille des textes

## Configuration Railway

Si vous passez à Railway Pro, vous pouvez configurer les ressources :

1. Allez dans Railway → Votre service → Settings
2. Section "Resources"
3. Augmentez la mémoire à **2GB minimum**
4. Redéployez

## Variables d'environnement Railway

Vous pouvez aussi ajouter ces variables dans Railway (Settings → Environment Variables) :

```
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
OMP_NUM_THREADS=1
MKL_NUM_THREADS=1
```

## Test

Après avoir appliqué les changements :

1. Redéployez sur Railway
2. Testez avec un texte très court (ex: "test")
3. Vérifiez les logs pour voir si le SIGKILL persiste

## Conclusion

Le problème principal est la **limite de mémoire du plan gratuit Railway**. Les optimisations peuvent aider, mais pour une utilisation fiable, il est recommandé de passer à un plan payant ou d'utiliser une autre plateforme avec plus de ressources.

