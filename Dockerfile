# 1. Image de base Python 3.10 légère
FROM python:3.10-slim

# 2. Installer Git et dépendances système nécessaires
RUN apt-get update && apt-get install -y git && apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. Créer un utilisateur non-root pour exécuter l'application
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/outputs && \
    chown -R appuser:appuser /app

# 4. Définir le dossier de travail
WORKDIR /app

# 5. Copier les fichiers du projet
COPY --chown=appuser:appuser . /app

# 6. Installer les dépendances Python en tant que root (plus simple et fiable)
RUN pip install --no-cache-dir -r requirements.txt

# 7. Passer à l'utilisateur non-root après l'installation
USER appuser

# Note: Les modèles kokoro seront téléchargés automatiquement au premier usage
# Cela peut prendre quelques minutes la première fois, mais évite de faire échouer le build

# 8. Exposer le port (Railway définit automatiquement PORT)
EXPOSE 8080

# 9. Démarrer le serveur FastAPI
# Railway définit automatiquement la variable PORT
# Bind sur 0.0.0.0 comme requis
CMD python -m uvicorn api:app --host 0.0.0.0 --port ${PORT:-8080}


