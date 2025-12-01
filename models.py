"""
Modèles de base de données SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text
from sqlalchemy.sql import func
from database import Base
import json


class User(Base):
    """
    Modèle utilisateur avec toutes les informations nécessaires
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Informations utilisateur
    name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Métadonnées
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Données utilisateur (stockées en JSON)
    # Voix favorites: ["ff_siwis", "voice2", ...]
    favorite_voices = Column(JSON, default=list)
    
    # Historique: liste d'objets avec {text, voice, created_at, audio_file}
    history = Column(JSON, default=list)
    
    # Crédits: nombre de générations restantes (None = illimité)
    credits = Column(Integer, nullable=True, default=None)
    
    # Préférences utilisateur
    preferences = Column(JSON, default=dict)  # Ex: {"default_voice": "ff_siwis", "default_speed": 1.0}
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
    
    def to_dict(self):
        """
        Convertir l'utilisateur en dictionnaire (sans le mot de passe)
        """
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "favorite_voices": self.favorite_voices or [],
            "credits": self.credits,
            "preferences": self.preferences or {},
        }



