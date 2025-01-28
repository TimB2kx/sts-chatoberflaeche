import streamlit as st
from database import load_user_conversations, delete_conversation, load_chat_history, rename_conversation

def render_sidebar() -> None:
    """Rendert die Seitenleiste mit der Chat-Historie"""
    with st.sidebar:
        st.title("Chat-Verlauf")
        try:
            result = load_user_conversations(st.session_state.session_id)
            
            for conv in result.data:
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(f"{conv['title']}", key=f"conv_{conv['id']}", use_container_width=True):
                        load_chat_history(conv["id"])
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"del_{conv['id']}", help="Chat löschen"):
                        delete_conversation(conv["id"])
                        st.rerun()
                
        except Exception as e:
            st.error("Fehler beim Laden der Chat-Historie")

def render_chat_rename() -> None:
    """Rendert das Formular zum Umbenennen eines Chats"""
    if st.session_state.get("current_conversation_id"):
        with st.expander("Chat umbenennen", expanded=False):
            new_title = st.text_input("Neuer Name", key="new_chat_title")
            if st.button("Umbenennen"):
                if new_title:  # Prüfe ob ein neuer Titel eingegeben wurde
                    try:
                        rename_conversation(st.session_state.current_conversation_id, new_title)
                        st.success("Chat wurde umbenannt")
                        st.rerun()
                    except Exception as e:
                        st.error("Fehler beim Umbenennen des Chats")