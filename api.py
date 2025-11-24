import logging
import os
import subprocess
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr
from starlette.concurrency import run_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from subprocess import CalledProcessError, TimeoutExpired

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI(
    title="Kokoro TTS API",
    description="API de synthèse vocale utilisant Kokoro",
    version="1.0.0"
)

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
    "https://tts-programme.onrender.com",
    "http://localhost:5173",  # Vite dev server
    "http://localhost:4173",  # Vite preview server
    "http://127.0.0.1:5173",
    "http://127.0.0.1:4173",
    # Railway.app - ajoutez votre URL Railway ici après déploiement
    # Exemple: "https://your-app.up.railway.app"
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
        "https://tts-programme.onrender.com",
        "http://localhost:5173",
        "http://localhost:4173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
    ]
    allow_origin = origin if origin in allowed_origins else allowed_origins[0]
    
    logging.error(f"Global exception: {str(exc)}")
    logging.error(traceback.format_exc())
    
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
        "https://tts-programme.onrender.com",
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
        "https://tts-programme.onrender.com",
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
        return JSONResponse(
            status_code=500,
            content={"detail": f"La génération audio a échoué: {error_msg[:200]}"},
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
