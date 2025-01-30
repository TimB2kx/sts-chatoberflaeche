import streamlit as st
import requests
from datetime import datetime
from database import save_chat_message
from config import (
    WEBHOOK_URL_RUDI,
    WEBHOOK_URL_PERPLEXITY,
    WEBHOOK_URL_CHATGPT,
    WEBHOOK_URL_MISTRAL,
    WEBHOOK_URL_DEEPSEEK,
    WEBHOOK_URL_GEMINI_FLASH,
    WEBHOOK_URL_GEMINI_THINKING,
    WEBHOOK_URL_CLAUDE
)
import uuid

def render_chat_history() -> None:
    """Rendert den Chat-Verlauf"""
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            with st.chat_message("user"):
                try:
                    st.markdown(message["user"])
                except:
                    st.write(message["user"])
            with st.chat_message("assistant"):
                try:
                    st.markdown(message["bot"])
                except:
                    st.write(message["bot"])
    else:
        st.info("Noch keine Nachrichten in diesem Chat. Schreiben Sie etwas, um zu beginnen!")

def render_chat_input() -> None:
    """Rendert das Chat-Eingabefeld"""
    if "current_message" not in st.session_state:
        st.session_state.current_message = ""
    
    # Container für das Eingabefeld und den Button
    input_container = st.container()
    
    # Chat-Input mit Button
    with input_container:
        cols = st.columns([8, 1])
        
        # Eingabefeld in der linken Spalte
        with cols[0]:
            message = st.text_area(
                "Ihre Nachricht...",
                value=st.session_state.current_message,
                height=100,
                key="message_input",
                label_visibility="collapsed"
            )
        
        # Button in der rechten Spalte
        with cols[1]:
            st.markdown("""
                <style>
                div[data-testid="column"]:nth-child(2) {
                    display: flex !important;
                    align-items: flex-end !important;
                }
                div[data-testid="tooltipHoverTarget"] {
                    justify-content: flex-start !important;
                }
                .stTooltipIcon {
                    display: flex !important;
                    justify-content: flex-start !important;
                }
                .st-emotion-cache-6dnr6u {
                    display: flex !important;
                    justify-content: flex-start !important;
                }
                .st-emotion-cache-upseer {
                    display: flex !important;
                    justify-content: flex-start !important;
                }
                .st-emotion-cache-nbt3vv.ef3psqc12:hover {
                    background-color: white !important;
                }
                </style>
            """, unsafe_allow_html=True)
            send_button = st.button(
                "➤",
                type="primary",
                key="send_button",
                help="Nachricht senden"
            )
        
        if send_button and message:
            handle_message_send(message, send_button)

def handle_message_send(message: str, send_button: bool) -> None:
    """Verarbeitet das Senden einer Nachricht"""
    try:
        # Session-ID generieren, wenn nicht vorhanden
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
            
        # Chat-Verlauf initialisieren, wenn nicht vorhanden
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        # Aktuelle Konversations-ID initialisieren, wenn nicht vorhanden
        if "current_conversation_id" not in st.session_state:
            st.session_state.current_conversation_id = None
            
        # Webhook-Auswahl aus der Session holen
        webhook_selection = st.session_state.get("webhook_selection", "deepseek r1 reasoner")
        
        # Wenn eine Nachricht gesendet wurde und der Button geklickt wurde
        if send_button and message:
            # Webhook URL basierend auf Auswahl
            webhook_selection = webhook_selection.lower()
            if webhook_selection == "rudi (internes wissen ds malaga)":
                webhook_url = WEBHOOK_URL_RUDI
            elif webhook_selection == "perplexity pro ai suche":
                webhook_url = WEBHOOK_URL_PERPLEXITY
            elif webhook_selection == "mistral (dsgvo konform)":
                webhook_url = WEBHOOK_URL_MISTRAL
            elif webhook_selection == "gemini 2.0 flash":
                webhook_url = WEBHOOK_URL_GEMINI_FLASH
            elif webhook_selection == "gemini 2.0 thinking":
                webhook_url = WEBHOOK_URL_GEMINI_THINKING
            elif webhook_selection == "anthropic claude 3.5":
                webhook_url = WEBHOOK_URL_CLAUDE
            else:  # DeepSeek R1 Reasoner/ Thinking (langsam)
                webhook_url = WEBHOOK_URL_DEEPSEEK
            
            # Custom headers for the request
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Origin": "https://n8ntb.sts.support",
                "Referer": "https://n8ntb.sts.support/"
            }
            
            # Webhook-Anfrage senden
            response = requests.post(
                webhook_url,
                json={"chatInput": message, "sessionId": st.session_state.session_id},
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            response_data = response.json()
            bot_response = response_data.get("output", "Keine Antwort erhalten")
            
            # Nachricht in der Datenbank speichern
            save_chat_message(
                st.session_state.session_id,
                st.session_state.current_conversation_id,
                message,
                bot_response
            )
            
            # Chat-Verlauf aktualisieren
            st.session_state.chat_history.append({
                "user": message,
                "bot": bot_response
            })
            
            # Chat-Input zurücksetzen
            st.session_state.current_message = ""
            
            # Seite neu laden
            st.rerun()
        
    except Exception as e:
        error_message = f"Fehler: {str(e)}"
        st.error(error_message)
        
        # Only try to access response attributes if it's a requests.exceptions.RequestException
        if isinstance(e, requests.exceptions.RequestException) and hasattr(e, 'response') and e.response is not None:
            st.error(f"Response Status: {e.response.status_code}")
            st.error(f"Response Headers: {e.response.headers}")
            try:
                st.error(f"Response Content: {e.response.text}")
            except:
                pass
        
        # Log specific timeout errors
        if isinstance(e, requests.exceptions.Timeout):
            st.error("Die Verbindung zum Server hat zu lange gedauert. Bitte versuchen Sie es später erneut.")
        elif isinstance(e, requests.exceptions.ConnectionError):
            st.error("Verbindung zum Server konnte nicht hergestellt werden. Bitte überprüfen Sie Ihre Internetverbindung.")