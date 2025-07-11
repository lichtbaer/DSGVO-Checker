"""
Configuration module for DSGVO-Checker
Handles all environment variables and application settings
"""

import os
from typing import List
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class AppConfig:
    """Application configuration class"""
    
    # OpenAI Configuration
    openai_api_key: str = os.getenv('OPENAI_API_KEY', '')
    openai_model: str = os.getenv('OPENAI_MODEL', 'gpt-4')
    openai_base_url: str = os.getenv('OPENAI_BASE_URL', '')
    
    # Application Settings
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    max_file_size: int = int(os.getenv('MAX_FILE_SIZE', '10485760'))  # 10MB default
    allowed_file_types: List[str] = field(default_factory=lambda: os.getenv('ALLOWED_FILE_TYPES', 'pdf,docx,doc,txt').split(','))
    
    # Streamlit Configuration
    streamlit_port: int = int(os.getenv('STREAMLIT_SERVER_PORT', '8501'))
    streamlit_address: str = os.getenv('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')
    
    # File Paths
    data_dir: str = os.getenv('DATA_DIR', './data')
    logs_dir: str = os.getenv('LOGS_DIR', './logs')
    protocol_file: str = os.getenv('PROTOCOL_FILE', './data/gdpr_protocol.json')
    
    # AI Analysis Settings
    max_tokens: int = int(os.getenv('MAX_TOKENS', '2000'))
    temperature: float = float(os.getenv('TEMPERATURE', '0.1'))
    max_content_length: int = int(os.getenv('MAX_CONTENT_LENGTH', '8000'))
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")
        
        # Validate OpenAI API key format (should start with 'sk-')
        if self.openai_api_key and not self.openai_api_key.startswith('sk-'):
            raise ValueError("OPENAI_API_KEY should start with 'sk-'")
        
        if self.max_file_size <= 0:
            raise ValueError("MAX_FILE_SIZE must be positive")
        
        if not self.allowed_file_types:
            raise ValueError("ALLOWED_FILE_TYPES cannot be empty")
        
        # Validate temperature range
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("TEMPERATURE must be between 0.0 and 2.0")
        
        # Validate max_tokens
        if self.max_tokens <= 0:
            raise ValueError("MAX_TOKENS must be positive")
        
        return True
    
    def get_openai_client_config(self) -> dict:
        """Get OpenAI client configuration including base URL for proxy support"""
        config = {
            'api_key': self.openai_api_key
        }
        
        if self.openai_base_url:
            config['base_url'] = self.openai_base_url
        
        return config
    
    def get_allowed_extensions(self) -> List[str]:
        """Get list of allowed file extensions"""
        return [f".{ext.strip()}" for ext in self.allowed_file_types]

# Global configuration instance
config = AppConfig()

def get_config() -> AppConfig:
    """Get the global configuration instance"""
    return config 