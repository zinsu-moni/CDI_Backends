#!/usr/bin/env python3
"""
Railway Deployment Test Script
Test your deployed Crop Disease Identification API
"""

import requests
import json

def test_railway_deployment(base_url):
    """Test the deployed API endpoints"""
    
    print(f"🚀 Testing Railway deployment at: {base_url}")
    print("=" * 60)
    
    # Test 1: Health Check
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health Check: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health Check: FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Health Check: ERROR - {str(e)}")
    
    print()
    
    # Test 2: API Info
    try:
        response = requests.get(f"{base_url}/api/info", timeout=10)
        if response.status_code == 200:
            print("✅ API Info: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ API Info: FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ API Info: ERROR - {str(e)}")
    
    print()
    
    # Test 3: Root Endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root Endpoint: PASSED")
            print(f"   Content Length: {len(response.text)} characters")
        else:
            print(f"❌ Root Endpoint: FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Root Endpoint: ERROR - {str(e)}")
    
    print()
    print("🔗 Available Endpoints:")
    print(f"   • Health Check: {base_url}/health")
    print(f"   • API Info: {base_url}/api/info")
    print(f"   • Web Interface: {base_url}/")
    print(f"   • Disease Analysis: {base_url}/analyze (POST)")
    print(f"   • Chatbot: {base_url}/send-to-chatbot (POST)")

if __name__ == "__main__":
    # Replace with your actual Railway URL
    railway_url = input("Enter your Railway URL (e.g., https://your-project-name.up.railway.app): ").strip()
    
    if not railway_url:
        print("❌ Please provide a valid Railway URL")
        exit(1)
    
    # Remove trailing slash if present
    railway_url = railway_url.rstrip('/')
    
    test_railway_deployment(railway_url)
