# Configuration API

## Übersicht

Die Konfiguration des DSGVO-Checkers erfolgt über Umgebungsvariablen und eine zentrale Konfigurationsklasse.

## Umgebungsvariablen

### OpenAI Konfiguration

| Variable | Typ | Standard | Beschreibung |
|----------|-----|----------|--------------|
| `OPENAI_API_KEY` | string | - | OpenAI API Schlüssel (erforderlich) |
| `OPENAI_MODEL` | string | `gpt-4` | Zu verwendendes KI-Modell |
| `OPENAI_BASE_URL` | string | - | LiteLLM Proxy URL (optional) |

### Anwendungs-Konfiguration

| Variable | Typ | Standard | Beschreibung |
|----------|-----|----------|--------------|
| `LOG_LEVEL` | string | `INFO` | Logging-Level |
| `MAX_FILE_SIZE` | int | `10485760` | Maximale Dateigröße in Bytes |
| `ALLOWED_FILE_TYPES` | string | `pdf,docx,doc,txt` | Komma-getrennte Liste erlaubter Dateitypen |

### AI-Analyse Konfiguration

| Variable | Typ | Standard | Beschreibung |
|----------|-----|----------|--------------|
| `MAX_TOKENS` | int | `2000` | Maximale Tokens für AI-Antworten |
| `TEMPERATURE` | float | `0.3` | AI-Modell Temperatur |
| `MAX_CONTENT_LENGTH` | int | `8000` | Maximale Dokumentlänge für Analyse |

### Datei-Pfade

| Variable | Typ | Standard | Beschreibung |
|----------|-----|----------|--------------|
| `DATA_DIR` | string | `./data` | Verzeichnis für Daten |
| `LOGS_DIR` | string | `./logs` | Verzeichnis für Logs |
| `PROTOCOL_FILE` | string | `gdpr_protocol.json` | Protokoll-Datei |

## Konfigurationsklasse

### AppConfig

Die zentrale Konfigurationsklasse `AppConfig` verwaltet alle Einstellungen:

```python
from config import get_config

config = get_config()

# OpenAI Konfiguration
api_key = config.openai_api_key
model = config.openai_model
base_url = config.openai_base_url

# Anwendungs-Konfiguration
log_level = config.log_level
max_file_size = config.max_file_size
allowed_types = config.allowed_file_types
```

### Validierung

Die Konfiguration wird automatisch validiert:

```python
try:
    config.validate()
except ValueError as e:
    print(f"Konfigurationsfehler: {e}")
```

### OpenAI Client Konfiguration

Für Proxy-Support:

```python
client_config = config.get_openai_client_config()
# Returns: {'api_key': '...', 'base_url': '...'} if proxy configured
```

## Beispiel-Konfigurationen

### Standard OpenAI

```bash
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
```

### Mit LiteLLM Proxy

```bash
OPENAI_API_KEY=your-proxy-key
OPENAI_BASE_URL=http://localhost:4000/v1
OPENAI_MODEL=gpt-4
```

### Produktions-Konfiguration

```bash
LOG_LEVEL=WARNING
MAX_FILE_SIZE=52428800  # 50MB
ALLOWED_FILE_TYPES=pdf,docx
MAX_TOKENS=4000
TEMPERATURE=0.1
```

## Docker-Konfiguration

### docker-compose.yml

```yaml
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}
  - OPENAI_MODEL=${OPENAI_MODEL:-gpt-4}
  - OPENAI_BASE_URL=${OPENAI_BASE_URL:-}
  - LOG_LEVEL=${LOG_LEVEL:-INFO}
  - MAX_FILE_SIZE=${MAX_FILE_SIZE:-10485760}
```

### .env Datei

```bash
# Erstellen Sie eine .env Datei
cp env_example.txt .env

# Bearbeiten Sie die Werte
OPENAI_API_KEY=your-key-here
OPENAI_BASE_URL=https://your-proxy.com/v1
```

## Fehlerbehebung

### Häufige Konfigurationsfehler

1. **Fehlender API Key**
   ```
   ValueError: OPENAI_API_KEY is required
   ```

2. **Ungültige Dateigröße**
   ```
   ValueError: MAX_FILE_SIZE must be positive
   ```

3. **Leere Dateitypen**
   ```
   ValueError: ALLOWED_FILE_TYPES cannot be empty
   ```

### Debugging

```python
from config import get_config

config = get_config()
print(f"API Key: {'Set' if config.openai_api_key else 'Not set'}")
print(f"Base URL: {config.openai_base_url or 'Direct API'}")
print(f"Model: {config.openai_model}")
``` 