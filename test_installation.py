#!/usr/bin/env python3
"""
Test script to verify DSGVO-Checker installation
"""

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import streamlit
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    try:
        import openai
        print("✓ OpenAI imported successfully")
    except ImportError as e:
        print(f"✗ OpenAI import failed: {e}")
        return False
    
    try:
        import PyPDF2
        print("✓ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"✗ PyPDF2 import failed: {e}")
        return False
    
    try:
        from docx import Document
        print("✓ python-docx imported successfully")
    except ImportError as e:
        print(f"✗ python-docx import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ python-dotenv import failed: {e}")
        return False
    
    try:
        import pandas
        print("✓ Pandas imported successfully")
    except ImportError as e:
        print(f"✗ Pandas import failed: {e}")
        return False
    
    try:
        import plotly
        print("✓ Plotly imported successfully")
    except ImportError as e:
        print(f"✗ Plotly import failed: {e}")
        return False
    
    return True

def test_local_modules():
    """Test that local modules can be imported"""
    try:
        from document_processor import DocumentProcessor
        print("✓ DocumentProcessor imported successfully")
    except ImportError as e:
        print(f"✗ DocumentProcessor import failed: {e}")
        return False
    
    try:
        from compliance_checker import ComplianceChecker
        print("✓ ComplianceChecker imported successfully")
    except ImportError as e:
        print(f"✗ ComplianceChecker import failed: {e}")
        return False
    
    try:
        from report_generator import ReportGenerator
        print("✓ ReportGenerator imported successfully")
    except ImportError as e:
        print(f"✗ ReportGenerator import failed: {e}")
        return False
    
    try:
        from protocol_manager import ProtocolManager
        print("✓ ProtocolManager imported successfully")
    except ImportError as e:
        print(f"✗ ProtocolManager import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment configuration"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your_openai_api_key_here':
        print("✓ OpenAI API key configured")
        return True
    else:
        print("⚠ OpenAI API key not configured (set OPENAI_API_KEY in .env file)")
        return False

def main():
    """Run all tests"""
    print("DSGVO-Checker Installation Test")
    print("=" * 40)
    
    all_passed = True
    
    print("\nTesting external dependencies...")
    if not test_imports():
        all_passed = False
    
    print("\nTesting local modules...")
    if not test_local_modules():
        all_passed = False
    
    print("\nTesting environment configuration...")
    if not test_environment():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ All tests passed! DSGVO-Checker is ready to use.")
        print("\nTo start the application, run:")
        print("streamlit run app.py")
    else:
        print("✗ Some tests failed. Please check the installation.")
        print("\nTo install dependencies, run:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main() 