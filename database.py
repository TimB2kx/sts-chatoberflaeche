from datetime import datetime
from config import supabase
import streamlit as st

def start_new_chat() -> str:
    """Erstellt einen neuen Chat und gibt die Chat-ID zurück"""
    try:
        result = supabase.table("conversations").insert({
            "user_id": st.session_state.session_id,
            "title": f"Chat vom {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        }).execute()
        return result.data[0]['id']
    except Exception as e:
        st.error("Fehler beim Erstellen eines neuen Chats")
        raise e

def load_chat_history(conversation_id: str) -> None:
    """Lädt den Chatverlauf für eine bestimmte Konversation"""
    try:
        result = supabase.table("chats").select("*").eq("conversation_id", conversation_id).order("message_order").execute()
        st.session_state.chat_history = [
            {"user": chat["message"], "bot": chat["response"]}
            for chat in result.data
        ]
        st.session_state.current_conversation_id = conversation_id
    except Exception as e:
        st.error("Fehler beim Laden des Chat-Verlaufs")
        raise e

def delete_conversation(conversation_id: str) -> None:
    """Löscht eine Konversation und zugehörige Chats"""
    try:
        supabase.table("chats").delete().eq("conversation_id", conversation_id).execute()
        supabase.table("conversations").delete().eq("id", conversation_id).execute()
        if st.session_state.get("current_conversation_id") == conversation_id:
            st.session_state.current_conversation_id = None
            st.session_state.chat_history = []
    except Exception as e:
        st.error("Fehler beim Löschen des Chats")
        raise e

def load_user_conversations(user_id: str):
    """Lädt alle Konversationen eines Benutzers"""
    try:
        return supabase.table("conversations").select("*").eq("user_id", user_id).order("last_updated", desc=True).execute()
    except Exception as e:
        st.error("Fehler beim Laden der Chat-Historie")
        raise e

def save_chat_message(user_id: str, conversation_id: str | None, message: str, response: str) -> None:
    """Speichert eine Chat-Nachricht und Antwort"""
    try:
        # Stelle sicher, dass chat_history existiert
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Erstelle neue Konversation falls keine existiert
        if not conversation_id:
            conversation_id = start_new_chat()
            st.session_state.current_conversation_id = conversation_id
            
        message_order = len(st.session_state.chat_history)
        
        # Speichere Chat-Nachricht
        supabase.table("chats").insert({
            "user_id": user_id,
            "conversation_id": conversation_id,
            "message": message,
            "response": response,
            "message_order": message_order,
            "timestamp": "now()"
        }).execute()

        # Aktualisiere last_updated der Konversation
        supabase.table("conversations").update({
            "last_updated": "now()"
        }).eq("id", conversation_id).execute()
    except Exception as e:
        st.error("Fehler beim Speichern der Nachricht")
        raise e

def rename_conversation(conversation_id: str, new_title: str) -> None:
    """Benennt eine Konversation um"""
    try:
        supabase.table("conversations").update({
            "title": new_title
        }).eq("id", conversation_id).execute()
    except Exception as e:
        st.error("Fehler beim Umbenennen des Chats")
        raise e