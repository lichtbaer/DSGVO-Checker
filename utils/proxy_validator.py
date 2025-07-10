"""
Proxy validation utilities for DSGVO-Checker
"""

import requests
from typing import Tuple, Optional
from config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)

class ProxyValidator:
    """Validates and tests proxy connections"""
    
    def __init__(self):
        self.config = get_config()
    
    def test_proxy_connection(self) -> Tuple[bool, str]:
        """
        Test the proxy connection
        
        Returns:
            Tuple of (is_valid, message)
        """
        if not self.config.openai_base_url:
            return True, "No proxy configured, using direct OpenAI API"
        
        try:
            # Test basic connectivity
            response = requests.get(
                f"{self.config.openai_base_url}/models",
                headers={
                    "Authorization": f"Bearer {self.config.openai_api_key}",
                    "Content-Type": "application/json"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return True, f"Proxy connection successful: {self.config.openai_base_url}"
            else:
                return False, f"Proxy connection failed with status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Proxy connection error: {str(e)}"
    
    def get_proxy_info(self) -> dict:
        """
        Get proxy configuration information
        
        Returns:
            Dictionary with proxy information
        """
        return {
            'base_url': self.config.openai_base_url or 'Direct OpenAI API',
            'model': self.config.openai_model,
            'has_proxy': bool(self.config.openai_base_url)
        }
    
    def validate_proxy_config(self) -> Tuple[bool, str]:
        """
        Validate proxy configuration
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.config.openai_api_key:
            return False, "OPENAI_API_KEY is required"
        
        if self.config.openai_base_url:
            # Validate URL format
            if not self.config.openai_base_url.startswith(('http://', 'https://')):
                return False, "OPENAI_BASE_URL must be a valid HTTP/HTTPS URL"
            
            # Test connection
            is_valid, message = self.test_proxy_connection()
            if not is_valid:
                return False, f"Proxy validation failed: {message}"
        
        return True, "" 