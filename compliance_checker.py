import openai
import os
import json
from typing import Dict, List, Any
import streamlit as st
from config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)

class ComplianceChecker:
    """
    Uses OpenAI GPT models to check documents for GDPR compliance
    """
    
    def __init__(self):
        """Initialize the compliance checker with OpenAI API"""
        self.config = get_config()
        client_config = self.config.get_openai_client_config()
        self.client = openai.OpenAI(**client_config)
        self.model = self.config.openai_model
    
    def check_compliance(self, text_content: str, protocol: Dict[str, List[str]], filename: str) -> Dict[str, Any]:
        """
        Check document compliance against GDPR protocol
        
        Args:
            text_content: Extracted text from document
            protocol: Dictionary of compliance criteria by section
            filename: Name of the file being checked
            
        Returns:
            Dict containing compliance results
        """
        if not text_content.strip():
            return self._create_empty_result(filename)
        
        # Prepare the analysis prompt
        prompt = self._create_analysis_prompt(text_content, protocol)
        
        try:
            # Get AI analysis
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a GDPR compliance expert. Analyze the provided document against the given compliance criteria and provide detailed assessment with scores, issues, and recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Parse the response
            analysis_result = self._parse_ai_response(response.choices[0].message.content)
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(analysis_result['section_results'])
            
            return {
                'filename': filename,
                'overall_score': overall_score,
                'section_results': analysis_result['section_results'],
                'summary': analysis_result.get('summary', '')
            }
            
        except Exception as e:
            st.error(f"Error during compliance check: {str(e)}")
            return self._create_error_result(filename, str(e))
    
    def _create_analysis_prompt(self, text_content: str, protocol: Dict[str, List[str]]) -> str:
        """Create the analysis prompt for the AI model"""
        
        # Truncate content if too long (GPT-4 has token limits)
        max_chars = self.config.max_content_length
        if len(text_content) > max_chars:
            text_content = text_content[:max_chars] + "\n[Content truncated due to length]"
        
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
        
        Please provide your analysis in the following JSON format:
        {
            "summary": "Brief overall assessment",
            "section_results": {
                "Section Name": {
                    "score": 85.5,
                    "issues": ["Issue 1", "Issue 2"],
                    "recommendations": ["Recommendation 1", "Recommendation 2"]
                }
            }
        }
        
        Guidelines:
        - Score each section from 0-100 based on compliance level
        - Identify specific issues found in the document
        - Provide actionable recommendations for improvement
        - Be specific and reference the document content
        - Consider both explicit mentions and implicit compliance requirements
        """
        
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the AI response into structured data"""
        try:
            # Try to extract JSON from the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback parsing if JSON extraction fails
                return self._fallback_parsing(response_text)
                
        except json.JSONDecodeError:
            return self._fallback_parsing(response_text)
    
    def _fallback_parsing(self, response_text: str) -> Dict[str, Any]:
        """Fallback parsing method if JSON parsing fails"""
        # Create a basic structure with default values
        default_sections = [
            "Personal Data Identification",
            "Legal Basis", 
            "Data Subject Rights",
            "Data Security",
            "Data Retention",
            "Third Party Sharing",
            "Consent Management",
            "Data Breach Procedures"
        ]
        
        section_results = {}
        for section in default_sections:
            section_results[section] = {
                "score": 50.0,  # Default neutral score
                "issues": ["Unable to parse AI response properly"],
                "recommendations": ["Review document manually for compliance"]
            }
        
        return {
            "summary": "Analysis completed but response parsing encountered issues",
            "section_results": section_results
        }
    
    def _calculate_overall_score(self, section_results: Dict[str, Dict]) -> float:
        """Calculate overall compliance score from section scores"""
        if not section_results:
            return 0.0
        
        total_score = sum(section['score'] for section in section_results.values())
        return total_score / len(section_results)
    
    def _create_empty_result(self, filename: str) -> Dict[str, Any]:
        """Create result for empty documents"""
        return {
            'filename': filename,
            'overall_score': 0.0,
            'section_results': {},
            'summary': 'Document is empty or could not be processed'
        }
    
    def _create_error_result(self, filename: str, error_message: str) -> Dict[str, Any]:
        """Create result for processing errors"""
        return {
            'filename': filename,
            'overall_score': 0.0,
            'section_results': {},
            'summary': f'Error during processing: {error_message}'
        } 