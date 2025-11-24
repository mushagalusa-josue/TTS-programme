# Build stage
FROM python:3.10-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Installer typing-extensions avant torch => corrige le bug
RUN pip install --no-cache-dir --user typing_extensions==4.12.2

# Installer torch CPU-only (plus léger)
RUN pip install --no-cache-dir --user torch==2.9.0 --index-url https://download.pytorch.org/whl/cpu

# Installer les autres dépendances
RUN pip install --no-cache-dir --user -r requirements.txt \
    && find /root/.local -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true \
    && find /root/.local -type f -name "*.pyc" -delete 2>/dev/null || true \
    && find /root/.local -type f -name "*.pyo" -delete 2>/dev/null || true

# Runtime stage
FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser
WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8080

CMD sh -c "echo 'Starting server on port ${PORT:-8080}' && python -m uvicorn api:app --host 0.0.0.0 --port ${PORT:-8080}"
