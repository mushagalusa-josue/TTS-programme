# Script pour configurer PostgreSQL local (port 5432)
# Assurez-vous que le service PostgreSQL est démarré

Write-Host "Configuration de PostgreSQL local..." -ForegroundColor Cyan

# Vérifier si PostgreSQL est en cours d'exécution
$postgresService = Get-Service -Name "postgresql-x64-17" -ErrorAction SilentlyContinue
if ($postgresService -and $postgresService.Status -eq "Running") {
    Write-Host "✅ Service PostgreSQL est en cours d'exécution" -ForegroundColor Green
} else {
    Write-Host "⚠️  Service PostgreSQL n'est pas démarré. Démarrage..." -ForegroundColor Yellow
    Start-Service -Name "postgresql-x64-17"
    Start-Sleep -Seconds 3
}

# Créer la base de données (nécessite psql dans le PATH)
Write-Host "`nCréation de la base de données 'kokoro_tts'..." -ForegroundColor Cyan

# Essayer de se connecter et créer la base de données
# Note: Vous devrez peut-être ajuster l'utilisateur et le mot de passe
$env:PGPASSWORD = "postgres"  # Changez si nécessaire

try {
    # Tester la connexion
    psql -U postgres -h localhost -c "SELECT version();" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Connexion à PostgreSQL réussie" -ForegroundColor Green
        
        # Créer la base de données si elle n'existe pas
        psql -U postgres -h localhost -c "SELECT 1 FROM pg_database WHERE datname='kokoro_tts';" -t | Out-Null
        if ($LASTEXITCODE -ne 0) {
            psql -U postgres -h localhost -c "CREATE DATABASE kokoro_tts;"
            Write-Host "✅ Base de données 'kokoro_tts' créée" -ForegroundColor Green
        } else {
            Write-Host "ℹ️  Base de données 'kokoro_tts' existe déjà" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "⚠️  Impossible d'exécuter psql automatiquement" -ForegroundColor Yellow
    Write-Host "   Créez manuellement la base de données avec:" -ForegroundColor Gray
    Write-Host "   psql -U postgres -c 'CREATE DATABASE kokoro_tts;'" -ForegroundColor Gray
}

# Définir les variables d'environnement
Write-Host "`nConfiguration des variables d'environnement..." -ForegroundColor Cyan
Write-Host "`nUtilisez ces commandes:" -ForegroundColor Yellow
Write-Host '$env:DATABASE_URL="postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/kokoro_tts"' -ForegroundColor White
Write-Host '$env:SECRET_KEY="dev-secret-key-change-in-production"' -ForegroundColor White
Write-Host "`n(Remplacez VOTRE_MOT_DE_PASSE par votre mot de passe PostgreSQL)" -ForegroundColor Gray



