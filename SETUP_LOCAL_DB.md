# Configuration de la Base de Données Locale

## Option 1 : Démarrer Docker Desktop (Recommandé)

### Windows
1. Ouvrez **Docker Desktop** depuis le menu Démarrer
2. Attendez que Docker démarre complètement (icône Docker dans la barre des tâches)
3. Vérifiez que Docker fonctionne :
   ```bash
   docker ps
   ```
4. Ensuite, lancez PostgreSQL :
   ```bash
   docker run --name kokoro-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=kokoro_tts -p 5432:5432 -d postgres:15
   ```

### Vérifier que le conteneur tourne
```bash
docker ps
```

Vous devriez voir un conteneur `kokoro-postgres` en cours d'exécution.

## Option 2 : PostgreSQL Installé Localement

Si vous avez PostgreSQL installé directement sur Windows :

1. Créez la base de données :
   ```sql
   CREATE DATABASE kokoro_tts;
   ```

2. Configurez la variable d'environnement :
   ```powershell
   $env:DATABASE_URL="postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/kokoro_tts"
   $env:SECRET_KEY="dev-secret-key-change-in-production"
   ```

## Option 3 : Utiliser Railway/Render (Production)

Pour tester en production directement :

1. **Railway** :
   - Ajoutez un service PostgreSQL dans votre projet
   - Railway créera automatiquement `DATABASE_URL`
   - Ajoutez `SECRET_KEY` dans les variables d'environnement

2. **Render** :
   - Créez une base de données PostgreSQL
   - Copiez l'URL de connexion interne
   - Ajoutez `DATABASE_URL` et `SECRET_KEY` dans les variables d'environnement

## Option 4 : SQLite pour le Développement (Alternative Simple)

Si vous voulez tester rapidement sans PostgreSQL, vous pouvez utiliser SQLite (modification du code requise).

## Script de Test Rapide

Créez un fichier `test_db_connection.py` :

```python
import os
from database import engine, init_db
from sqlalchemy import text

# Configuration
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/kokoro_tts"
)

print(f"Testing connection to: {DATABASE_URL.split('@')[0]}@***")

try:
    # Tester la connexion
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Connexion réussie!")
    
    # Initialiser les tables
    print("Initialisation des tables...")
    init_db()
    print("✅ Tables créées avec succès!")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    print("\nVérifiez que:")
    print("1. PostgreSQL est démarré")
    print("2. DATABASE_URL est correcte")
    print("3. Les identifiants sont valides")
```

Exécutez :
```bash
python test_db_connection.py
```

## Commandes Utiles Docker

```bash
# Démarrer le conteneur
docker start kokoro-postgres

# Arrêter le conteneur
docker stop kokoro-postgres

# Voir les logs
docker logs kokoro-postgres

# Supprimer le conteneur (si besoin de recommencer)
docker rm -f kokoro-postgres

# Se connecter à PostgreSQL dans le conteneur
docker exec -it kokoro-postgres psql -U postgres -d kokoro_tts
```

## Dépannage

### Erreur: "docker: error during connect"
- **Solution** : Démarrez Docker Desktop manuellement

### Erreur: "port 5432 already in use"
- **Solution** : Changez le port ou arrêtez le service PostgreSQL local
  ```bash
  docker run --name kokoro-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=kokoro_tts -p 5433:5432 -d postgres:15
  ```
  Puis utilisez `DATABASE_URL=postgresql://postgres:postgres@localhost:5433/kokoro_tts`

### Erreur: "password authentication failed"
- Vérifiez que le mot de passe dans `DATABASE_URL` correspond à celui du conteneur



