# Configuration de la Base de Données PostgreSQL

Ce document explique comment configurer la base de données PostgreSQL pour l'application Kokoro TTS.

## Variables d'environnement requises

### 1. DATABASE_URL
L'URL de connexion à la base de données PostgreSQL.

**Format:** `postgresql://user:password@host:port/database`

**Exemples:**
- **Railway:** La variable `DATABASE_URL` est automatiquement fournie lors de l'ajout d'un service PostgreSQL
- **Local:** `postgresql://postgres:postgres@localhost:5432/kokoro_tts`
- **Render:** `postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com/kokoro_tts`

**Note:** Si votre service utilise `postgres://` au lieu de `postgresql://`, le code le convertira automatiquement.

### 2. SECRET_KEY
Clé secrète pour signer les tokens JWT. **IMPORTANT:** Changez cette valeur en production!

**Génération d'une clé sécurisée:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Exemple:** `SECRET_KEY=your-super-secret-key-here`

## Configuration sur Railway

1. Dans votre projet Railway, ajoutez un service **PostgreSQL**
2. Railway créera automatiquement la variable `DATABASE_URL`
3. Ajoutez la variable `SECRET_KEY` dans les variables d'environnement de votre service backend
4. Les tables seront créées automatiquement au démarrage de l'application

## Configuration locale (Docker)

**Important:** Assurez-vous que Docker Desktop est démarré avant d'exécuter ces commandes.

### Windows PowerShell
```powershell
# Démarrer PostgreSQL avec Docker
docker run --name kokoro-postgres `
  -e POSTGRES_PASSWORD=postgres `
  -e POSTGRES_DB=kokoro_tts `
  -p 5432:5432 `
  -d postgres:15

# Variables d'environnement pour développement local
$env:DATABASE_URL="postgresql://postgres:postgres@localhost:5432/kokoro_tts"
$env:SECRET_KEY="dev-secret-key-change-in-production"
```

### Linux/Mac/Git Bash
```bash
# Démarrer PostgreSQL avec Docker
docker run --name kokoro-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=kokoro_tts \
  -p 5432:5432 \
  -d postgres:15

# Variables d'environnement pour développement local
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/kokoro_tts
export SECRET_KEY=dev-secret-key-change-in-production
```

### Tester la connexion
```bash
python test_db_connection.py
```

**Si Docker Desktop n'est pas démarré:**
- Windows: Ouvrez Docker Desktop depuis le menu Démarrer
- Vérifiez avec: `docker ps`
- Voir `SETUP_LOCAL_DB.md` pour plus d'options

## Structure de la base de données

### Table `users`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER | Clé primaire |
| `email` | VARCHAR(255) | Email unique de l'utilisateur |
| `hashed_password` | VARCHAR(255) | Mot de passe hashé avec bcrypt |
| `name` | VARCHAR(255) | Nom de l'utilisateur (optionnel) |
| `is_active` | BOOLEAN | Compte actif ou non |
| `is_verified` | BOOLEAN | Email vérifié ou non |
| `created_at` | TIMESTAMP | Date de création |
| `updated_at` | TIMESTAMP | Date de mise à jour |
| `last_login` | TIMESTAMP | Dernière connexion |
| `favorite_voices` | JSON | Liste des voix favorites |
| `history` | JSON | Historique des générations |
| `credits` | INTEGER | Crédits restants (NULL = illimité) |
| `preferences` | JSON | Préférences utilisateur |

## Initialisation automatique

Les tables sont créées automatiquement au démarrage de l'application via `init_db()` dans `database.py`.

Si vous devez réinitialiser la base de données:
```python
from database import init_db
init_db()
```

## Sécurité

- ✅ Les mots de passe sont hashés avec **bcrypt** (algorithme sécurisé)
- ✅ Les tokens JWT sont signés avec une clé secrète
- ✅ Les tokens expirent après 30 jours
- ✅ Les mots de passe ne sont jamais stockés en clair

## Endpoints API

### POST `/api/auth/register`
Inscription d'un nouvel utilisateur

**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe" // optionnel
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    ...
  }
}
```

### POST `/api/auth/login`
Connexion d'un utilisateur

**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** Même format que `/register`

### GET `/api/auth/me`
Obtenir les informations de l'utilisateur connecté

**Headers:**
```
Authorization: Bearer <token>
```

### PUT `/api/auth/preferences`
Mettre à jour les préférences utilisateur

**Headers:**
```
Authorization: Bearer <token>
```

**Body:**
```json
{
  "default_voice": "ff_siwis",
  "default_speed": 1.0
}
```

## Dépannage

### Erreur: "could not connect to server"
- Vérifiez que PostgreSQL est démarré
- Vérifiez que `DATABASE_URL` est correcte
- Vérifiez les permissions de connexion

### Erreur: "relation 'users' does not exist"
- Les tables n'ont pas été créées. Vérifiez les logs au démarrage
- Exécutez manuellement `init_db()`

### Erreur: "password authentication failed"
- Vérifiez les identifiants dans `DATABASE_URL`
- Vérifiez que l'utilisateur PostgreSQL existe et a les bonnes permissions

