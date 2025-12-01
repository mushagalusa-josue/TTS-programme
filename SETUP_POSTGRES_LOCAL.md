# Configuration PostgreSQL en Local (Windows)

## Option 1 : Démarrer Docker Desktop (Recommandé si déjà installé)

1. **Démarrer Docker Desktop**
   - Ouvrez Docker Desktop depuis le menu Démarrer
   - Attendez que l'icône Docker dans la barre des tâches soit verte
   - Ensuite, réessayez la commande :
   ```bash
   docker run --name kokoro-postgres \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_DB=kokoro_tts \
     -p 5432:5432 \
     -d postgres:15
   ```

2. **Vérifier que le conteneur tourne**
   ```bash
   docker ps
   ```

## Option 2 : Installer PostgreSQL directement sur Windows

### Étape 1 : Télécharger PostgreSQL
1. Allez sur https://www.postgresql.org/download/windows/
2. Téléchargez le **PostgreSQL Installer** (version 15 ou 16)
3. Exécutez l'installateur

### Étape 2 : Installation
1. **Port** : Gardez `5432` (par défaut)
2. **Mot de passe superutilisateur** : Choisissez un mot de passe (ex: `postgres`)
3. **Locale** : Français (ou votre préférence)
4. Laissez les autres options par défaut

### Étape 3 : Créer la base de données
1. Ouvrez **pgAdmin** (installé avec PostgreSQL) ou utilisez `psql` en ligne de commande
2. Connectez-vous avec :
   - **Host** : `localhost`
   - **Port** : `5432`
   - **Username** : `postgres`
   - **Password** : Le mot de passe que vous avez choisi

3. Créez la base de données :
   ```sql
   CREATE DATABASE kokoro_tts;
   ```

### Étape 4 : Configurer les variables d'environnement
Créez un fichier `.env` à la racine du projet :
```env
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/kokoro_tts
SECRET_KEY=votre-cle-secrete-ici
```

Ou exportez-les dans PowerShell :
```powershell
$env:DATABASE_URL="postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/kokoro_tts"
$env:SECRET_KEY="votre-cle-secrete-ici"
```

## Option 3 : Utiliser un service cloud (Recommandé pour production)

### Railway (Gratuit au début)
1. Allez sur https://railway.app
2. Créez un nouveau projet
3. Ajoutez un service **PostgreSQL**
4. Railway créera automatiquement la variable `DATABASE_URL`
5. Copiez cette URL et ajoutez-la dans les variables d'environnement de votre service backend

### Render (Alternative)
1. Allez sur https://render.com
2. Créez une nouvelle **PostgreSQL Database**
3. Notez les informations de connexion
4. Configurez `DATABASE_URL` dans votre service backend

## Option 4 : Utiliser SQLite pour le développement (Plus simple)

Si vous voulez juste tester rapidement sans installer PostgreSQL, vous pouvez modifier temporairement `database.py` pour utiliser SQLite :

```python
# Dans database.py, remplacez :
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./kokoro_tts.db"  # SQLite au lieu de PostgreSQL
)

# Et changez l'import :
from sqlalchemy import create_engine
# SQLite n'a pas besoin de psycopg2
```

**Note** : SQLite n'est pas recommandé pour la production, mais fonctionne bien pour le développement local.

## Vérification

Une fois PostgreSQL configuré, testez la connexion :

```python
# Test Python
python -c "from database import engine; print('Connection OK!' if engine else 'Error')"
```

Ou testez avec `psql` :
```bash
psql -h localhost -U postgres -d kokoro_tts
```

## Dépannage

### Erreur : "could not connect to server"
- Vérifiez que PostgreSQL est démarré (Services Windows → PostgreSQL)
- Vérifiez que le port 5432 n'est pas utilisé par un autre service
- Vérifiez le mot de passe dans `DATABASE_URL`

### Erreur : "password authentication failed"
- Vérifiez que le mot de passe dans `DATABASE_URL` correspond au mot de passe PostgreSQL
- Essayez de vous connecter avec pgAdmin pour vérifier les identifiants

### Erreur : "database does not exist"
- Créez la base de données avec `CREATE DATABASE kokoro_tts;`
- Ou laissez l'application la créer automatiquement (si les permissions le permettent)

