from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.shared import OxmlElement, qn
from datetime import datetime
from typing import Dict, List, Any
import io

class ReportGenerator:
    """
    Generates compliance reports in various formats
    """
    
    def generate_word_report(self, report_data: Dict[str, Any]) -> bytes:
        """
        Generate a Word document report
        
        Args:
            report_data: Dictionary containing report data
            
        Returns:
            bytes: Word document as bytes
        """
        doc = Document()
        
        # Add title
        title = doc.add_heading('GDPR Compliance Report', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add generation date
        date_para = doc.add_paragraph(f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph()  # Add spacing
        
        # Executive Summary
        if report_data['options']['include_summary']:
            self._add_executive_summary(doc, report_data)
        
        # Detailed Results
        if report_data['options']['include_details']:
            self._add_detailed_results(doc, report_data)
        
        # Recommendations
        if report_data['options']['include_recommendations']:
            self._add_recommendations(doc, report_data)
        
        # Save to bytes
        doc_bytes = io.BytesIO()
        doc.save(doc_bytes)
        doc_bytes.seek(0)
        
        return doc_bytes.getvalue()
    
    def _add_executive_summary(self, doc: Document, report_data: Dict[str, Any]):
        """Add executive summary section to the document"""
        doc.add_heading('Executive Summary', level=1)
        
        results = report_data['results']
        total_files = len(results)
        avg_score = sum(r['overall_score'] for r in results) / total_files if results else 0
        
        # Summary statistics
        doc.add_paragraph(f'Total Documents Analyzed: {total_files}')
        doc.add_paragraph(f'Average Compliance Score: {avg_score:.1f}%')
        
        # Compliance distribution
        scores = [r['overall_score'] for r in results]
        compliant = len([s for s in scores if s >= 80])
        needs_improvement = len([s for s in scores if 60 <= s < 80])
        non_compliant = len([s for s in scores if s < 60])
        
        doc.add_paragraph(f'Compliant Documents (≥80%): {compliant}')
        doc.add_paragraph(f'Documents Needing Improvement (60-79%): {needs_improvement}')
        doc.add_paragraph(f'Non-Compliant Documents (<60%): {non_compliant}')
        
        doc.add_paragraph()  # Add spacing
    
    def _add_detailed_results(self, doc: Document, report_data: Dict[str, Any]):
        """Add detailed results section to the document"""
        doc.add_heading('Detailed Findings', level=1)
        
        for result in report_data['results']:
            # Document header
            doc.add_heading(f"{result['filename']} - {result['overall_score']:.1f}%", level=2)
            
            # Section results
            for section_name, section_result in result['section_results'].items():
                doc.add_heading(section_name, level=3)
                
                # Score
                doc.add_paragraph(f"Compliance Score: {section_result['score']:.1f}%")
                
                # Issues
                if section_result['issues']:
                    doc.add_paragraph("Issues Found:")
                    for issue in section_result['issues']:
                        p = doc.add_paragraph()
                        p.add_run("• ").bold = True
                        p.add_run(issue)
                
                # Recommendations
                if section_result['recommendations']:
                    doc.add_paragraph("Recommendations:")
                    for rec in section_result['recommendations']:
                        p = doc.add_paragraph()
                        p.add_run("• ").bold = True
                        p.add_run(rec)
                
                doc.add_paragraph()  # Add spacing
    
    def _add_recommendations(self, doc: Document, report_data: Dict[str, Any]):
        """Add overall recommendations section to the document"""
        doc.add_heading('Overall Recommendations', level=1)
        
        # Collect all recommendations
        all_recommendations = []
        for result in report_data['results']:
            for section_result in result['section_results'].values():
                all_recommendations.extend(section_result['recommendations'])
        
        # Remove duplicates and add to document
        unique_recommendations = list(set(all_recommendations))
        for rec in unique_recommendations:
            p = doc.add_paragraph()
            p.add_run("• ").bold = True
            p.add_run(rec)
    
    def generate_pdf_report(self, report_data: Dict[str, Any]) -> bytes:
        """
        Generate a PDF report (placeholder for future implementation)
        
        Args:
            report_data: Dictionary containing report data
            
        Returns:
            bytes: PDF document as bytes
        """
        # This would be implemented with a library like reportlab or weasyprint
        # For now, return empty bytes
        return b"PDF generation not yet implemented" 