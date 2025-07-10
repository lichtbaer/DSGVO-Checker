import streamlit as st
import os
from pathlib import Path
import tempfile
import json
from datetime import datetime

from config import get_config
from utils.logger import get_logger
from utils.file_validator import FileValidator
from utils.proxy_validator import ProxyValidator
from document_processor import DocumentProcessor
from compliance_checker import ComplianceChecker
from report_generator import ReportGenerator
from protocol_manager import ProtocolManager

# Initialize configuration and logging
config = get_config()
logger = get_logger(__name__)

# Validate configuration
try:
    config.validate()
except ValueError as e:
    st.error(f"Configuration error: {e}")
    st.stop()

# Validate proxy configuration
proxy_validator = ProxyValidator()
is_valid, error_msg = proxy_validator.validate_proxy_config()
if not is_valid:
    st.error(f"Proxy configuration error: {error_msg}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="DSGVO-Checker",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🔒 DSGVO-Checker")
    st.markdown("AI-powered GDPR compliance document checker")
    
    # Display proxy information
    proxy_info = proxy_validator.get_proxy_info()
    if proxy_info['has_proxy']:
        st.info(f"🔗 Using proxy: {proxy_info['base_url']}")
    else:
        st.info("🔗 Using direct OpenAI API")
    
    # Initialize session state
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'check_protocol' not in st.session_state:
        st.session_state.check_protocol = {}
    if 'compliance_results' not in st.session_state:
        st.session_state.compliance_results = []
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["Document Upload", "Protocol Management", "Compliance Check", "Report Generation"]
        )
    
    # Main content based on selected page
    if page == "Document Upload":
        show_document_upload()
    elif page == "Protocol Management":
        show_protocol_management()
    elif page == "Compliance Check":
        show_compliance_check()
    elif page == "Report Generation":
        show_report_generation()

def show_document_upload():
    st.header("📄 Document Upload")
    
    uploaded_files = st.file_uploader(
        "Upload documents to check for GDPR compliance",
        type=config.allowed_file_types,
        accept_multiple_files=True,
        help=f"Supported formats: {', '.join(config.allowed_file_types)}"
    )
    
    if uploaded_files:
        # Validate uploaded files
        file_validator = FileValidator()
        valid_files = []
        
        for file in uploaded_files:
            is_valid, error_msg = file_validator.validate_file(file)
            if is_valid:
                valid_files.append(file)
            else:
                st.error(f"Invalid file {file.name}: {error_msg}")
        
        if valid_files:
            st.session_state.uploaded_files = valid_files
            st.success(f"Uploaded {len(valid_files)} valid document(s)")
            
            # Display uploaded files
            st.subheader("Uploaded Documents:")
            for i, file in enumerate(valid_files):
                file_info = file_validator.get_file_info(file)
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"📎 {file_info['name']} ({file_info['size']} bytes)")
                with col2:
                    if st.button(f"Remove", key=f"remove_{i}"):
                        st.session_state.uploaded_files.pop(i)
                        st.rerun()
        else:
            st.warning("No valid files uploaded")

def show_protocol_management():
    st.header("📋 Protocol Management")
    
    protocol_manager = ProtocolManager()
    
    # Load existing protocol
    protocol = protocol_manager.load_protocol()
    
    st.subheader("GDPR Compliance Check Protocol")
    st.markdown("Define the criteria for GDPR compliance checking:")
    
    # Protocol sections
    sections = {
        "Personal Data Identification": "Check if personal data is being processed",
        "Legal Basis": "Verify legal basis for data processing",
        "Data Subject Rights": "Ensure data subject rights are addressed",
        "Data Security": "Check security measures and data protection",
        "Data Retention": "Verify data retention policies",
        "Third Party Sharing": "Check third party data sharing practices",
        "Consent Management": "Verify consent collection and management",
        "Data Breach Procedures": "Check data breach notification procedures"
    }
    
    updated_protocol = {}
    
    for section, description in sections.items():
        st.markdown(f"**{section}**")
        st.caption(description)
        
        # Get existing criteria or create new ones
        existing_criteria = protocol.get(section, [])
        
        criteria_list = []
        for i, criterion in enumerate(existing_criteria):
            col1, col2 = st.columns([4, 1])
            with col1:
                criteria_list.append(st.text_input(
                    f"Criterion {i+1}",
                    value=criterion,
                    key=f"{section}_{i}"
                ))
            with col2:
                if st.button("❌", key=f"del_{section}_{i}"):
                    existing_criteria.pop(i)
                    st.rerun()
        
        # Add new criterion
        new_criterion = st.text_input(
            "Add new criterion",
            key=f"new_{section}",
            placeholder="Enter new criterion..."
        )
        
        if new_criterion:
            criteria_list.append(new_criterion)
        
        updated_protocol[section] = [c for c in criteria_list if c.strip()]
    
    # Save protocol
    if st.button("💾 Save Protocol"):
        protocol_manager.save_protocol(updated_protocol)
        st.success("Protocol saved successfully!")
    
    # Display current protocol
    if protocol:
        st.subheader("Current Protocol")
        for section, criteria in protocol.items():
            with st.expander(f"📋 {section}"):
                for criterion in criteria:
                    st.write(f"• {criterion}")

def show_compliance_check():
    st.header("🔍 Compliance Check")
    
    if not st.session_state.uploaded_files:
        st.warning("Please upload documents first in the Document Upload section.")
        return
    
    if not st.session_state.check_protocol:
        st.warning("Please define a check protocol in the Protocol Management section.")
        return
    
    # Initialize components
    document_processor = DocumentProcessor()
    compliance_checker = ComplianceChecker()
    
    if st.button("🚀 Start Compliance Check", type="primary"):
        with st.spinner("Processing documents and checking compliance..."):
            results = []
            
            for file in st.session_state.uploaded_files:
                st.write(f"Processing {file.name}...")
                
                # Process document
                text_content = document_processor.extract_text(file)
                
                # Check compliance
                file_result = compliance_checker.check_compliance(
                    text_content,
                    st.session_state.check_protocol,
                    file.name
                )
                
                results.append(file_result)
            
            st.session_state.compliance_results = results
            st.success("Compliance check completed!")
    
    # Display results
    if st.session_state.compliance_results:
        st.subheader("Compliance Check Results")
        
        for result in st.session_state.compliance_results:
            with st.expander(f"📄 {result['filename']}"):
                st.write(f"**Overall Compliance Score:** {result['overall_score']:.1f}%")
                
                # Display section results
                for section, section_result in result['section_results'].items():
                    st.markdown(f"**{section}:** {section_result['score']:.1f}%")
                    st.progress(section_result['score'] / 100)
                    
                    if section_result['issues']:
                        st.write("**Issues found:**")
                        for issue in section_result['issues']:
                            st.write(f"• {issue}")
                    
                    if section_result['recommendations']:
                        st.write("**Recommendations:**")
                        for rec in section_result['recommendations']:
                            st.write(f"• {rec}")

def show_report_generation():
    st.header("📊 Report Generation")
    
    if not st.session_state.compliance_results:
        st.warning("Please run a compliance check first.")
        return
    
    report_generator = ReportGenerator()
    
    st.subheader("Generate Compliance Report")
    
    # Report options
    col1, col2 = st.columns(2)
    with col1:
        include_summary = st.checkbox("Include Executive Summary", value=True)
        include_details = st.checkbox("Include Detailed Findings", value=True)
        include_recommendations = st.checkbox("Include Recommendations", value=True)
    
    with col2:
        report_format = st.selectbox(
            "Report Format",
            ["Streamlit Display", "Word Document", "PDF"]
        )
    
    if st.button("📄 Generate Report", type="primary"):
        with st.spinner("Generating report..."):
            report_data = {
                'results': st.session_state.compliance_results,
                'protocol': st.session_state.check_protocol,
                'options': {
                    'include_summary': include_summary,
                    'include_details': include_details,
                    'include_recommendations': include_recommendations
                }
            }
            
            if report_format == "Streamlit Display":
                display_report(report_data)
            elif report_format == "Word Document":
                download_word_report(report_data)
            elif report_format == "PDF":
                download_pdf_report(report_data)

def display_report(report_data):
    st.subheader("📊 Compliance Report")
    
    # Executive Summary
    if report_data['options']['include_summary']:
        st.markdown("## Executive Summary")
        
        total_files = len(report_data['results'])
        avg_score = sum(r['overall_score'] for r in report_data['results']) / total_files
        
        st.metric("Total Documents Analyzed", total_files)
        st.metric("Average Compliance Score", f"{avg_score:.1f}%")
        
        # Compliance distribution
        scores = [r['overall_score'] for r in report_data['results']]
        compliant = len([s for s in scores if s >= 80])
        needs_improvement = len([s for s in scores if 60 <= s < 80])
        non_compliant = len([s for s in scores if s < 60])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Compliant (≥80%)", compliant)
        col2.metric("Needs Improvement (60-79%)", needs_improvement)
        col3.metric("Non-Compliant (<60%)", non_compliant)
    
    # Detailed Results
    if report_data['options']['include_details']:
        st.markdown("## Detailed Findings")
        
        for result in report_data['results']:
            with st.expander(f"📄 {result['filename']} - {result['overall_score']:.1f}%"):
                for section, section_result in result['section_results'].items():
                    st.markdown(f"**{section}:** {section_result['score']:.1f}%")
                    
                    if section_result['issues']:
                        st.write("**Issues:**")
                        for issue in section_result['issues']:
                            st.write(f"• {issue}")
                    
                    if section_result['recommendations']:
                        st.write("**Recommendations:**")
                        for rec in section_result['recommendations']:
                            st.write(f"• {rec}")
    
    # Recommendations
    if report_data['options']['include_recommendations']:
        st.markdown("## Overall Recommendations")
        
        # Collect all recommendations
        all_recommendations = []
        for result in report_data['results']:
            for section_result in result['section_results'].values():
                all_recommendations.extend(section_result['recommendations'])
        
        # Remove duplicates and display
        unique_recommendations = list(set(all_recommendations))
        for rec in unique_recommendations:
            st.write(f"• {rec}")

def download_word_report(report_data):
    report_generator = ReportGenerator()
    doc_bytes = report_generator.generate_word_report(report_data)
    
    st.download_button(
        label="📥 Download Word Report",
        data=doc_bytes,
        file_name=f"gdpr_compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

def download_pdf_report(report_data):
    st.info("PDF export functionality will be implemented in a future version.")

if __name__ == "__main__":
    main() 