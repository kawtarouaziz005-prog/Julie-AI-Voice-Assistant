from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid

# Importation avec les VRAIS noms de fonctions de tes collègues
from Audio.audio_expert import speech_to_text
from agent.agent import get_ai_response

app = FastAPI(title="Julie AI - Intégration Sprint 1")

# Autoriser le Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
def health_check():
    return {"status": "Julie API is running"}

@app.post("/process")
async def process_audio(file: UploadFile = File(...)):
    # 1. Création d'un nom unique
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(TEMP_DIR, unique_filename)

    try:
        # 2. Sauvegarde du fichier
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. Transcription (Fatima)
        transcription = speech_to_text(file_path)
        
        # Vérification si Fatima a renvoyé une erreur sous forme de string
        if "Erreur" in transcription:
            raise HTTPException(status_code=500, detail=transcription)

        # 4. Réponse de l'IA (Imad)
        resultat_ia = get_ai_response(transcription)

        # 5. Retour au Frontend
        return {
            "transcription": transcription,
            "reponse_ia": resultat_ia.get("reponse_ia", ""),
            "statut": resultat_ia.get("statut", "faq")
        }

    except Exception as e:
        print(f"Erreur Backend: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # On réactive le nettoyage ici !
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Nettoyage réussi : {unique_filename} supprimé.")
            except Exception as e:
                print(f"⚠️ Impossible de supprimer le fichier : {e}")