# Build stage - pour installer les dépendances
FROM python:3.10-slim as builder

# Installer Git et dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier requirements.txt (utiliser la version optimisée si disponible)
COPY requirements*.txt ./

# Installer PyTorch CPU-only d'abord (plus léger, ~1.5GB au lieu de ~3GB)
# Puis installer les autres dépendances
RUN pip install --no-cache-dir --user torch==2.9.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir --user $(grep -v "^torch" requirements.txt) && \
    # Nettoyer les caches et fichiers inutiles pour réduire la taille
    find /root/.local -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true && \
    find /root/.local -type f -name "*.pyc" -delete 2>/dev/null || true && \
    find /root/.local -type f -name "*.pyo" -delete 2>/dev/null || true

# Runtime stage - image finale minimale
FROM python:3.10-slim

# Installer uniquement Git (nécessaire pour kokoro)
RUN apt-get update && apt-get install -y --no-install-recommends git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/outputs && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copier les dépendances installées depuis le builder
COPY --from=builder /root/.local /home/appuser/.local

# Copier les fichiers du projet
COPY --chown=appuser:appuser . /app

# Passer à l'utilisateur non-root
USER appuser

# Ajouter le répertoire local bin au PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Note: Les modèles kokoro seront téléchargés automatiquement au premier usage
# Cela peut prendre quelques minutes la première fois, mais évite de faire échouer le build

# Exposer le port (Railway définit automatiquement PORT)
EXPOSE 8080

# Démarrer le serveur FastAPI
CMD python -m uvicorn api:app --host 0.0.0.0 --port ${PORT:-8080}


