#!/bin/bash

# DSGVO-Checker Startup Script

set -e

echo "🔒 DSGVO-Checker Startup Script"
echo "================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env_example.txt .env
    echo "📝 Please edit .env file and add your OpenAI API key"
    echo "   Then run this script again."
    exit 1
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY=your_openai_api_key_here" .env; then
    echo "✅ Environment configuration looks good"
else
    echo "⚠️  Please set your OpenAI API key in .env file"
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data logs

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "🐳 Docker detected. Starting with Docker Compose..."
    
    # Build and start with docker-compose
    docker-compose up -d --build
    
    echo "✅ DSGVO-Checker is starting..."
    echo "🌐 Access the application at: http://localhost:8501"
    echo "📊 View logs with: docker-compose logs -f"
    
else
    echo "🐍 Docker not available. Starting with Python..."
    
    # Check if Python dependencies are installed
    if ! python -c "import streamlit" &> /dev/null; then
        echo "📦 Installing Python dependencies..."
        pip install -r requirements.txt
    fi
    
    echo "🚀 Starting DSGVO-Checker..."
    streamlit run app.py
fi

echo "�� Setup complete!" 