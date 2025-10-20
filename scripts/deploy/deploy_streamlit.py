#!/usr/bin/env python3
"""
Deployment script for Streamlit EDA Dashboard
This script prepares the project for cloud deployment
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly', 
        'seaborn', 'matplotlib', 'openpyxl', 'xlrd'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages)
    
    return len(missing_packages) == 0

def create_deployment_files():
    """Create necessary files for deployment"""
    print("📝 Creating deployment files...")
    
    # Create .streamlit/config.toml if it doesn't exist
    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)
    
    config_content = """[global]
dataFrameSerialization = "legacy"

[server]
port = 8504
address = "0.0.0.0"

[browser]
gatherUsageStats = false
"""
    
    config_file = streamlit_dir / "config.toml"
    if not config_file.exists():
        config_file.write_text(config_content)
        print("✅ Created .streamlit/config.toml")
    
    # Ensure requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found!")
        return False
    
    print("✅ Deployment files ready")
    return True

def test_dashboard():
    """Test if the dashboard can be imported and run"""
    print("🧪 Testing dashboard...")
    
    try:
        # Test import
        import streamlit_eda_dashboard
        print("✅ Dashboard imports successfully")
        
        # Test data loading
        from streamlit_eda_dashboard import load_data_files
        data_files = load_data_files()
        print(f"✅ Data loading works: {len(data_files)} files loaded")
        
        return True
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

def main():
    """Main deployment preparation"""
    print("🚀 Preparing Streamlit EDA Dashboard for deployment...")
    
    # Check if we're in the right directory
    if not Path("streamlit_eda_dashboard.py").exists():
        print("❌ streamlit_eda_dashboard.py not found in current directory")
        print("Please run this script from the project root directory")
        return False
    
    # Check requirements
    if not check_requirements():
        print("❌ Failed to install required packages")
        return False
    
    # Create deployment files
    if not create_deployment_files():
        print("❌ Failed to create deployment files")
        return False
    
    # Test dashboard
    if not test_dashboard():
        print("❌ Dashboard test failed")
        return False
    
    print("\n🎉 Dashboard is ready for deployment!")
    print("\n📋 Deployment Checklist:")
    print("✅ All dependencies installed")
    print("✅ Configuration files created")
    print("✅ Dashboard tested successfully")
    print("\n🌐 For Streamlit Cloud deployment:")
    print("1. Push your code to GitHub")
    print("2. Go to https://share.streamlit.io")
    print("3. Connect your GitHub repository")
    print("4. Set main file: streamlit_eda_dashboard.py")
    print("5. Deploy!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
