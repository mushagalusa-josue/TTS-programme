import logging
import os
import subprocess
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, constr
from starlette.concurrency import run_in_threadpool
from subprocess import CalledProcessError, TimeoutExpired

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()

# Autoriser le frontend Vercel
origins = [
    "https://tts-programme.vercel.app",  # remplace par ton vrai domaine Vercel
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir les fichiers générés
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")


class TTSRequest(BaseModel):
    text: constr(strip_whitespace=True, min_length=1, max_length=500)

VOICE = "ff_siwis"

@app.post("/tts")
async def generate_tts(request: TTSRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Le texte ne peut pas être vide.")

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

    try:
        def _run():
            return subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                timeout=120,  # Augmenté à 120 secondes pour la génération TTS
            )

        completed_process = await run_in_threadpool(_run)
        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Le fichier audio n'a pas été généré.")
        logging.info(
            "TTS generated successfully: %s",
            completed_process.stdout.strip() or "No output",
        )
        return {"audio_file": f"/outputs/{output_file}"}
    except TimeoutExpired:
        logging.error("TTS generation timed out after 120 seconds.")
        raise HTTPException(status_code=504, detail="La génération audio a pris trop de temps. Veuillez réessayer avec un texte plus court.")
    except CalledProcessError as e:
        logging.error("TTS generation failed: %s", e.stderr or e.stdout or str(e))
        raise HTTPException(status_code=500, detail="La génération audio a échoué.")
