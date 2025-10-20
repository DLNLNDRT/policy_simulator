#!/usr/bin/env python3
"""
Test script to verify all dependencies for the Streamlit EDA Dashboard
Run this before deploying to ensure all packages are available
"""

def test_imports():
    """Test all required imports for the dashboard"""
    try:
        print("Testing imports...")
        
        # Core imports
        import streamlit as st
        print("✅ streamlit")
        
        import pandas as pd
        print("✅ pandas")
        
        import numpy as np
        print("✅ numpy")
        
        # Visualization imports
        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        print("✅ plotly")
        
        import seaborn as sns
        print("✅ seaborn")
        
        import matplotlib.pyplot as plt
        print("✅ matplotlib")
        
        # Data processing imports
        import openpyxl
        print("✅ openpyxl")
        
        import xlrd
        print("✅ xlrd")
        
        # Streamlit extensions
        from streamlit_option_menu import option_menu
        print("✅ streamlit-option-menu")
        
        # Additional imports
        from pathlib import Path
        import json
        import re
        from datetime import datetime
        import warnings
        print("✅ standard library modules")
        
        print("\n🎉 All dependencies are available!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_data_loading():
    """Test if data files can be loaded"""
    try:
        print("\nTesting data loading...")
        
        import pandas as pd
        from pathlib import Path
        
        # Check if data directory exists
        data_dir = Path("adapt_context/data")
        if not data_dir.exists():
            print("❌ adapt_context/data directory not found")
            return False
        
        # Test loading a CSV file
        csv_files = list(data_dir.glob("*.csv"))
        if csv_files:
            df = pd.read_csv(csv_files[0])
            print(f"✅ Successfully loaded {csv_files[0].name} ({len(df)} rows)")
        else:
            print("❌ No CSV files found in adapt_context/data")
            return False
        
        # Test loading an Excel file
        excel_files = list(data_dir.glob("*.xlsx"))
        if excel_files:
            df = pd.read_excel(excel_files[0])
            print(f"✅ Successfully loaded {excel_files[0].name} ({len(df)} rows)")
        else:
            print("⚠️  No Excel files found in adapt_context/data")
        
        print("✅ Data loading test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def test_streamlit_config():
    """Test Streamlit configuration"""
    try:
        print("\nTesting Streamlit configuration...")
        
        import streamlit as st
        
        # Test basic Streamlit functionality
        print("✅ Streamlit version:", st.__version__)
        
        # Test if we can create a simple app
        print("✅ Streamlit configuration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Streamlit configuration error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Policy Simulation Assistant Dependencies")
    print("=" * 50)
    
    # Run all tests
    tests = [
        test_imports,
        test_data_loading,
        test_streamlit_config
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"✅ Passed: {sum(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("\n🎉 All tests passed! Ready for deployment!")
        exit(0)
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before deploying.")
        exit(1)
