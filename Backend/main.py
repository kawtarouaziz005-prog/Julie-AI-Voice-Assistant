import os
import shutil
from fastapi import FastAPI, UploadFile, File
from Audio.audio_expert import speech_to_text
from agent.agent import get_ai_response

app = FastAPI()
os.makedirs("temp_audio", exist_ok=True)

@app.post("/process")
async def process_call(file: UploadFile = File(...)):
    # Sauvegarde
    file_path = os.path.join("temp_audio", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Transcription (Fatima)
    transcription = speech_to_text(file_path)
    
    # IA (Imad)
    resultat_ia = get_ai_response(transcription)
    
    # RÉPONSE FINALE (Contrat JSON)
    return {
        "transcription": transcription,
        "reponse_ia": resultat_ia.get("reponse_ia", ""),
        "audio_url": f"/audio/{file.filename}",
        "statut": resultat_ia.get("statut", "attente")
    }