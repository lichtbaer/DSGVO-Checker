#!/bin/bash

# DSGVO-Checker Documentation Server

echo "📚 DSGVO-Checker Documentation Server"
echo "======================================"

# Check if mkdocs is installed
if ! command -v mkdocs &> /dev/null; then
    echo "📦 Installing MkDocs dependencies..."
    pip install mkdocs==1.5.3 mkdocs-material==9.5.13 mkdocs-git-revision-date-localized-plugin==1.2.1 mkdocs-minify-plugin==0.7.2
fi

# Check if docs directory exists
if [ ! -d "docs" ]; then
    echo "❌ Docs directory not found. Please ensure the documentation files are present."
    exit 1
fi

# Check if mkdocs.yml exists
if [ ! -f "mkdocs.yml" ]; then
    echo "❌ mkdocs.yml not found. Please ensure the MkDocs configuration is present."
    exit 1
fi

echo "🚀 Starting MkDocs documentation server..."
echo "📖 Documentation will be available at: http://localhost:8000"
echo "🔄 Press Ctrl+C to stop the server"
echo ""

# Start MkDocs server
mkdocs serve --dev-addr=0.0.0.0:8000 