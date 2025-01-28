# Streamlit App Architektur

## Zielstruktur
```
.
├── ARCHITECTURE.md
├── my_app.py         → Hauptanwendung
├── config.py         # Konfigurationen und Umgebungsvariablen
├── auth.py           # Authentifizierungslogik
├── database.py       # Datenbankoperationen
├── styles.py         # Styling und CSS
├── templates.py      # Promptvorlagen Handling
└── components/       # UI-Komponenten
    ├── chat.py
    ├── sidebar.py
    └── input.py
```

## Dateiverantwortlichkeiten

### config.py
```python
SUPABASE_URL = "https://aws-supabase-u31663.vm.elestio.app/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
WEBHOOK_URL_RUDI = "https://n8ntb.sts.support/webhook/9ba11544-5c4e-4f91-818a-08a4ecb596c5"
WEBHOOK_URL_TEST = "https://n8ntb.sts.support/webhook/2c474e5f-0350-4bdf-b0c4-dbf73f919659"

# Supabase Client Initialisierung
from supabase import create_client
client = create_client(SUPABASE_URL, SUPABASE_KEY)
```

### auth.py
```python
from config import client

def handle_login(email: str, password: str) -> dict:
    """Verarbeitet den Login-Prozess"""
    
def handle_logout():
    """Verarbeitet den Logout-Prozess"""

def check_session() -> bool:
    """Überprüft die aktuelle Session"""
```

### database.py
```python
from config import client

def create_conversation(user_id: str, title: str) -> str:
    """Erstellt eine neue Konversation und gibt die ID zurück"""

def load_conversations(user_id: str) -> list:
    """Lädt alle Konversationen eines Benutzers"""

def save_message(conversation_id: str, message: str, response: str):
    """Speichert eine Chat-Nachricht"""
```

### styles.py
```python
import streamlit as st

def apply_custom_styles():
    """Wendet das benutzerdefinierte CSS an"""
    st.markdown("""
        <style>
            /* CSS aus der Originaldatei */
        </style>
    """, unsafe_allow_html=True)
```

### components/chat.py
```python
import streamlit as st

def show_chat_history():
    """Zeigt den Chat-Verlauf an"""
    
def show_input_field():
    """Rendert das Nachrichten-Eingabefeld"""
```

## Migrationsschritte
1. Neue Dateien mit den oben gezeigten Grundstrukturen erstellen
2. Code aus my_app.py in entsprechende Module verschieben
3. Importe in my_app.py anpassen
4. UI-Komponenten isolieren
5. Cross-Module Abhängigkeiten überprüfen