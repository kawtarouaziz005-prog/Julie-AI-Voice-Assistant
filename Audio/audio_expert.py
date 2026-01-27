import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(token=HF_TOKEN)

def speech_to_text(chemin_fichier_audio):
    
    if client is None:
        return "Erreur Configuration : Clé API manquante."
    
    if not os.path.exists(chemin_fichier_audio):
        return f"Erreur : Le fichier {chemin_fichier_audio} est introuvable."

   
    try:
       
        reponse = client.automatic_speech_recognition(
            audio=chemin_fichier_audio,
            model="openai/whisper-large-v3-turbo"
        )
        return reponse.text
        
    except Exception as e:
        return f"Erreur de transcription : {str(e)}"
