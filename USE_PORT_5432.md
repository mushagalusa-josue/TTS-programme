# Utiliser le port 5432 standard

Vous avez deux options pour utiliser le port 5432 standard :

## Option 1 : Arrêter PostgreSQL local et utiliser Docker

### Étape 1 : Arrêter le service PostgreSQL local
```powershell
Stop-Service -Name "postgresql-x64-17"
```

### Étape 2 : Démarrer Docker sur le port 5432
```powershell
docker run --name kokoro-postgres `
  -e POSTGRES_PASSWORD=postgres `
  -e POSTGRES_DB=kokoro_tts `
  -p 5432:5432 `
  -d postgres:15
```

### Étape 3 : Configurer les variables d'environnement
```powershell
$env:DATABASE_URL="postgresql://postgres:postgres@localhost:5432/kokoro_tts"
$env:SECRET_KEY="dev-secret-key-change-in-production"
```

### Étape 4 : Tester
```powershell
python test_db_connection.py
```

### Pour redémarrer PostgreSQL local plus tard
```powershell
Start-Service -Name "postgresql-x64-17"
```

---

## Option 2 : Utiliser PostgreSQL local directement

### Étape 1 : Créer la base de données
Vous devez connaître le mot de passe de votre installation PostgreSQL.

```powershell
# Avec votre mot de passe
$env:PGPASSWORD="VOTRE_MOT_DE_PASSE"
psql -U postgres -h localhost -c "CREATE DATABASE kokoro_tts;"
```

### Étape 2 : Configurer les variables d'environnement
```powershell
$env:DATABASE_URL="postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/kokoro_tts"
$env:SECRET_KEY="dev-secret-key-change-in-production"
```

### Étape 3 : Tester
```powershell
python test_db_connection.py
```

### Si vous ne connaissez pas le mot de passe

**Option A : Réinitialiser le mot de passe PostgreSQL**

1. Modifiez `pg_hba.conf` (généralement dans `C:\Program Files\PostgreSQL\17\data\`)
   - Changez `md5` en `trust` pour la ligne `host all all 127.0.0.1/32`
2. Redémarrez PostgreSQL : `Restart-Service -Name "postgresql-x64-17"`
3. Connectez-vous sans mot de passe : `psql -U postgres`
4. Changez le mot de passe : `ALTER USER postgres PASSWORD 'nouveau_mot_de_passe';`
5. Remettez `md5` dans `pg_hba.conf` et redémarrez

**Option B : Utiliser l'authentification Windows**
Si votre installation PostgreSQL le permet :
```powershell
$env:DATABASE_URL="postgresql://$env:USERNAME@localhost:5432/kokoro_tts"
```

---

## Recommandation

Pour le développement, **Option 1 (Docker)** est plus simple car :
- ✅ Mot de passe connu (`postgres`)
- ✅ Configuration isolée
- ✅ Facile à réinitialiser
- ✅ Pas de conflit avec d'autres projets

Pour la production, utilisez l'installation PostgreSQL locale ou une base de données gérée (Railway, Render, etc.).



