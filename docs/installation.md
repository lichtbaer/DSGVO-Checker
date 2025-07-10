# Installation

## Voraussetzungen

- Python 3.8+ (für lokale Entwicklung)
- Docker (für Container-Deployment)
- OpenAI API Key
- Internetverbindung für KI-Modelle

## Option 1: Docker Installation (Empfohlen)

### 1. Repository klonen

```bash
git clone <repository-url>
cd DSGVO-Checker
```

### 2. Umgebungsvariablen konfigurieren

```bash
cp env_example.txt .env
```

Bearbeiten Sie die `.env` Datei:

```bash
# OpenAI API Key (erforderlich)
OPENAI_API_KEY=your_openai_api_key_here

# OpenAI Model (optional)
OPENAI_MODEL=gpt-4

# LiteLLM Proxy (optional)
OPENAI_BASE_URL=https://your-proxy-url.com/v1
```

### 3. Container starten

```bash
docker compose up -d
```

### 4. Anwendung öffnen

Öffnen Sie http://localhost:8501 in Ihrem Browser.

## Option 2: Lokale Installation

### 1. Python-Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 2. Umgebungsvariablen konfigurieren

```bash
cp env_example.txt .env
# Bearbeiten Sie die .env Datei wie oben beschrieben
```

### 3. Anwendung starten

```bash
streamlit run app.py
```

## Konfiguration

### Umgebungsvariablen

| Variable | Beschreibung | Standard |
|----------|--------------|----------|
| `OPENAI_API_KEY` | OpenAI API Schlüssel | - |
| `OPENAI_MODEL` | Zu verwendendes Modell | `gpt-4` |
| `OPENAI_BASE_URL` | LiteLLM Proxy URL | - |
| `LOG_LEVEL` | Logging-Level | `INFO` |
| `MAX_FILE_SIZE` | Maximale Dateigröße (Bytes) | `10485760` |
| `ALLOWED_FILE_TYPES` | Erlaubte Dateitypen | `pdf,docx,doc,txt` |

### LiteLLM Proxy Konfiguration

Für die Verwendung von LiteLLM Proxy:

```bash
# LiteLLM Proxy starten
litellm --model gpt-4 --port 4000

# DSGVO-Checker konfigurieren
OPENAI_BASE_URL=http://localhost:4000/v1
OPENAI_API_KEY=your_proxy_key
```

## Verifizierung

### Installation testen

```bash
python test_installation.py
```

### Proxy-Verbindung testen

```bash
python test_proxy.py
```

## Troubleshooting

### Häufige Probleme

1. **Container startet nicht**
   - Prüfen Sie die `.env` Datei
   - Stellen Sie sicher, dass Docker läuft

2. **OpenAI API Fehler**
   - Überprüfen Sie den API Key
   - Prüfen Sie die Internetverbindung

3. **Proxy-Verbindung fehlschlägt**
   - Testen Sie die Proxy-URL
   - Überprüfen Sie die Authentifizierung

### Logs anzeigen

```bash
# Docker Logs
docker compose logs -f

# Lokale Logs
tail -f logs/dsgvo_checker_*.log
``` 