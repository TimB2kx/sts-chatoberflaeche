import streamlit as st
from supabase import create_client, Client
import requests

# Initialisiere Supabase-Client
SUPABASE_URL = "https://aws-supabase-u31663.vm.elestio.app/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlzcyI6InN1cGFiYXNlIiwiaWF0IjoxNzM3NzI5OTIzLCJleHAiOjIwNTMwODk5MjN9.L-oUAxVZHbi2QzmAy0mgFV9AA0Wql1wLkW1kYUcGmO0"
WEBHOOK_URL = "https://n8ntb.sts.support/webhook/9ba11544-5c4e-4f91-818a-08a4ecb596c5"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    st.title("Secure Chat Interface")
    
    # Authentifizierungsstatus prüfen
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.session_id = None
        st.session_state.chat_history = []

    if not st.session_state.authenticated:
        # Login-Formular
        with st.form("Login"):
            email = st.text_input("E-Mail")
            password = st.text_input("Passwort", type="password")
            if st.form_submit_button("Login"):
                try:
                    # Supabase-Authentifizierung
                    user = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })
                    st.session_state.authenticated = True
                    st.session_state.session_id = user.user.id  # Session-ID aus User-ID
                    st.rerun()
                except Exception as e:
                    st.error(f"Login fehlgeschlagen: {str(e)}")
        return

    # Chat-Interface nach erfolgreichem Login
    st.subheader("Chat")
    
    # Chat-Eingabe
    chat_input = st.chat_input("Ihre Nachricht...")
    
    if chat_input:
        # Webhook mit korrekter Body-Struktur
        payload = {
            "body": {  # Hinzufügen der "body"-Ebene
                "chatInput": chat_input,
                "sessionId": st.session_state.session_id
            }
        }
        
        try:
            # Füge explizite Headers hinzu
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                WEBHOOK_URL,
                json=payload,  # Korrektes JSON-Format
                headers=headers
            )
            
            # Debug-Ausgabe für Response
            st.write(f"Server Response: {response.status_code}, {response.text}")
            
            # Fehlerbehandlung verbessern
            response.raise_for_status()  # Wirft Exception bei 4xx/5xx
            response_data = response.json()
            
            # Chatverlauf aktualisieren
            st.session_state.chat_history.append({
                "user": chat_input,
                "bot": response_data.get("response", "Keine Antwort erhalten")
            })
            
            # Optional: In Supabase speichern
            supabase.table("chats").insert({
                "user_id": st.session_state.session_id,
                "message": chat_input,
                "response": response_data,
                "timestamp": "now()"
            }).execute()
            
        except requests.exceptions.HTTPError as e:
            st.error(f"Webhook Fehler: {e.response.status_code} - {e.response.text}")
            return
        except Exception as e:
            st.error(f"Verbindungsfehler: {str(e)}")
            return

    # Chatverlauf anzeigen
    for message in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(message["user"])
        with st.chat_message("assistant"):
            st.write(message["bot"])

if __name__ == "__main__":
    main()
