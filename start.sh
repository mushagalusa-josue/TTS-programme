#!/bin/sh
set -e  # Arrêter en cas d'erreur

# Script de démarrage pour Render

echo "=== Starting Render service ==="

# Afficher la version de Python
echo "Python version:"
python --version

# Afficher le port
echo "PORT environment variable: $PORT"
PORT=${PORT:-10000}
echo "Using port: $PORT"

# Vérifier que uvicorn est installé
echo "Checking uvicorn..."
if ! python -m uvicorn --version; then
    echo "ERROR: uvicorn not found!"
    exit 1
fi

# Vérifier que l'API peut être importée
echo "Checking API import..."
if ! python -c "import api; print('API imported successfully')"; then
    echo "ERROR: API import failed!"
    exit 1
fi

# Démarrer le serveur
echo "Starting uvicorn on port $PORT..."
exec python -m uvicorn api:app --host 0.0.0.0 --port $PORT

