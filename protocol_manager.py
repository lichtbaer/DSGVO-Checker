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
        self.config = get_config()
        self.protocol_file = protocol_file if protocol_file else self.config.protocol_file
        """
        Initialize the protocol manager
        
        Args:
            protocol_file: Path to the protocol JSON file
        """
        self.protocol_file = protocol_file
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
            print(f"Error saving protocol: {e}")
            return False
    
    def _ensure_protocol_file_exists(self):
        """Ensure the protocol file exists with default content"""
        # Create data directory if it doesn't exist
        protocol_dir = os.path.dirname(self.protocol_file)
        if protocol_dir and not os.path.exists(protocol_dir):
            os.makedirs(protocol_dir, exist_ok=True)
            
        if not os.path.exists(self.protocol_file):
            default_protocol = self._get_default_protocol()
            self.save_protocol(default_protocol)
    
    def _get_default_protocol(self) -> Dict[str, List[str]]:
        """Get the default GDPR compliance protocol"""
        return {
            "Personal Data Identification": [
                "Check if personal data is being processed",
                "Identify types of personal data collected",
                "Verify data minimization principles",
                "Check for special categories of personal data"
            ],
            "Legal Basis": [
                "Verify legal basis for data processing",
                "Check if consent is properly obtained",
                "Ensure legitimate interest is properly documented",
                "Verify contractual necessity claims"
            ],
            "Data Subject Rights": [
                "Ensure right to access is addressed",
                "Check right to rectification procedures",
                "Verify right to erasure (right to be forgotten)",
                "Ensure right to data portability",
                "Check right to object procedures"
            ],
            "Data Security": [
                "Verify appropriate technical measures",
                "Check organizational security measures",
                "Ensure data encryption in transit and at rest",
                "Verify access controls and authentication"
            ],
            "Data Retention": [
                "Check data retention policies",
                "Verify deletion procedures",
                "Ensure retention periods are justified",
                "Check data archiving practices"
            ],
            "Third Party Sharing": [
                "Verify data processor agreements",
                "Check third party data sharing practices",
                "Ensure appropriate safeguards for transfers",
                "Verify international data transfer compliance"
            ],
            "Consent Management": [
                "Check consent collection procedures",
                "Verify consent withdrawal mechanisms",
                "Ensure consent is freely given",
                "Check consent record keeping"
            ],
            "Data Breach Procedures": [
                "Verify data breach detection procedures",
                "Check notification requirements",
                "Ensure incident response plans",
                "Verify breach documentation procedures"
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