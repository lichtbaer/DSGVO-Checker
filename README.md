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
- **Docker Support**: Containerized deployment with environment-based configuration
- **Modular Architecture**: Well-structured, maintainable codebase

## Quick Start with Docker

### Option 1: Using Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd DSGVO-Checker
   ```

2. **Set up environment variables:**
   ```bash
   cp env_example.txt .env
   ```
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Start the application:**
   ```bash
   docker-compose up -d
   ```

4. **Access the application:**
   Open your browser and navigate to `http://localhost:8501`

### Option 2: Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t dsgvo-checker .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8501:8501 \
     -e OPENAI_API_KEY=your_api_key_here \
     -v $(pwd)/data:/app/data \
     -v $(pwd)/logs:/app/logs \
     dsgvo-checker
   ```

## Local Development

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd DSGVO-Checker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env_example.txt .env
   ```
   Edit `.env` and add your OpenAI API key.

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Test installation:**
   ```bash
   python test_installation.py
   ```

## Configuration

The application uses environment variables for configuration. Key settings include:

### OpenAI Configuration
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: GPT model to use (default: gpt-4)

### Application Settings
- `LOG_LEVEL`: Logging level (default: INFO)
- `MAX_FILE_SIZE`: Maximum file size in bytes (default: 10MB)
- `ALLOWED_FILE_TYPES`: Comma-separated list of allowed file types

### AI Analysis Settings
- `MAX_TOKENS`: Maximum tokens for AI responses (default: 2000)
- `TEMPERATURE`: AI model temperature (default: 0.3)
- `MAX_CONTENT_LENGTH`: Maximum document content length (default: 8000)

### File Paths
- `DATA_DIR`: Directory for data storage (default: ./data)
- `LOGS_DIR`: Directory for log files (default: ./logs)
- `PROTOCOL_FILE`: Protocol file path (default: gdpr_protocol.json)

## Project Structure

```
DSGVO-Checker/
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration management
├── document_processor.py     # Document text extraction
├── compliance_checker.py     # AI-powered compliance analysis
├── report_generator.py       # Report generation and export
├── protocol_manager.py       # Protocol management
├── utils/                    # Shared utilities
│   ├── __init__.py
│   ├── logger.py            # Logging utilities
│   └── file_validator.py    # File validation
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker container definition
├── docker-compose.yml       # Docker Compose configuration
├── .dockerignore           # Docker ignore file
├── env_example.txt         # Environment variables example
├── test_installation.py    # Installation verification
└── README.md              # This file
```

## Architecture

### Modular Design

The application follows a modular architecture with clear separation of concerns:

- **Configuration Management**: Centralized configuration using environment variables
- **Document Processing**: Handles multiple file formats with validation
- **AI Analysis**: OpenAI integration for compliance checking
- **Protocol Management**: Customizable GDPR compliance criteria
- **Report Generation**: Multiple output formats with export functionality
- **Utilities**: Shared logging and validation utilities

### Key Components

#### Document Processor
- Extracts text from various document formats
- Supports PDF, DOCX, DOC, and TXT files
- Handles file parsing errors gracefully
- Configurable file size and type restrictions

#### Compliance Checker
- Uses OpenAI GPT models for intelligent analysis
- Checks documents against customizable criteria
- Provides detailed scores, issues, and recommendations
- Configurable AI parameters (temperature, max tokens)

#### Report Generator
- Creates comprehensive compliance reports
- Supports Word document export
- Includes executive summaries and detailed findings
- Configurable report options

#### Protocol Manager
- Manages GDPR compliance criteria
- Provides default protocol with common GDPR requirements
- Allows custom criteria definition
- JSON-based storage for persistence

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

## Docker Deployment

### Production Deployment

For production deployment, consider:

1. **Environment Variables**: Use proper secrets management
2. **Volumes**: Mount persistent storage for data and logs
3. **Health Checks**: Monitor application health
4. **Resource Limits**: Set appropriate CPU/memory limits

### Example Production docker-compose.yml

```yaml
version: '3.8'

services:
  dsgvo-checker:
    build: .
    container_name: dsgvo-checker
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LOG_LEVEL=WARNING
      - MAX_FILE_SIZE=52428800  # 50MB
    volumes:
      - dsgvo_data:/app/data
      - dsgvo_logs:/app/logs
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'

volumes:
  dsgvo_data:
  dsgvo_logs:
```

## Development

### Adding New Document Formats
Extend the `DocumentProcessor` class to support additional file formats.

### Customizing AI Analysis
Modify the `ComplianceChecker` class to adjust AI prompts and analysis logic.

### Report Customization
Extend the `ReportGenerator` class to add new report formats or modify existing ones.

### Adding New Configuration Options
1. Add new fields to `AppConfig` in `config.py`
2. Update environment variable handling
3. Add validation if needed

## Requirements

- Python 3.8+ (for local development)
- Docker (for containerized deployment)
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