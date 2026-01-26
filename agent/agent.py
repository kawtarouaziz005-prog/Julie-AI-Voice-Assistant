import os
import requests
from dotenv import load_dotenv
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SYSTEM_PROMPT = """
Contexte:
Tu es Julie, assistante virtuelle spécialisée en assurance.

Objectif:
Répondre aux clients de manière professionnelle et claire.

Scope:
- Identifier si la demande est un sinistre ou une FAQ
- Donner des réponses simples et utiles

Tone:
Professionnel, calme et empathique

Action:
Répondre à la demande et indiquer le statut

Résultat:
Retourner une réponse claire + statut
"""

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("DEBUG GROQ_API_KEY =", GROQ_API_KEY)
def get_ai_response(user_text):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    data = response.json()

    # extraction آمنة للنص
    answer = ""
    if "choices" in data:
        answer = data["choices"][0]["message"]["content"]
    elif "output" in data:
        answer = data["output"][0]["content"][0]["text"]
    else:
        answer = str(data)

    # classification بسيطة
    statut = "faq"
    if "accident" in user_text.lower() or "sinistre" in user_text.lower():
        statut = "sinistre"

    return {
        "reponse_ia": answer,
        "statut": statut
    }

if __name__ == "__main__":
    test_text = "تعرضت لحادث سيارة شنو ندير؟"
    result = get_ai_response(test_text)
    print(result)
