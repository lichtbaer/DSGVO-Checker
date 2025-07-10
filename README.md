# DSGVO-Checker

AI-powered GDPR compliance document checker using OpenAI GPT models and Streamlit.

## Overview

DSGVO-Checker is a comprehensive tool for analyzing documents for GDPR (General Data Protection Regulation) compliance. It uses advanced AI models to automatically check documents against customizable compliance criteria and generates detailed reports.

## Features

- **Multi-format Document Support**: PDF, DOCX, DOC, TXT files
- **AI-Powered Analysis**: Uses OpenAI GPT models for intelligent compliance checking
- **Customizable Protocol**: Define and edit compliance criteria through the web interface
- **Comprehensive Reports**: Generate detailed compliance reports with scores, issues, and recommendations
- **Export Functionality**: Export reports as Word documents
- **User-Friendly Interface**: Clean Streamlit-based web interface

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DSGVO-Checker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env_example.txt .env
```
Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided URL (usually `http://localhost:8501`)

3. Use the application:
   - **Document Upload**: Upload documents to analyze
   - **Protocol Management**: Define or edit compliance criteria
   - **Compliance Check**: Run AI-powered compliance analysis
   - **Report Generation**: Generate and export detailed reports

## Project Structure

```
DSGVO-Checker/
├── app.py                 # Main Streamlit application
├── document_processor.py  # Document text extraction
├── compliance_checker.py  # AI-powered compliance analysis
├── report_generator.py    # Report generation and export
├── protocol_manager.py    # Protocol management
├── requirements.txt       # Python dependencies
├── env_example.txt       # Environment variables example
└── README.md            # This file
```

## Components

### Document Processor
- Extracts text from various document formats
- Supports PDF, DOCX, DOC, and TXT files
- Handles file parsing errors gracefully

### Compliance Checker
- Uses OpenAI GPT models for intelligent analysis
- Checks documents against customizable criteria
- Provides detailed scores, issues, and recommendations

### Report Generator
- Creates comprehensive compliance reports
- Supports Word document export
- Includes executive summaries and detailed findings

### Protocol Manager
- Manages GDPR compliance criteria
- Provides default protocol with common GDPR requirements
- Allows custom criteria definition

## Default Compliance Criteria

The application includes default GDPR compliance criteria across 8 key areas:

1. **Personal Data Identification**
2. **Legal Basis**
3. **Data Subject Rights**
4. **Data Security**
5. **Data Retention**
6. **Third Party Sharing**
7. **Consent Management**
8. **Data Breach Procedures**

## Configuration

### OpenAI API
- Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Add the key to your `.env` file
- The application uses GPT-4 by default (configurable)

### Custom Protocols
- Edit compliance criteria through the web interface
- Protocols are saved as JSON files
- Default protocol is automatically created on first run

## Development

### Adding New Document Formats
Extend the `DocumentProcessor` class to support additional file formats.

### Customizing AI Analysis
Modify the `ComplianceChecker` class to adjust AI prompts and analysis logic.

### Report Customization
Extend the `ReportGenerator` class to add new report formats or modify existing ones.

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for AI model access

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please create an issue in the repository.