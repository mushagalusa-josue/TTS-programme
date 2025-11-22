# 1. Image de base Python 3.10 légère
FROM python:3.10-slim

# 2. Définir le dossier de travail
WORKDIR /app

# 3. Copier les fichiers du projet
COPY . /app

# 4. Installer Git et dépendances système nécessaires
RUN apt-get update && apt-get install -y git && apt-get clean && rm -rf /var/lib/apt/lists/*

# 5. Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Créer le dossier pour les sorties audio
RUN mkdir -p /app/outputs

# 7. Exposer le port (configurable via PORT env var, défaut 8000)
EXPOSE 8000

# 8. Démarrer le serveur FastAPI (port configurable via variable d'environnement PORT)
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]


