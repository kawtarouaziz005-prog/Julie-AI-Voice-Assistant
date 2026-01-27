"""
Julie Assistant - AI Voice Assistant Frontend
Production-ready Streamlit application for insurance use case
"""

import streamlit as st
import requests
from io import BytesIO
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

BACKEND_URL = "http://localhost:8000/process"
UPLOAD_FOLDER = "temp_audio"

# Create temp folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Julie Assistant",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .result-container {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .result-label {
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    .result-content {
        font-size: 1rem;
        line-height: 1.6;
    }
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1rem;
    }
    .status-sinistre {
        background-color: #ff6b6b;
        color: white;
    }
    .status-faq {
        background-color: #4ecdc4;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def send_audio_to_backend(audio_file):
    """
    Send audio file to FastAPI backend
    
    Args:
        audio_file: Audio file (UploadedFile or bytes)
    
    Returns:
        dict: JSON response from backend
    
    Raises:
        requests.exceptions.RequestException: If request fails
    """
    try:
        # Prepare file for upload
        files = {"file": ("audio.wav", audio_file, "audio/wav")}
        
        # Send POST request
        response = requests.post(BACKEND_URL, files=files, timeout=30)
        
        # Raise exception for bad status codes
        response.raise_for_status()
        
        # Return JSON response
        return response.json()
    
    except requests.exceptions.ConnectionError:
        raise Exception("❌ Impossible de se connecter au serveur backend. Assurez-vous qu'il est démarré sur http://localhost:8000")
    
    except requests.exceptions.Timeout:
        raise Exception("⏱️ Le serveur a mis trop de temps à répondre. Veuillez réessayer.")
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"❌ Erreur serveur (HTTP {response.status_code}): {str(e)}")
    
    except Exception as e:
        raise Exception(f"❌ Erreur inattendue: {str(e)}")


def validate_response(response_data):
    """
    Validate backend response structure
    
    Args:
        response_data: JSON response from backend
    
    Returns:
        bool: True if valid, raises Exception otherwise
    """
    required_keys = ["transcription", "reponse_ia", "statut"]
    
    for key in required_keys:
        if key not in response_data:
            raise Exception(f"❌ Réponse invalide du serveur: clé '{key}' manquante")
    
    return True


def display_results(response_data):
    """
    Display results in a formatted way
    
    Args:
        response_data: JSON response from backend
    """
    # Transcription section
    st.markdown("### 📝 Transcription")
    st.markdown(f"""
        <div class="result-container">
            <div class="result-content">{response_data['transcription']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # AI Response section
    st.markdown("### 🤖 Réponse IA")
    st.markdown(f"""
        <div class="result-container">
            <div class="result-content">{response_data['reponse_ia']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Status section
    st.markdown("### 📌 Statut")
    status = response_data['statut'].lower()
    status_class = "status-sinistre" if status == "sinistre" else "status-faq"
    status_display = status.upper()
    
    st.markdown(f"""
        <div class="result-container">
            <span class="status-badge {status_class}">{status_display}</span>
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application function"""
    
    # Title
    st.markdown('<h1 class="main-title">🎙️ Julie Assistant</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Introduction
    st.markdown("""
        Bienvenue sur **Julie Assistant**, votre assistant vocal intelligent pour l'assurance.
        
        **Instructions:**
        1. Téléchargez un fichier audio `.wav` ou enregistrez votre voix
        2. Cliquez sur "Envoyer" pour obtenir une réponse
    """)
    
    st.markdown("---")
    
    # Audio input section
    st.markdown("### 🎤 Entrée Audio")
    
    # Create tabs for upload and recording
    tab1, tab2 = st.tabs(["📁 Télécharger un fichier", "🎙️ Enregistrer"])
    
    audio_file = None
    
    with tab1:
        uploaded_file = st.file_uploader(
            "Sélectionnez un fichier audio (.wav)",
            type=["wav"],
            help="Téléchargez un fichier audio au format WAV"
        )
        if uploaded_file is not None:
            audio_file = uploaded_file
            st.audio(uploaded_file, format="audio/wav")
    
    with tab2:
        recorded_audio = st.audio_input("Enregistrez votre message")
        if recorded_audio is not None:
            audio_file = recorded_audio
            st.success("✅ Audio enregistré avec succès!")
    
    st.markdown("---")
    
    # Send button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        send_button = st.button("🚀 Envoyer", use_container_width=True, type="primary")
    
    # Process audio when button is clicked
    if send_button:
        if audio_file is None:
            st.error("⚠️ Veuillez d'abord télécharger ou enregistrer un fichier audio.")
        else:
            # Show loading spinner
            with st.spinner("🔄 Traitement en cours... Veuillez patienter."):
                try:
                    # Reset audio_file pointer to beginning
                    audio_file.seek(0)
                    
                    # Send audio to backend
                    response_data = send_audio_to_backend(audio_file)
                    
                    # Validate response
                    validate_response(response_data)
                    
                    # Display success message
                    st.success("✅ Traitement terminé avec succès!")
                    
                    st.markdown("---")
                    
                    # Display results
                    display_results(response_data)
                    
                except Exception as e:
                    st.error(str(e))
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            Julie Assistant v1.0 | Powered by AI
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()