"""
Julie Assistant - AI Insurance Voice Assistant
Sprint 2: Professional pitch-ready interface with voice playback and recording
"""

import streamlit as st
import requests
import random
from datetime import datetime, timedelta
import io

# ============================================================================
# CONFIGURATION
# ============================================================================

BACKEND_URL = "http://127.0.0.1:8000/process"
APP_TITLE = "Julie Assistant"
APP_SUBTITLE = "Assistante Vocale Intelligente pour l'Assurance"

# ============================================================================
# MOCK DATA GENERATION
# ============================================================================

def generate_mock_client_data():
    """Generate realistic mock client data for demo purposes"""
    first_names = ["Sophie", "Jean", "Marie", "Pierre", "Isabelle", "Thomas", "Nathalie", "Laurent"]
    last_names = ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Petit", "Durand", "Leroy"]
    
    client_data = {
        "nom_complet": f"{random.choice(first_names)} {random.choice(last_names)}",
        "numero_police": f"POL-{random.randint(100000, 999999)}",
        "id_sinistre": f"SIN-{random.randint(10000, 99999)}",
        "type_assurance": random.choice(["Auto", "Habitation", "Santé", "Vie"]),
        "date_souscription": (datetime.now() - timedelta(days=random.randint(365, 1825))).strftime("%d/%m/%Y"),
        "statut": random.choice(["Actif", "En cours de traitement", "À renouveler"])
    }
    return client_data

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_mime_type(filename):
    """Detect MIME type from filename extension"""
    ext = filename.lower().split('.')[-1]
    mime_types = {
        'wav': 'audio/wav',
        'mp3': 'audio/mpeg',
        'm4a': 'audio/mp4',
        'ogg': 'audio/ogg',
        'webm': 'audio/webm'
    }
    return mime_types.get(ext, 'audio/wav')

# ============================================================================
# UI COMPONENTS
# ============================================================================

def display_header():
    """Display application header with branding"""
    st.markdown(
        """
        <style>
        .main-header {
            background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5rem;
        }
        .main-header p {
            color: #e0e7ff;
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div class="main-header">
            <h1>🎙️ {APP_TITLE}</h1>
            <p>{APP_SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_client_card(client_data):
    """Display professional client information card"""
    st.markdown(
        """
        <style>
        .client-card {
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .client-card h3 {
            color: #1e3a8a;
            margin-top: 0;
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid #f3f4f6;
        }
        .info-row:last-child {
            border-bottom: none;
        }
        .info-label {
            font-weight: 600;
            color: #4b5563;
        }
        .info-value {
            color: #1f2937;
        }
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
        }
        .status-actif {
            background-color: #d1fae5;
            color: #065f46;
        }
        .status-traitement {
            background-color: #fef3c7;
            color: #92400e;
        }
        .status-renouveler {
            background-color: #dbeafe;
            color: #1e40af;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    status_class = "status-actif"
    if "traitement" in client_data["statut"].lower():
        status_class = "status-traitement"
    elif "renouveler" in client_data["statut"].lower():
        status_class = "status-renouveler"
    
    st.markdown(
        f"""
        <div class="client-card">
            <h3>📋 Dossier Client</h3>
            <div class="info-row">
                <span class="info-label">👤 Client:</span>
                <span class="info-value">{client_data["nom_complet"]}</span>
            </div>
            <div class="info-row">
                <span class="info-label">🔢 N° Police:</span>
                <span class="info-value">{client_data["numero_police"]}</span>
            </div>
            <div class="info-row">
                <span class="info-label">📄 ID Sinistre:</span>
                <span class="info-value">{client_data["id_sinistre"]}</span>
            </div>
            <div class="info-row">
                <span class="info-label">🛡️ Type:</span>
                <span class="info-value">{client_data["type_assurance"]}</span>
            </div>
            <div class="info-row">
                <span class="info-label">📅 Souscription:</span>
                <span class="info-value">{client_data["date_souscription"]}</span>
            </div>
            <div class="info-row">
                <span class="info-label">✅ Statut:</span>
                <span class="info-value">
                    <span class="status-badge {status_class}">{client_data["statut"]}</span>
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_response_section(transcription, response_ia, audio_url):
    """Display transcription, AI response, and audio player"""
    
    st.markdown("### 🎤 Transcription")
    st.info(transcription if transcription else "Aucune transcription disponible")
    
    st.markdown("---")
    
    st.markdown("### 💬 Réponse de Julie")
    st.success(response_ia if response_ia else "Aucune réponse disponible")
    
    if audio_url:
        st.markdown("### 🔊 Réponse Vocale")
        try:
            if audio_url.startswith("http://") or audio_url.startswith("https://"):
                audio_response = requests.get(audio_url, timeout=10)
                
                if audio_response.status_code == 200:
                    st.audio(audio_response.content, format="audio/wav", autoplay=True)
                    st.caption("🎵 Audio en cours de lecture automatique")
                else:
                    st.warning("⚠️ Audio non disponible (erreur serveur)")
            else:
                with open(audio_url, "rb") as f:
                    st.audio(f.read(), format="audio/wav", autoplay=True)
                    st.caption("🎵 Audio en cours de lecture automatique")
        except requests.exceptions.RequestException as e:
            st.warning(f"⚠️ Impossible de charger l'audio: {str(e)}")
        except FileNotFoundError:
            st.warning(f"⚠️ Fichier audio introuvable: {audio_url}")
        except Exception as e:
            st.warning(f"⚠️ Erreur audio: {str(e)}")
    else:
        st.warning("⚠️ Aucun audio disponible")

def send_audio_to_backend(audio_data, filename="audio.wav"):
    """
    Send audio file to backend for processing
    Returns: dict with transcription, reponse_ia, and audio_url
    """
    try:
        mime_type = get_mime_type(filename)
        
        audio_buffer = io.BytesIO(audio_data)
        audio_buffer.name = filename
        
        files = {
            "file": (
                filename,
                audio_buffer,
                mime_type
            )
        }
        
        response = requests.post(BACKEND_URL, files=files, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ Erreur backend (code {response.status_code}): {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("❌ Délai d'attente dépassé. Le serveur ne répond pas.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Impossible de se connecter au serveur. Vérifiez que le backend est démarré.")
        return None
    except Exception as e:
        st.error(f"❌ Erreur inattendue: {str(e)}")
        return None

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application logic"""
    
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f9fafb;
        }
        .uploadedFile {
            border: 2px dashed #3b82f6;
            border-radius: 10px;
            padding: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    display_header()
    
    if "client_data" not in st.session_state:
        st.session_state.client_data = generate_mock_client_data()
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        display_client_card(st.session_state.client_data)
        
        if st.button("🔄 Nouveau Client", use_container_width=True):
            st.session_state.client_data = generate_mock_client_data()
            st.rerun()
    
    with col1:
        st.markdown("### 📤 Envoi Audio")
        
        input_method = st.radio(
            "Choisissez une méthode:",
            ["🎙️ Enregistrer un audio", "📁 Télécharger un fichier audio"],
            horizontal=True
        )
        
        audio_data = None
        audio_filename = "audio.wav"
        
        if input_method == "🎙️ Enregistrer un audio":
            recorded_audio = st.audio_input("Cliquez pour enregistrer")
            if recorded_audio is not None:
                audio_data = recorded_audio.getvalue()
                audio_filename = recorded_audio.name if hasattr(recorded_audio, 'name') else "recorded_audio.wav"
        else:
            uploaded_file = st.file_uploader(
                "Sélectionnez un fichier audio",
                type=["wav", "mp3", "m4a", "ogg"],
                help="Formats acceptés: WAV, MP3, M4A, OGG"
            )
            if uploaded_file is not None:
                audio_data = uploaded_file.getvalue()
                audio_filename = uploaded_file.name
        
        if audio_data is not None:
            if st.button("🚀 Envoyer à Julie", type="primary", use_container_width=True):
                with st.spinner("🤔 Julie réfléchit..."):
                    result = send_audio_to_backend(audio_data, audio_filename)
                    
                    if result:
                        st.session_state.result = result
                        st.success("✅ Traitement terminé!")
                        st.rerun()
    
    st.markdown("---")
    
    if "result" in st.session_state and st.session_state.result:
        result = st.session_state.result
        display_response_section(
            transcription=result.get("transcription", ""),
            response_ia=result.get("reponse_ia", ""),
            audio_url=result.get("audio_url", "")
        )
    else:
        st.markdown(
            """
            <div style="text-align: center; padding: 3rem; color: #6b7280;">
                <h3>👆 Enregistrez ou téléchargez un fichier audio pour commencer</h3>
                <p>Julie est prête à vous assister avec vos questions d'assurance</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #6b7280; padding: 1rem;">
            <small>Julie Assistant v2.0 | Sprint 2 - Demo Ready | © 2026</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()