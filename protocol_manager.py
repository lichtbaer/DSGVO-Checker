import json
import os
from typing import Dict, List, Any
from pathlib import Path
from config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)

class ProtocolManager:
    """
    Manages GDPR compliance check protocols
    """
    
    def __init__(self, protocol_file: str = ""):
        """
        Initialize the protocol manager
        
        Args:
            protocol_file: Path to the protocol JSON file
        """
        self.config = get_config()
        self.protocol_file = protocol_file if protocol_file else self.config.protocol_file
        self._ensure_protocol_file_exists()
    
    def load_protocol(self) -> Dict[str, List[str]]:
        """
        Load the current protocol from file
        
        Returns:
            Dict containing protocol sections and criteria
        """
        try:
            with open(self.protocol_file, 'r', encoding='utf-8') as f:
                protocol = json.load(f)
            return protocol
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default protocol if file doesn't exist or is invalid
            return self._get_default_protocol()
    
    def save_protocol(self, protocol: Dict[str, List[str]]) -> bool:
        """
        Save protocol to file
        
        Args:
            protocol: Dictionary containing protocol sections and criteria
            
        Returns:
            bool: True if save was successful
        """
        try:
            with open(self.protocol_file, 'w', encoding='utf-8') as f:
                json.dump(protocol, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error saving protocol: {e}")
            return False
    
    def _ensure_protocol_file_exists(self):
        """Ensure the protocol file exists with default content"""
        try:
            # Create data directory if it doesn't exist
            protocol_dir = os.path.dirname(self.protocol_file)
            if protocol_dir and not os.path.exists(protocol_dir):
                os.makedirs(protocol_dir, exist_ok=True)
                
            if not os.path.exists(self.protocol_file):
                default_protocol = self._get_default_protocol()
                self.save_protocol(default_protocol)
        except Exception as e:
            logger.error(f"Error ensuring protocol file exists: {e}")
            # Fallback: try to save to current directory
            self.protocol_file = "gdpr_protocol.json"
            if not os.path.exists(self.protocol_file):
                default_protocol = self._get_default_protocol()
                self.save_protocol(default_protocol)
    
    def _get_default_protocol(self) -> Dict[str, List[str]]:
        """Get the default GDPR compliance protocol in German"""
        return {
            "Identifikation personenbezogener Daten": [
                "Prüfung der Verarbeitung personenbezogener Daten",
                "Identifikation der Arten gesammelter personenbezogener Daten",
                "Überprüfung der Datensparsamkeit",
                "Prüfung auf besondere Kategorien personenbezogener Daten",
                "Verifizierung der Zweckbestimmung der Datenverarbeitung"
            ],
            "Rechtliche Grundlagen": [
                "Überprüfung der rechtlichen Grundlage für die Datenverarbeitung",
                "Prüfung der ordnungsgemäßen Einwilligung",
                "Dokumentation des berechtigten Interesses",
                "Verifizierung der vertraglichen Notwendigkeit",
                "Prüfung der gesetzlichen Verpflichtungen"
            ],
            "Rechte der betroffenen Person": [
                "Sicherstellung des Auskunftsrechts",
                "Prüfung der Berichtigungsverfahren",
                "Verifizierung des Löschungsrechts (Recht auf Vergessenwerden)",
                "Sicherstellung der Datenübertragbarkeit",
                "Prüfung der Widerspruchsverfahren",
                "Überprüfung der Einschränkungsrechte"
            ],
            "Datensicherheit": [
                "Verifizierung angemessener technischer Maßnahmen",
                "Prüfung organisatorischer Sicherheitsmaßnahmen",
                "Sicherstellung der Datenverschlüsselung bei Übertragung und Speicherung",
                "Verifizierung von Zugriffskontrollen und Authentifizierung",
                "Prüfung der Pseudonymisierung und Anonymisierung"
            ],
            "Datenaufbewahrung": [
                "Prüfung der Datenaufbewahrungsrichtlinien",
                "Verifizierung der Löschverfahren",
                "Sicherstellung gerechtfertigter Aufbewahrungsfristen",
                "Prüfung der Datenarchivierungspraktiken",
                "Überprüfung der automatisierten Löschung"
            ],
            "Datenweitergabe an Dritte": [
                "Verifizierung von Auftragsverarbeitungsverträgen",
                "Prüfung der Datenweitergabe an Dritte",
                "Sicherstellung angemessener Schutzmaßnahmen bei Übermittlungen",
                "Verifizierung der internationalen Datenübermittlung",
                "Prüfung der Standardvertragsklauseln"
            ],
            "Einwilligungsverwaltung": [
                "Prüfung der Einwilligungserhebung",
                "Verifizierung der Widerrufsmechanismen",
                "Sicherstellung der freiwilligen Einwilligung",
                "Prüfung der Einwilligungsdokumentation",
                "Überprüfung der altersgerechten Einwilligung"
            ],
            "Datenschutzverletzungen": [
                "Verifizierung der Erkennungsverfahren für Datenschutzverletzungen",
                "Prüfung der Benachrichtigungspflichten",
                "Sicherstellung von Incident-Response-Plänen",
                "Verifizierung der Dokumentationsverfahren für Verletzungen",
                "Prüfung der Meldung an Aufsichtsbehörden"
            ],
            "Medizinische Datenverarbeitung": [
                "Prüfung der ärztlichen Schweigepflicht",
                "Verifizierung der medizinischen Zweckbestimmung",
                "Sicherstellung der Qualitätssicherung in der Medizin",
                "Prüfung der Forschungszwecke in der Medizin",
                "Überprüfung der Gesundheitsdatenverarbeitung",
                "Verifizierung der medizinischen Notfallverarbeitung"
            ],
            "Daten von Minderjährigen": [
                "Prüfung der Altersverifizierung",
                "Verifizierung der elterlichen Einwilligung",
                "Sicherstellung des Kinderschutzes",
                "Prüfung der altersgerechten Informationsvermittlung",
                "Überprüfung der besonderen Schutzmaßnahmen",
                "Verifizierung der Risikobewertung für Minderjährige"
            ],
            "Forschungsdatenverarbeitung": [
                "Prüfung der wissenschaftlichen Forschungszwecke",
                "Verifizierung der Forschungsethik",
                "Sicherstellung der Forschungsfreiheit",
                "Prüfung der wissenschaftlichen Interessen",
                "Überprüfung der Forschungsdokumentation",
                "Verifizierung der Forschungsdatenarchivierung"
            ],
            "Öffentliche Verwaltung": [
                "Prüfung der behördlichen Aufgabenwahrnehmung",
                "Verifizierung der öffentlichen Interessen",
                "Sicherstellung der Transparenzpflichten",
                "Prüfung der behördlichen Informationspflichten",
                "Überprüfung der Verwaltungsverfahren",
                "Verifizierung der öffentlichen Sicherheit"
            ],
            "Beschäftigtendatenschutz": [
                "Prüfung der Beschäftigtendatenverarbeitung",
                "Verifizierung der betrieblichen Interessen",
                "Sicherstellung der Mitbestimmungsrechte",
                "Prüfung der Arbeitsplatzüberwachung",
                "Überprüfung der Beschäftigtendokumentation"
            ],
            "Marketing und Werbung": [
                "Prüfung der Direktwerbung",
                "Verifizierung der Profilbildung",
                "Sicherstellung der Werbeeinwilligung",
                "Prüfung der Tracking-Technologien",
                "Überprüfung der Marketingdatenverarbeitung"
            ],
            "Videoüberwachung": [
                "Prüfung der Überwachungszwecke",
                "Verifizierung der Kennzeichnungspflichten",
                "Sicherstellung der Verhältnismäßigkeit",
                "Prüfung der Aufbewahrungsfristen für Aufnahmen",
                "Überprüfung der Zugriffsberechtigungen"
            ],
            "Big Data und KI": [
                "Prüfung der automatisierten Entscheidungsfindung",
                "Verifizierung der Profilbildung",
                "Sicherstellung der Erklärbarkeit",
                "Prüfung der algorithmischen Transparenz",
                "Überprüfung der KI-Ethik",
                "Verifizierung der menschlichen Aufsicht"
            ]
        }
    
    def add_criterion(self, section: str, criterion: str) -> bool:
        """
        Add a new criterion to a section
        
        Args:
            section: Section name
            criterion: New criterion to add
            
        Returns:
            bool: True if addition was successful
        """
        protocol = self.load_protocol()
        
        if section not in protocol:
            protocol[section] = []
        
        if criterion not in protocol[section]:
            protocol[section].append(criterion)
            return self.save_protocol(protocol)
        
        return False
    
    def remove_criterion(self, section: str, criterion: str) -> bool:
        """
        Remove a criterion from a section
        
        Args:
            section: Section name
            criterion: Criterion to remove
            
        Returns:
            bool: True if removal was successful
        """
        protocol = self.load_protocol()
        
        if section in protocol and criterion in protocol[section]:
            protocol[section].remove(criterion)
            return self.save_protocol(protocol)
        
        return False
    
    def get_sections(self) -> List[str]:
        """
        Get list of all protocol sections
        
        Returns:
            List of section names
        """
        protocol = self.load_protocol()
        return list(protocol.keys())
    
    def get_criteria(self, section: str) -> List[str]:
        """
        Get criteria for a specific section
        
        Args:
            section: Section name
            
        Returns:
            List of criteria for the section
        """
        protocol = self.load_protocol()
        return protocol.get(section, []) 