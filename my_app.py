import streamlit as st
from supabase import create_client, Client
import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from typing import List, Dict, TypedDict

class PromptTemplate(TypedDict):
    title: str
    description: str
    template: str


# Initialisiere Supabase-Client
SUPABASE_URL = "https://aws-supabase-u31663.vm.elestio.app/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlzcyI6InN1cGFiYXNlIiwiaWF0IjoxNzM3NzI5OTIzLCJleHAiOjIwNTMwODk5MjN9.L-oUAxVZHbi2QzmAy0mgFV9AA0Wql1wLkW1kYUcGmO0"
# Webhook URLs
WEBHOOK_URL_RUDI = "https://n8ntb.sts.support/webhook/9ba11544-5c4e-4f91-818a-08a4ecb596c5"
WEBHOOK_URL_TEST = "https://n8ntb.sts.support/webhook/2c474e5f-0350-4bdf-b0c4-dbf73f919659"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def start_new_chat():
    """Startet einen neuen Chat mit aktuellem Zeitstempel"""
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

            /* Hauptcontainer-Padding reduzieren */
            .block-container {
                padding: 0.5rem !important;
            }

            /* Container fürs Chat-Eingabefeld fixieren */
            .chat-input-container {
                position: fixed !important;
                bottom: 0;
                left: 0;
                right: 0;
                z-index: 9999;
                background-color: white !important;
                padding: 0.5rem !important;
            }
            
            /* Verstecke Menü und Deploy Button */
            #MainMenu {visibility: hidden !important;}
            .stDeployButton {display: none !important;}
            header {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            
            /* Weißer Hintergrund */
            .stApp {
                background: white;
                font-family: 'Open Sans', sans-serif;
            }

            /* Main Content Bereich */
            .main > * {
                color: black !important;
            }

            /* Dropdown Styling */
            .stSelectbox {
                margin-top: 0 !important;
            }
            
            /* Expander Styling */
            div[data-testid="stExpander"] {
                border: 1px solid black !important;
                border-radius: 5px !important;
                margin: 10px 0 !important;
            }

            .streamlit-expanderHeader {
                background-color: #f0f0f0 !important;
                border-radius: 5px !important;
                color: black !important;
                font-weight: 600 !important;
                padding: 10px !important;
            }

            /* Zusätzliche spezifische Selektoren für den Expander-Text */
            div[data-testid="stExpander"] span {
                color: black !important;
            }
            
            div[data-testid="stExpander"] p {
                color: black !important;
            }

            .streamlit-expanderHeader:hover {
                background-color: #e0e0e0 !important;
            }

            .streamlit-expanderContent {
                border-top: 1px solid black !important;
                background-color: white !important;
            }
            
            /* Sidebar Styling */
            .sidebar .block-container {
                color: white !important;
            }
            
            /* Sidebar Titel */
            .sidebar h1, .sidebar h2, .sidebar h3 {
                color: black !important;
            }

            .st-emotion-cache-r421ms {
                white-space: normal;
                color: black !important;
            }
            
            /* Titel und Überschriften */
            h1, h2, h3 {
                color: black !important;
                font-weight: 600;
            }

            /* Chat Messages */
            .st-emotion-cache-1gulkj5 {
                background-color: white !important;
            }

            .st-emotion-cache-1gulkj5 p {
                color: black !important;
            }

            /* Spezifische Chat-Nachrichten Styles */
            .stChatMessage div[data-testid="stMarkdownContainer"] > p {
                color: black !important;
            }

            [data-testid="chatAvatarIcon"] {
                background-color: black !important;
            }

            .st-emotion-cache-1c7y2kd {
                color: black !important;
            }

            /* Alle Chat-Message Container */
            [data-testid="stChatMessage"] {
                background-color: white !important;
            }
            
            /* Buttons */
            .stButton button {
                background: white !important;
                color: black !important;
                border: 1px solid black !important;
                border-radius: 5px;
                padding: 0.5rem 1rem;
                font-weight: 600;
            }
            .stButton button:hover {
                background: #f0f0f0 !important;
            }

            /* Markdown und Text Styling */
            div[data-testid="stMarkdownContainer"] p,
            div[data-testid="stMarkdownContainer"] span,
            div[data-testid="stMarkdownContainer"] strong {
                color: black !important;
            }
            
            /* Chat-Nachrichten */
            .stChatMessage {
                background: white;
                border-radius: 10px;
                border: 1px solid #ddd;
                margin: 0.5rem 0;
            }

            /* Verbesserte Lesbarkeit für Text-Inputs und Expander */
            .streamlit-expanderContent {
                background-color: white !important;
                border-radius: 0 0 5px 5px !important;
                padding: 10px !important;
            }

            /* Überschriften */
            h1, h2, h3 {
                margin-top: 0 !important;
                padding-top: 0.5rem !important;
                color: black !important;
            }

            /* Trennlinien */
            hr {
                margin: 0.5rem 0 !important;
            }

            /* Text-Inputs */
            .stTextInput input {
                border-radius: 5px;
                border: 1px solid #ddd;
                background-color: white !important;
                color: black !important;
            }
            .stTextInput input:focus {
                border-color: black;
                box-shadow: 0 0 0 2px rgba(0,0,0,0.1);
            }

            /* Info Message Styling */
            .stAlert {
                background-color: #f0f0f0 !important;
                border: 1px solid #ddd !important;
            }
            
            .stAlert p {
                color: black !important;
            }

            /* Login Form Styling */
            .stForm [data-baseweb="input"] {
                background-color: white !important;
            }
            .stForm [data-baseweb="input"] input {
                color: black !important;
            }
            .stForm label {
                color: black !important;
            }
        </style>
    """, unsafe_allow_html=True)

# Streamlit-Konfiguration
st.set_page_config(
    page_title="KI @ dsmalaga.com",
    page_icon="🤖",
    menu_items={},  # Versteckt das Menü
    initial_sidebar_state="expanded"
)

def load_prompt_templates() -> List[PromptTemplate]:
    """Lädt die Promptvorlagen aus der XML-Datei"""
    try:
        tree = ET.parse('prompt_templates.xml')
        root = tree.getroot()
        templates = []
        
        for prompt in root.findall('.//prompt'):
            template = PromptTemplate(
                title=prompt.find('title').text,
                description=prompt.find('description').text,
                template=prompt.find('template').text
            )
            templates.append(template)
        
        return templates
    except Exception as e:
        st.error(f"Fehler beim Laden der Promptvorlagen: {str(e)}")
        return []

def main():
    """Hauptfunktion der Chat-Anwendung"""
    apply_custom_styles()
    
    # Initialisiere Session State
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.session_id = None
        st.session_state.chat_history = []
        st.session_state.current_conversation_id = None
        st.session_state.webhook_selection = "rudi"  # Standard: Rudi Webhook
        st.session_state.template_content = None  # Für Promptvorlagen

    st.title("KI @ dsmalaga.com")

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

        # Header-Bereich mit Buttons - alle in einer Linie
        st.markdown("### Aktionen")  # Überschrift für den Aktionsbereich
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col1:
            if st.button("Neuer Chat", use_container_width=True, key="new_chat_btn"):
                start_new_chat()
        with col2:
            # Webhook Auswahl als Dropdown - ohne Label für bessere Ausrichtung
            prev_webhook = st.session_state.webhook_selection  # Vorherige Auswahl speichern
            webhook_selection = st.selectbox(
                "",  # Label entfernt
                ["Rudi", "Test"],
                index=0 if st.session_state.webhook_selection == "rudi" else 1,
                key="webhook_dropdown",
                label_visibility="collapsed"  # Versteckt das Label vollständig
            )
            
            # Wenn sich die Auswahl ändert, starte einen neuen Chat
            new_webhook = webhook_selection.lower()
            if new_webhook != prev_webhook:
                st.session_state.webhook_selection = new_webhook
                if st.session_state.authenticated:  # Nur wenn User eingeloggt ist
                    start_new_chat()

        with col3:
            if st.button("Abmelden", type="primary", use_container_width=True, key="logout_btn"):
                logout()
                return

        # Chat umbenennen - direkt unter den Buttons
        st.markdown("---")  # Trennlinie
        if st.session_state.get("current_conversation_id"):
            with st.expander("Chat umbenennen", expanded=False):
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

        # Chat-Container mit automatischem Scrolling
        st.markdown("### Chatverlauf")
        chat_container = st.empty()  # Leerer Container für dynamische Updates
        
        # Chat-Verlauf in einem scrollbaren Container anzeigen
        with chat_container.container():
            # Wrapper für besseres Scrolling
            with st.container():
                if st.session_state.chat_history:
                    # Nachrichten in umgekehrter Reihenfolge, neueste zuerst
                    for message in list(reversed(st.session_state.chat_history)):
                        with st.chat_message("user"):
                            try:
                                # Versuche als Markdown zu rendern
                                st.markdown(message["user"])
                            except:
                                # Fallback zu normalem Text
                                st.write(message["user"])
                        
                        with st.chat_message("assistant"):
                            try:
                                st.markdown(message["bot"])
                            except:
                                st.write(message["bot"])
                else:
                    st.info("Noch keine Nachrichten in diesem Chat. Schreiben Sie etwas, um zu beginnen!")

        st.markdown("---")  # Trennlinie

        # Chat-Eingabebereich
        input_container = st.container()
        with input_container:
            st.markdown("### Nachricht eingeben")
            # Chat-Eingabefeld mit eindeutigem Key und Template-Integration
            if "current_message" not in st.session_state:
                st.session_state.current_message = ""
                
            message = st.text_area(
                "Ihre Nachricht...",
                value=st.session_state.current_message,
                height=150,  # Erhöhte Höhe für bessere Übersicht
                key="message_input"
            )
            st.session_state.current_message = message

            # Senden-Button
            if st.button("Senden", type="primary", key="send_button") and message:
                try:
                    # Zuerst Conversation erstellen/prüfen
                    if not st.session_state.get("current_conversation_id"):
                        conv_result = supabase.table("conversations").insert({
                            "user_id": st.session_state.session_id,
                            "title": f"Chat vom {datetime.now().strftime('%d.%m.%Y %H:%M')}"
                        }).execute()
                        st.session_state.current_conversation_id = conv_result.data[0]['id']
                    
                    # Webhook-Anfrage
                    webhook_url = WEBHOOK_URL_RUDI if st.session_state.webhook_selection == "rudi" else WEBHOOK_URL_TEST
                    response = requests.post(
                        webhook_url,
                        json={"chatInput": message, "sessionId": st.session_state.session_id},
                        headers={"Content-Type": "application/json"}
                    )
                    
                    response.raise_for_status()
                    response_data = response.json()
                    
                    # Chat in Datenbank speichern
                    supabase.table("chats").insert({
                        "user_id": st.session_state.session_id,
                        "conversation_id": st.session_state.current_conversation_id,
                        "message": message,
                        "response": response_data.get("output"),
                        "message_order": len(st.session_state.chat_history),
                        "timestamp": "now()"
                    }).execute()

                    # Conversation aktualisieren
                    supabase.table("conversations").update({
                        "last_updated": "now()"
                    }).eq("id", st.session_state.current_conversation_id).execute()

                    # Chatverlauf aktualisieren
                    st.session_state.chat_history.append({
                        "user": message,
                        "bot": response_data.get("output", "Keine Antwort erhalten")
                    })

                    # Chat-Input und Session State zurücksetzen
                    st.session_state.current_message = ""
                    st.rerun()

                except Exception as e:
                    st.error(f"Fehler: {str(e)}")

        # Promptvorlagen
        template_container = st.container()
        with template_container:
            st.markdown("### Promptvorlagen")
            templates = load_prompt_templates()
            if templates:
                # Container für bessere Ausrichtung
                with st.container():
                    # Erste Zeile für Auswahl und Button
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        template_options = ["Vorlage auswählen..."] + [f"{t['title']}" for t in templates]
                        selected_index = st.selectbox(
                            "",  # Label entfernt für bessere Ausrichtung
                            range(len(template_options)),
                            format_func=lambda x: template_options[x],
                            key="template_selector",
                            label_visibility="collapsed"
                        )
                    
                    with col2:
                        insert_disabled = selected_index == 0
                        if st.button("Einfügen", key="insert_template", disabled=insert_disabled):
                            st.session_state.current_message = templates[selected_index-1]['template']
                            st.rerun()
                    
                    # Zweite Zeile für Beschreibung
                    if selected_index > 0:
                        st.markdown(f"**Beschreibung:** {templates[selected_index-1]['description']}")


if __name__ == "__main__":
    main()
