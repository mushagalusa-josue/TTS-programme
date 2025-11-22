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

# 6. Passer à l'utilisateur non-root AVANT d'installer les dépendances
USER appuser

# 7. Installer les dépendances Python en tant qu'utilisateur non-root
RUN pip install --no-cache-dir --user -r requirements.txt

# 8. Ajouter le répertoire local bin au PATH pour l'utilisateur
ENV PATH=/home/appuser/.local/bin:$PATH

# 9. Exposer le port (Render utilise le port défini par la variable PORT, généralement 10000)
EXPOSE 10000

# 10. Démarrer le serveur FastAPI (port configurable via variable d'environnement PORT)
# Utiliser le python du PATH qui inclut maintenant /home/appuser/.local/bin
# Render définit automatiquement PORT, donc on utilise cette variable
CMD ["sh", "-c", "python -m uvicorn api:app --host 0.0.0.0 --port ${PORT:-10000}"]


