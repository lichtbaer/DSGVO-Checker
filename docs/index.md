# DSGVO-Checker Documentation

Willkommen zur DSGVO-Checker Dokumentation!

## Überblick

DSGVO-Checker ist ein KI-gestütztes Tool zur automatischen Überprüfung von Dokumenten auf DSGVO-Compliance. Das System verwendet OpenAI GPT-Modelle und bietet eine benutzerfreundliche Streamlit-Oberfläche.

## Schnellstart

### 1. Installation

```bash
# Repository klonen
git clone <repository-url>
cd DSGVO-Checker

# Mit Docker (empfohlen)
docker compose up -d

# Oder lokal
pip install -r requirements.txt
streamlit run app.py
```

### 2. Konfiguration

Erstellen Sie eine `.env` Datei:

```bash
cp env_example.txt .env
```

Bearbeiten Sie die `.env` Datei:

```bash
# OpenAI API Key
OPENAI_API_KEY=your_api_key_here

# LiteLLM Proxy (optional)
OPENAI_BASE_URL=https://your-proxy-url.com/v1
```

### 3. Anwendung starten

Öffnen Sie http://localhost:8501 in Ihrem Browser.

## Workflow

### Schritt 1: Dokumente hochladen
- Laden Sie PDF, DOCX, DOC oder TXT Dateien hoch
- Das System validiert automatisch Dateityp und Größe

### Schritt 2: Automatische Prüfung starten
- Klicken Sie auf "Prüfung starten"
- Das System leitet Sie zur Prüfungsseite weiter
- Die KI-Analyse läuft automatisch für alle Dokumente

### Schritt 3: Ergebnisse anzeigen
- Nach Abschluss der Prüfung erscheint "Ergebnisse anzeigen"
- Klicken Sie auf den Button für detaillierte Ergebnisse
- Exportieren Sie Berichte als Word-Dokument

## Features

- **Multi-Format Support**: PDF, DOCX, DOC, TXT
- **KI-gestützte Analyse**: OpenAI GPT Modelle
- **Automatische Weiterleitung**: Optimierter Workflow
- **Export-Funktionen**: Word-Dokumente
- **Docker-Support**: Einfache Bereitstellung
- **LiteLLM Proxy**: Flexible LLM-Anbieter

## Support

Bei Fragen oder Problemen erstellen Sie ein Issue im Repository. 