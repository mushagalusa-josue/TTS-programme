import logging
import os
import subprocess
import uuid
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, constr, EmailStr
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from subprocess import CalledProcessError, TimeoutExpired

# Imports pour l'authentification
from database import get_db, init_db
from models import User
from auth import verify_password, get_password_hash, create_access_token, decode_access_token, validate_password

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI(
    title="Kokoro TTS API",
    description="API de synthèse vocale utilisant Kokoro",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Handler de démarrage pour diagnostiquer les problèmes"""
    # Limiter l'utilisation mémoire de PyTorch pour éviter les SIGKILL sur Railway
    os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:128")
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    
    logging.info("=" * 50)
    logging.info("FastAPI application starting...")
    logging.info(f"PORT environment variable: {os.environ.get('PORT', 'not set')}")
    logging.info(f"Output directory: {OUTPUT_DIR}")
    logging.info(f"Output directory exists: {os.path.exists(OUTPUT_DIR)}")
    logging.info(f"PYTORCH_CUDA_ALLOC_CONF: {os.environ.get('PYTORCH_CUDA_ALLOC_CONF', 'not set')}")
    logging.info(f"OMP_NUM_THREADS: {os.environ.get('OMP_NUM_THREADS', 'not set')}")
    
    # Initialiser la base de données
    try:
        init_db()
    except Exception as e:
        logging.warning(f"Database initialization failed (might be expected if DB not available): {e}")
    
    logging.info("=" * 50)

# Middleware pour logger les requêtes
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin", "no origin")
        logging.info(f"{request.method} {request.url.path} from {request.client.host if request.client else 'unknown'} (origin: {origin})")
        response = await call_next(request)
        cors_headers = {k: v for k, v in response.headers.items() if k.lower().startswith("access-control")}
        logging.info(f"Response: {response.status_code}, CORS headers: {cors_headers}")
        return response

# Autoriser le frontend et les domaines de déploiement
origins = [
    "https://tts-programme.vercel.app",
    "https://kokoro-tts-api-production-b52e.up.railway.app",
    "http://localhost:5173",  # Vite dev server
    "http://localhost:4173",  # Vite preview server
    "http://localhost:8000",  # API locale
    "http://127.0.0.1:5173",
    "http://127.0.0.1:4173",
    "http://127.0.0.1:8000",  # API locale
]

# Configuration CORS - doit être ajouté en premier (dernier dans la liste)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Middleware de logging - ajouté après CORS
app.add_middleware(LoggingMiddleware)

# Exception handler global pour s'assurer que les headers CORS sont toujours présents
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler global pour s'assurer que les headers CORS sont toujours présents même en cas d'erreur"""
    from fastapi.responses import JSONResponse
    import traceback
    
    origin = request.headers.get("origin", "")
    allowed_origins = [
        "https://tts-programme.vercel.app",
        "https://kokoro-tts-api-production-b52e.up.railway.app",
        "http://localhost:5173",
        "http://localhost:4173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
    ]
    allow_origin = origin if origin in allowed_origins else allowed_origins[0]
    
    error_detail = str(exc)
    error_traceback = traceback.format_exc()
    logging.error(f"Global exception: {error_detail}")
    logging.error(error_traceback)
    
    return JSONResponse(
        status_code=500,
        content={"detail": f"Erreur serveur: {str(exc)[:200]}"},
        headers={
            "Access-Control-Allow-Origin": allow_origin,
            "Access-Control-Allow-Credentials": "true",
        }
    )

# Servir les fichiers générés
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

# ==================== AUTHENTIFICATION ====================

# Security scheme pour JWT
security = HTTPBearer()


# Modèles Pydantic pour l'authentification
class UserRegister(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=100)
    name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


# Dependency pour obtenir l'utilisateur actuel depuis le token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Récupérer l'utilisateur actuel depuis le token JWT
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte utilisateur désactivé"
        )
    
    return user


# Route d'inscription
@app.post("/api/auth/register", response_model=TokenResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Inscription d'un nouvel utilisateur
    """
    try:
        # Valider la force du mot de passe
        is_valid, error_message = validate_password(user_data.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Vérifier si l'email existe déjà
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cet email est déjà utilisé"
            )
        
        # Créer le nouvel utilisateur
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            name=user_data.name,
            is_active=True,
            favorite_voices=[],
            history=[],
            credits=None,  # Illimité par défaut
            preferences={}
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Créer le token JWT
        access_token = create_access_token(data={"sub": new_user.id})
        
        logging.info(f"New user registered: {new_user.email}")
        
        return TokenResponse(
            access_token=access_token,
            user=new_user.to_dict()
        )
    except HTTPException:
        # Re-raise les HTTPException (erreurs de validation)
        raise
    except Exception as e:
        # Logger toutes les autres erreurs pour le débogage
        logging.error(f"Error during user registration: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'inscription: {str(e)}"
        )


# Route de connexion
@app.post("/api/auth/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Connexion d'un utilisateur
    """
    # Trouver l'utilisateur
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    # Vérifier le mot de passe
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    # Vérifier si le compte est actif
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte utilisateur désactivé"
        )
    
    # Mettre à jour la date de dernière connexion
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Créer le token JWT
    access_token = create_access_token(data={"sub": user.id})
    
    logging.info(f"User logged in: {user.email}")
    
    return TokenResponse(
        access_token=access_token,
        user=user.to_dict()
    )


# Route pour obtenir les informations de l'utilisateur actuel
@app.get("/api/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Obtenir les informations de l'utilisateur actuellement connecté
    """
    return current_user.to_dict()


# Route pour mettre à jour les préférences utilisateur
@app.put("/api/auth/preferences")
async def update_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mettre à jour les préférences de l'utilisateur
    """
    current_user.preferences = preferences
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Préférences mises à jour", "preferences": current_user.preferences}


# Route pour ajouter une voix favorite
@app.post("/api/auth/favorite-voice/{voice_name}")
async def add_favorite_voice(
    voice_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ajouter une voix aux favoris
    """
    if current_user.favorite_voices is None:
        current_user.favorite_voices = []
    
    if voice_name not in current_user.favorite_voices:
        current_user.favorite_voices.append(voice_name)
        db.commit()
    
    return {"message": "Voix ajoutée aux favoris", "favorite_voices": current_user.favorite_voices}


# ==================== FIN AUTHENTIFICATION ====================


@app.get("/")
async def root():
    """Route racine - Informations sur l'API"""
    return {
        "message": "Kokoro TTS API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "tts": "/tts (POST)",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Route de santé pour les vérifications de disponibilité"""
    # Vérifier si kokoro est accessible
    python_cmd = os.environ.get("PYTHON_CMD", "python")
    try:
        result = subprocess.run(
            [python_cmd, "-m", "kokoro", "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        kokoro_available = result.returncode == 0
    except:
        kokoro_available = False
    
    return {
        "status": "healthy",
        "service": "kokoro-tts-api",
        "kokoro_available": kokoro_available
    }


@app.get("/healthy")
@app.head("/healthy")
async def healthy_check():
    """Route de santé alternative pour compatibilité avec Render"""
    return {"status": "healthy", "service": "kokoro-tts-api"}


@app.get("/test-kokoro")
async def test_kokoro():
    """Endpoint de test pour vérifier que kokoro fonctionne"""
    python_cmd = os.environ.get("PYTHON_CMD", "python")
    test_output = os.path.join(OUTPUT_DIR, "test_kokoro.wav")
    
    try:
        # Test simple avec un texte court
        cmd = [
            python_cmd,
            "-m", "kokoro",
            "--voice", "ff_siwis",
            "--text", "test",
            "--output-file", test_output,
            "--speed", "1.0"
        ]
        
        logging.info(f"Testing kokoro with command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes pour permettre le téléchargement des modèles
        )
        
        success = result.returncode == 0 and os.path.exists(test_output)
        
        return {
            "kokoro_available": True,
            "test_successful": success,
            "return_code": result.returncode,
            "stdout": result.stdout[:500] if result.stdout else None,
            "stderr": result.stderr[:500] if result.stderr else None,
            "output_file_exists": os.path.exists(test_output),
        }
    except subprocess.TimeoutExpired:
        return {
            "kokoro_available": True,
            "test_successful": False,
            "error": "Timeout after 60 seconds"
        }
    except Exception as e:
        logging.error(f"Error testing kokoro: {str(e)}", exc_info=True)
        return {
            "kokoro_available": False,
            "test_successful": False,
            "error": str(e)[:200]
        }


class TTSRequest(BaseModel):
    text: constr(strip_whitespace=True, min_length=1, max_length=500)

VOICE = "ff_siwis"

@app.options("/tts")
async def options_tts(request: Request):
    """Handler OPTIONS explicite pour CORS"""
    from fastapi.responses import Response
    origin = request.headers.get("origin", "")
    # Vérifier si l'origine est autorisée
    allowed_origins = [
        "https://tts-programme.vercel.app",
        "https://kokoro-tts-api-production-b52e.up.railway.app",
        "http://localhost:5173",
        "http://localhost:4173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
    ]
    allow_origin = origin if origin in allowed_origins else allowed_origins[0]
    
    logging.info(f"OPTIONS /tts from origin: {origin}, allowing: {allow_origin}")
    
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": allow_origin,
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "3600",
        }
    )

@app.post("/tts")
async def generate_tts(request: TTSRequest, http_request: Request):
    # Récupérer l'origine pour les headers CORS dans les erreurs
    origin = http_request.headers.get("origin", "")
    allowed_origins = [
        "https://tts-programme.vercel.app",
        "https://kokoro-tts-api-production-b52e.up.railway.app",
        "http://localhost:5173",
        "http://localhost:4173",
    ]
    allow_origin = origin if origin in allowed_origins else allowed_origins[0]
    
    logging.info("POST /tts received - Starting TTS generation")
    text = request.text.strip()
    logging.info(f"Text received: {text[:50]}... (length: {len(text)})")
    if not text:
        logging.warning("Empty text received")
        return JSONResponse(
            status_code=400,
            content={"detail": "Le texte ne peut pas être vide."},
            headers={
                "Access-Control-Allow-Origin": allow_origin,
                "Access-Control-Allow-Credentials": "true",
            }
        )

    output_file = f"output_{uuid.uuid4().hex}.wav"
    output_path = os.path.join(OUTPUT_DIR, output_file)

    # Utiliser python du système (fonctionne sur Linux/Docker)
    python_cmd = os.environ.get("PYTHON_CMD", "python")
    cmd = [
        python_cmd,
        "-m", "kokoro",
        "--voice", VOICE,
        "--text", text,
        "--output-file", output_path,
        "--speed", "1.0"
    ]

    logging.info(f"Executing command: {' '.join(cmd)}")
    logging.info(f"Output file will be: {output_path}")

    try:
        def _run():
            logging.info("Starting kokoro subprocess...")
            try:
                result = subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minutes pour permettre le téléchargement des modèles si nécessaire
                )
                logging.info(f"Subprocess completed. Return code: {result.returncode}")
                if result.stdout:
                    logging.info(f"Subprocess stdout (first 1000 chars): {result.stdout[:1000]}")
                if result.stderr:
                    logging.warning(f"Subprocess stderr (first 1000 chars): {result.stderr[:1000]}")
                return result
            except subprocess.TimeoutExpired as e:
                logging.error(f"kokoro subprocess timed out after 120 seconds")
                raise
            except subprocess.CalledProcessError as e:
                logging.error(f"kokoro subprocess failed with return code {e.returncode}")
                logging.error(f"stdout: {e.stdout[:1000] if e.stdout else 'None'}")
                logging.error(f"stderr: {e.stderr[:1000] if e.stderr else 'None'}")
                raise
            except Exception as e:
                logging.error(f"Unexpected error in subprocess: {str(e)}", exc_info=True)
                raise

        logging.info("Running kokoro in threadpool...")
        completed_process = await run_in_threadpool(_run)
        logging.info("Threadpool execution completed successfully")
        if not os.path.exists(output_path):
            return JSONResponse(
                status_code=500,
                content={"detail": "Le fichier audio n'a pas été généré."},
                headers={
                    "Access-Control-Allow-Origin": allow_origin,
                    "Access-Control-Allow-Credentials": "true",
                }
            )
        logging.info(
            "TTS generated successfully: %s",
            completed_process.stdout.strip() or "No output",
        )
        # Retourner avec headers CORS
        response = JSONResponse(
            content={"audio_file": f"/outputs/{output_file}"},
            headers={
                "Access-Control-Allow-Origin": allow_origin,
                "Access-Control-Allow-Credentials": "true",
            }
        )
        return response
    except TimeoutExpired:
        logging.error("TTS generation timed out after 120 seconds.")
        return JSONResponse(
            status_code=504,
            content={"detail": "La génération audio a pris trop de temps. Veuillez réessayer avec un texte plus court."},
            headers={
                "Access-Control-Allow-Origin": allow_origin,
                "Access-Control-Allow-Credentials": "true",
            }
        )
    except CalledProcessError as e:
        error_msg = e.stderr or e.stdout or str(e)
        logging.error("TTS generation failed: %s", error_msg)
        logging.error("Command: %s", " ".join(cmd))
        
        # Détecter si c'est un SIGKILL (processus tué par le système)
        if "SIGKILL" in str(e) or e.returncode == -9:
            detail_msg = "Le processus a été tué par le système (dépassement de mémoire). Railway free tier a des limites strictes. Essayez avec un texte plus court ou passez à un plan payant."
        else:
            detail_msg = f"La génération audio a échoué: {error_msg[:200]}"
        
        return JSONResponse(
            status_code=500,
            content={"detail": detail_msg},
            headers={
                "Access-Control-Allow-Origin": allow_origin,
                "Access-Control-Allow-Credentials": "true",
            }
        )
    except Exception as e:
        logging.error("Unexpected error: %s", str(e), exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": f"Erreur inattendue: {str(e)[:200]}"},
            headers={
                "Access-Control-Allow-Origin": allow_origin,
                "Access-Control-Allow-Credentials": "true",
            }
        )
