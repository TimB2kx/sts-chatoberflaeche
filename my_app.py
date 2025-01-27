import streamlit as st
from supabase import create_client, Client
import requests
from datetime import datetime

# Initialisiere Supabase-Client
SUPABASE_URL = "https://aws-supabase-u31663.vm.elestio.app/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlzcyI6InN1cGFiYXNlIiwiaWF0IjoxNzM3NzI5OTIzLCJleHAiOjIwNTMwODk5MjN9.L-oUAxVZHbi2QzmAy0mgFV9AA0Wql1wLkW1kYUcGmO0"
WEBHOOK_URL = "https://n8ntb.sts.support/webhook/9ba11544-5c4e-4f91-818a-08a4ecb596c5"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def logout():
    """Benutzer ausloggen und Session zurücksetzen"""
    st.session_state.authenticated = False
    st.session_state.session_id = None
    st.session_state.chat_history = []
    supabase.auth.sign_out()
    st.rerun()

def load_chat_history(conversation_id):
    """Lade den Chat-Verlauf für eine bestimmte Conversation"""
    try:
        result = supabase.table("chats").select("*").eq("conversation_id", conversation_id).order("message_order").execute()
        st.session_state.chat_history = [
            {"user": chat["message"], "bot": chat["response"]}
            for chat in result.data
        ]
        st.session_state.current_conversation_id = conversation_id
    except Exception as e:
        st.error("Fehler beim Laden des Chat-Verlaufs")

def delete_conversation(conversation_id):
    """Löscht eine Conversation und alle zugehörigen Chat-Nachrichten"""
    try:
        # Zuerst die Chat-Nachrichten löschen
        supabase.table("chats").delete().eq("conversation_id", conversation_id).execute()
        # Dann die Conversation selbst löschen
        supabase.table("conversations").delete().eq("id", conversation_id).execute()
        # Session zurücksetzen wenn der aktuelle Chat gelöscht wurde
        if st.session_state.get("current_conversation_id") == conversation_id:
            st.session_state.current_conversation_id = None
            st.session_state.chat_history = []
        st.rerun()
    except Exception as e:
        st.error("Fehler beim Löschen des Chats")

def show_login():
    """Login-Formular anzeigen"""
    with st.form("Login"):
        email = st.text_input("E-Mail-Adresse")
        password = st.text_input("Passwort", type="password")
        if st.form_submit_button("Anmelden"):
            try:
                user = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                st.session_state.authenticated = True
                st.session_state.session_id = user.user.id
                st.rerun()
            except Exception as e:
                st.error("Anmeldung fehlgeschlagen. Bitte überprüfen Sie Ihre Zugangsdaten.")

def apply_custom_styles():
    """Anwendung des benutzerdefinierten Designs"""
    st.markdown("""
        <style>
            /* Globale Styles */
            @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');
            
            /* Verstecke Menü und Deploy Button */
            #MainMenu {visibility: hidden !important;}
            .stDeployButton {display: none !important;}
            header {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            
            /* Moderneres Design */
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
                font-family: 'Open Sans', sans-serif;
            }

            /* Main Content Bereich */
            .main > * {
                color: #2c3e50 !important;
            }

            .st-emotion-cache-r421ms {
                white-space: normal;
                color: #2c3e50 !important;
            }
            
            /* Titel und Überschriften */
            h1, h2, h3 {
                color: #2c3e50 !important;
                font-weight: 600;
            }

            /* Chat Messages */
            .st-emotion-cache-1gulkj5 {
                background-color: rgba(255, 255, 255, 0.9) !important;
            }

            .st-emotion-cache-1gulkj5 p {
                color: #2c3e50 !important;
            }

            /* Spezifische Chat-Nachrichten Styles */
            .stChatMessage div[data-testid="stMarkdownContainer"] > p {
                color: #2c3e50 !important;
            }

            [data-testid="chatAvatarIcon"] {
                background-color: #3498db !important;
            }

            .st-emotion-cache-1c7y2kd {
                color: #2c3e50 !important;
            }

            /* Alle Chat-Message Container */
            [data-testid="stChatMessage"] {
                background-color: rgba(255, 255, 255, 0.9) !important;
            }
            
            /* Buttons */
            .stButton button {
                background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 0.5rem 1rem;
                font-weight: 600;
            }
            .stButton button:hover {
                background: linear-gradient(135deg, #2980b9 0%, #2573a7 100%);
            }
            
            /* Chat-Nachrichten */
            .stChatMessage {
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                margin: 0.5rem 0;
            }

            /* Zusätzliche Anpassungen */
            .stTextInput input {
                border-radius: 5px;
                border: 1px solid #e0e0e0;
            }
            .stTextInput input:focus {
                border-color: #3498db;
                box-shadow: 0 0 0 2px rgba(52,152,219,0.2);
            }
        </style>
    """, unsafe_allow_html=True)

# Streamlit-Konfiguration
st.set_page_config(
    page_title="Rudi @ dsmalaga.com",
    page_icon="🤖",
    menu_items={},  # Versteckt das Menü
    initial_sidebar_state="expanded"
)

def main():
    """Hauptfunktion der Chat-Anwendung"""
    apply_custom_styles()
    
    # Initialisiere Session State
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.session_id = None
        st.session_state.chat_history = []
        st.session_state.current_conversation_id = None

    st.title("Rudi @ dsmalaga.com")

    # Zeige Login oder Chat Interface
    if not st.session_state.authenticated:
        show_login()
    else:
        # Sidebar für Chat-Verlauf
        with st.sidebar:
            st.title("Chat-Verlauf")
            try:
                result = supabase.table("conversations").select("*").eq("user_id", st.session_state.session_id).order("last_updated", desc=True).execute()
                for conv in result.data:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        if st.button(f"{conv['title']}", key=f"conv_{conv['id']}", use_container_width=True):
                            load_chat_history(conv["id"])
                            st.rerun()
                    with col2:
                        if st.button("🗑️", key=f"del_{conv['id']}", help="Chat löschen"):
                            delete_conversation(conv["id"])
            except Exception as e:
                st.error("Fehler beim Laden der Chat-Historie")

        # Header-Bereich mit Buttons
        col1, col2 = st.columns([2, 2])
        with col1:
            if st.button("Neuer Chat", use_container_width=True):
                try:
                    result = supabase.table("conversations").insert({
                        "user_id": st.session_state.session_id,
                        "title": f"Chat vom {datetime.now().strftime('%d.%m.%Y %H:%M')}"
                    }).execute()
                    st.session_state.current_conversation_id = result.data[0]['id']
                    st.session_state.chat_history = []
                    st.rerun()
                except Exception as e:
                    st.error("Fehler beim Erstellen eines neuen Chats")
        with col2:
            if st.button("Abmelden", type="primary", use_container_width=True):
                logout()
                return

        # Chat umbenennen
        if st.session_state.get("current_conversation_id"):
            with st.expander("Chat umbenennen"):
                new_title = st.text_input("Neuer Name", key="new_chat_title")
                if st.button("Umbenennen"):
                    try:
                        supabase.table("conversations").update({
                            "title": new_title
                        }).eq("id", st.session_state.current_conversation_id).execute()
                        st.success("Chat wurde umbenannt")
                        st.rerun()
                    except Exception as e:
                        st.error("Fehler beim Umbenennen des Chats")

        # Chat-Eingabe
        chat_input = st.chat_input("Ihre Nachricht...")
        if chat_input:
            # Webhook Payload
            payload = {
                "chatInput": chat_input,
                "sessionId": st.session_state.session_id
            }
            
            try:
                # Webhook-Anfrage
                response = requests.post(
                    WEBHOOK_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                response.raise_for_status()
                response_data = response.json()
                
                # Chatverlauf aktualisieren
                st.session_state.chat_history.append({
                    "user": chat_input,
                    "bot": response_data.get("output", "Keine Antwort erhalten")
                })
                
                # In Datenbank speichern
                try:
                    if not st.session_state.get("current_conversation_id"):
                        conv_result = supabase.table("conversations").insert({
                            "user_id": st.session_state.session_id,
                            "title": f"Chat vom {datetime.now().strftime('%d.%m.%Y %H:%M')}"
                        }).execute()
                        st.session_state.current_conversation_id = conv_result.data[0]['id']
                    
                    message_order = len(st.session_state.chat_history)
                    supabase.table("chats").insert({
                        "user_id": st.session_state.session_id,
                        "conversation_id": st.session_state.current_conversation_id,
                        "message": chat_input,
                        "response": response_data.get("output"),
                        "message_order": message_order,
                        "timestamp": "now()"
                    }).execute()

                    # Conversation aktualisieren
                    supabase.table("conversations").update({
                        "last_updated": "now()"
                    }).eq("id", st.session_state.current_conversation_id).execute()

                except Exception as db_error:
                    st.warning("Chat-Verlauf konnte nicht gespeichert werden")
                
            except requests.exceptions.RequestException as e:
                st.error("Fehler bei der Kommunikation mit dem Server")
                return

        # Chatverlauf anzeigen
        for message in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(message["user"])
            with st.chat_message("assistant"):
                st.write(message["bot"])

if __name__ == "__main__":
    main()
