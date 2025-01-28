import streamlit as st
from config import supabase

def show_login():
    """Zeigt das Login-Formular an und verarbeitet die Anmeldung"""
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
                st.error("Anmeldung fehlgeschlagen")

def logout():
    """Meldet den Benutzer ab und setzt die Session zurück"""
    st.session_state.authenticated = False
    st.session_state.session_id = None
    st.session_state.chat_history = []
    supabase.auth.sign_out()
    st.rerun()

def init_session_state():
    """Initialisiert die Session-State-Variablen"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.session_id = None
        st.session_state.chat_history = []
        st.session_state.current_conversation_id = None
        st.session_state.webhook_selection = "rudi"
        st.session_state.template_content = None

def is_authenticated() -> bool:
    """Überprüft, ob der Benutzer authentifiziert ist"""
    return st.session_state.authenticated