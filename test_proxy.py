#!/usr/bin/env python3
"""
Test script to validate LiteLLM proxy connections
"""

import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import get_config
from utils.proxy_validator import ProxyValidator

def test_proxy_connection():
    """Test proxy connection and configuration"""
    print("🔗 DSGVO-Checker Proxy Connection Test")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    config = get_config()
    
    print(f"OpenAI API Key: {'✓ Set' if config.openai_api_key else '✗ Not set'}")
    print(f"OpenAI Model: {config.openai_model}")
    print(f"Base URL: {config.openai_base_url or 'Direct OpenAI API'}")
    print()
    
    # Test proxy validation
    proxy_validator = ProxyValidator()
    
    # Validate configuration
    is_valid, error_msg = proxy_validator.validate_proxy_config()
    if not is_valid:
        print(f"✗ Configuration error: {error_msg}")
        return False
    
    # Test connection
    is_connected, message = proxy_validator.test_proxy_connection()
    if is_connected:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")
        return False
    
    # Get proxy info
    proxy_info = proxy_validator.get_proxy_info()
    print(f"\nProxy Information:")
    print(f"  Base URL: {proxy_info['base_url']}")
    print(f"  Model: {proxy_info['model']}")
    print(f"  Using Proxy: {proxy_info['has_proxy']}")
    
    print("\n✅ Proxy configuration is valid!")
    return True

def main():
    """Main test function"""
    try:
        success = test_proxy_connection()
        if success:
            print("\n🎉 All tests passed! Proxy is ready to use.")
        else:
            print("\n❌ Tests failed. Please check your configuration.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 