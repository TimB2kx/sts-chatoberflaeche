import streamlit as st
from database import load_user_conversations, delete_conversation, load_chat_history, rename_conversation

def render_sidebar() -> None:
    """Rendert die Seitenleiste mit der Chat-Historie"""
    with st.sidebar:
        st.title("Chat-Verlauf")
        try:
            result = load_user_conversations(st.session_state.session_id)
            
            for conv in result.data:
                col1, col2, col3 = st.columns([4, 0.7, 0.7])
                with col1:
                    if st.button(f"{conv['title']}", key=f"conv_{conv['id']}", use_container_width=True):
                        load_chat_history(conv["id"])
                        st.rerun()
                with col2:
                    if st.button("✏️", key=f"edit_{conv['id']}", help="Chat umbenennen"):
                        st.session_state[f"rename_chat_{conv['id']}"] = True
                        st.rerun()
                with col3:
                    if st.button("🗑️", key=f"del_{conv['id']}", help="Chat löschen"):
                        delete_conversation(conv["id"])
                        st.rerun()
                
                # Zeige Umbenennen-Dialog wenn aktiv
                if st.session_state.get(f"rename_chat_{conv['id']}", False):
                    with st.container():
                        new_title = st.text_input("Neuer Name", key=f"new_title_{conv['id']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Speichern", key=f"save_{conv['id']}"):
                                if new_title:
                                    rename_conversation(conv["id"], new_title)
                                    st.session_state[f"rename_chat_{conv['id']}"] = False
                                    st.rerun()
                        with col2:
                            if st.button("Abbrechen", key=f"cancel_{conv['id']}"):
                                st.session_state[f"rename_chat_{conv['id']}"] = False
                                st.rerun()
                
        except Exception as e:
            st.error("Fehler beim Laden der Chat-Historie")