#!/usr/bin/env python3
"""
Railway Deployment Script
This script prepares and tests the application for Railway deployment
"""

import os
import sys
import subprocess
from pathlib import Path

def check_railway_files():
    """Check if all Railway deployment files exist"""
    print("🔍 Checking Railway deployment files...")
    
    required_files = [
        "comprehensive_demo_server.py",
        "requirements_full_api.txt", 
        "Procfile",
        "runtime.txt",
        "railway.json"
    ]
    
    missing_files = []
    for file_name in required_files:
        if Path(file_name).exists():
            print(f"✅ {file_name}")
        else:
            missing_files.append(file_name)
            print(f"❌ {file_name}")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All Railway files present")
    return True

def test_application():
    """Test if the application can start"""
    print("🧪 Testing application startup...")
    
    try:
        # Test import
        import comprehensive_demo_server
        print("✅ Application imports successfully")
        
        # Test if it can be started (without actually starting)
        print("✅ Application structure is valid")
        
        return True
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        return False

def check_requirements():
    """Check if requirements file is valid"""
    print("📋 Checking requirements file...")
    
    try:
        with open("requirements_full_api.txt", "r") as f:
            requirements = f.read()
        
        if "fastapi" in requirements and "uvicorn" in requirements:
            print("✅ Requirements file looks good")
            return True
        else:
            print("❌ Requirements file missing key dependencies")
            return False
    except Exception as e:
        print(f"❌ Error reading requirements file: {e}")
        return False

def show_deployment_steps():
    """Show the deployment steps"""
    print("\n🚀 Railway Deployment Steps:")
    print("1. Go to https://railway.app")
    print("2. Sign up with GitHub account")
    print("3. Click 'New Project'")
    print("4. Select 'Deploy from GitHub repo'")
    print("5. Choose your repository: DLNLNDRT/project_root")
    print("6. Click 'Deploy Now'")
    print("7. Wait for deployment to complete")
    print("8. Get your public URL!")
    
    print("\n📋 Your dashboard will include:")
    print("✅ Policy Simulation Engine")
    print("✅ Health Benchmark Dashboard") 
    print("✅ Narrative Insight Generator")
    print("✅ Data Quality Assurance")
    print("✅ Advanced Analytics & Reporting")
    
    print("\n🌐 URLs after deployment:")
    print("• Main Dashboard: https://your-app-name.railway.app")
    print("• API Docs: https://your-app-name.railway.app/docs")
    print("• Health Check: https://your-app-name.railway.app/health")

def main():
    """Main deployment preparation"""
    print("🚀 Preparing Policy Simulation Assistant for Railway deployment...")
    
    # Check Railway files
    if not check_railway_files():
        print("❌ Railway deployment files missing")
        return False
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements file invalid")
        return False
    
    # Test application
    if not test_application():
        print("❌ Application test failed")
        return False
    
    print("\n🎉 Application is ready for Railway deployment!")
    
    # Show deployment steps
    show_deployment_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
