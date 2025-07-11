# API Components

## Overview

DSGVO-Checker consists of several core components that work together to provide GDPR compliance checking functionality.

## Core Components

### DocumentProcessor

Handles text extraction from various document formats.

**Location**: `document_processor.py`

**Key Methods**:
- `extract_text(uploaded_file)`: Extracts text from uploaded files
- `_extract_from_pdf(uploaded_file)`: PDF text extraction
- `_extract_from_docx(uploaded_file)`: DOCX text extraction
- `_extract_from_txt(uploaded_file)`: TXT text extraction

**Supported Formats**: PDF, DOCX, DOC, TXT

### ComplianceChecker

Uses OpenAI GPT models to analyze documents for GDPR compliance.

**Location**: `compliance_checker.py`

**Key Methods**:
- `check_compliance(text_content, protocol, filename, language)`: Main compliance checking method
- `_create_analysis_prompt(text_content, protocol, language)`: Creates AI prompts
- `_parse_ai_response(response_text, language)`: Parses AI responses

**Features**:
- Multi-language support (German/English)
- Structured JSON output
- Configurable AI parameters

### ReportGenerator

Generates compliance reports in various formats.

**Location**: `report_generator.py`

**Key Methods**:
- `generate_word_report(report_data)`: Creates Word documents
- `generate_pdf_report(report_data)`: Creates PDF reports

**Supported Formats**: Word (.docx), PDF

### ProtocolManager

Manages GDPR compliance criteria and protocols.

**Location**: `protocol_manager.py`

**Key Methods**:
- `load_protocol()`: Loads protocol from file
- `save_protocol(protocol)`: Saves protocol to file
- `_get_default_protocol()`: Returns default GDPR criteria

**Features**:
- JSON-based storage
- Default GDPR compliance criteria
- Customizable protocols

## Utility Components

### FileValidator

Validates uploaded files for size, type, and content.

**Location**: `utils/file_validator.py`

**Key Methods**:
- `validate_file(uploaded_file)`: Validates file properties
- `get_file_info(uploaded_file)`: Returns file information

### ProxyValidator

Validates and tests proxy connections for LiteLLM.

**Location**: `utils/proxy_validator.py`

**Key Methods**:
- `test_proxy_connection()`: Tests proxy connectivity
- `validate_proxy_config()`: Validates proxy configuration

### Logger

Centralized logging functionality.

**Location**: `utils/logger.py`

**Key Functions**:
- `setup_logger(name)`: Sets up logger with file and console handlers
- `get_logger(name)`: Returns logger instance

## Configuration

### AppConfig

Central configuration management.

**Location**: `config.py`

**Key Properties**:
- OpenAI API configuration
- File size and type limits
- AI model parameters
- File paths and directories

## Integration

All components are integrated through the main Streamlit application (`app.py`) which provides:

- Web-based user interface
- Session state management
- Navigation between different sections
- Error handling and user feedback 