"""
Configuration de la base de données PostgreSQL
"""
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)

# Récupérer l'URL de la base de données depuis les variables d'environnement
# Format attendu: postgresql://user:password@host:port/database
DATABASE_URL = os.environ.get("DATABASE_URL")

# Si DATABASE_URL n'est pas définie, utiliser la valeur par défaut (développement local uniquement)
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/kokoro_tts"
    logging.warning("DATABASE_URL not set in environment, using default localhost (development only)")

# Si Railway ou autre service utilise postgres:// au lieu de postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Logger l'URL (masquer le mot de passe)
db_host = DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else "unknown"
logging.info(f"Database URL configured: ***@{db_host}")

# Créer le moteur SQLAlchemy
# Forcer l'utilisation d'IPv4 si localhost est utilisé
connect_args = {}
if "localhost" in DATABASE_URL or "127.0.0.1" in DATABASE_URL:
    # Forcer IPv4 pour éviter les problèmes de résolution
    connect_args = {"connect_timeout": 10}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Vérifier la connexion avant utilisation
    pool_size=5,
    max_overflow=10,
    echo=False,  # Mettre à True pour voir les requêtes SQL en développement
    connect_args=connect_args
)

# Créer la session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()


def get_db():
    """
    Dependency pour obtenir une session de base de données
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialiser la base de données (créer les tables)
    """
    from models import User  # Import ici pour éviter les imports circulaires
    
    logging.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logging.info("Database initialized successfully")

