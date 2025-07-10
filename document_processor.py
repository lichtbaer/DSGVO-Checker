import PyPDF2
from docx import Document
import io
import streamlit as st
from config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)

class DocumentProcessor:
    """
    Handles extraction of text content from various document formats
    """
    
    def __init__(self):
        self.config = get_config()
    
    def extract_text(self, uploaded_file):
        """
        Extract text content from uploaded file based on its format
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            str: Extracted text content
        """
        file_extension = uploaded_file.name.lower().split('.')[-1]
        
        try:
            if file_extension == 'pdf':
                return self._extract_from_pdf(uploaded_file)
            elif file_extension in ['docx', 'doc']:
                return self._extract_from_docx(uploaded_file)
            elif file_extension == 'txt':
                return self._extract_from_txt(uploaded_file)
            else:
                st.error(f"Unsupported file format: {file_extension}")
                return ""
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            return ""
    
    def _extract_from_pdf(self, uploaded_file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"
            
            return text_content.strip()
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    def _extract_from_docx(self, uploaded_file):
        """Extract text from DOCX file"""
        try:
            doc = Document(uploaded_file)
            text_content = ""
            
            for paragraph in doc.paragraphs:
                text_content += paragraph.text + "\n"
            
            return text_content.strip()
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    def _extract_from_txt(self, uploaded_file):
        """Extract text from TXT file"""
        try:
            # Reset file pointer to beginning
            uploaded_file.seek(0)
            text_content = uploaded_file.read().decode('utf-8')
            return text_content.strip()
        except Exception as e:
            st.error(f"Error reading TXT: {str(e)}")
            return "" 