#!/usr/bin/env python3
"""
Test script to verify minimal dependencies work for Streamlit Cloud
"""

def test_imports():
    """Test all required imports"""
    try:
        print("Testing core imports...")
        
        # Core imports
        import streamlit as st
        print("✅ streamlit")
        
        import pandas as pd
        print("✅ pandas")
        
        import numpy as np
        print("✅ numpy")
        
        # Visualization imports
        import plotly.express as px
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
        
        # Utility imports
        import dateutil
        print("✅ python-dateutil")
        
        import pytz
        print("✅ pytz")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_data_loading():
    """Test data loading functionality"""
    try:
        print("\nTesting data loading...")
        
        from pathlib import Path
        import pandas as pd
        
        # Check if data directory exists
        data_dir = Path("adapt_context/data")
        if not data_dir.exists():
            print("❌ Data directory not found")
            return False
        
        # Try to load a sample file
        sample_files = [
            "Life Expectancy.csv",
            "Density of Doctors.csv",
            "Government Spending.csv"
        ]
        
        for file_name in sample_files:
            file_path = data_dir / file_name
            if file_path.exists():
                try:
                    df = pd.read_csv(file_path)
                    print(f"✅ {file_name}: {len(df)} rows")
                except Exception as e:
                    print(f"❌ Error loading {file_name}: {e}")
                    return False
        
        print("✅ Data loading successful!")
        return True
        
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing minimal dependencies for Streamlit Cloud...")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test data loading
    data_ok = test_data_loading()
    
    if imports_ok and data_ok:
        print("\n🎉 All tests passed! Ready for deployment.")
        return True
    else:
        print("\n❌ Some tests failed. Check dependencies.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
