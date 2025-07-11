#!/usr/bin/env python3
"""
Render Startup Diagnostic Script
Check if all dependencies and configurations are correct before starting the main app
"""

import sys
import os
import importlib

def check_python_version():
    """Check Python version"""
    print(f"🐍 Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python version too old. Need 3.8+")
        return False
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'requests',
        'PIL',
        'openai',
        'httpx'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                importlib.import_module('PIL')
            else:
                importlib.import_module(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_environment_variables():
    """Check if required environment variables are set"""
    required_vars = ['PORT']
    optional_vars = ['API_KEY', 'DEEPSEEK_API_KEY']
    
    print("\n🔧 Environment Variables:")
    for var in required_vars:
        if os.environ.get(var):
            print(f"✅ {var} - Set")
        else:
            print(f"❌ {var} - Missing")
    
    for var in optional_vars:
        if os.environ.get(var):
            print(f"✅ {var} - Set")
        else:
            print(f"⚠️  {var} - Not set (will use default)")

def check_directories():
    """Check if required directories exist or can be created"""
    try:
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
            print("✅ Created uploads directory")
        else:
            print("✅ uploads directory exists")
        return True
    except Exception as e:
        print(f"❌ Failed to create uploads directory: {e}")
        return False

def test_fastapi_import():
    """Test if the main FastAPI app can be imported"""
    try:
        from main_fastapi import app
        print("✅ FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import FastAPI app: {e}")
        return False

def main():
    """Run all diagnostic checks"""
    print("🔍 Render Deployment Diagnostics")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Directories", check_directories),
        ("FastAPI Import", test_fastapi_import),
    ]
    
    check_environment_variables()
    print()
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! App should start successfully.")
        return 0
    else:
        print("❌ Some checks failed. Fix issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
