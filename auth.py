"""
Utilitaires d'authentification: hashage de mots de passe et JWT
"""
import os
import re
from datetime import datetime, timedelta
from typing import Optional, Tuple
from jose import JWTError, jwt
import bcrypt
import logging

# Configuration JWT
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 jours

logging.info("Auth module initialized")


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Valider un mot de passe selon les critères:
    - Au moins 8 caractères
    - Au moins un caractère spécial
    - Au moins un chiffre
    - Au moins une lettre
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    
    if not re.search(r'[a-zA-Z]', password):
        return False, "Le mot de passe doit contenir au moins une lettre"
    
    if not re.search(r'[0-9]', password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password):
        return False, "Le mot de passe doit contenir au moins un caractère spécial"
    
    return True, ""


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifier un mot de passe en clair contre un hash
    """
    try:
        # hashed_password est déjà une string encodée, on doit la convertir en bytes
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
    except Exception as e:
        logging.error(f"Error verifying password: {e}")
        return False


def get_password_hash(password: str) -> str:
    """
    Hasher un mot de passe avec bcrypt
    """
    # Générer un salt et hasher le mot de passe
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Retourner en string pour stockage en base
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Créer un token JWT
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Décoder et vérifier un token JWT
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

