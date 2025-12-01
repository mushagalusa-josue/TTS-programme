# Configuration des Variables d'Environnement

## Où mettre les variables d'environnement ?

Vous avez plusieurs options selon votre cas d'usage :

### Option 1 : Fichier `.env` (Recommandé pour le développement local)

1. **Créez un fichier `.env`** à la racine du projet (même niveau que `api.py`)
2. **Copiez le contenu de `.env.example`** dans `.env`
3. **Modifiez les valeurs** si nécessaire :

```env
DATABASE_URL=postgresql://postgres:2022@127.0.0.1:5432/kokoro_tts
SECRET_KEY=dev-secret-key-change-in-production
PORT=10000
```

**Avantages :**
- ✅ Variables chargées automatiquement au démarrage
- ✅ Pas besoin de les redéfinir à chaque fois
- ✅ Le fichier `.env` est dans `.gitignore` (pas commité)

**Le code charge automatiquement le fichier `.env` grâce à `python-dotenv`**

---

### Option 2 : Terminal PowerShell (Temporaire)

Pour une session de terminal uniquement :

```powershell
$env:DATABASE_URL="postgresql://postgres:2022@127.0.0.1:5432/kokoro_tts"
$env:SECRET_KEY="dev-secret-key-change-in-production"
```

**Avantages :**
- ✅ Rapide pour tester
- ✅ Pas de fichier à créer

**Inconvénients :**
- ❌ Perdu quand vous fermez le terminal
- ❌ Doit être redéfini à chaque nouvelle session

---

### Option 3 : Variables d'environnement système Windows (Permanent)

Pour définir globalement sur votre machine :

1. **Ouvrez les Variables d'environnement Windows :**
   - Appuyez sur `Win + R`
   - Tapez `sysdm.cpl` et Entrée
   - Onglet "Avancé" → "Variables d'environnement"

2. **Ajoutez les variables :**
   - Cliquez sur "Nouveau" dans "Variables utilisateur"
   - Nom : `DATABASE_URL`
   - Valeur : `postgresql://postgres:2022@127.0.0.1:5432/kokoro_tts`
   - Répétez pour `SECRET_KEY`

**Avantages :**
- ✅ Permanent sur votre machine
- ✅ Disponible pour tous les projets

**Inconvénients :**
- ❌ Peut entrer en conflit avec d'autres projets
- ❌ Moins flexible

---

### Option 4 : Variables d'environnement sur Railway/Render (Production)

Pour le déploiement en production :

#### Railway
1. Allez dans votre projet Railway
2. Sélectionnez votre service backend
3. Onglet "Variables"
4. Ajoutez :
   - `DATABASE_URL` : Automatiquement fournie si vous avez un service PostgreSQL
   - `SECRET_KEY` : Générez une clé sécurisée

#### Render
1. Allez dans votre service sur Render
2. Section "Environment"
3. Ajoutez les variables d'environnement

**Important pour la production :**
- ✅ Utilisez une `SECRET_KEY` forte (générez avec `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- ✅ Ne commitez JAMAIS le fichier `.env` en production
- ✅ `DATABASE_URL` est généralement fournie automatiquement par la plateforme

---

## Recommandation

**Pour le développement local :** Utilisez **Option 1** (fichier `.env`)
- Créez le fichier `.env` à partir de `.env.example`
- Le code chargera automatiquement les variables

**Pour la production :** Utilisez **Option 4** (variables d'environnement de la plateforme)

---

## Vérifier que les variables sont chargées

Vous pouvez vérifier dans les logs au démarrage de l'API :
```
INFO:root:Database URL: postgresql://postgres:2022@***
```

Ou tester avec :
```python
import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("DATABASE_URL"))
```



