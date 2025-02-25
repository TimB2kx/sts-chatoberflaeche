import streamlit as st
from database import start_new_chat
from auth import logout

def render_header() -> None:
    """Rendert den Header-Bereich mit Aktionsbuttons"""
    st.markdown("### Aktionen")
    col1, col2, col3 = st.columns([0.3, 3, 0.3])
    
    # Neuer Chat Button
    with col1:
        if st.button("✚", help="Neuer Chat", key="new_chat_btn"):
            new_chat_id = start_new_chat()
            st.session_state.current_conversation_id = new_chat_id
            st.session_state.chat_history = []
            st.rerun()
    
    # Webhook Auswahl
    with col2:
        prev_webhook = st.session_state.webhook_selection
        webhook_selection = st.selectbox(
            "",
            ["Rudi (internes Wissen DS Malaga)", 
             "Perplexity Pro AI Suche",
             "Mistral (DSGVO konform)", 
             "Gemini 2.0 Flash",
             "Gemini 2.0 Thinking",
             "Anthropic Claude 3.5",
             "DeepSeek R1 Reasoner/ Thinking (langsam)"],
            index=(0 if st.session_state.webhook_selection == "rudi (internes wissen ds malaga)"
                  else 1 if st.session_state.webhook_selection == "perplexity pro ai suche"
                  else 2 if st.session_state.webhook_selection == "mistral (dsgvo konform)"
                  else 3 if st.session_state.webhook_selection == "gemini 2.0 flash"
                  else 4 if st.session_state.webhook_selection == "gemini 2.0 thinking"
                  else 5 if st.session_state.webhook_selection == "anthropic claude 3.5"
                  else 6),
            key="webhook_dropdown",
            label_visibility="collapsed"
        )
        
        # Wenn sich die Auswahl ändert, starte einen neuen Chat
        new_webhook = webhook_selection.lower()
        if new_webhook != prev_webhook:
            st.session_state.webhook_selection = new_webhook
            if st.session_state.authenticated:
                new_chat_id = start_new_chat()
                st.session_state.current_conversation_id = new_chat_id
                st.session_state.chat_history = []
                st.rerun()
    
    # Abmelden Button
    with col3:
        if st.button("⏻", help="Abmelden", key="logout_btn"):
            logout()
            st.rerun()