# Verwendung

## Workflow Übersicht

Der DSGVO-Checker bietet einen optimierten Workflow mit automatischen Weiterleitungen:

1. **Dokumente hochladen** → 2. **Prüfung starten** → 3. **Ergebnisse anzeigen**

## Schritt-für-Schritt Anleitung

### Schritt 1: Dokumente hochladen

1. Öffnen Sie die Anwendung unter http://localhost:8501
2. Navigieren Sie zur Seite "Document Upload"
3. Laden Sie Ihre Dokumente hoch:
   - **Unterstützte Formate**: PDF, DOCX, DOC, TXT
   - **Maximale Größe**: 10MB pro Datei
   - **Mehrere Dateien**: Möglich

4. Nach dem Hochladen erscheint der **"Prüfung starten"** Button

### Schritt 2: Automatische Prüfung

1. Klicken Sie auf **"Prüfung starten"**
2. Das System leitet Sie automatisch zur Prüfungsseite weiter
3. Die KI-Analyse läuft automatisch für alle hochgeladenen Dokumente
4. Fortschrittsanzeige zeigt den Status der Prüfung
5. Nach Abschluss erscheint der **"Ergebnisse anzeigen"** Button

### Schritt 3: Ergebnisse und Export

1. Klicken Sie auf **"Ergebnisse anzeigen"**
2. Das System leitet Sie zur Ergebnis-Seite weiter
3. Betrachten Sie die detaillierten Compliance-Bewertungen
4. Exportieren Sie Berichte als Word-Dokument

## Protokoll-Management

### Standard-Protokoll

Das System verwendet ein vordefiniertes DSGVO-Compliance-Protokoll:

- **Personenbezogene Daten Identifikation**
- **Rechtliche Grundlage**
- **Betroffenenrechte**
- **Datensicherheit**
- **Datenaufbewahrung**
- **Drittanbieter-Weitergabe**
- **Einwilligungsverwaltung**
- **Datenverletzungsverfahren**

### Protokoll anpassen

1. Navigieren Sie zur Seite "Protocol Management"
2. Bearbeiten Sie die Kriterien für jeden Bereich
3. Fügen Sie neue Kriterien hinzu oder entfernen Sie bestehende
4. Speichern Sie das Protokoll

## Berichtgenerierung

### Bericht-Optionen

- **Executive Summary**: Übersicht und Statistiken
- **Detaillierte Ergebnisse**: Einzelne Dokument-Analysen
- **Empfehlungen**: Verbesserungsvorschläge

### Export-Formate

- **Streamlit-Anzeige**: Interaktive Darstellung
- **Word-Dokument**: Download als .docx
- **PDF** (in Entwicklung)

## Erweiterte Funktionen

### LiteLLM Proxy

Für die Verwendung verschiedener LLM-Anbieter:

1. Konfigurieren Sie `OPENAI_BASE_URL` in der `.env` Datei
2. Starten Sie Ihren LiteLLM Proxy
3. Die Anwendung verwendet automatisch den konfigurierten Proxy

### Batch-Verarbeitung

- Laden Sie mehrere Dokumente gleichzeitig hoch
- Das System verarbeitet alle Dokumente in einer Sitzung
- Vergleichbare Ergebnisse für alle Dokumente

### Validierung

Das System validiert automatisch:

- **Dateityp**: Nur erlaubte Formate
- **Dateigröße**: Maximale Größe beachten
- **Inhalt**: Leere Dateien werden abgelehnt
- **Proxy-Verbindung**: Bei konfiguriertem Proxy

## Tipps für optimale Ergebnisse

### Dokumentvorbereitung

- Verwenden Sie klare, strukturierte Dokumente
- Stellen Sie sicher, dass der Text gut lesbar ist
- Vermeiden Sie stark formatierte oder gescannte Dokumente

### Protokoll-Optimierung

- Passen Sie die Kriterien an Ihre spezifischen Anforderungen an
- Fügen Sie branchenspezifische Compliance-Anforderungen hinzu
- Testen Sie das Protokoll mit bekannten Dokumenten

### System-Performance

- Begrenzen Sie die Anzahl gleichzeitig verarbeiteter Dokumente
- Verwenden Sie eine stabile Internetverbindung
- Überwachen Sie die API-Nutzung bei OpenAI

## Fehlerbehebung

### Häufige Probleme

1. **Dokumente werden nicht hochgeladen**
   - Prüfen Sie Dateityp und -größe
   - Stellen Sie sicher, dass die Datei nicht beschädigt ist

2. **Prüfung schlägt fehl**
   - Überprüfen Sie die OpenAI API Konfiguration
   - Prüfen Sie die Internetverbindung
   - Schauen Sie in die Logs für Details

3. **Proxy-Verbindung funktioniert nicht**
   - Testen Sie die Proxy-URL manuell
   - Überprüfen Sie die Authentifizierung
   - Verwenden Sie `python test_proxy.py`

### Logs und Debugging

```bash
# Docker Logs
docker compose logs -f

# Lokale Logs
tail -f logs/dsgvo_checker_*.log

# Proxy-Test
python test_proxy.py
``` 