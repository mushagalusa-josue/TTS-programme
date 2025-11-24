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

# 7. Pré-télécharger les modèles kokoro pour éviter le téléchargement au runtime
# Cela peut prendre plusieurs minutes mais évite les timeouts en production
RUN python -m kokoro --voice ff_siwis --text "test" --output-file /tmp/test_model_download.wav --speed 1.0 || true
RUN rm -f /tmp/test_model_download.wav || true

# 8. Passer à l'utilisateur non-root après l'installation
USER appuser

# 8. Exposer le port (Render définit automatiquement PORT, généralement 10000)
EXPOSE 10000

# 9. Démarrer le serveur FastAPI
# Render définit automatiquement la variable PORT (généralement 10000)
# Bind sur 0.0.0.0 comme requis par Render
CMD ["sh", "-c", "python -m uvicorn api:app --host 0.0.0.0 --port ${PORT:-10000}"]


