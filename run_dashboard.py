#!/usr/bin/env python3
"""
Policy Simulation Assistant - Streamlit Dashboard Startup Script
Run this script to start the Streamlit EDA dashboard.
"""

import subprocess
import sys
import os

def main():
    """Start the Streamlit dashboard"""
    dashboard_path = os.path.join(os.path.dirname(__file__), 'examples', 'streamlit_eda_dashboard.py')
    
    if not os.path.exists(dashboard_path):
        print(f"❌ Error: Dashboard file not found at {dashboard_path}")
        sys.exit(1)
    
    print("🚀 Starting Streamlit EDA Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8501")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")

if __name__ == "__main__":
    main()
