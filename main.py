import streamlit as st
from auth import show_login, init_session_state, is_authenticated
from styles import apply_custom_styles
from components.header import render_header
from components.sidebar import render_sidebar
from components.chat import render_chat_history, render_chat_input
from templates import load_prompt_templates, render_template_selector

# Theme customization
st.set_page_config(
    page_title="STS Support Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    """Hauptfunktion der Streamlit App"""
    # Styles anwenden
    apply_custom_styles()
    
    # Session State initialisieren
    init_session_state()
    
    # App-Titel
    st.title("KI @ dsmalaga.com")
    
    # Auth-Check
    if not is_authenticated():
        show_login()
        return
    
    # Seitenleiste mit Chat-Historie
    render_sidebar()
    
    # Hauptcontainer
    with st.container():
        # Header mit Aktionen
        render_header()
        
        st.markdown("---")
        
        # Chat-Verlauf
        st.markdown("### Chatverlauf")
        render_chat_history()
        
        # Chat-Eingabe
        render_chat_input()
        
        # Promptvorlagen
        st.markdown("### Promptvorlagen")
        templates = load_prompt_templates()
        render_template_selector(templates)

if __name__ == "__main__":
    main()