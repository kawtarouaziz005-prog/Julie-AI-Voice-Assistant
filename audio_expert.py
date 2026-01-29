
import os
import asyncio          # Pour gérer la vitesse 
import edge_tts         # Le moteur de voix 
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# On définit la "personnalité" de la voix ici 
VOIX_JULIE = "fr-FR-VivienneNeural"  
FICHIER_SORTIE_DEFAULT = "reponse_julie.mp3"

# Initialisation du client d'écoute 
if not HF_TOKEN:
    print("ATTENTION : La clé 'HF_TOKEN' est absente du fichier .env !")
    client_whisper = None
else:
    client_whisper = InferenceClient(token=HF_TOKEN)



def speech_to_text(chemin_fichier_audio):
    # Vérifications de sécurité
    if client_whisper is None:
        return "Erreur technique : API non configurée."
    
    if not os.path.exists(chemin_fichier_audio):
        return f"Erreur : Le fichier audio '{chemin_fichier_audio}' est introuvable."


    try:
        
        resultat = client_whisper.automatic_speech_recognition(
            audio=chemin_fichier_audio,
            model="openai/whisper-large-v3-turbo"
        )
        
        texte_transcrit = resultat.text
        print(f"le test  '{texte_transcrit}'")
        return texte_transcrit

    except Exception as erreur:
        print(f"erreur TTS : {erreur}")
        return "Désolé, je n'ai pas pu transcrire l'audio."


#Text-to-Speech
async def _moteur_voix_interne(texte, fichier_sortie, emotion):
   
    # Voix normale
    vitesse = "+0%"
    tonalite = "+0Hz"

    # On adapte la voix au contexte
    if emotion == "rapide":
        vitesse = "+20%"  # Julie est pressée
    elif emotion == "calme":
        vitesse = "-10%"  # Julie explique doucement
        tonalite = "-2Hz" # Voix plus posée

    communication = edge_tts.Communicate(texte, VOIX_JULIE, rate=vitesse, pitch=tonalite)
    await communication.save(fichier_sortie)


def text_to_speech(texte_a_dire, emotion="neutre"):
    
    print(f"Génération de la voix ({emotion}) pour : '{texte_a_dire[:30]} en cours '")
    
    try:
       
        boucle = asyncio.new_event_loop()
        asyncio.set_event_loop(boucle)
        
        boucle.run_until_complete(
            _moteur_voix_interne(texte_a_dire, FICHIER_SORTIE_DEFAULT, emotion)
        )
        boucle.close()

        if os.path.exists(FICHIER_SORTIE_DEFAULT):
            print(f"Fichier audio prêt : {FICHIER_SORTIE_DEFAULT}")
            return FICHIER_SORTIE_DEFAULT
        else:
            return "Erreur : Le fichier n'a pas été créé."

    except Exception as erreur:
        return f"Erreur critique TTS : {str(erreur)}"


if __name__ == "__main__":
    print("\nphase de test")
    
    # Test 1 : La voix
    phrase_test = "Je suis votre assistant intelligent, conçu pour vous aider simplement et efficacement. Vous pouvez me parler naturellement, comme à une vraie personne. J’écoute votre voix, je la comprends, puis je vous réponds à l’oral."
    fichier = text_to_speech(phrase_test, emotion="calme")
    
    
    if os.path.exists(fichier):
        print("Test validé ! Tu peux écouter 'reponse_julie.mp3'.")
    else:
        print("Test échoué.")