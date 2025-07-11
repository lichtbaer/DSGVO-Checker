import streamlit as st
import os
from pathlib import Path
import tempfile
import json
from datetime import datetime
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
import time

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

class ProgressTracker:
    """Tracks progress for async operations"""
    
    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.current_step = 0
        self.current_file = ""
        self.current_operation = ""
        self.lock = threading.Lock()
    
    def update_progress(self, step, file_name="", operation=""):
        """Update progress with thread safety"""
        with self.lock:
            self.current_step = step
            self.current_file = file_name
            self.current_operation = operation
    
    def get_progress(self):
        """Get current progress information"""
        with self.lock:
            return {
                'current_step': self.current_step,
                'total_steps': self.total_steps,
                'progress': self.current_step / self.total_steps if self.total_steps > 0 else 0,
                'current_file': self.current_file,
                'current_operation': self.current_operation
            }

def process_single_file(file, protocol, language, progress_tracker, file_index):
    """Process a single file with progress tracking"""
    try:
        # Create progress callback for document processing
        def document_progress_callback(progress, message):
            # Map document processing progress (0-1) to overall progress (0-50% of file processing)
            overall_progress = file_index * 2 + progress * 0.5
            progress_tracker.update_progress(overall_progress, file.name, message)
        
        # Update progress - Document processing
        progress_tracker.update_progress(
            file_index * 2, 
            file.name, 
            "Starting document processing"
        )
        
        # Process document with progress tracking
        document_processor = DocumentProcessor()
        text_content = document_processor.extract_text(file, document_progress_callback)
        
        # Update progress - Compliance checking
        progress_tracker.update_progress(
            file_index * 2 + 0.5, 
            file.name, 
            "Analyzing compliance with AI"
        )
        
        # Check compliance
        compliance_checker = ComplianceChecker()
        file_result = compliance_checker.check_compliance(
            text_content,
            protocol,
            file.name,
            language
        )
        
        # Update progress - Completed
        progress_tracker.update_progress(
            file_index * 2 + 1, 
            file.name, 
            "Completed"
        )
        
        return file_result
        
    except Exception as e:
        logger.error(f"Error processing file {file.name}: {str(e)}")
        return {
            'filename': file.name,
            'overall_score': 0.0,
            'section_results': {},
            'summary': f"Error processing file: {str(e)}"
        }

def run_async_compliance_check(files, protocol, language):
    """Run compliance check asynchronously with progress tracking"""
    total_steps = len(files) * 2  # 2 steps per file: processing + compliance check
    progress_tracker = ProgressTracker(total_steps)
    
    # Create progress placeholder
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    def update_progress_display():
        """Update progress display in Streamlit"""
        try:
            while True:
                progress_info = progress_tracker.get_progress()
                
                # Use st.session_state to communicate between threads
                st.session_state['progress_info'] = progress_info
                
                time.sleep(0.1)  # Update every 100ms
                
                # Stop if all files are processed
                if progress_info['current_step'] >= progress_info['total_steps']:
                    break
        except Exception as e:
            logger.error(f"Error in progress display thread: {e}")
    
    # Start progress display in a separate thread
    progress_thread = threading.Thread(target=update_progress_display)
    progress_thread.daemon = True
    progress_thread.start()
    
    # Process files with ThreadPoolExecutor
    results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(process_single_file, file, protocol, language, progress_tracker, i): file 
            for i, file in enumerate(files)
        }
        
        # Collect results as they complete
        for future in future_to_file:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"Error in async processing: {str(e)}")
                # Add error result
                file = future_to_file[future]
                results.append({
                    'filename': file.name,
                    'overall_score': 0.0,
                    'section_results': {},
                    'summary': f"Error: {str(e)}"
                })
    
    # Clear progress display
    progress_placeholder.empty()
    status_placeholder.empty()
    
    return results

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
    
    # Initialize session state
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'check_protocol' not in st.session_state:
        st.session_state.check_protocol = {}
    if 'compliance_results' not in st.session_state:
        st.session_state.compliance_results = []
    if 'selected_protocol' not in st.session_state:
        st.session_state.selected_protocol = None
    if 'language' not in st.session_state:
        st.session_state.language = "Deutsch"
    
    # Initialize current page in session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Document Upload"
    
    # Sidebar for navigation and settings
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Seite wählen:",
            ["Document Upload", "Protocol Management", "Compliance Check", "Report Generation"],
            index=["Document Upload", "Protocol Management", "Compliance Check", "Report Generation"].index(st.session_state.current_page)
        )
        
        # Update current page
        st.session_state.current_page = page
        
        st.markdown("---")
        st.header("Einstellungen")
        
        # Language selection
        language = st.selectbox(
            "Sprache für Berichte:",
            ["Deutsch", "English"],
            index=0 if st.session_state.language == "Deutsch" else 1
        )
        st.session_state.language = language
    
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
        # Validate uploaded files with progress tracking
        file_validator = FileValidator()
        valid_files = []
        
        # Create progress tracking for file validation
        validation_progress = st.progress(0)
        validation_status = st.empty()
        
        total_files = len(uploaded_files)
        for i, file in enumerate(uploaded_files):
            validation_progress.progress((i + 1) / total_files)
            validation_status.text(f"Validating {file.name}...")
            
            is_valid, error_msg = file_validator.validate_file(file)
            if is_valid:
                valid_files.append(file)
            else:
                st.error(f"Invalid file {file.name}: {error_msg}")
        
        # Clear progress indicators
        validation_progress.empty()
        validation_status.empty()
        
        if valid_files:
            # Store valid files in session state
            st.session_state.uploaded_files = valid_files
            st.success(f"✅ Uploaded {len(valid_files)} valid document(s)")
            
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
            
            # Add navigation button for workflow improvement
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔍 Zur Compliance-Prüfung", type="primary", use_container_width=True):
                    st.session_state.current_page = "Compliance Check"
                    st.rerun()
        else:
            st.warning("No valid files uploaded")
    else:
        # Clear uploaded files from session state if no files are uploaded
        if 'uploaded_files' in st.session_state:
            del st.session_state.uploaded_files

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
    
    # Debug information
    st.write(f"Debug: Session state keys: {list(st.session_state.keys())}")
    st.write(f"Debug: uploaded_files in session: {'uploaded_files' in st.session_state}")
    if 'uploaded_files' in st.session_state:
        st.write(f"Debug: Number of uploaded files: {len(st.session_state.uploaded_files)}")
    
    if not st.session_state.get('uploaded_files'):
        st.warning("Please upload documents first in the Document Upload section.")
        st.info("💡 Tip: Go to 'Document Upload' page, upload files, and then return here.")
        return
    
    # Load available protocols
    protocol_manager = ProtocolManager()
    available_protocols = protocol_manager.load_protocol()
    
    # Protocol selection
    st.subheader("📋 Select Check Protocol")
    
    if not available_protocols:
        st.warning("No protocols available. Please create a protocol in the Protocol Management section.")
        return
    
    # Create protocol options for selection
    protocol_options = ["Use All Available Protocols (Default)"]
    protocol_options.extend(list(available_protocols.keys()))
    
    selected_protocol = st.selectbox(
        "Choose protocol to use for compliance checking:",
        protocol_options,
        index=0,
        help="Select 'Use All Available Protocols' to check against all criteria, or choose a specific section"
    )
    
    # Set the protocol for checking
    if selected_protocol == "Use All Available Protocols (Default)":
        st.session_state.check_protocol = available_protocols
        st.info("✅ Using all available protocols for comprehensive compliance checking")
    else:
        st.session_state.check_protocol = {selected_protocol: available_protocols[selected_protocol]}
        st.info(f"✅ Using protocol: {selected_protocol}")
    
    # Display selected protocol
    st.subheader("Selected Protocol")
    for section, criteria in st.session_state.check_protocol.items():
        with st.expander(f"📋 {section}"):
            for criterion in criteria:
                st.write(f"• {criterion}")
    
    # Manual start button only (removed auto-start)
    if st.button("🚀 Start Compliance Check", type="primary"):
        st.info("🚀 Starting compliance check...")
        
        # Initialize progress tracking
        st.session_state['progress_info'] = None
        
        # Run async compliance check
        results = run_async_compliance_check(
            st.session_state.uploaded_files,
            st.session_state.check_protocol,
            st.session_state.language
        )
        
        st.session_state.compliance_results = results
        st.success("✅ Compliance check completed!")
    
    # Display progress if available
    if 'progress_info' in st.session_state and st.session_state['progress_info']:
        progress_info = st.session_state['progress_info']
        st.progress(progress_info['progress'])
        if progress_info['current_file']:
            st.text(f"Processing: {progress_info['current_file']} - {progress_info['current_operation']}")
    
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
        
        # Add "View Results" button for workflow improvement
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📊 Ergebnisse anzeigen", type="primary", use_container_width=True):
                st.session_state.current_page = "Report Generation"
                st.rerun()

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
        # Create progress tracking for report generation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Prepare report data
            status_text.text("📊 Preparing report data...")
            progress_bar.progress(25)
            
            report_data = {
                'results': st.session_state.compliance_results,
                'protocol': st.session_state.check_protocol,
                'options': {
                    'include_summary': include_summary,
                    'include_details': include_details,
                    'include_recommendations': include_recommendations
                }
            }
            
            # Step 2: Generate report based on format
            status_text.text("📄 Generating report...")
            progress_bar.progress(50)
            
            if report_format == "Streamlit Display":
                progress_bar.progress(75)
                status_text.text("📊 Displaying report...")
                display_report(report_data)
                progress_bar.progress(100)
                status_text.text("✅ Report displayed successfully!")
                
            elif report_format == "Word Document":
                progress_bar.progress(75)
                status_text.text("📄 Creating Word document...")
                download_word_report(report_data)
                progress_bar.progress(100)
                status_text.text("✅ Word report ready for download!")
                
            elif report_format == "PDF":
                progress_bar.progress(75)
                status_text.text("📄 Creating PDF document...")
                download_pdf_report(report_data)
                progress_bar.progress(100)
                status_text.text("✅ PDF report ready for download!")
                
        except Exception as e:
            st.error(f"❌ Error generating report: {str(e)}")
            logger.error(f"Report generation error: {str(e)}")
        finally:
            # Clear progress indicators after a delay
            time.sleep(2)
            progress_bar.empty()
            status_text.empty()

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
                    
                    if section_result.get('references'):
                        st.write("**References (Fundstellen):**")
                        for criterion, refs in section_result['references'].items():
                            st.write(f"- {criterion}:")
                            for ref in refs:
                                st.write(f"    • {ref}")
    
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
    
    # Create progress callback for report generation
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    def report_progress_callback(progress, message):
        progress_placeholder.progress(progress)
        status_placeholder.text(message)
    
    try:
        doc_bytes = report_generator.generate_word_report(report_data, report_progress_callback)
        
        # Clear progress indicators
        progress_placeholder.empty()
        status_placeholder.empty()
        
        st.download_button(
            label="📥 Download Word Report",
            data=doc_bytes,
            file_name=f"gdpr_compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"❌ Error generating Word report: {str(e)}")
        logger.error(f"Word report generation error: {str(e)}")
    finally:
        # Clear progress indicators
        progress_placeholder.empty()
        status_placeholder.empty()

def download_pdf_report(report_data):
    report_generator = ReportGenerator()
    
    # Create progress callback for report generation
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    def report_progress_callback(progress, message):
        progress_placeholder.progress(progress)
        status_placeholder.text(message)
    
    try:
        pdf_bytes = report_generator.generate_pdf_report(report_data, report_progress_callback)
        
        # Clear progress indicators
        progress_placeholder.empty()
        status_placeholder.empty()
        
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name=f"gdpr_compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"❌ Error generating PDF report: {str(e)}")
        logger.error(f"PDF report generation error: {str(e)}")
    finally:
        # Clear progress indicators
        progress_placeholder.empty()
        status_placeholder.empty()

if __name__ == "__main__":
    main() 