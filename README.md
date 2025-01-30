# STS Chat Interface

Eine Streamlit-basierte Chat-Oberfläche für die STS Support GmbH, die eine intuitive Benutzeroberfläche für KI-gestützte Interaktionen bietet.

## Architektur & Projektstruktur

Das Projekt folgt einer modularen Architektur mit klarer Trennung der Verantwortlichkeiten:

```
sts-chat/
├── components/                 # Wiederverwendbare UI-Komponenten
│   ├── chat.py                # Chat-Interface und Verlaufsanzeige
│   ├── header.py              # Header-Komponente
│   └── sidebar.py             # Sidebar-Navigation und Filterung
├── auth.py                    # Authentifizierung und Sessionmanagement
├── config.py                  # Konfiguration und Umgebungsvariablen
├── database.py                # Supabase Datenbankoperationen
├── main.py                    # Hauptanwendung und Routing
├── prompt_templates.xml       # XML-Vorlagen für Prompts
├── requirements.txt           # Projektabhängigkeiten
├── styles.py                  # CSS und UI-Styling
└── templates.py               # Template-Verarbeitung
```

### Kernkomponenten

#### Config (`config.py`)
- Zentrale Konfigurationsdatei
- Verwaltung von Umgebungsvariablen (Supabase URL, API Keys)
- Initialisierung des Supabase Clients

#### Auth (`auth.py`)
Hauptfunktionen:
- `handle_login(email: str, password: str) -> dict`: Login-Prozess
- `handle_logout()`: Logout-Prozess
- `check_session() -> bool`: Sessionüberprüfung

#### Database (`database.py`)
Kernfunktionalitäten:
- `create_conversation(user_id: str, title: str) -> str`: Neue Konversationen
- `load_conversations(user_id: str) -> list`: Laden von Benutzerkonversationen
- `save_message(conversation_id: str, message: str, response: str)`: Chatnachrichten speichern

#### UI-Komponenten
- **Chat (`components/chat.py`)**: Chat-Verlauf und Nachrichteneingabe
- **Header (`components/header.py`)**: Navigation und Branding
- **Sidebar (`components/sidebar.py`)**: Zusätzliche Navigation und Filter

## Technische Anforderungen

- Python 3.11.2
- Debian 12 Server
- Supabase-Datenbank
- Streamlit 1.27.2

## Installation auf Debian 12 Server

1. **System-Pakete aktualisieren:**
```bash
sudo apt update
sudo apt upgrade -y
```

2. **Python und benötigte Systempakete installieren:**
```bash
sudo apt install -y python3.11 python3.11-venv python3-pip git
```

3. **Projekt klonen:**
```bash
git clone [repository-url] /opt/sts-chat
cd /opt/sts-chat
```

4. **Virtuelle Umgebung erstellen und aktivieren:**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

5. **Abhängigkeiten installieren:**
```bash
pip install -r requirements.txt
```

6. **Umgebungsvariablen konfigurieren:**
Erstellen Sie eine `.env` Datei im Projektroot mit folgenden Variablen:
```env
SUPABASE_URL=ihre_supabase_url
SUPABASE_KEY=ihr_supabase_key
OPENAI_API_KEY=ihr_openai_api_key
```

## Deployment

1. **Systemd Service einrichten:**
Erstellen Sie eine Service-Datei unter `/etc/systemd/system/sts-chat.service`:
```ini
[Unit]
Description=STS Chat Interface
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/sts-chat
Environment="PATH=/opt/sts-chat/venv/bin"
ExecStart=/opt/sts-chat/venv/bin/streamlit run main.py --server.port 8501

[Install]
WantedBy=multi-user.target
```

2. **Service aktivieren und starten:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable sts-chat
sudo systemctl start sts-chat
```

## Entwicklungsumgebung

Für die lokale Entwicklung:
```bash
source venv/bin/activate
streamlit run main.py
```

Die Anwendung ist dann unter `http://localhost:8501` erreichbar.

## Wichtige Konfigurationen

### Streamlit-Konfiguration
Die Streamlit-Konfiguration kann in `.streamlit/config.toml` angepasst werden:
```toml
[server]
port = 8501
address = "0.0.0.0"

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Logging
Logs werden standardmäßig nach `/var/log/sts-chat.log` geschrieben. Die Log-Level können in `config.py` angepasst werden.

## Datenbank-Schema

Die Supabase-Datenbank verwendet folgende Haupttabellen:
- `conversations`: Speichert Chat-Verläufe
- `users`: Benutzerverwaltung
- `templates`: Prompt-Template-Verwaltung

## Sicherheitshinweise

- Alle API-Keys sollten sicher in der `.env` Datei gespeichert werden
- Die `.env` Datei ist in `.gitignore` aufgeführt und wird nicht versioniert
- Regelmäßige Backups der Datenbank sind empfohlen
- SSL/TLS-Verschlüsselung für Produktionsumgebungen ist erforderlich

## Wartung und Updates

1. **Code-Updates:**
```bash
cd /opt/sts-chat
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart sts-chat
```

2. **Datenbank-Backups:**
Regelmäßige Backups über Supabase Dashboard oder API durchführen.

## Fehlerbehandlung

Häufige Fehler und Lösungen:
1. **Verbindungsprobleme mit Supabase:**
   - Überprüfen Sie die Supabase-Credentials
   - Testen Sie die Netzwerkverbindung
   - Prüfen Sie die Supabase-Serverstatus

2. **Streamlit-Startprobleme:**
   - Überprüfen Sie die Log-Dateien
   - Stellen Sie sicher, dass der Port nicht belegt ist
   - Prüfen Sie die Python-Umgebung

## Support und Kontakt

Bei technischen Problemen oder Fragen wenden Sie sich an:
- Technischer Support: [Kontakt-Email]
- Dokumentation: [Link zur ausführlichen Dokumentation]
