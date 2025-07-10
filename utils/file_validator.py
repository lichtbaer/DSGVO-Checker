"""
File validation utilities for DSGVO-Checker
"""

import os
from typing import List, Tuple
from pathlib import Path
from config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)

class FileValidator:
    """Validates uploaded files for size, type, and content"""
    
    def __init__(self):
        self.config = get_config()
    
    def validate_file(self, uploaded_file) -> Tuple[bool, str]:
        """
        Validate uploaded file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check file size
            if uploaded_file.size > self.config.max_file_size:
                return False, f"File size exceeds maximum allowed size of {self.config.max_file_size} bytes"
            
            # Check file extension
            file_extension = self._get_file_extension(uploaded_file.name)
            if not self._is_allowed_extension(file_extension):
                allowed_types = ", ".join(self.config.allowed_file_types)
                return False, f"File type not allowed. Allowed types: {allowed_types}"
            
            # Check if file is empty
            if uploaded_file.size == 0:
                return False, "File is empty"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"Error validating file {uploaded_file.name}: {str(e)}")
            return False, f"Error validating file: {str(e)}"
    
    def _get_file_extension(self, filename: str) -> str:
        """Get file extension from filename"""
        return Path(filename).suffix.lower()
    
    def _is_allowed_extension(self, extension: str) -> bool:
        """Check if file extension is allowed"""
        allowed_extensions = self.config.get_allowed_extensions()
        return extension in allowed_extensions
    
    def get_file_info(self, uploaded_file) -> dict:
        """
        Get file information
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Dictionary with file information
        """
        return {
            'name': uploaded_file.name,
            'size': uploaded_file.size,
            'type': uploaded_file.type,
            'extension': self._get_file_extension(uploaded_file.name)
        } 