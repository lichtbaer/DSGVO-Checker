import openai
import os
import json
import re
from typing import Dict, List, Any, Optional
import streamlit as st
from config import get_config
from utils.logger import get_logger
from pydantic import BaseModel, Field
from pydantic_ai import Agent

logger = get_logger(__name__)

class SectionResult(BaseModel):
    """Model for individual section compliance results"""
    score: float = Field(..., ge=0, le=100, description="Compliance score from 0-100")
    issues: List[str] = Field(..., description="List of compliance issues found")
    recommendations: List[str] = Field(..., description="List of recommendations for improvement")
    references: Dict[str, List[str]] = Field(..., description="References to document sections for each criterion")

class ComplianceAnalysis(BaseModel):
    """Model for complete compliance analysis"""
    summary: str = Field(..., description="Overall compliance assessment summary")
    section_results: Dict[str, SectionResult] = Field(..., description="Results for each compliance section")

class ComplianceChecker:
    """
    Uses OpenAI GPT models to check documents for GDPR compliance with Pydantic AI
    """
    
    def __init__(self):
        """Initialize the compliance checker with OpenAI API"""
        self.config = get_config()
        
        # Initialize Pydantic AI agent with better configuration
        model_name = f"openai:{self.config.openai_model}"
        self.agent = Agent(
            model_name,
            output_type=ComplianceAnalysis,
            api_key=self.config.openai_api_key,
            base_url=self.config.openai_base_url if self.config.openai_base_url else None,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
    
    def check_compliance(self, text_content: str, protocol: Dict[str, List[str]], filename: str, language: str = "Deutsch") -> Dict[str, Any]:
        """
        Check document compliance against GDPR protocol using Pydantic AI
        
        Args:
            text_content: Extracted text from document
            protocol: Dictionary of compliance criteria by section
            filename: Name of the file being checked
            language: Language for the analysis ("Deutsch" or "English")
            
        Returns:
            Dict containing compliance results
        """
        if not text_content.strip():
            return self._create_empty_result(filename, language)
        
        try:
            # Prepare the analysis prompt
            prompt = self._create_analysis_prompt(text_content, protocol, language)
            
            logger.info(f"Starting compliance check for {filename}")
            
            # Use Pydantic AI for structured output with synchronous call
            analysis_result = self.agent.run_sync(prompt)
            
            logger.info(f"Received AI response for {filename}")
            
            # Convert Pydantic model to dict
            result_dict = analysis_result.output.model_dump()
            
            logger.info(f"Parsed result for {filename}: {result_dict.get('summary', '')[:100]}...")
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(result_dict['section_results'])
            
            return {
                'filename': filename,
                'overall_score': overall_score,
                'section_results': result_dict['section_results'],
                'summary': result_dict.get('summary', '')
            }
            
        except Exception as e:
            logger.error(f"Error during compliance check for {filename}: {str(e)}")
            return self._create_error_result(filename, str(e), language)
    
    def _create_analysis_prompt(self, text_content: str, protocol: Dict[str, List[str]], language: str = "Deutsch") -> str:
        """Create the analysis prompt for the AI model"""
        
        # Truncate content if too long (GPT-4 has token limits)
        max_chars = self.config.max_content_length
        if len(text_content) > max_chars:
            text_content = text_content[:max_chars] + "\n[Content truncated due to length]"
        
        if language == "Deutsch":
            prompt = f"""
            Analysieren Sie das folgende Dokument auf DSGVO-Compliance basierend auf den bereitgestellten Kriterien.

            DOKUMENTINHALT:
            {text_content}

            COMPLIANCE-KRITERIEN:
            """
            
            for section, criteria in protocol.items():
                prompt += f"\n{section}:\n"
                for criterion in criteria:
                    prompt += f"- {criterion}\n"
            
            prompt += """
            
            Bitte analysieren Sie das Dokument und geben Sie eine strukturierte Bewertung zurück.
            
            Wichtige Anforderungen:
            - Scores zwischen 0-100 für jeden Abschnitt
            - Mindestens ein Issue und eine Recommendation pro Abschnitt
            - References für jedes Kriterium
            - Eine kurze Zusammenfassung der Gesamtbewertung
            """
        else:
            prompt = f"""
            Please analyze the following document for GDPR compliance based on the provided criteria.

            DOCUMENT CONTENT:
            {text_content}

            COMPLIANCE CRITERIA:
            """
            
            for section, criteria in protocol.items():
                prompt += f"\n{section}:\n"
                for criterion in criteria:
                    prompt += f"- {criterion}\n"
            
            prompt += """
            
            Please analyze the document and provide a structured assessment.
            
            Important requirements:
            - Scores between 0-100 for each section
            - At least one issue and one recommendation per section
            - References for each criterion
            - A brief summary of the overall assessment
            """
        
        return prompt
    
    def _calculate_overall_score(self, section_results: Dict[str, Dict]) -> float:
        """Calculate overall compliance score from section scores"""
        if not section_results:
            return 0.0
        
        total_score = sum(section.get('score', 0.0) for section in section_results.values())
        return total_score / len(section_results)
    
    def _create_empty_result(self, filename: str, language: str = "Deutsch") -> Dict[str, Any]:
        """Create result for empty documents"""
        if language == "Deutsch":
            return {
                'filename': filename,
                'overall_score': 0.0,
                'section_results': {},
                'summary': 'Dokument ist leer oder konnte nicht verarbeitet werden'
            }
        else:
            return {
                'filename': filename,
                'overall_score': 0.0,
                'section_results': {},
                'summary': 'Document is empty or could not be processed'
            }
    
    def _create_error_result(self, filename: str, error_message: str, language: str = "Deutsch") -> Dict[str, Any]:
        """Create result for processing errors"""
        if language == "Deutsch":
            return {
                'filename': filename,
                'overall_score': 0.0,
                'section_results': {},
                'summary': f'Fehler bei der Verarbeitung: {error_message}'
            }
        else:
            return {
                'filename': filename,
                'overall_score': 0.0,
                'section_results': {},
                'summary': f'Error during processing: {error_message}'
            } 