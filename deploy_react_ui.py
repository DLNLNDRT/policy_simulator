#!/usr/bin/env python3
"""
React UI Deployment Script
This script prepares the React frontend for deployment
"""

import os
import sys
import subprocess
from pathlib import Path

def check_frontend_structure():
    """Check if React frontend exists and is properly structured"""
    print("🔍 Checking React frontend structure...")
    
    frontend_dir = Path("src/frontend")
    required_files = [
        "package.json",
        "vite.config.ts",
        "src/main.tsx",
        "src/App.tsx"
    ]
    
    missing_files = []
    for file_name in required_files:
        file_path = frontend_dir / file_name
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            missing_files.append(file_name)
            print(f"❌ {file_name}")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ React frontend structure is valid")
    return True

def create_vercel_config():
    """Create Vercel configuration for deployment"""
    print("📝 Creating Vercel configuration...")
    
    vercel_config = {
        "version": 2,
        "builds": [
            {
                "src": "src/frontend/package.json",
                "use": "@vercel/static-build",
                "config": {
                    "distDir": "dist"
                }
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "/src/frontend/$1"
            }
        ],
        "env": {
            "VITE_API_BASE_URL": "https://web-production-21904.up.railway.app"
        }
    }
    
    import json
    with open("vercel.json", "w") as f:
        json.dump(vercel_config, f, indent=2)
    
    print("✅ Created vercel.json")
    return True

def create_netlify_config():
    """Create Netlify configuration for deployment"""
    print("📝 Creating Netlify configuration...")
    
    netlify_config = """[build]
  base = "src/frontend"
  publish = "dist"
  command = "npm run build"

[build.environment]
  VITE_API_BASE_URL = "https://web-production-21904.up.railway.app"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
    
    with open("netlify.toml", "w") as f:
        f.write(netlify_config)
    
    print("✅ Created netlify.toml")
    return True

def create_railway_config():
    """Create Railway configuration for frontend deployment"""
    print("📝 Creating Railway configuration for frontend...")
    
    railway_config = """{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd src/frontend && npm run preview",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
"""
    
    with open("railway-frontend.json", "w") as f:
        f.write(railway_config)
    
    print("✅ Created railway-frontend.json")
    return True

def show_deployment_options():
    """Show deployment options and steps"""
    print("\n🚀 React UI Deployment Options:")
    print("\n1. Vercel (Recommended):")
    print("   - Go to https://vercel.com")
    print("   - Connect GitHub repository")
    print("   - Set Root Directory: src/frontend")
    print("   - Add Environment Variable: VITE_API_BASE_URL=https://web-production-21904.up.railway.app")
    print("   - Deploy!")
    
    print("\n2. Netlify:")
    print("   - Go to https://netlify.com")
    print("   - Connect GitHub repository")
    print("   - Set Build Command: cd src/frontend && npm run build")
    print("   - Set Publish Directory: src/frontend/dist")
    print("   - Add Environment Variable: VITE_API_BASE_URL=https://web-production-21904.up.railway.app")
    print("   - Deploy!")
    
    print("\n3. Railway (Separate Project):")
    print("   - Go to https://railway.app")
    print("   - Create new project")
    print("   - Select GitHub repository")
    print("   - Set Root Directory: src/frontend")
    print("   - Add Environment Variable: VITE_API_BASE_URL=https://web-production-21904.up.railway.app")
    print("   - Deploy!")
    
    print("\n📋 What You'll Get:")
    print("✅ Full Interactive React UI")
    print("✅ Policy Simulation Engine with forms")
    print("✅ Health Benchmark Dashboard with charts")
    print("✅ Narrative Insight Generator")
    print("✅ Data Quality Assurance dashboard")
    print("✅ Advanced Analytics & Reporting")
    print("✅ Mobile-responsive design")
    print("✅ Real-time API integration")

def main():
    """Main deployment preparation"""
    print("🚀 Preparing React UI for deployment...")
    
    # Check frontend structure
    if not check_frontend_structure():
        print("❌ React frontend structure invalid")
        return False
    
    # Create deployment configurations
    create_vercel_config()
    create_netlify_config()
    create_railway_config()
    
    print("\n🎉 React UI is ready for deployment!")
    
    # Show deployment options
    show_deployment_options()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)



